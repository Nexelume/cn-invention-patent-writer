#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_form.py — formal compliance checker for Chinese invention-patent drafts.

Implements the machine-checkable items of references/formal-checklist.md.
Stdlib only: no python-docx, no lxml. Reads .md/.txt directly, .docx via zipfile.

Verdicts
  FAIL  a clear formal violation of a listed rule
  WARN  suspicious, needs human confirmation (the rule has a legal exception)
  SKIP  not checkable with the available input — always named in the report
  PASS  checked and clean

Usage
  python check_form.py draft.md
  python check_form.py application.docx --kind application --term-table terms.tsv --request-form request.md
  python check_form.py --self-test

Exit code: 0 no FAIL, 1 has FAIL, 2 usage error.

Provision numbers follow references/legal-baseline.md (2023 修订版细则, 2024-01-20).
The evidence-language blacklist is this skill's own rule, not a statutory requirement.
"""
from __future__ import annotations

import argparse
import html
import os
import re
import sys
import zipfile

# ---------------------------------------------------------------- rule tables

# 商业性宣传用语：clear cases vs borderline
PROMO_CLEAR = ["最佳", "最优", "最好", "领先", "革命性", "颠覆性", "填补空白",
               "国际先进", "国内领先", "世界第一", "独一无二", "完美", "极致"]
PROMO_BORDER = ["优异", "卓越", "高效", "智能", "精准", "强大", "先进", "新颖"]

# 本技能自有证据纪律（非法律规定）：出现即提示人工确认上下文
EVIDENCE_BLACK = ["显著提高", "显著提升", "大幅提高", "大幅提升", "明显改善",
                  "已实现", "已达到", "现场应用后", "量产验证", "客户验证"]

# 残留占位符
PLACEHOLDERS = re.compile(
    r"【(?:待确认|待补充|待核|术语待核|条号待核)(?:[:：][^】\n]*)?】"
    r"|\[待补充\]|\b(?:TODO|TBD|XXX)\b|[（(]此处|待填写|待提供"
)

SPEC_PARTS = ["技术领域", "背景技术", "发明内容", "附图说明", "具体实施方式"]

CN_NUM = "一二三四五六七八九十"
DOCUMENT_KINDS = {
    "application": "成套申请文本", "specification": "说明书", "claims": "权利要求书",
    "abstract": "说明书摘要", "disclosure": "技术交底书／构思稿", "unknown": "未识别",
}
SECTION_HEADINGS = {
    "abstract": ("说明书摘要", "摘要"), "claims": ("权利要求书", "权利要求"), "spec": ("说明书",),
}
CLAIM_NUMBER = re.compile(r"(?m)^[ \t]*(\d+)[ \t]*[.、．)）][ \t]*")


# ---------------------------------------------------------------- readers

def read_text(path: str) -> tuple[str, dict]:
    """Return (plain text, metadata). Supports .docx and plain text."""
    meta: dict = {"kind": "text", "revision": False, "images": 0, "media": []}
    low = path.lower()
    if low.endswith(".docx"):
        meta["kind"] = "docx"
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            try:
                xml = z.read("word/document.xml").decode("utf-8", "ignore")
            except KeyError:
                sys.exit(f"不是有效的 docx（缺少 word/document.xml）：{path}")
        meta["revision"] = bool(re.search(r"<w:(ins|del)[\s>]", xml)) or \
            "commentReference" in xml or "commentRangeStart" in xml
        meta["images"] = len(re.findall(r"<w:(?:drawing|pict|object)(?=[\s/>])", xml))
        meta["media"] = [n for n in names if n.startswith("word/media/")]
        text = xml
        text = text.replace("</w:p>", "\n").replace("<w:br/>", "\n").replace("<w:tab/>", "\t")
        text = re.sub(r"<w:instrText[^>]*>.*?</w:instrText>", "", text, flags=re.S)  # field codes
        text = re.sub(r"<[^>]+>", "", text)
        text = html.unescape(text)
    else:
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    meta["chars"] = len(text)
    return text, meta


def read_term_table(path: str) -> tuple[list[str], list[str]]:
    """Return (allowed terms, forbidden terms) from a TSV/CSV term table.

    Column convention follows references/terminology.md:
    中文术语 | 英文对应 | 缩写 | 定义 | 首次出现 | 禁用/易混词 | 依据来源
    """
    allowed, forbidden = [], []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.strip():
                continue
            cols = [c.strip() for c in re.split(r"[\t,，]", line)]
            if not cols or cols[0].startswith("#"):
                continue
            if cols[0] in ("中文术语", "术语"):
                continue
            allowed.append(cols[0])
            if len(cols) >= 6 and cols[5] not in ("", "-", "无"):
                forbidden += [w.strip() for w in re.split(r"[/、;；,，]", cols[5]) if w.strip()]
    return allowed, forbidden


# ---------------------------------------------------------------- structure

def heading_text(line: str) -> str:
    heading = re.sub(r"^\s*#{1,6}\s*", "", line.lstrip("\ufeff")).strip().strip("*").strip()
    heading = re.sub(rf"^[{CN_NUM}]+[、.．]\s*", "", heading)
    return heading.rstrip(":：").strip()


def find_sections(text: str) -> dict[str, str]:
    """Read only explicit filing-text sections from mixed documents."""
    lines = text.splitlines()
    headings = [re.sub(r"[（(](?:草案|草稿|送审稿|初稿)[)）]$", "", heading_text(line)).strip()
                for line in lines]
    section_names = {name: key for key, names in SECTION_HEADINGS.items() for name in names}
    sections: dict[str, str] = {}
    for start, title in enumerate(headings):
        key = section_names.get(title)
        if key is None or key in sections:
            continue
        markdown_level = len(lines[start].lstrip()) - len(lines[start].lstrip().lstrip("#"))
        end = start + 1
        while end < len(lines):
            next_heading = headings[end]
            marker = re.match(r"^\s*(#{1,6})\s+", lines[end])
            if key == "spec" and (next_heading in SPEC_PARTS or next_heading.startswith("实施例")):
                end += 1
                continue
            if next_heading in section_names or re.fullmatch(
                    r"附图|说明书附图|摘要附图|请求书|术语表|待确认(?:事项|清单)|实施例\s*\d+.*",
                    next_heading):
                break
            if marker and markdown_level and len(marker[1]) <= markdown_level:
                break
            if key != "spec" and (next_heading in SPEC_PARTS
                                  or re.match(rf"^\s*[{CN_NUM}]+[、.．]", lines[end])):
                break
            end += 1
        sections[key] = "\n".join(lines[start + 1:end]).strip()
    return sections


def document_kind(text: str, sections: dict[str, str]) -> str:
    headings = [heading_text(line.lstrip("\ufeff")) for line in text.splitlines()]
    opening = [heading for heading in headings if heading][:5]
    if any(re.fullmatch(r"(?:发明专利)?技术交底书(?:[（(].*[)）])?|发明构思稿|专利构思稿",
                        heading) for heading in opening):
        return "disclosure"
    if len(sections) >= 2 or "发明专利申请文件" in opening:
        return "application"
    if sections:
        return {"spec": "specification", "claims": "claims", "abstract": "abstract"}[next(iter(sections))]
    if len(set(headings).intersection(SPEC_PARTS)) >= 3 and "技术领域" in opening:
        return "specification"
    return "unknown"


def extract_claims(block: str) -> tuple[list[int], dict[int, str]]:
    """Split a known claims block and retain sequence and duplicate numbers."""
    markers = list(CLAIM_NUMBER.finditer(block))
    numbers = [int(marker[1]) for marker in markers]
    claims = {}
    for index, (number, marker) in enumerate(zip(numbers, markers)):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(block)
        claims[number] = block[marker.end():end].strip()
    return numbers, claims


def figure_numbers(text: str) -> list[int]:
    nums = set()
    for m in re.finditer(r"图\s*(\d+)", text):
        nums.add(int(m.group(1)))
    return sorted(nums)


# ---------------------------------------------------------------- report

class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str, str]] = []  # status, item, detail, basis

    def add(self, status: str, item: str, detail: str = "", basis: str = "") -> None:
        self.rows.append((status, item, detail, basis))

    def count(self, status: str) -> int:
        return sum(1 for r in self.rows if r[0] == status)

    def render(self, meta: dict) -> str:
        icon = {"FAIL": "✗ 违规", "WARN": "! 待确认", "SKIP": "- 未检查", "PASS": "✓ 通过"}
        out = []
        out.append("=" * 74)
        out.append("中国发明专利形式合规检查（check_form.py）")
        out.append("=" * 74)
        out.append(f"输入：{meta.get('path','')}  类型：{meta.get('kind','')}  字符数：{meta.get('chars',0)}")
        out.append(f"文档类型：{DOCUMENT_KINDS[meta['document_kind']]}")
        out.append(f"条款基线：2023 修订版细则（2024-01-20 施行）+ 2023 版审查指南")
        out.append("")
        for status in ("FAIL", "WARN", "SKIP", "PASS"):
            rows = [r for r in self.rows if r[0] == status]
            if not rows:
                continue
            out.append(f"—— {icon[status]}（{len(rows)}）" + " " + "-" * 40)
            for _, item, detail, basis in rows:
                out.append(f"  {item}")
                if detail:
                    for ln in str(detail).split("\n"):
                        out.append(f"      {ln}")
                if basis and status in ("FAIL", "WARN"):
                    out.append(f"      依据：{basis}")
            out.append("")
        out.append("-" * 74)
        out.append(f"合计：违规 {self.count('FAIL')}，待确认 {self.count('WARN')}，"
                   f"未检查 {self.count('SKIP')}，通过 {self.count('PASS')}")
        if self.count("SKIP"):
            out.append("未检查项不能视为通过；请在 closure report 中逐项说明原因。")
        out.append("机械校验通过 ≠ 法律合规。正式提交前应由有资质专利代理师复核。")
        return "\n".join(out)


# ---------------------------------------------------------------- checks

def check_all(text: str, meta: dict, term_table: str | None,
              request_form: str | None, rep: Report, kind: str = "auto") -> None:
    sections = find_sections(text)
    inferred = document_kind(text, sections)
    selected = inferred if kind == "auto" else kind
    meta["document_kind"] = selected
    spec_body = sections.get("spec")
    claim_body = sections.get("claims")
    abstract = sections.get("abstract")
    if not sections and inferred in ("unknown", selected):
        if selected == "specification":
            spec_body = text
        if kind == "claims":
            claim_body = text
        if kind == "abstract":
            abstract = text
    if selected == "unknown":
        rep.add("SKIP", "文档类型", "未定位到正式文件章节，可用 --kind 明确指定检查对象")
    if selected == "application" and kind == "application":
        missing = [label for key, label in (("spec", "说明书"), ("claims", "权利要求书"),
                                            ("abstract", "说明书摘要"))
                   if not sections.get(key)]
        if missing:
            rep.add("FAIL", "成套申请文本缺少可识别的正文", "、".join(missing))

    if spec_body is None:
        rep.add("SKIP", "S/F 说明书与附图形式", "未定位到说明书正文")
    else:
        check_specification(spec_body, request_form, rep)
    if claim_body is None:
        rep.add("SKIP", "C1–C15 权利要求检查", "未定位到权利要求书正文")
    else:
        check_claims(claim_body, meta, term_table, rep)
    check_abstract(abstract, rep)
    check_package(text, meta, rep)


def check_specification(spec_body: str, request_form: str | None, rep: Report) -> None:
    if request_form and os.path.exists(request_form):
        rf, _ = read_text(request_form)
        name = re.search(r"发明名称\s*[:：]\s*(.+)", rf)
        first = next((line for line in spec_body.splitlines() if line.strip()), "")
        spec_name = heading_text(first)
        if not name or not spec_name or spec_name in SPEC_PARTS:
            rep.add("SKIP", "S1 名称与请求书一致", "未能定位两份文件的发明名称")
        elif name[1].strip() != spec_name:
            rep.add("WARN", "S1 说明书名称与请求书名称不一致",
                    f"请求书：{name[1].strip()}｜说明书首行：{spec_name}", "细则第20条")
        else:
            rep.add("PASS", "S1 名称一致性（按请求书比对）")
    else:
        rep.add("SKIP", "S1 名称与请求书一致", "未提供可读的请求书（--request-form）")
    text = spec_body
    lines = text.split("\n")

    # ---------- S: 说明书（细则第20条）
    headings = [heading_text(line) for line in lines]
    missing = [p for p in SPEC_PARTS if p not in headings]
    if missing:
        rep.add("FAIL", "S2/S3 说明书五部分不齐备或标题缺失",
                "缺少：" + "、".join(missing), "细则第20条")
    else:
        pos = [headings.index(p) for p in SPEC_PARTS]
        if pos != sorted(pos):
            rep.add("FAIL", "S2 说明书五部分顺序错误",
                    "实际顺序：" + "→".join(
                        p for _, p in sorted(zip(pos, SPEC_PARTS))), "细则第20条")
        else:
            rep.add("PASS", "S2/S3 说明书五部分齐备且顺序正确")

    bad_ref = [f"第{i+1}行：{ln.strip()[:60]}" for i, ln in enumerate(lines)
               if re.search(r"如权利要求.{0,12}所述的", ln)]
    if bad_ref:
        rep.add("FAIL", "S7 说明书使用「如权利要求……所述的……」引用语",
                "\n".join(bad_ref[:5]), "细则第20条第三款")
    else:
        rep.add("PASS", "S7 说明书无被禁引用语")

    hits = [(w, ln.strip()[:60]) for ln in lines for w in PROMO_CLEAR if w in ln]
    if hits:
        rep.add("FAIL", "S8 说明书含商业性宣传用语",
                "\n".join(f"「{w}」 {c}" for w, c in hits[:5]), "细则第20条第三款")
    else:
        rep.add("PASS", "S8 说明书无明确商业宣传用语")
    border = []
    for w in PROMO_BORDER:
        for m in re.finditer(w, text):
            a, b = max(0, m.start() - 14), min(len(text), m.start() + len(w) + 14)
            border.append((w, "…" + text[a:b].replace("\n", " ") + "…"))
    if border:
        rep.add("WARN", "S8 说明书含边界宣传词（需判断是否已给出可核查指标）",
                "\n".join(f"「{w}」 {c}" for w, c in border[:6]))

    if re.search(r"SEQ\s*ID\s*NO", text, re.I):
        if "序列表" not in text:
            rep.add("FAIL", "S9 含序列但说明书未包含序列表",
                    "检出 SEQ ID NO，未找到「序列表」", "细则第20条第四款")
        else:
            rep.add("PASS", "S9 序列与序列表并存")
    else:
        rep.add("SKIP", "S9 序列表", "文中未检出核苷酸/氨基酸序列")

    # ---------- F: 附图（细则第21条）
    figs = figure_numbers(spec_body)
    if figs:
        if figs != list(range(1, len(figs) + 1)):
            rep.add("FAIL", "F1 附图编号不连续", f"检出编号 {figs}", "细则第21条")
        else:
            rep.add("PASS", f"F1 附图编号连续（图1–图{max(figs)}）")
        undeclared = [n for n in figs if not re.search(rf"图\s*{n}\b", spec_body)]
        if undeclared:
            rep.add("WARN", "F1 部分图号未在附图说明中说明", f"图{undeclared}")
    else:
        rep.add("SKIP", "F1 附图编号", "未检出「图N」表述")

    marks = {}
    for m in re.finditer(r"([\u4e00-\u9fa5]{2,10})\s*[（(]\s*(\d{1,3})\s*[)）]", text):
        marks.setdefault(int(m.group(2)), set()).add(m.group(1))
    dup = {k: v for k, v in marks.items() if len(v) > 1}
    if dup:
        rep.add("WARN", "F4 同一附图标记对应多个部件名",
                "\n".join(f"标记{k}：{'、'.join(sorted(v))}" for k, v in list(dup.items())[:5]),
                "细则第21条第二款")
    elif marks:
        rep.add("PASS", f"F4 附图标记与部件名一一对应（{len(marks)} 个标记）")
    else:
        rep.add("SKIP", "F4 附图标记一致性", "未检出形如「传感器（1）」的标记")
    rep.add("SKIP", "F2/F3 附图标记双向一致",
            "需要附图图像本身；文本侧无法确认标记是否实际出现在图中")
    rep.add("SKIP", "F5/F6/F7 附图注释、线条、版心框线", "需渲染后目视检查")

def check_claims(block: str, meta: dict, term_table: str | None, rep: Report) -> None:
    numbers, claims = extract_claims(block)
    lines = block.splitlines()
    if not claims:
        rep.add("FAIL", "C1 权利要求书未检出权项编号", "已定位权利要求书，请核对权项编号格式")
    else:
        nums = sorted(claims)
        if numbers != list(range(1, len(numbers) + 1)):
            rep.add("FAIL", "C1 权利要求编号顺序错误、不连续或重复",
                    f"检出编号 {numbers}", "细则第22条")
        else:
            rep.add("PASS", f"C1 权利要求编号连续（1–{len(nums)}）")

        if meta["kind"] == "docx" and meta["images"]:
            rep.add("WARN", "C3 文档含图片，需确认未嵌入权利要求书",
                    f"整篇检出 {meta['images']} 个图形对象", "细则第22条第三款")
        elif meta["kind"] == "docx":
            rep.add("PASS", "C3 未检出嵌入图形对象")
        else:
            imgs = [ln.strip()[:40] for ln in lines if re.search(r"!\[[^\]]*\]\(", ln)]
            if imgs:
                rep.add("WARN", "C3 文本含图片引用，需确认不在权利要求书中",
                        "\n".join(imgs[:3]))
            else:
                rep.add("PASS", "C3 未检出图片引用")

        bad4 = [(n, m.group(0)) for n, b in claims.items()
                for m in re.finditer(r"如说明书.{0,10}?所述|如图\s*\d*\s*所示", b)]
        if bad4:
            rep.add("WARN", "C4 权利要求使用受限引用语（须确属绝对必要）",
                    "\n".join(f"权利要求{n}：{s}" for n, s in bad4[:5]), "细则第22条第三款")
        else:
            rep.add("PASS", "C4 权利要求无受限引用语")

        bare = []
        for n, b in claims.items():
            for m in re.finditer(r"[\u4e00-\u9fa5]{2,}(?<![（(])(\d{1,3})(?![)）])", b):
                if 0 < int(m.group(1)) <= 200 and "权利要求" not in m.group(0):
                    bare.append((n, m.group(0)))
        if bare:
            rep.add("WARN", "C5 疑似附图标记未加括号",
                    "\n".join(f"权利要求{n}：{s}" for n, s in bare[:5]), "细则第22条第四款")
        else:
            rep.add("PASS", "C5 未检出未加括号的部件标记")

        indep = [n for n, b in claims.items() if not re.search(r"根据权利要求", b)]
        if not indep:
            rep.add("FAIL", "C8 未找到独立权利要求", "全部权项均引用其他权项", "细则第23条")
        elif len(indep) == 1:
            first = min(nums)
            if indep[0] != first:
                rep.add("FAIL", "C8 独立权利要求未写在同一发明的从属权利要求之前",
                        f"独权为权利要求{indep[0]}，首项为{first}", "细则第24条第三款")
            else:
                rep.add("PASS", f"C8 单一独权（权利要求{indep[0]}）且置于从权之前")
            if not re.search(r"其特征(在于|是)", claims[indep[0]]):
                rep.add("WARN", "C7 独权未使用「其特征在于」引出特征部分",
                        "若性质不适于前序+特征写法可另行说明", "细则第24条第二款")
            else:
                rep.add("PASS", "C7 独权含「其特征在于」特征部分")
        else:
            rep.add("WARN", "C8 检出多个独立权利要求",
                    f"独权：{indep}。方法+产品并列时须审查单一性与是否属同一发明构思",
                    "细则第24条第三款；专利法第31条第1款")

        refs: dict[int, list[int]] = {}
        for n, b in claims.items():
            r: list[int] = []
            for m in re.finditer(r"根据权利要求\s*([\d\s至到~\-－、,，和或及]+?)\s*(?:中)?\s*(?:任一项|任一)?\s*所述", b):
                seg = m.group(1)
                for part in re.split(r"[、,，和或及]", seg):
                    part = part.strip()
                    rng = re.match(r"(\d+)\s*[至到~\-－]\s*(\d+)$", part)
                    if rng:
                        a, z = int(rng.group(1)), int(rng.group(2))
                        r += list(range(min(a, z), max(a, z) + 1))
                    elif part.isdigit():
                        r.append(int(part))
            if r:
                refs[n] = r

        unresolved_refs = [n for n in claims if n not in indep and n not in refs]
        bad10 = [(n, x) for n, r in refs.items() for x in r if x >= n or x not in claims]
        if bad10:
            rep.add("FAIL", "C10 从属权利要求引用了非在前或不存在的权项",
                    "\n".join(f"权利要求{n} → 引用权利要求{x}" for n, x in bad10[:6]),
                    "细则第25条第二款")
        elif unresolved_refs:
            rep.add("SKIP", "C10 从属引用未完整解析",
                    f"权利要求 {unresolved_refs} 的引用编号或句式需人工确认")
        else:
            rep.add("PASS", "C10 全部从属权利要求仅引用在前权项")

        bad9 = list(unresolved_refs)
        for n, b in claims.items():
            if n in refs and not re.search(r"根据权利要求\s*[\d\s至到~\-－、,，和或及]+?(?:中)?\s*(?:任一项|任一)?\s*所述[^。]{0,20}其特征", b):
                bad9.append(n)
        if bad9:
            rep.add("WARN", "C9 从权缺少「引用部分 + 限定部分」标准句式",
                    f"权利要求 {bad9}", "细则第25条第一款")
        else:
            rep.add("PASS", "C9 从权句式合于引用部分+限定部分")

        multi = {n: r for n, r in refs.items() if len(r) > 1}
        bad11 = []
        for n, r in multi.items():
            body = claims[n]
            seg = re.search(r"根据权利要求\s*([\d\s至到~\-－、,，和或及]+?)\s*(?:中)?\s*(任一项|任一|或|和|及|、|,|，)?\s*所述", body)
            tail = seg.group(2) if seg else None
            explicit_or = bool(seg and re.fullmatch(r"\d+(?:\s*或\s*\d+)+", seg.group(1).strip()))
            if tail not in ("任一项", "任一", "或") and not explicit_or:
                bad11.append((n, r, tail))
        if bad11:
            rep.add("WARN", "C11 多项从属可能未采用择一引用表述",
                    "\n".join(f"权利要求{n} 引用 {r}（连接词：{t or '无'}）；"
                              f"建议写成「…中任一项所述」" for n, r, t in bad11[:5]),
                    "细则第25条第二款")
        elif unresolved_refs:
            rep.add("SKIP", "C11 从属引用未完整解析", f"权利要求 {unresolved_refs}")
        elif multi:
            rep.add("PASS", f"C11 多项从属均为择一引用（{len(multi)} 项）")
        else:
            rep.add("PASS", "C11 无多项从属权利要求")

        bad12 = []
        for n, r in multi.items():
            for x in r:
                if x in multi and x != n:
                    bad12.append((n, x))
        if bad12:
            rep.add("FAIL", "C12 多项从属权利要求以另一项多项从属权利要求为基础",
                    "\n".join(f"权利要求{n}（多项）→ 权利要求{x}（多项）" for n, x in bad12[:6]),
                    "细则第25条第二款")
        elif unresolved_refs:
            rep.add("SKIP", "C12 从属引用链未完整解析", f"权利要求 {unresolved_refs}")
        else:
            rep.add("PASS", "C12 无多项从属叠加引用")

        if term_table and os.path.exists(term_table):
            allowed, forbidden = read_term_table(term_table)
            claim_text = "\n".join(claims.values())
            fh = [w for w in forbidden if w in claim_text]
            if fh:
                rep.add("FAIL", "C2/T4 权利要求使用了术语表禁用词",
                        "、".join(fh[:10]), "细则第22条第三款")
            else:
                rep.add("PASS", "C2/T4 权利要求未使用禁用术语")
        else:
            rep.add("SKIP", "C2/T3/T4 术语一致性",
                    "未提供术语表（--term-table）；术语与说明书逐字一致需人工比对")

def check_abstract(abstract: str | None, rep: Report) -> None:
    if not abstract:
        rep.add("SKIP", "A1–A6 说明书摘要", "未定位到「说明书摘要」一节")
    else:
        flat = re.sub(r"\s", "", abstract)
        if len(flat) > 300:
            rep.add("FAIL", "A3 摘要超过 300 字",
                    f"实际 {len(flat)} 字（含标点，上限 300）；超出 {len(flat)-300} 字",
                    "《专利审查指南》第二部分第二章 2.4（不在细则中）")
        else:
            rep.add("PASS", f"A3 摘要 {len(flat)} 字（≤300）")

        if re.search(r"^\s*(摘要|说明书摘要)\s*[:：]", abstract) or abstract.lstrip().startswith("#"):
            rep.add("FAIL", "A4 摘要使用了标题", abstract.strip().split("\n")[0][:40],
                    "指南 2.4（初审 4.5.1）")
        else:
            rep.add("PASS", "A4 摘要未使用标题")

        ah = [w for w in PROMO_CLEAR if w in abstract]
        if ah:
            rep.add("FAIL", "A5 摘要含商业性宣传用语", "、".join(ah), "细则第26条第二款")
        else:
            rep.add("PASS", "A5 摘要无明确商业宣传用语")

        if not re.search(r"(技术领域|属于.{2,20}领域)", abstract[:80]):
            rep.add("WARN", "A1 摘要首段未写明所属技术领域", abstract[:60])
        else:
            rep.add("PASS", "A1 摘要写明名称与技术领域")

        rep.add("SKIP", "A2 摘要以技术方案为主", "需人工判断技术问题/方案要点/用途的配比")
        rep.add("SKIP", "A7/A8 摘要附图指定与可分辨性",
                "需请求书图号字段与渲染后目视检查")

def check_package(text: str, meta: dict, rep: Report) -> None:
    filing = meta["document_kind"] in ("application", "specification", "claims", "abstract")
    ph = [match[0] for match in PLACEHOLDERS.finditer(text)]
    if ph:
        item = "P4 申请文本残留占位符或待补充标记" if filing else "草稿待确认或待补充项"
        rep.add("FAIL" if filing else "WARN", item, "、".join(dict.fromkeys(ph[:6])))
    elif filing:
        rep.add("PASS", "P4 无残留占位符")

    ev = []
    for w in EVIDENCE_BLACK:
        for m in re.finditer(w, text):
            if re.search(r"(?:不是|并非|尚未)\s*$", text[max(0, m.start() - 8):m.start()]):
                continue
            a, b = max(0, m.start() - 18), min(len(text), m.start() + len(w) + 18)
            ev.append((w, "…" + text[a:b].replace("\n", " ") + "…"))
    if ev:
        rep.add("WARN", "证据语言：疑似把目标/设计值写成已取得的结果",
                "\n".join(f"「{w}」 {c}" for w, c in ev[:8])
                + "\n本项为技能自有证据纪律，非法律规定；改法：改为验收标准或设计参数，并标注证据等级")
    else:
        rep.add("PASS", "证据语言未检出高风险表述")

    if not filing:
        rep.add("SKIP", "P1–P4 申请文件交付检查", "目前按交底书或未识别文档处理")
    elif meta["kind"] == "docx":
        if meta["revision"]:
            rep.add("WARN", "P3 文档含修订痕迹或批注", "检出 w:ins / w:del / 批注引用")
        else:
            rep.add("PASS", "P3 无修订痕迹与批注残留")
        rep.add("SKIP", "P1 页码分文件连续", "需检查各 sectPr 页脚域；建议人工确认")
        rep.add("SKIP", "P2 黑白与线条清晰度", "需渲染后检查")
    else:
        rep.add("SKIP", "P1–P3 页码、黑白、修订痕迹", "非 docx 输入，不适用")


# ---------------------------------------------------------------- self-test

DEMO_BAD = """# 一种示例方法

## 说明书摘要

本发明公开一种基于多通道音频的环境音场景重建方法，属于声学信号处理技术领域。该方法采集多通道音频信号并提取双耳房间冲激响应特征，通过声事件检测网络获得声事件类别与方位，结合房间几何先验反演反射路径，最终渲染出可听化的空间音频场景。该方法显著提高场景还原度，现场应用后还原度达到92%，已实现端到端实时输出，可广泛用于虚拟现实、影视后期与智能座舱等场景，具有精准的空间定位能力与良好的听感一致性表现。相比现有技术，本发明大幅提升了重建效率与主观听感评分，并且在复杂混响环境下依然保持稳定表现，适用于需要高保真空间音频的多种应用场合，可广泛部署于虚拟现实终端、影视后期工作站、智能座舱与远程会议系统等各类需要实时空间音频渲染的产品之中。

## 权利要求书

1. 一种基于多通道音频的环境音场景重建方法，其特征在于，包括：采集音频；渲染场景。

2. 根据权利要求 4 所述的方法，其特征在于，所述冲激响应按倍频程归一化。

3. 根据权利要求 1 至 3 所述的方法，其特征在于，所述网络为卷积循环神经网络。

4. 根据权利要求 3 所述的方法，其特征在于，所述反演采用镜像源法。

5. 根据权利要求 2 所述的方法，其特征在于，参数如说明书第三部分所述。

## 说明书

技术领域

本发明属于声学信号处理技术领域。

背景技术

现有方法还原度不足。

发明内容

本发明解决上述问题。

具体实施方式

【待补充】
"""


def self_test() -> int:
    rep = Report()
    meta = {"path": "<self-test:bad>", "kind": "text", "chars": len(DEMO_BAD),
            "revision": False, "images": 0}
    check_all(DEMO_BAD, meta, None, None, rep)
    print(rep.render(meta))
    caught = {r[1].split()[0] for r in rep.rows if r[0] in ("FAIL", "WARN")}
    required = ["S2/S3", "C10", "C11", "A3", "P4"]
    missing = [e for e in required if e not in caught]
    print("\n[self-test] 应命中：" + "、".join(required))
    if missing:
        print("[self-test] 失败：以下项未被检出 " + "、".join(missing))
        return 1

    disclosure = (
        "技术交底书\n一、技术领域\n二、背景技术及其缺陷\n三、具体实施方式\n"
        "1. 将止挡安装在支架上。\n2. 施加推力。\n"
        "建议保护布局\n【待确认：止挡材料】\n不是已实现的样机。"
    )
    disclosure_report = Report()
    check_all(disclosure, meta, None, None, disclosure_report)
    if (meta["document_kind"] != "disclosure" or disclosure_report.count("FAIL")
            or not any(status == "SKIP" and item.startswith("C1–C15")
                       for status, item, _, _ in disclosure_report.rows)
            or not any(status == "WARN" and item.startswith("草稿待确认")
                       for status, item, _, _ in disclosure_report.rows)
            or any(item.startswith("证据语言：") for _, item, _, _ in disclosure_report.rows)):
        print("[self-test] 失败：交底书实施步骤、待确认项或否定句处理有误")
        return 1

    claim = "1. 一种止挡装置，其特征在于，包括止挡和支架。"
    mixed_report = Report()
    check_all(f"技术交底书\n一、权利要求书（草案）\n{claim}\n二、实施例\n1. 装配。",
              meta, None, None, mixed_report)
    raw_claim_report = Report()
    check_all(f"{claim}\n{claim}", meta, None, None, raw_claim_report, "claims")
    if (mixed_report.count("FAIL")
            or not any(status == "PASS" and item.startswith("C1 权利要求编号连续")
                       for status, item, _, _ in mixed_report.rows)
            or not any(status == "FAIL" and item.startswith("C1 权利要求编号")
                       for status, item, _, _ in raw_claim_report.rows)):
        print("[self-test] 失败：交底书内的显式权项区段或独立权利要求书编号处理有误")
        return 1

    print("[self-test] 通过：正式申请错误样例、交底书误报、混合章节边界及重复权项编号")
    return 0


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description="中国发明专利形式合规检查（实现 formal-checklist.md 的机器可判项）")
    ap.add_argument("path", nargs="?", help="待检查的 .md/.txt/.docx")
    ap.add_argument("--kind", choices=("auto", "disclosure", "claims", "specification", "abstract",
                                      "application"), default="auto",
                    help="文档类型。无标题的单件申请文件请显式指定")
    ap.add_argument("--term-table", help="术语表 TSV/CSV（中文术语|英文|缩写|定义|首次出现|禁用词|来源）")
    ap.add_argument("--request-form", help="请求书文本，用于核对发明名称（S1）")
    ap.add_argument("--self-test", action="store_true", help="用内置错误样本自检")
    ap.add_argument("--quiet", action="store_true", help="只输出统计行")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if not args.path:
        ap.print_help()
        return 2
    if not os.path.exists(args.path):
        sys.exit(f"文件不存在：{args.path}")

    text, meta = read_text(args.path)
    meta["path"] = args.path
    rep = Report()
    check_all(text, meta, args.term_table, args.request_form, rep, args.kind)
    out = rep.render(meta)
    if args.quiet:
        print(f"违规 {rep.count('FAIL')}，待确认 {rep.count('WARN')}，"
              f"未检查 {rep.count('SKIP')}，通过 {rep.count('PASS')}")
    else:
        print(out)
    return 1 if rep.count("FAIL") else 0


if __name__ == "__main__":
    # Use the same encoding in the terminal and in captured reports.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
