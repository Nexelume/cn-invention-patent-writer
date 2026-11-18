#!/usr/bin/env python3
"""Check the order and traceability of a patent exploration record, not its merits."""
import argparse
import json
import sys
from pathlib import Path

from patent_validation import check_problem, grade_assessment, select_mode


MODES = {"OPEN_ENDED", "PROBLEM_DRIVEN", "IDEA_VALIDATION"}
ROLLBACK_MAX = {
    "SCOPE_TOO_NARROW": 1, "PROBLEM_UNCLEAR": 2,
    "ROUTES_TOO_SIMILAR": 3, "NO_SUBSTANTIVE_DIFFERENCE": 3,
    "SIMPLE_BASELINE": 3, "MECHANISM_TOO_COMPLEX": 3,
    "PRIOR_ART": 4, "TEST_REFUTED": 4, "NEW_EVIDENCE": 4,
}
OUTCOMES = {"KEEP", "REVISE", "EXPLORE", "DEFER", "REJECT"}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def text(row, key):
    value = row.get(key)
    check(isinstance(value, str) and bool(value.strip()), f"{key}: text required")
    return value.strip()


def rows(row, key):
    value = row.get(key)
    check(isinstance(value, list) and all(isinstance(x, dict) for x in value),
          f"{key}: list of objects required")
    return value


def references(row, key):
    value = row.get(key)
    check(isinstance(value, list) and bool(value)
          and all(isinstance(x, str) and x.strip() for x in value),
          f"{key}: at least one reference required")
    return value


def normal(value):
    return "".join(c for c in value.casefold() if c.isalnum())


def handoff_text(value, key):
    missing = {"unknown", "tbd", "todo", "none", "na", "notchecked",
               "待核", "待核实", "待确认", "待补充", "未知", "暂无", "未核验", "不确定"}
    value = normal(value)
    check(bool(value) and value not in missing, f"{key}: unresolved handoff field")


def validate(record):
    check(isinstance(record, dict), "Record must be a JSON object")
    mode = text(record, "mode")
    check(mode in MODES, "Unknown discovery mode")
    new_record = "mode_selection" in record
    if new_record:
        check(isinstance(record["mode_selection"], dict)
              and mode == select_mode(record["mode_selection"]), "Mode contradicts input precedence")
    text(record, "scope")
    events = rows(record, "events")
    check(bool(events), "Record must contain an opportunity map")
    active_problems, routes, shortlist = {}, {}, set()
    fingerprints = set()
    full_map = False
    comparable = False
    needs_map = True
    needs_routes = False
    broaden = mode == "OPEN_ENDED"
    patent_ready = set()
    assessments = {}
    all_routes, reusable = {}, {}
    last_return, invalidated = None, set()
    for number, event in enumerate(events, 1):
        kind = text(event, "kind")
        try:
            if kind == "MAP":
                check(needs_map, "Replacing a map requires a recorded L1/L2 return")
                full_map = text(event, "decision") == "COMPARED"
                check(full_map or event["decision"] == "INCOMPLETE", "Unknown map decision")
                text(event, "basis")
                opportunities = rows(event, "opportunities")
                opp_ids = set()
                active_problems = {}
                opportunity_signatures = set()
                for opportunity in opportunities:
                    oid = text(opportunity, "id")
                    check(oid not in opp_ids, f"Duplicate opportunity {oid}")
                    opp_ids.add(oid)
                    gap = normal(text(opportunity, "capability_gap"))
                    check(gap and gap not in opportunity_signatures, "Repeated capability gap")
                    opportunity_signatures.add(gap)
                    text(opportunity, "value_basis")
                    references(opportunity, "sources")
                    for problem in rows(opportunity, "problems"):
                        pid = text(problem, "id")
                        check(pid not in active_problems, f"Duplicate problem {pid}")
                        for key in ("problem", "condition", "bottleneck", "cause",
                                    "observation", "assumption_boundary"):
                            text(problem, key)
                        references(problem, "sources")
                        if new_record:
                            check_problem(problem)
                        active_problems[pid] = problem
                if full_map:
                    check(bool(active_problems), "Compared map must contain a grounded problem or testable conjecture")
                    if broaden and len(opp_ids) < 2:
                        text(event, "limited_opportunity_reason")
                needs_map = not full_map
                needs_routes = full_map
                comparable = False
                patent_ready.clear()

            elif kind == "ROUTES":
                check(full_map and not needs_map and needs_routes, "Compare a current L1/L2 map before drawing up routes; record a return before re-comparison")
                candidates = rows(event, "routes")
                carry = rows(event, "carry") if "carry" in event else []
                original_ids = set(all_routes)
                total = len(candidates) + len(carry)
                text(event, "comparison_basis")
                if broaden and total < 3:
                    text(event, "limited_route_reason")
                if total > 5:
                    text(event, "extended_route_reason")
                routes = {}
                shortlist = set()
                for item in carry:
                    rid = text(item, "route_id")
                    check(rid in reusable and rid not in routes, f"Route cannot be carried: {rid}")
                    route = reusable[rid]
                    pid = text(item, "problem_id")
                    check(pid in active_problems and normal(active_problems[pid]["problem"])
                          == route["problem_signature"], f"Retained route no longer matches the problem: {rid}")
                    outcome = text(item, "decision")
                    check(outcome in OUTCOMES, f"Unknown decision: {outcome}")
                    reason = text(item, "decision_basis")
                    routes[rid] = dict(route, problem_id=pid, decision=outcome, decision_basis=reason)
                    all_routes[rid] = routes[rid]
                    if outcome == "KEEP":
                        shortlist.add(rid)
                for route in candidates:
                    rid = text(route, "id")
                    check(rid not in all_routes, f"Route ID already used: {rid}")
                    pid = text(route, "problem_id")
                    check(pid in active_problems, f"Unknown or stale problem: {pid}")
                    mechanism = text(route, "mechanism")
                    hypothesis = text(route, "hypothesis")
                    text(route, "decision_basis")
                    outcome = text(route, "decision")
                    check(outcome in OUTCOMES, f"Unknown decision: {outcome}")
                    fingerprint = (normal(active_problems[pid]["problem"]), normal(mechanism))
                    check(all(fingerprint) and normal(hypothesis), "Empty technical identity")
                    previous = route.get("supersedes")
                    old = None
                    if previous is not None:
                        check(isinstance(previous, str) and previous in original_ids and previous not in routes,
                              "supersedes must cite a route from an earlier comparison")
                        old = all_routes[previous]
                        text(route, "substantive_change")
                    if fingerprint in fingerprints:
                        check(last_return == 4 and old is not None and previous in invalidated
                              and old["decision"] != "REJECT"
                              and (old["problem_signature"], normal(old["mechanism"])) == fingerprint
                              and isinstance(route.get("implementation"), str)
                              and bool(normal(route["implementation"]))
                              and normal(route["implementation"]) != normal(old.get("implementation", "")),
                              f"Repeated problem and mechanism: {rid}; reference the old route, don't rename it")
                    if "implementation" in route:
                        text(route, "implementation")
                    fingerprints.add(fingerprint)
                    routes[rid] = dict(route, problem_signature=fingerprint[0])
                    all_routes[rid] = routes[rid]
                    if outcome == "KEEP":
                        shortlist.add(rid)
                check(len(shortlist) <= 3, "Recommend at most 3 routes; keep the full comparison")
                if broaden and len({normal(r['mechanism']) for r in routes.values()}) < min(3, len(routes)):
                    text(event, "limited_route_reason")
                comparable = True
                needs_routes = False
                reusable = {}
                last_return, invalidated = None, set()

            elif kind == "RETURN":
                check(full_map, "No assessed map to reopen")
                why = text(event, "trigger")
                target = event.get("to_level")
                check(type(target) is int and why in ROLLBACK_MAX
                      and 1 <= target <= ROLLBACK_MAX[why], "Return targets the wrong level")
                if why in {"PRIOR_ART", "TEST_REFUTED", "NEW_EVIDENCE"}:
                    affected_level = event.get("affected_level")
                    check(type(affected_level) is int and target <= affected_level <= 4,
                          "Return must revisit at least as high as the level invalidated by evidence")
                text(event, "reason")
                text(event, "next_exploration")
                references(event, "sources")
                affected = event.get("affected_routes", [])
                check(isinstance(affected, list) and all(isinstance(x, str) and x in routes for x in affected),
                      "Return references unknown or stale routes")
                if routes:
                    check(bool(affected), "Identify which current routes the return affects")
                patent_ready.clear()
                for rid, grade in assessments.items():
                    if grade == "D" and rid in routes:
                        routes[rid]["decision"] = "REJECT"
                        all_routes[rid]["decision"] = "REJECT"
                assessments.clear()
                last_return, invalidated = target, set(affected)
                reusable = {rid: route for rid, route in routes.items()
                            if rid not in invalidated and route["decision"] != "REJECT"}
                if target <= 2:
                    needs_map, full_map = True, False
                    active_problems = {}
                    broaden = broaden or target == 1
                else:
                    needs_routes = True
                comparable = False
                routes, shortlist = {}, set()

            elif kind == "VALIDATE":
                check(comparable and not needs_map and not needs_routes, "No current comparison to hand off")
                rid = text(event, "route_id")
                check(rid in shortlist, f"Route {rid} is not currently recommended")
                check(rid not in patent_ready, f"Duplicate handoff: {rid}")
                for key in ("implementation", "covered_boundary", "remaining_difference",
                            "combination_risk", "minimum_test", "falsifier"):
                    handoff_text(text(event, key), key)
                for source in references(event, "sources"):
                    handoff_text(source, "sources")
                patent_ready.add(rid)

            elif kind == "ASSESS":
                check(new_record, "An assessment requires recorded mode selection and problem evidence")
                rid = text(event, "route_id")
                check(comparable and rid in routes, f"No current route to assess: {rid}")
                check(assessments.get(rid) != "D", f"Retired mechanism needs a recorded return: {rid}")
                grade = grade_assessment(event)
                check(grade != "A" or rid in patent_ready, f"Grade A needs a current handoff for {rid}")
                check(text(event, "grade") == grade, f"Evidence supports grade {grade}")
                assessments[rid] = grade

            else:
                raise ValueError(f"Unknown event kind {kind}")
        except ValueError as exc:
            raise ValueError(f"Event {number} ({kind}): {exc}") from exc
    next_stage = ("OPPORTUNITY_MAP" if needs_map else
                  "ROUTE_COMPARISON" if needs_routes else "DISCOVERY_COMPLETE")
    blocked = {rid for rid, grade in assessments.items() if grade in {"C", "D"}}
    result = {"next_stage": next_stage, "recommended": sorted(shortlist - blocked),
              "patent_validation": sorted(patent_ready - blocked)}
    if new_record:
        result["candidate_grades"] = assessments
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", help="UTF-8 JSON file or - for stdin")
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if args.record == "-" else Path(args.record).read_text(encoding="utf-8-sig")
        result = validate(json.loads(raw))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Invalid exploration record: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
