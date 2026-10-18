# Requirements — formal model

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).
>
> Brought in line with the decision records at the WP4b docs sweep (2026-10-18); each changed requirement says
> "(updated: <record>)". The consistent summary is [current-state.md](../current-state.md).

The formal model is an abstract architecture: observe → classify → compare → correct. It names no kind, type,
signal, sensor or actuator. It becomes realizable only when a taxonomy, a policy, sensors and actuators fill its
slots. The engine does name the three kind attributes (type, lifecycle, tier) that every applies-if rule reads
*(updated: WP0 A1; WP1 R-7)*.

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| FM-1 | Plant and controller are separate. The controller affects the plant only through declared actuators. | M | Architecture doc review |
| FM-2 | The model names no kind, type, signal, sensor or actuator. Those are slots. It names only the three kind attributes, type, lifecycle and tier *(updated: WP0 A1; WP1 R-7)*. | M | Toy-taxonomy swap needs zero code change |
| FM-3 | Every check's result can be "can't tell" (yellow). Anything unmeasurable is yellow, never green *(updated: WP0 R-13)*. | M | Test with a credential lacking admin |
| FM-4 | Classification is total and pure: every repo gets exactly one inferred kind, or `unclassified` (no kind fits) with a reason. There is no `unknown` kind *(updated: WP0 OD3; WP1 R-5)*. | M | Property test over generated observations |
| FM-5 | Each check on a repo has a status: green (known compliant), yellow (can't tell) or red (known non-compliant); an accepted exception (PO-8) is green, marked; a policy that doesn't apply is not in effect *(updated: WP0 R-13, A1)*. The taxonomy, the policies, a repo's kind and the exclude list all change only in the policy plane (governors), by PR *(updated: WP0 OD3; WP4b OD3)*. | M | Unit tests; plane-permission check |
| FM-6 | Each gap routes to a change request (an issue in the repo concerned) or, for an attested check, a request for the attestation. `unclassified` → policy plane. Automatic fixes are future work *(updated: WP0 Tension 3, non-goals)*. | M | Routing table tests |
| FM-7 | Steady-state error is tracked with its age and reported. Convergence isn't assumed. | M | The status log and the wiki views show error age *(updated: WP0 D-3, D-7)* |
| FM-8 | Every kind and verdict carries a trace: rule, values, evidence *(updated: WP0 terminology)*. | M | Sample traces are readable without the code |
| FM-9 | The two planes have separate interfaces. Neither can write the other's inputs. | M | Permission review |
| FM-10 | Realization binds sensors to `gh` reads, actuators to `gh` writes and issues plus `git push` to the wiki, and compute to GitHub Actions. Changing a binding is a policy-plane change. | M | Bindings live only in this repo |
| FM-11 | Sensors and actuators can also bind to stored snapshots: a stored snapshot of the pilot repos in, a recorded action log out. Nothing touches GitHub. Toy fixtures survive only for the toy-taxonomy swap (WP0 R-6) *(updated: WP0 D-5; `tests/fixtures/`)*. | M | The same run works on stored and live bindings |
