# Candidate validation and admission

The opportunity record is the continuing record from user input to the final decision. Work through these stages and reopen a stage when the evidence changes.

| Stage | Work and decision |
|---|---|
| A. Select the mode | Record the requested or inferred mode, priority rule and scope. |
| B. Map opportunities and problems | Compare technical routes and needs, operating constraints, evidence for bottlenecks, competing causes and existing solutions. |
| C. Compare distinct mechanisms | Develop opportunities from observed problems, mechanism transfer, new capabilities and changed constraints. Record the relevant input, operation and effect. |
| D. Search at mechanism level | Search the five source categories and neighboring fields for the distinguishing sub-combination and close alternatives. |
| E. Establish the technical boundary | Compare each publication separately, challenge combinations, drop defeated routes and re-search any changed technical relationship. |
| F. Design technical validation | Specify implementation, boundary conditions, simple and closest baselines, ablation, outcome and falsifier. Record the evidence actually available. |
| G. Review and decide | Independently challenge the candidate and record the A–D disposition. Retain previous routes and reasons. |

Early-stage discussion may return a provisional opportunity or a gap. If the user asks for a candidate judgment, give the applicable grade even when bounded evidence blocks progress. Use B/C for unresolved or blocked cases and D for a decisive defect. Describe the assessment depth and missing checks. A grade A requires a current validation handoff. A user request restricted to search, exploration or audit keeps that scope.

## Search and comparison

Use the [existing search workflow](prior-art.md) to construct Chinese and English queries and execute the rare distinguishing sub-combination first. Search across disciplines for equivalent operations and prior transfers. For a borrowed mechanism, trace what operates on the target input, which conditions differ and what changes in the downstream system. Treat routine application as a possible alternative. Separate bibliographic dates, eligibility and current registry status. Use the relevant original publication for feature evidence and record unavailable or unverified information explicitly.

For each candidate judgment, append an `ASSESS` event in the [opportunity record](opportunity-record.md). Use a current `VALIDATE` handoff to advance toward A. Before handoff, a compared route can receive a preliminary B, C or D with explicit coverage and evidence gaps. The event has `route_id`, `candidate`, `evidence`, `technology`, `axes`, `review` (receipt or null), `review_pending_reason` if null, and final `grade`. A supported first-pass difference remains subject to deeper search.

- `evidence.scope`, `relevant_date` and `combination_limits` record what was covered, the date context and the limitations or reason no combination is credible. If a relevant date is unknown, assess conditionally and capture the gap.
- `coverage` is keyed by `CN_PATENT`, `INTERNATIONAL_PATENT`, `PAPER`, `STANDARD`, `PRODUCT`. Each entry has `status` (REVIEWED, NO_HITS, PARTIAL, UNAVAILABLE, OUT_OF_SCOPE, NOT_RUN), `database`, `language`, `date`, `scope`, exact `queries` (list) and `limits`. NO_HITS means the stated search yielded no relevant hit. Include Chinese invention patents and utility models, and identify international families within their respective entries.
- `references` is a list of records with stable `id`, exact `publication_id`, `title`, `url`, `category`, publication `publication_date`, `read` (FULL relevant original disclosure, PARTIAL or UNAVAILABLE) and `eligibility` (ELIGIBLE, CONFLICTING, INELIGIBLE, UNKNOWN). Patent entries also include `publication_kind`, `family`, `priority_date`, `filing_date`, `legal_status` and `legal_status_source`. Add applicant, application number, bibliographic sources and dates of access as required by the prior-art workflow.
- `features` is a list of essential features and relationships, with `id` and `description`. `matrix` is keyed by reference ID, then by feature ID. Each cell has `finding` (EXPLICIT, IMPLICIT, NOT_FOUND, UNCERTAIN), original `locator` and the `evidence` it supports or the text that was checked. Identify the independent or dependent claim and its parent chain, or the exact embodiment, figure or paper section. For NOT_FOUND, the relevant original disclosure and searched sections are required. For UNCERTAIN, record what is missing. If the material is abstract-only, state the limitation and keep the affected findings uncertain.
- `single` is keyed by the same IDs with `outcome` (ALL, PARTIAL, UNCERTAIN) and `basis`. Assess all essential features together as one teaching in that version. If all features appear but their stated relationship is ambiguous or stitched across embodiments, record UNCERTAIN. Keep novelty, inventive step and granted scope separate.
- `combinations` is a list of records with `id`, `start`, `supplement` (source IDs), `adds` (missing feature IDs), `motivation`, `interfaces` (and adaptations), `conditions`, `expected_effect`, `locators` (list), and `outcome` (PLAUSIBLE, INCOMPATIBLE, UNCERTAIN, DECISIVE). For more than two documents, link each successive addition to the previous combination ID via `previous`; keep the same `start` and supply a distinct supplement whose disclosure adds a still-missing feature. Explain how each interface adapts and what cumulative effect follows. Use `DECISIVE` only for an eligible chain that covers the required features and relationships, with no incompatibility left unresolved. A possible combination remains a risk. A documented decisive combination or a single eligible publication covering the complete teaching defeats the affected candidate.

## Technical validation

The `candidate` fields are `title`, `field`, `problem`, `closest` (source ID or null with reason in the record), `known_limit`, `mechanism`, `steps` (list), `difference`, `effect_cause`, `minimum_implementation`, `operating_conditions`, `failure_handling`, `claim_core` (essential feature IDs), `claim_fallbacks` (list), `unknowns` (list) and `next_action`. In the mechanism and steps, identify inputs, processing, decisions, output and state changes. A claim outline identifies the functional relationships, dependencies and fallback features. Where evidence is absent, leave an empty claim list or state the precise gap.

The `technology` fields are `hypothesis`, `metric`, `controls`, `simple`, `closest`, `ablation`, `falsifier`, `consequence`, and `result_status`. Each comparator has `method`, `comparison_conditions` and `criterion`. Choose the same target, resources and constraints, check if the simpler process already suffices, and test the proposed causal relationship. Include a negative/boundary case. Status is PLANNED, INCONCLUSIVE, SUPPORTED, REFUTED or SIMPLE_SUFFICIENT. Any status other than PLANNED requires an `observation` and `result_source`. An unexecuted experiment remains PLANNED. Explain whether its possible outcomes change the difference, implementation, problem or next action.

A failure of the causal mechanism or an equal simple baseline returns to the mechanism comparison. A defect limited to implementation can return there while preserving the independently supported technical mechanism. When evidence changes the problem or capability gap, reopen the map. Record the original evidence and revise the source comparison for the changed candidate before requesting another review.

## Independent adversarial review

Give a fresh reviewer the neutral candidate, baselines, search scope, publication identifiers and relevant checked passages. Leave out the author's ranking, score, risk conclusions and recommendation. The reviewer must be free to reject, require redesign, suspend, or clear a candidate at this depth. It assesses problem, novelty, inventive step, necessity, causal effect, feasibility, implementation detail, transfer and protection. For each point, identify a concrete counterexample or the strongest remaining objection and an original evidence locator or evidence gap. A same-session challenge can help prepare the packet.

Use a bounded independent host session if available, or run this command from the skill directory on the same single-event file you will include in the record.

    python -B -X utf8 scripts/patent_validation.py assessment.json --model <available-model>

The CLI starts a fresh temporary session and disables web search in that session. Supply original passages and enough evidence in the packet. Use only candidate materials authorized for the selected runtime. For an independent public counter-search in the host session, use generic public search terms. Add any material new sources and reading limitations to the evidence and bind the review to the updated packet. The tool returns an independent-session receipt. For a host review, record its actual session ID, model, executor `host_independent_session`, packet digest and review body. Retain the original trace for a host review. Never manufacture a receipt or reuse the generating session. If the independent run is unavailable or incomplete, record why and leave A pending. An independent model review is scoped technical analysis. A reviewer may use the same model in a separate session.

The review body has `disposition` (CLEAR, REVISE, BLOCK, REJECT) and `points`, keyed by `problem`, `novelty`, `inventive_step`, `necessity`, `effect`, `feasibility`, `implementation`, `transfer` and `protection`. Each point has `status` (SUPPORTED, OPEN, BLOCKED, DEFEATED), `basis`, `locator`. The most serious finding determines the disposition. The receipt records the digest of the candidate evidence the reviewer saw. A material change to the neutral packet requires a current receipt.

## Admission and delivery

Record `axes` for `novelty`, `inventive_step`, `effect` and `feasibility`, each with `status` (SUPPORTED, OPEN, BLOCKED, DEFEATED), `basis` and `locator`. SUPPORTED at this stage means supported enough to invest in the next review under the stated conditions. State separately whether an effect rationale is theoretical and whether a test has been run. Consider protection potential, including whether the independent feature chain can be bounded and supported.

| Grade | Decision | Gate |
|---|---|---|
| A | 值得进入深度查新 | Scope has searched all five categories, closest eligible full disclosure and supported claim outline are mapped, four axes have preliminary support, and a fresh independent review clears the current packet. |
| B | 值得继续构思 | A specific route remains worth exploring. Open or incomplete evidence, a pending independent review or a revision need keeps the route at this stage. Give the smallest next check. |
| C | 暂不建议申请 | The evidence or review identifies a material blocker. Explain what must change to reopen the candidacy. |
| D | 淘汰 | A decisive flaw, refuted effect, sufficient simple baseline, decisive prior art or independently substantiated rejection defeats the recorded candidate. Preserve the reasons and return if there is a different viable mechanism. |

A recommends deeper search at the recorded scope. Patentability and filing decisions require their own evidence. A failed axis cannot be offset by another strong axis. A G-stage rejection returns to the affected stage or closes the route as retired. A B/C/D assessment made before handoff still records the search gaps, reviewer availability and the evidence supporting the disposition.

Report, in the user's language, each candidate's name, field, problem, closest art, known limit, mechanism and steps, feature comparison, effect and causal basis, minimum implementation and boundary, validation and failure criterion, possible claim structure, novelty and inventive-step risks, gaps, grade and next action. Keep the opportunity history and the dispositions of alternatives. Report partial records as partial. Run the [record checker](opportunity-record.md) on the current chronology and verify citations against originals. The checker validates structure and gate consistency. The user or a qualified technical or patent reviewer judges evidence accuracy and the strength of a substantive distinction.
