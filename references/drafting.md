# Drafting technical disclosures and claim strategies

Use this reference for invention selection, application splitting, technical disclosure documents, claims, embodiments, algorithms, interfaces, or numerical parameters.

## Select the inventive spine

Write the invention in one sentence:

> Under [technical condition], apply [necessary structure or operation] to [technical object] via [mechanism], producing [direct technical effect].

If this sentence contains several “and independently also” branches, test whether separate applications are warranted. Each split direction must have its own complete input–mechanism–output–effect chain and its own closest-prior-art comparison.

## Problem and innovation matrix

Retain the template's problem labels exactly when the user requests it. Populate each row as:

- problem: a concrete technical deficiency in the closest prior art;
- innovation: the distinguishing technical means that resolves that deficiency;
- effect: the result directly caused by that means;
- evidence status: measured, calculated, proposed, configured, acceptance criterion, or unknown.

The main problem and main innovation must cover the independent-claim spine. Secondary rows should normally become dependent claims, optional embodiments, or fallback positions.

## Claims architecture

For a data-driven or control method, the independent claim should specify the applicable parts of this chain:

1. obtaining defined industrial data;
2. establishing the material, object, spatial, temporal, or process association needed by later steps;
3. generating a state, candidate set, prediction, or control quantity;
4. applying the distinguishing rule, constraint, calibration, optimization, or control mechanism;
5. producing and executing a disposition or control action;
6. recording or feeding back the result when it is part of the technical loop.

Use functional wording only when the description supports multiple implementations. Avoid claiming merely “using AI to improve quality”. Explain what is predicted, for which candidate action, under which constraint, how uncertainty changes execution, and what downstream system receives the result.

Dependent claims can progressively limit:

- material identity and process-position mapping;
- feature construction and missing/conflicting-data handling;
- rule data structures, priorities, versions, and conflict resolution;
- model family, action-specific heads, calibration, uncertainty, or out-of-distribution detection;
- risk objective, thresholds, execution levels, interface fields, idempotency, and fail-safe behavior;
- feedback samples, drift detection, and model/rule separation.

For a device, define the necessary components and their relationships. For a material, define the relevant constituents, ranges or structure. For a process, identify the operations and conditions that produce the stated outcome. Choose the subject matter from the disclosure.

For each proposed independent feature, map `feature → why necessary → disclosure paragraph → implementation step, structure or condition`. Add a figure and reference numeral when a corresponding drawing exists. Resolve missing support before using the feature in final claims. Draft corresponding system, electronic-device and storage-medium claims where the disclosure supports each form. Place optional implementations in supported dependent claims or embodiments.

## Parameters and evidence

When actual production evidence is unavailable, choose concrete implementable values only if the user asks for a completed embodiment. Label them as exemplary configuration or acceptance criteria, not as achieved results. Explain the role and failure behavior of the parameter.

Never write an unverified target as a historical outcome. For example:

- acceptable: “系统验收标准为自动处置率不低于75%”；
- unacceptable without evidence: “现场应用后自动处置率达到75%”。

For reported results, require the dataset or production period, denominator, exclusions, comparator, version, and test protocol. Keep locked-test results separate from training, calibration, exploratory, or historical evidence.

## Embodiment sufficiency

Give at least one implementable path from inputs, components or materials to the technical result. For a data-driven or control embodiment, choose the applicable items:

- inputs and sources;
- record keys, spatial or temporal mapping, and data-quality gates;
- candidate actions or control outputs;
- model inputs, labels, outputs, training/calibration split, and inference path;
- hard rules, risk or safety constraints, thresholds, and fallback behavior;
- downstream interface, execution acknowledgement, idempotency, and fault handling;
- audit fields and feedback update path;
- acceptance metrics without misrepresenting them as measured results.

For mechanical, electronic or material inventions, use applicable details such as component geometry and connections, tolerances, operating limits, composition, process order, processing windows and measurement conditions. Add software or feedback details where they are part of the design.

If a formula is used, define every symbol, unit or normalization, feasible set, threshold, and no-feasible-solution behavior.

## Walk through the mechanism

For an ordered rule, record its inputs, the conditions in evaluation order, whether a match terminates processing, tie or failure behavior and the output. Step through a normal case and a conflicting, boundary or failure case that could change the result. For a mechanical or material invention, use a relevant physical or process limit. Compare the result against the embodiment, claim outline, figures and stated effect. If interpretations produce different outputs, record each and keep the affected design open pending confirmation. In a read-only audit, cite the conflicting passages and show the expected result under the stated rule.

Distinguish an effect guaranteed by the structure within stated preconditions, a calculated example, a predicted effect and a measured outcome. For a worked example without observations, use traceable inputs, label them as synthetic and show how the output follows.

## Software and algorithmic features

Identify which feature changes a technical operation, such as validation before a database write, a state transition with a defined trigger, resource allocation with a defined input and output, or a device command. Explain which observable checks support the asserted effect. Flag contributions that rest on evaluation, ranking or management rules without a supported technical link. Assess eligibility and scope risks from the actual disclosure and verified official sources. Include hardware or a device control loop only when supported or explicitly confirmed as a proposed design.

For evidence processing, distinguish a valid locator, a relevant text match and an evidentiary link to the assertion. Review a counterexample where the same terms occur but the cited text gives a different or opposing result. Describe a scoring heuristic using its actual definition and assumptions.

## Final audit

Reject or revise language that:

- makes the technical effect broader than the mechanism;
- hides a required feature only in a figure;
- introduces an algorithm or threshold in a claim without descriptive support;
- confuses a customer, contract, or approval rule with a technical mechanism;
- relies on “智能、精准、显著、实时” without a defined operation or metric;
- uses inconsistent names for the same material, event, model output, or action.
