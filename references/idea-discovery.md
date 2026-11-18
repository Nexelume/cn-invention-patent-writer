# Active invention discovery

Use one Explore workflow with two phases. **Innovation Discovery** builds the opportunity space, compares problems and mechanisms, and validates whether any route merits further work. It does not need patent titles or claim language. **Patent Validation** begins only for a grounded mechanism with a specific, testable difference; it uses the existing [prior-art workflow](prior-art.md). A handoff is not a drafting decision, a patentability conclusion, or an experimental result.

## Choose the starting mode

| Input and intent | First action |
|---|---|
| **Open-ended discovery**: only a broad technical direction, a request for ideas or a contribution to explore | Infer the domain from the supplied context, map current approaches, and propose observable questions with evidence. If several meanings matter, state a working interpretation and make progress where they overlap. |
| **Problem-driven discovery**: a known failure, requirement or design constraint | Separate observation from cause; compare existing ways of addressing the problem under the stated constraints before developing mechanisms. |
| **Idea evaluation**: an existing proposal, wish to test its contribution, or a direction that may overlap prior work | Record the proposed distinguishing mechanism as a hypothesis and try to disprove the difference first. Reopen the problem if its premise is unsupported. |

Apply precedence in this order: explicit user mode and scope, otherwise a concrete executable idea, otherwise a concrete problem or observed phenomenon, otherwise a broad direction. An executable idea has identifiable inputs or components, operative relationship and downstream output or action. In mixed inputs with an executable idea, test it against the supplied problem first; if falsified, reopen problem-driven exploration when authorized. With a concrete problem and only tentative technology names, start problem-driven. Record the mode and why it fits. A popular technology pairing without an executable mechanism is a broad direction, not an existing invention. Ask only for facts that would materially change the answer and cannot be recovered from authorized sources. A wide direction does not require the user to supply a research question or hypothesis. When search or full text is unavailable, use what can be verified, state the gaps, and keep unsupported ideas provisional. A standalone search, audit or formal check keeps its own scope.

## Build an opportunity map before developing mechanisms

| Level | Question | Evidence to advance |
|---|---|---|
| **L1 Capability opportunity** | What materially useful capability is missing or newly attainable? | Domain-specific map of what mature routes already enable, remaining needs and why the opportunity matters. |
| **L2 Technical problem** | Under which conditions do existing methods fail, and why? | An observation or testable conjecture linking a real constraint or failure to a plausible physical, mathematical, computing or system cause. Record the evidence locator or proposed observation, plausible competing explanations (or why none is supported), the discriminating observation, and where a mature solution ceases to suffice under the same constraints. Label the problem OBSERVED or CONJECTURE. An observed symptom leaves its cause open. |
| **L3 Core mechanism** | Which processing, physical or control relationship must change? | Trace input → operation or state change → output → effect. Explain which bottleneck it removes and when an existing simpler mechanism would suffice. |
| **L4 Implementation** | How would the mechanism operate outside the ideal case? | A small buildable or derivable example, required data or components, an observable metric, a boundary and a falsifier. |

Do not rank implementations while L1/L2 are still unsupported or the search only covers one familiar example. In a broad start or scope reset, compare different capability gaps and technical problems; a user-selected narrow problem bounds the map, it does not authorize changing the goal. If the evidence leaves only one defensible opportunity, explain which alternatives were checked and why there is no useful second one. If no problem is grounded, record an incomplete map and the missing observation or source, then stop before promoting a mechanism. A documented conjecture can lead to a verification proposal without being presented as a confirmed bottleneck.

### Work in both directions

Compare existing approaches and the conditions under which they solve the problem while tracing constraints and unexplained failures from the other direction. Use the nearest passages, data or a first-principles argument to turn each plausible boundary into a question, then test proposed mechanisms with new searches. If an existing method already solves the question, revise the opportunity, problem or mechanism at the affected level. Do not change wording merely to avoid a known reference.

## Map the domain and compare mechanisms

Build a bounded map of the object, technical needs and trade-offs, governing principles, major approaches and their relationship, representative results, metrics and test protocols, and limiting conditions. Search more than one relevant source type: foundational sources, representative work from the past five years, especially the last two, and relevant recent preprints, patents, implementations, data or benchmarks and adjacent fields. Log what was actually searched and read, dates, scope and coverage gaps; adapt sources and depth to the field and request. Use public, generic search terms until authorized to expose any unpublished technical details.

Read the original sections of the closest work. Compare problem, conditions and assumptions, model or physical mechanism, inputs, outputs and intermediate states, objective or design criterion, steps, resource constraints, experiments, reported results and failures or limits. Record exact locations. Relate works as competing, inherited, complementary, overlapping or proposing alternative mechanisms, and explain why. Titles, abstracts, authors' Future Work and missed search hits are leads only. A combination of known features is not in itself a technical difference. Once a specific distinction can be queried, follow [prior-art search](prior-art.md) for distinguishing sub-combinations and feature mapping.

## Mine opportunities

Apply all eight lenses to the bounded question. For each, give a source or a stated premise, the concrete reasoning from it, and the resulting question; if it gives no supported lead, record why rather than forcing an idea.

| Lens | What to look for |
|---|---|
| First principles | Which physical, mathematical or computational relation makes the current approximation insufficient, and under what conditions? |
| Relax an assumption | What observable failure could occur when a stated assumption about the object or operating environment no longer holds? |
| Mechanism gap | Which missing signal, state, interaction or constraint would change a measurable downstream action? |
| Failure driven | What verified failure, anomaly or boundary suggests a specific unresolved problem? Treat reported results within their own conditions. |
| Objective or evaluation gap | When would the existing objective or metric improve while the actual technical task failed? |
| Constraint driven | Under which specific data, compute, delay, resource, precision or deployment limit might two methods behave differently? |
| Cross-domain transfer | What invariant, mathematical structure or mechanism carries over, and what must change under the target constraints? |
| Contradiction driven | Which differences in assumptions, data, protocol, metric or mechanism could explain apparently inconsistent results? If no comparable results exist, mark this lens unresolved. |

For a broad start or scope reset, aim to compare **3–5 meaningfully distinct routes** before choosing implementations; fewer is valid with an evidence-based reason, never add routes to fill a quota. Compare routes side by side using their problem, the operation or state they change, and a differing prediction. Check problem-driven solutions, mechanism transfer, capability expansion and changed performance or resource constraints for supported routes. Record material exclusions. For example, passive diagnosis, choosing a new observation, and changing an action-outcome model act on different parts of a system. Changes of industry, object name, model name or tuning do not count if they leave the technical relationship unchanged. Preserve excluded routes; the shortlist still contains at most three.

## Develop and challenge each surviving idea

1. **Develop:** Record the candidate question (object, condition, observed or predicted limitation, criterion), closest work and its limits, proposed input → operation → output → effect, substantive difference, falsifiable prediction, expected technical and potential research contribution, feasibility (data, code, equipment, time or computing), minimal test and an outcome that would refute the hypothesis. Record unresolved elements as unknown. A public source can establish how an existing mechanism works; it cannot establish the applicant used it or achieved an effect.
2. **Check cross-domain transfer:** Search for the same operation or mathematical structure in neighboring fields. Apply the [cross-domain mechanism check](terminology.md#cross-domain-mechanism-check): map target inputs and state, specific operation, what output/action changes, and what differs without it. Explain which assumptions survive, what must be redesigned and why a difference matters. A routine port to a new dataset, device or field is an application; an unsupported borrowed concept stays out of the main chain.
3. **Challenge in a separate pass:** Restate the claimed difference and compare it against original evidence without relying on the generator's rationale or ranking. Search for equivalent operations under different names, the same objective or protocol, highly similar mechanisms, and combinations a skilled practitioner could make without the proposed change. Try a stronger comparator or a counterexample where the mechanism adds no effect. Record queries, passages, contrary evidence, coverage gaps, and the challenge verdict separately from the candidate. This exploration pass challenges the provisional shortlist. Formal candidate admission uses [independent adversarial review](candidate-validation.md#independent-adversarial-review).
4. **Classify the review:** **Supported** = documented initial support for the specific technical distinction after challenge; **Plausible** = concrete possibility with a material open question; **Overlapping** = substantial overlap with published work, with any remainder identified; **Unsupported** = too little evidence or no working mechanism; **Rejected** = the current route has a decisive flaw or is not worth pursuing on the evidence. Keep the reason and evidence per idea. A partial search cannot support a confirmed originality claim, and none of these labels represents a patentability decision.

## Record the innovation boundary and return when it moves

For each route still under consideration, record **what was actually covered, by which passage and under what conditions; what overlap excludes; what remains to test or search; and what would defeat that narrower difference**. Compare mature solutions and technically compatible combinations; where coverage or a simpler baseline can erase the distinction, do not invent a gap as a workaround. The boundary describes the evidence read so far, not confirmed novelty.

| Trigger | Reopen | Required action |
|---|---|---|
| Scope too narrow | L1, then L2 | Preserve the user's actual feedback and recompute the opportunity map. Changing the implementation example alone does not respond to the feedback. |
| Wrong or unclear problem | L2 or L1 | Recheck the observed failure, demand and competing explanations. |
| Routes too similar, no substantive difference, too complex, or a simpler baseline suffices | L3 or earlier | Compare truly different mechanisms; exclude the defeated route unless new evidence changes the conclusion. |
| Prior art, test failure, or new evidence | The affected level or higher | If newly found art or a refuted causal effect removes the distinction, revisit L3 and redo the search for any redesigned mechanism. A simpler baseline that meets the same target and constraints retires the defeated mechanism and reopens L3 or earlier. If evidence removes the problem or capability gap, revisit L2 or L1. Use L4 for an implementation-specific defect when the mechanism and effect rationale still stand. For inconclusive evidence, suspend advancement and record the missing comparison. |

Record each return in the [opportunity record](opportunity-record.md): trigger, invalidated assumption or route, reason, source, level, and next exploration. Preserve excluded IDs; record a substantive change and recheck affected evidence before recommending a revised route. Unaffected routes can be carried forward with a reason. A return cancels the current handoff until the comparison is redone; it does not automatically change the user's agreed scope. Stop when sources or experiments can no longer change the decision at a proportionate cost.

## Minimal discriminating check and value

For each retained mechanism, name the hypothesis and competing explanations, manipulated and controlled variables, closest defensible external baseline and necessary ablation, independently observed outcome and metric, predicted results, result that would refute it, inconclusive case and stopping rule. Prefer the smallest check that can change the decision: a source check, derivation, log replay, design walkthrough, simulation or controlled measurement as appropriate. If the problem itself is uncertain, first distinguish whether it exists and what causes it. Label proposed tests as not run; reserve measured claims for actual evidence.

Judge problem importance, practical need, difference from prior work, mechanism originality and rationale, falsifiability, data/code/equipment access, cost and time, expected contribution and risk independently. Missing necessary inputs, unresolved overlap or no way to test the important claim cannot be outweighed by convenience or application value. For the next action, explain what uncertainty it resolves, why now, what a cheaper alternative could show, what each result changes and when to stop. This is the Experiment Value Audit for the discovery handoff; it does not authorize execution.

## Idea record and decision

Keep the map, route comparison, boundaries and returns in one [opportunity record](opportunity-record.md); use the existing task note if present. If no file write is authorized, return the findings in the answer and run the structural check on stdin when available. State research value, substantive technical difference, protection potential and provability separately. Report source and reading limits, verification status, exclusions, and the smallest action that can change the decision. A valuable research question can have little protection potential and a promising mechanism can lack usable verification.

Before handing a route to Patent Validation, record the specific implementation, covered boundary and remaining difference, combination risk, original source locations, minimal test and falsifier; validate the current record. Use [candidate validation and admission](candidate-validation.md) to search and compare each candidate, test alternatives and combinations, seek independent review and record the grade. If evidence is missing or the record checker cannot run, say which check is incomplete and keep the handoff pending. A passed record check verifies the order and required fields, not the correctness of the research.

## Handoff to drafting

Before an idea developed or changed in Explore enters drafting, require all of the following:

- Complete the [problem and material check](project-intake.md#problem-and-material-check). Separate the applicant's actual materials, public evidence, and any proposed implementation. A draft-ready design need not already have bench results.
- Complete [candidate validation](candidate-validation.md) for the current mechanism, including its independent challenge. A provisional or blocked disposition remains in exploration. Confirm the user's technical spine separately before drafting. A valid discovery handoff only starts this review. If missing disclosure or overlap could overturn the claimed difference, keep it in exploration and specify what to check next.
- Record the minimum discriminating test design and the Experiment Value Audit. If it has not been run, mark it as such; if it is needed to resolve a decision that would change the main mechanism, wait for that evidence.
- Record the confirmed question, object and conditions, mechanism, predicted effect, and evaluation criterion (**Research Thesis Lock** here means confirmation of the technical spine, not a new project system). Reuse the user's existing explicit decision if it covers this scope. Obtain confirmation for a new goal, core mechanism, main hypothesis or changed evaluation protocol before treating it as fixed. Use the ordinary drafting request to establish which deliverable is authorized; substantive adoption, substantial experiments, and formal claims about contribution or achieved results are not implied by permission to explore.

Apply the [concept gate](invention-selection.md) to the grounded chain. Do not start a disclosure, claims, an application or experiments merely because a direction was recommended. Use the same primary workflow throughout. The independent review is one bounded pass in a separate session.
