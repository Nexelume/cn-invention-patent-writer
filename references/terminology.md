# Terminology discipline

Use this reference before drafting any deliverable text, and again in the final audit. The rule it implements is absolute: **a patent must be written in the established technical terminology of its own field.**

Terminology affects whether the description is clear and complete (专利法第二十六条第三款), whether the claims are supported and define their scope clearly and concisely (第二十六条第四款), and whether a later amendment adds matter (第三十三条). Use terms that identify the actual technical object and mechanism.

## Rule

1. **Name the field first.** Before writing a sentence, state the field in one line and the classification context if available (IPC/CPC main group, or the closest 分类号 found during prior-art search). The field determines the vocabulary; the vocabulary does not determine the field.
2. **Use the field's own words.** Every technical noun, quantity, operation, and unit must be the term a practitioner in that field would use in a paper, a standard, or a product datasheet — not a general-purpose synonym, not a translation of convenience, not a word borrowed from a neighbouring field.
3. **One concept, one term, everywhere.** Title, abstract, claims, specification, embodiments, and figures use the same term for the same thing. Synonym rotation is a defect, not variety. The claim term and the specification term must match verbatim (细则第 22 条第三款).
4. **No invented terms.** Do not coin a term to make the invention sound novel. If the field has no term for the thing, either it is not a technical feature, or it must be defined explicitly in the specification at first use and used consistently afterwards.
5. **Label uncertainty instead of substituting a generic word.** When the correct domain term is unknown, write the candidate term followed by `【术语待核】`, propose two or three alternatives with their sources, and ask. Never silently downgrade to a generic word such as 模块、装置、单元、数据、信息、处理.
6. **Multi-field inventions keep both vocabularies.** For a cross-domain chain (for example acoustics plus machine learning, or mechanics plus control), use each field's own terms and add one sentence at the junction that states how the two vocabularies refer to the same object. Do not flatten one field into the other's words.

## Term sourcing hierarchy

Prefer, in order:

1. National or international standards — GB/T, GB, JJG, ISO, IEC, ITU-T — quoted with the standard number and the clause.
2. Authoritative textbooks, monographs, and review articles in the field.
3. 《专利审查指南》 and granted patents in the same classification, for terms that CNIPA examiners already accept.
4. Official datasheets, manuals, and specifications of the actual equipment, instrument, or software involved.
5. Manufacturer and industry-association glossaries.
6. General dictionaries — last resort, for spelling only, never for scope.

Every non-obvious term in the term table carries the source it came from. A term with no source is a term to confirm.

## Term table (build before drafting)

Maintain one table and attach it to the working notes. It is the artefact the audit runs against.

| 中文术语 | 英文对应 | 缩写 | 定义（一句话，含单位/量纲） | 首次出现位置 | 禁用/易混词 | 依据来源 |
|---|---|---|---|---|---|---|

Rules for the table:

- Fill the 定义 column with what the term denotes in this invention, not a dictionary definition.
- The 禁用/易混词 column is what prevents synonym drift: list the words that must **not** be used, including the general word the user or the source material happened to use.
- An abbreviation appears once as 中文全称（英文全称，缩写）at first use, then only as the abbreviation. Never introduce an abbreviation that is used only once.
- Quantities carry units in the table, so that the specification, the claims, and any formula agree.

## Field-specific traps

- **Upper versus lower generality.** Claims normally take the broader concept; embodiments take the specific one. Generalising a term is allowed only if the specification supports the broader scope — otherwise the generalisation becomes an unsupported claim (专利法第二十六条第四款).
- **Borrowed metaphor.** Words that are vivid in speech (阈值线、漏斗、骨架、血缘、画像) are marketing shorthand unless the field defines them. Either define them or replace them.
- **Translation artefacts.** Machine-translated terms often pick a literal but wrong rendering. Cross-check the English term against the field's own usage before adopting the Chinese one, and record which English term the Chinese one maps to.
- **Unit and symbol discipline.** Same symbol, same meaning, no reuse; every symbol in a formula defined with unit, normalisation, feasible set, and behaviour when no feasible solution exists (see [drafting.md](drafting.md)).
- **Action verbs.** 采集、标定、解算、滤波、配准、反演、拟合、推理、下发、联锁 carry different technical commitments. Choose the verb that states what physically happens, not the one that sounds advanced.
- **Product and vendor names.** A brand name is not a technical term. Write the device class, and if the specific model matters, put it in an embodiment.

## Audit pass

Run these before delivery; most are mechanically checkable against the term table.

| # | Check | |
|---|---|---|
| T1 | 领域与分类已明确写出 | `[机]` |
| T2 | 术语表中每个术语都能定位到首次出现位置 | `[机]` |
| T3 | 全文只使用术语表中的词，无同义替换 | `[机]` |
| T4 | 禁用/易混词在全文出现次数为零 | `[机]` |
| T5 | 权利要求术语与说明书术语逐条一致 | `[机]` |
| T6 | 缩写首次出现有全称，且全文只出现缩写 | `[机]` |
| T7 | 量、符号、单位与术语表一致，符号无复用 | `[机]` |
| T8 | 无自造词、无营销词、无未定义比喻 | `[人]` |
| T9 | 跨领域方案的两套术语在衔接处已说明对应关系 | `[人]` |
| T10 | 上位概括处有说明书支撑，未超出公开范围 | `[人]` |
| T11 | `【术语待核】` 已全部清零或列入待确认清单 | `[机]` |

T3 and T4 are the two that catch the most real defects: synonym rotation and the user's own colloquial words leaking into the text.

## Reporting

In the closure report, state: the field and classification used, how many terms the table holds, which terms were sourced from standards or literature, which were confirmed by the user, and which remain `【术语待核】`. Do not report "terminology consistent" unless T3 to T7 were actually run.

Terminology work is technical drafting support, not legal advice; a patent attorney reviews the final wording.
