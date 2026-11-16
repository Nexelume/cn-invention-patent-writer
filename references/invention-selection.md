# Invention selection and application architecture

Use this reference when mining patent points, ranking alternatives, or deciding whether to split applications.

## Concept gate (run before drafting any disclosure or claim)

Do not write the first idea that forms. The inventive concept is the one thing no rule can check for you — it comes from the model, and a weak concept cannot be rescued by clean formatting. The gate below forces a real selection instead of letting the first plausible thought through.

Before drafting, produce and record:

1. **At least three candidate technical chains**, each stated as one full chain — input → mechanism → output → effect — not as module names, feature lists, or "AI + X" slogans.
2. **For each chain, the closest prior art and the distinction**, in two parts: (a) what the closest art actually does; (b) what this chain does differently. State whether that difference is a technical mechanism or merely an effect-level phrasing such as "more accurate", "more intelligent", "more efficient".
3. **A stated rejection for all but one chain.** Each discarded chain gets a one-line reason that names the specific defect (for example: the mechanism is replaceable without changing the effect; the difference is only a desired result; the chain has no executable downstream action; the support is missing). A chain with no recorded rejection must not be silently dropped.
4. **The one retained chain, with its three supporting tests**: (a) the effect is directly produced by the distinguishing mechanism, not asserted alongside it; (b) the mechanism survives the Industrial-AI test in SKILL.md (or, for non-AI inventions, has a concrete physical / signal-processing / control mechanism); (c) it has fallback positions that become dependent claims.

This is a hard gate: if fewer than three chains are examined, state that and why. Record the comparison so the selection can be reviewed. This process consumes additional context and does not by itself demonstrate better invention quality or patentability.

The gate does not substitute for a novelty search. It only guarantees that the concept was chosen, not that the choice is novel. A prior-art search may still overturn it.

## Candidate-point card

For each candidate, state: technical object and limited state; input data and how records, positions, times, materials, or devices are associated; distinguishing operation or structure; executable output or controlled state; direct technical effect; closest-prior-art risk; evidence status and missing support; possible independent claim and fallback limitations.

## Ranking

Prefer candidates with a complete technical chain, a concrete distinction from the closest art, implementable support, a measurable or explainable technical effect, and useful fallback positions. Do not rank a candidate highly merely because it uses AI, a novel name, or a large claimed result.

## Split test

Split only when each application has its own input, mechanism, output, effect, closest-art distinction, and implementation support. Otherwise keep a single inventive spine and use dependent claims or alternative embodiments.

## Protection ladder

Start with the broadest supportable mechanism, then add dependent limitations for data association, structures, model or circuit choices, calibration, constraints, thresholds, interfaces, fault handling, and feedback. A desired outcome alone is not a limitation.
