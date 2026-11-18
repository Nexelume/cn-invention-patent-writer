# Prior-art search and novelty mapping

Use this reference when the task includes related-patent search, novelty, inventive-step positioning, patent-family analysis, or citation verification.

A novelty assessment requires feature-by-feature comparison against the full disclosure of the closest references. Label a requested preliminary scan as preliminary, and record any evidence gap that prevents a completed assessment.

## Search decomposition

Search the invention through several independent concept groups:

1. industrial object and failure or quality state;
2. data association or process-tracking mechanism;
3. prediction, optimization, control, or decision mechanism;
4. knowledge, rules, constraints, uncertainty, calibration, or safety mechanism;
5. executable disposition or control action;
6. downstream technical effect.

Run Chinese and English synonym variants. Search both the complete chain and the rare distinguishing sub-combinations. Classification codes can expand results but do not replace keyword searches.

## Search-string template (do not improvise)

For every concept group, build a search string mechanically. The template below is the minimum repeatable form; adapt the keywords but not the structure.

**Step 1 — keyword pools.** For the invention, list keywords per group in a two-column table (中文 / English synonym), drawn from the term table in [terminology.md](terminology.md). Example pools:

| Group | 中文关键词 | English synonym |
|---|---|---|
| object + state | 多智能体 / 科研自动化 / 报告生成 | multi-agent / scientific automation / report generation |
| data association | 证据对齐 / 断言校验 / 引用可验证 | assertion-evidence alignment / verifiable citation |
| mechanism | 冲突仲裁 / 置信治理 / 预算调度 | conflict arbitration / confidence governance |
| rule / uncertainty | 最小充分支持 / 支持度阈值 | minimum sufficient support / support threshold |
| action | 再检索 / 重写 / 人工复核 | re-search / rewrite / manual review |
| effect | 可溯源 / 可审计 / 减少无效实验 | traceability / auditability |

**Step 2 — combine.** Build three kinds of query, always in both languages:

- **Chain query** (breadth): object + mechanism + action, e.g. `多智能体 科研 冲突仲裁 证据` / `multi-agent scientific conflict arbitration evidence`.
- **Distinguishing sub-combination query** (precision): the one or two features you believe are rarest, e.g. `断言证据对齐 最小充分支持` / `assertion evidence alignment minimum sufficient support`. **This is the query most likely to surface the single closest reference — run it first, not last.**
- **Classification query**: IPC/CPC main group + mechanism keyword, e.g. `G10L 双耳房间冲激响应` / `G10L binaural room impulse response`.

**Step 3 — record.** Write every query string verbatim into the evidence register, with the date and the database used. A search whose queries were not recorded cannot be reproduced and must be reported as such.

## Source hierarchy (calibrated to what each source actually returns)

Rank sources by what they actually provide, not by authority name alone:

- **Publication full text:** Prefer the official publication and published language. Use patent office sources (including CNIPA, EPO Espacenet, and WIPO PATENTSCOPE) or full-text indexes such as Google Patents or PatSnap to locate it. Resolve material differences in extracted text, translated terms, claims, and drawings against the publication.
- **Bibliographic and legal-status verification:** Use the relevant patent office records to confirm application number, dates, publication version, and status. Record anything that could not be verified and assess conditionally where it matters.
- **Non-patent literature:** original standards, journal or conference papers, theses, official technical manuals, product documentation. Cite the original, not a search-results page.

## Coverage for patent candidate validation

Record five search entries for each candidate: Chinese invention patents and utility models, international patent publications and families, papers, technical standards, and public products or technical documentation. Search neighboring fields for the same mechanism across these sources and record which adjacent mechanisms were checked. For each entry record date, database, languages, scope, exact queries, results, original-text access and gaps. An unsuccessful search describes its own coverage. Record user-scoped or inaccessible categories explicitly. See [candidate validation](candidate-validation.md#search-and-comparison) for the schema.

## Evidence record

For every retained patent, record:

- publication number, application number when available, and family relationship;
- title, applicant or assignee, inventors if relevant;
- priority date, filing date, publication date, and legal status where needed;
- exact paragraphs, claims (including applicable parent claims), pages, or figures supporting each mapped feature;
- source URL and access date;
- whether the record is a patent application publication, grant publication, utility model, or non-patent reference, and which version supplied the mapped text;
- the date relevant to the assessed claim, if known, and whether the reference is eligible as prior art, a potential conflicting application (抵触申请), or of uncertain status for this analysis. If the relevant date is unknown, give a conditional assessment.

Never infer content from the title or abstract alone when the mapped feature depends on claim language or a detailed embodiment.

Link each material assertion about what an existing technique does or fails to do to a source and locator. Keep unverified statements as background hypotheses, including in a disclosure. A patent publication can document disclosure of a feature, an external paper can document the author's reported result, and a project run can document an observation under its own conditions. State what the source supports before comparing effects. Use authorized search terms that avoid exposing unpublished invention details.

## Novelty matrix

Use one row per essential feature (including required relationships or steps) and one column per specific publication and version. Keep different publications in separate columns, including a patent and a similar paper. Use the retrieved A/B or international member actually read as its own column if mapped. The register records family relationships; each matrix cell uses the disclosure of its own publication. Record two separate fields in each cell:

| Field | Values |
|---|---|
| Disclosure finding | 明示公开 (explicit) / 隐含公开 (directly and unambiguously derivable) / 未找到 (not found in the reviewed full text) / 不确定 (unavailable or ambiguous evidence) |
| Evidence location | 独立权利要求 / 从属权利要求（注明引用链） / 说明书、实施例或附图 / 非专利文献. Record each material location and a precise locator. For 未找到 or 不确定, record the sections checked and any missing evidence. |

For an implicit finding, explain the link from the cited text or figure to the feature. Record partial matches at their actual level of detail and identify the missing limitation. A broad label may disclose a general function while leaving a specific implementation unresolved.

Do not use percentages as a substitute for this matrix. A document can be semantically similar yet miss an essential feature, or look different while disclosing the same technical chain.

## Disclosure checklist

For each essential feature and reference:

1. Review the independent claims for the same technical operation or structure, including its inputs, outputs, and required relationships. Record the claim number and the limitation actually disclosed.
2. Review the dependent claims and trace their references. Identify the added limitation, its parent chain, and the applicable branch of any alternative dependency. Check compatibility before combining features.
3. Review the description, embodiments, and drawings. An optional embodiment can disclose an implemented feature. A statement of desired effect, an unexplained mention, or a drawing that permits several interpretations does not by itself disclose the specific means. Record the related passage and what it establishes.
4. Use **未找到** only after reviewing the complete relevant disclosure of that publication and documenting the search terms or sections checked, including synonyms, conditions, and relationships. Use **不确定** when missing material or ambiguity could change the finding. For non-patent sources, apply the same check to the full relevant text, figures, and supplements where needed.

Disclosure location does not determine its legal effect. For novelty, test whether one eligible reference discloses the assessed claim's complete combination in a single technical teaching, explicitly or directly and unambiguously. A dependent claim with its inherited features or an embodiment in the description can supply that teaching. Do not assemble a novelty objection from unrelated embodiments, sibling claim branches, or multiple references. Treat claim scope separately: a feature mentioned in a publication does not by itself show that a patent was granted or that an in-force claim covers the proposed implementation. A feature omitted from the claims has not necessarily been relinquished. See [legal-baseline.md](legal-baseline.md) for the Chinese examination sources.

## Mandatory workflow (this is what makes a search a search)

A search is **not complete** when similar patents are found. It is complete only after the feature comparison is done. Execute these steps in order and report the scope and any skipped steps. For an assessment restricted to user-supplied references, use the supplied corpus, start at step 3, and report that no external search was performed.

1. **Decompose and build strings.** Produce the three query kinds above in both languages and record them verbatim.
2. **Run the distinguishing sub-combination query first**, then the chain query, then the classification query.
3. **Select the closest references** by technical relevance, starting with 1–3 and adding material references that affect the conclusion.
4. **Retrieve the claims and full disclosure** for each patent reference, or the original text for a non-patent reference. An abstract-only record remains a screening lead. Without the relevant text, mark the feature comparison 不确定.
5. **Apply the disclosure checklist and fill the novelty matrix** feature by feature. Record the disclosure finding, locator, and limits of each match.
6. **Assess each claim as a whole.** Record the document's eligibility and the technical teaching that does or does not disclose the combination. Evaluate inventive step separately, then follow the search-to-revision loop within the requested scope.

## Search-to-revision loop (close the loop)

1. **Decide whether the current combination can remain.** If one eligible reference discloses it, report the novelty risk and stop drafting that combination as a new invention. If only part matches, retain known features that are necessary to define the mechanism, its operation, or its relationship to other features. Their role in the claim is independent of novelty.
2. **Test candidate distinctions.** Take the 未找到 features or relationships from the comparison and, if further search is in scope, search them again using synonyms, the distinctive sub-combination, and adjacent technical fields. Resolve material 不确定 entries where possible. A single reference's silence does not establish an unoccupied area. A desired effect needs a disclosed mechanism that produces it.
3. **Test the proposed chain.** Identify a defined input, executable mechanism, output or system action, and directly attributable technical effect. Explain how the candidate distinctions interact with the necessary known features, where the user's materials support the mechanism, and what technical problem and combination rationale the closest art suggests. Flag any genuinely new or unsupported mechanism for confirmation.
4. **Close within the authorized deliverable.** In exploration, search, or audit, report which candidate chain merits further review or which evidence is missing. Where drafting or revision is authorized and the chain is supported, use the chain to revise the claim outline and cite the closest reference in the disclosure. If no coherent supported chain remains, pause claim drafting and identify the smallest missing technical or evidence item. Record the decision and any revision actually made.

## Combination and simple alternatives

After the single-document findings, test technically credible combinations separately. Record the starting document and its operation, each missing feature and the supplementary disclosure supplying it with precise locations, the technical reason a skilled person would adopt it, interfaces and state/data compatibility, operating conditions and constraints, required adaptations, and whether the resulting effect would reasonably follow. Record successive additions for combinations involving more than two documents and assess the cumulative technical teaching. Shared field or objective alone does not establish a combination.

Test the simplest credible alternative separately from the closest published mechanism under the same target, constraints, metric and conditions. If evidence establishes it suffices, retire the extra mechanism and reopen route comparison. If equality is only suspected, record the comparison that could resolve it. Explain which effect requires the added operation.

## Conclusion discipline

Separate:

- novelty risk: one eligible reference discloses all essential features in the claimed combination, including the required relationships. Check dates and the applicable conditions before treating an earlier-filed, later-published application as a conflicting application. A conflicting application in that capacity is considered for novelty, not inventive step;
- inventive-step risk: identify the closest prior art, the differences and their technical effects, the technical problem actually solved, and whether prior art gives a reason to make the proposed modification or combination. A difference may be obvious even if no single reference discloses the combination;
- drafting risk: the supposed distinction is only a desired result, generic AI wording, or an unsupported parameter;
- search limitation: database, language, time, family, or full-text gaps.

State the searched scope and unresolved gaps. A negative search finding supports a candidate distinction for further assessment. It does not establish patentability or freedom to operate.
