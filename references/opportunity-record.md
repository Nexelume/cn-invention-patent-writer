# Innovation opportunity record

Keep one chronological record per exploration request. Preserve earlier events and their reasons. The same record can stay inline for a read-only or conversational task. Keep source locators close to each judgment: source ID or URL with a passage, project record, derivation premise or user feedback. Distinguish verified facts, inferred causes, and proposed mechanisms in `basis`, `cause` and decision notes. A provisional problem is not a verified result.

The UTF-8 JSON fields below are the subset checked by `scripts/check_discovery.py`. More explanation can go beside the record. Write it to disk only within the authorized deliverable. To check the record, run from the skill directory:

```text
python -X utf8 scripts/check_discovery.py <record.json>
python -X utf8 scripts/check_discovery.py -
```

With `-`, pass the JSON on stdin using the host tool. The script is read-only. Exit 0 means structurally valid; it can still return `OPPORTUNITY_MAP` or `ROUTE_COMPARISON` with no recommendation or handoff. `patent_validation` lists only routes permitted by this workflow to **start** patent validation. Exit 1 means the specified rule was not satisfied. This check cannot verify cited text, real novelty or semantic equivalence. Review those against original evidence; a convenient synonym can evade mechanical duplicate detection.

## Record fields and order

For a new record, add `mode_selection` with `explicit` (mode or null), `concrete_problem` and `executable_idea` (booleans), and `basis`. Older discovery-only records still work. A new assessment needs these fields and the additional problem evidence below.

Top level: `scope` is the actual user-approved or provisional scope; `mode` is `OPEN_ENDED`, `PROBLEM_DRIVEN` or `IDEA_VALIDATION`; `events` is the ordered array below. A user-approved scope change should be made explicit in a return and described in the new map, preserving the prior map.

| Event | Fields and meaning |
|---|---|
| `MAP` | `kind`, `decision` (`COMPARED` or `INCOMPLETE`), `basis` (scope, existing routes, trade-offs, evidence limits), and `opportunities` (list). Each opportunity has `id`, `capability_gap`, `value_basis`, `sources`, and `problems`. A problem has `id`, `problem`, `condition`, `bottleneck`, `cause`, `observation`, `assumption_boundary`, and `sources`. If a broad map contains fewer than two different opportunities, give `limited_opportunity_reason` with the comparison or missing evidence. For the new record add `status` (OBSERVED or CONJECTURE), `evidence_basis`, `competing_explanations` (text list), `discriminator` and `existing_limit`. No grounded problem: mark the map incomplete. |
| `ROUTES` | After a current compared map, supply `comparison_basis` and `routes` (list of `id`, `problem_id`, `mechanism`, `hypothesis`, `decision`, `decision_basis`; optional `implementation`). Decisions: `KEEP`, `REVISE`, `EXPLORE`, `DEFER`, `REJECT`. Explain `limited_route_reason` if fewer than three routes are supportable when exploring broadly, and `extended_route_reason` if more than five need comparison. Compare problem, mechanism and prediction, then shortlist no more than three. Material revisions get a new route ID with `supersedes` and `substantive_change`; an L4-only revision must also specify the changed `implementation`. For an unaffected retained route from the comparison reopened most recently, use optional `carry` (list of `route_id`, current `problem_id`, `decision`, `decision_basis`). Explain why it still applies. |
| `RETURN` | `trigger` from below, numeric `to_level` (1–4), `reason`, `next_exploration`, `sources`, and `affected_routes` (current IDs, empty only before any route comparison). For `PRIOR_ART`, `TEST_REFUTED`, or `NEW_EVIDENCE`, add numeric `affected_level`. Revisit the affected level or a higher one. L1/L2 require another map; L3/L4 require another route comparison. All previous handoffs become stale. |
| `VALIDATE` | For one current `KEEP` route, give `route_id`, `implementation`, `covered_boundary`, `remaining_difference`, `combination_risk`, `minimum_test`, `falsifier`, `sources`. This is a handoff to the existing prior-art and protection workflow. Record any gaps as gaps; do not use a placeholder to pass the handoff. |
| `ASSESS` | For a current route, append the [candidate assessment](candidate-validation.md). Require a live handoff for grade A; a compared route may receive a preliminary B, C or D. New evidence can update a live route; old evidence and reviews remain in the chronology. A retired D route needs a recorded return and substantive reconsideration. Each return invalidates the previous admissions. |

`sources` is a list of non-empty source locators. `SCOPE_TOO_NARROW` goes to L1 and rechecks L2; `PROBLEM_UNCLEAR` goes to L2 or above. `ROUTES_TOO_SIMILAR`, `NO_SUBSTANTIVE_DIFFERENCE`, `SIMPLE_BASELINE` and `MECHANISM_TOO_COMPLEX` go to L3 or above. For new evidence, mark the highest layer it actually defeats: changing an implementation is insufficient when the mechanism is already disclosed.

Example of a return itself, after a map and comparison:

```json
{
  "kind": "RETURN",
  "trigger": "SCOPE_TOO_NARROW",
  "to_level": 1,
  "reason": "The user rejected treating a single rendering optimization as the whole opportunity.",
  "affected_routes": ["R1"],
  "sources": ["User feedback: direction was too narrow"],
  "next_exploration": "Compare sensing, decision and model update opportunities; identify their different technical problems."
}
```

When closing any round, show the user what changed, the evidence, the remaining work, any routes not recommended, and the smallest next action. Compare separately: research value, technical difference, protection potential, and whether effectiveness can be demonstrated.
