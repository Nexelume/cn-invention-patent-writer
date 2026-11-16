# Formal compliance checklist

Use this reference whenever the deliverable is a Chinese invention-patent application text or a package intended for filing. Run it as a mechanical checklist, not as prose advice. Each item states its source; items marked `[机]` can be checked by text inspection, items marked `[人]` require reading the document.

Provision numbers follow [legal-baseline.md](legal-baseline.md) (2023 修订版细则, in force 2024-01-20). Do not carry a number into a filed document without re-verifying it.

## Specification (说明书) — 细则第 20 条

| # | Check | How to judge | |
|---|---|---|---|
| S1 | 名称与请求书中的名称完全一致 | string equality between 请求书 name field and 说明书首行名称 | `[机]` |
| S2 | 五个部分齐备且按顺序出现 | 技术领域 → 背景技术 → 发明内容 → 附图说明 → 具体实施方式 | `[机]` |
| S3 | 每一部分前写明标题 | 五个标题逐字存在 | `[机]` |
| S4 | 发明内容同时写明：所要解决的技术问题、技术方案、对照现有技术的有益效果 | 三要素都能定位到具体段落 | `[人]` |
| S5 | 有附图时，附图说明对各幅附图逐幅作简略说明，编号与附图一致 | 图 1..N 一一对应，无缺号、无多余 | `[机]` |
| S6 | 具体实施方式写到本领域技术人员能够实现 | 每个权利要求特征都有对应实现细节 | `[人]` |
| S7 | 不使用"如权利要求……所述的……"一类引用语 | 全文扫描该句式 | `[机]` |
| S8 | 不使用商业性宣传用语 | 扫描"最佳、领先、革命性、填补空白、性能优异"等 | `[机]` |
| S9 | 含核苷酸或氨基酸序列时，说明书包含符合规定的序列表 | 存在序列即检查独立成节 | `[机]` |
| S10 | 术语全文一致（同一部件、同一量、同一动作只有一种叫法） | 建立术语表后比对 | `[机]` |

## Drawings (附图) — 细则第 21 条

| # | Check | How to judge | |
|---|---|---|---|
| F1 | 多幅附图按"图1、图2……"顺序编号排列 | 编号连续、无跳号 | `[机]` |
| F2 | 文中未提及的附图标记不得出现在附图中 | 附图标记集合 ⊆ 正文提及集合 | `[机]` |
| F3 | 附图中未出现的附图标记不得在正文中提及 | 正文提及集合 ⊆ 附图标记集合 | `[机]` |
| F4 | 同一组成部分在全文中使用同一附图标记 | 标记与部件名的映射唯一 | `[机]` |
| F5 | 附图中除必需词语外不含其他注释 | 人工查看：无说明文字、无结论性标注、无表格 | `[人]` |
| F6 | 线条清晰可辨，黑白，背景干净 | 渲染后目视检查 | `[人]` |
| F7 | 版心四周无框线 | 渲染后目视检查 | `[人]` |

## Claims (权利要求书) — 细则第 22 条至第 25 条

| # | Check | How to judge | |
|---|---|---|---|
| C1 | 用阿拉伯数字顺序编号，从 1 开始连续 | 编号序列完整无缺 | `[机]` |
| C2 | 科技术语与说明书完全一致 | 与 S10 的术语表比对 | `[机]` |
| C3 | 无插图 | 无嵌入图片对象 | `[机]` |
| C4 | 除绝对必要外不使用"如说明书……部分所述""如图……所示" | 扫描句式；出现则须说明必要性 | `[机]` |
| C5 | 引用附图中标记时置于括号内 | 形如"所述传感器（1）" | `[机]` |
| C6 | 附图标记不作为限定特征使用 | 人工判断：删除标记后保护范围不应变化 | `[人]` |
| C7 | 独立权利要求包含前序部分与特征部分，特征部分用"其特征是"或类似用语引出 | 定位"其特征在于/其特征是" | `[机]` |
| C8 | 一项发明只有一个独立权利要求，且写在全部从属权利要求之前 | 独权计数 = 1（方法权利要求与对应产品权利要求并存时按同日申请或多独权规则单独判断） | `[机]` + `[人]` |
| C9 | 从属权利要求包含引用部分（引用的权项编号及主题名称）与限定部分 | 形如"根据权利要求 2 所述的方法，其特征在于……" | `[机]` |
| C10 | 从属权利要求只能引用在前的权利要求 | 引用的编号 < 当前编号 | `[机]` |
| C11 | 引用两项以上权利要求的多项从属权利要求只能以择一方式引用 | 形如"根据权利要求 1 或 2 所述"，不得写成"根据权利要求 1 至 4 所述"的并列全取形式 | `[机]` |
| C12 | 多项从属权利要求不得作为另一项多项从属权利要求的基础 | 逐项检查引用链 | `[机]` |
| C13 | 每个技术特征在说明书中有明确记载 | 特征 → 段落映射表 | `[人]` |
| C14 | 独立权利要求不依赖未解释的商务规则、期望结果或纯数学表述 | 人工判断 | `[人]` |
| C15 | 方法、系统、设备、存储介质形式的对应关系只在说明书有支撑时才写入 | 形式与支撑逐一对照 | `[人]` |

C8 note: one independent claim per invention is the default rule; a method claim plus a corresponding apparatus claim in the same application requires a separate look at unity (专利法第三十一条第一款) and at whether the claims still form one inventive concept. Do not apply C8 mechanically to reject a legitimate method-plus-apparatus set — flag it and explain.

## Abstract (说明书摘要) — 细则第 26 条 + 指南第二部分第二章 2.4

| # | Check | How to judge | |
|---|---|---|---|
| A1 | 写明名称与所属技术领域 | 首句可识别 | `[机]` |
| A2 | 清楚反映所要解决的技术问题、技术方案要点、主要用途，且以技术方案为主 | 三要素齐备，方案占比最大 | `[人]` |
| A3 | 文字部分（含标点符号）不超过 300 字 | 字符计数；**注意此项依据在指南 2.4，不在细则** | `[机]` |
| A4 | 不使用标题 | 摘要段首无独立标题行 | `[机]` |
| A5 | 不使用商业性宣传用语 | 同 S8 词表 | `[机]` |
| A6 | 出现的附图标记加括号 | 同 C5 | `[机]` |
| A7 | 有附图时在请求书中指定一幅摘要附图并写明图号 | 请求书图号字段非空且为说明书附图之一 | `[机]` |
| A8 | 摘要附图缩小到 4cm×6cm 仍可分辨细节 | 缩放后目视检查 | `[人]` |

A3 reminder: invoking "细则第 26 条要求 300 字" is a wrong citation. The 300-character rule lives in the guideline; the regulation only prescribes content, chemical formula, abstract figure, and the ban on promotional wording.

## Package-level (申请文件整体) — 指南第一部分第一章 4.6

| # | Check | How to judge | |
|---|---|---|---|
| P1 | 各文件页码分别连续编写 | 说明书、权利要求书、摘要各自从 1 起 | `[机]` |
| P2 | 文字和线条为黑色，背景干净，可复印扫描 | 渲染检查 | `[人]` |
| P3 | 无涂改，行间无加字 | 检查修订痕迹与批注残留 | `[机]` |
| P4 | 无残留占位符、待补充标记、确认清单、起草备注 | 扫描 `【待确认】`、`[待补充]`、`TODO`、`XXX`、`（此处…）` | `[机]` |
| P5 | 文件名、案件名、申请人信息在各文件中一致 | 交叉比对 | `[机]` |

## Evidence language blacklist (this skill's own rule — not a statutory requirement)

These are internal discipline, not legal provisions. Never present them to the user as 法条要求.

Reject any sentence that:

- states a target, design value, simulation result, or paper plan as an achieved industrial outcome ("现场应用后达到…"、"已实现…"、"较现有技术提高 X%" without evidence);
- uses 智能、精准、显著、实时、高效 without a defined operation or measurable metric;
- reports a result without dataset or production period, denominator, exclusions, comparator, version, and protocol;
- blurs measured / calculated / exploratory / training / calibration / historical results into one number;
- attributes an effect to the mechanism when the mechanism does not directly produce it.

Acceptable rewrite: 把无证据的结果改成验收标准、设计参数或拟议目标，并标注证据等级。

## How to report this checklist

Report per section: items checked mechanically (with counts), items checked by reading, items not checkable in this environment and why. A package is not "complete" because the sections exist; it is complete when the requested gates passed and the unrun gates are named. See [deliverable-matrix.md](deliverable-matrix.md) for the closure report.

## Running the checker

`scripts/check_form.py` implements the `[机]` items below in three verdicts — `FAIL` (clear violation), `WARN` (suspicious, rule has a legal exception, human must decide), `SKIP` (not checkable with the available input). It never converts a `SKIP` into a pass.

```bash
python scripts/check_form.py draft.md
python scripts/check_form.py disclosure.md --kind disclosure
python scripts/check_form.py claims.docx --kind claims
python scripts/check_form.py application.docx --kind application --term-table terms.tsv --request-form request.md
python scripts/check_form.py --self-test        # 用内置错误样本验证脚本本身
```

Stdlib only. `.docx` is read through `zipfile`, so paragraph text, revision marks, and embedded graphics are visible without python-docx.

Auto mode uses the document heading and explicit filing sections. Use `--kind claims`, `--kind specification`, or `--kind abstract` for a standalone filing document without a heading. For a single file containing a complete filing text, use `--kind application` and identifiable headings for the three text components. Check separate files individually and use the delivery inventory for the complete package. In a disclosure, embodiment numbering stays outside the claims checks, and pending notes are reported as drafting warnings. An explicit claims section is checked when present. For ambiguous input, review skipped checks and specify the document type where needed.

What the script cannot see, and what therefore stays with the author: whether the disclosure is sufficient, whether each claim feature has support, whether a term is the field's established term (unless a term table is supplied), whether the abstract leads with the technical solution, and every item requiring a rendered page image. Treat a clean `FAIL` count as "no formal defect found by machine", never as "ready to file".
