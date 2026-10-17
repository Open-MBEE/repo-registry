# Requirements — formal model

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).

The formal model is an abstract architecture: observe → classify → compare → correct. It names no class,
attribute, sensor or actuator. It becomes realizable only when a taxonomy, a policy, sensors and actuators fill its
slots.

| ID | Requirement | Src | Assessed by |
|---|---|---|---|
| FM-1 | Plant and controller are separate. The controller affects the plant only through declared actuators. | M | Architecture doc review |
| FM-2 | The model names no class, attribute, sensor or actuator. Those are slots. | M | Toy-taxonomy swap needs zero code change |
| FM-3 | Every attribute's domain includes `unknown`. Anything unmeasurable is `unknown`, never `ok`. | M | Test with a credential lacking admin |
| FM-4 | Classification is total and pure: exactly one class, or `unknown` (incomplete info), or `unclassified` (no class fits). | M | Property test over generated observations |
| FM-5 | Error is computed per attribute as `ok` / `violation` / `unknown` / `don't-care` / `deviation` (accepted exception, PO-8). A class's assigned values, a repo's class assignment and the exclude list all change only in the policy plane (governors). | M | Unit tests; plane-permission check |
| FM-6 | Each error routes to the channel the policy names: automatic, change request, or attestation. `unknown` → attestation. `unclassified` → policy plane. | M | Routing table tests |
| FM-7 | Steady-state error is tracked with its age and reported. Convergence isn't assumed. | M | Repo wiki pages show error age |
| FM-8 | Every class and verdict carries a trace: rule, values, evidence. | M | Sample traces are readable without the code |
| FM-9 | The two planes have separate interfaces. Neither can write the other's inputs. | M | Permission review |
| FM-10 | Realization binds sensors to `gh` reads, actuators to `gh` writes and issues plus `git push` to the wiki, and compute to GitHub Actions. Changing a binding is a policy-plane change. | M | Bindings live only in this repo |
| FM-11 | Sensors and actuators can also bind to a **hypothetical plant**: a fixture org snapshot in, a recorded action log out. Nothing touches GitHub. | M | The same run works on fixture and live bindings |
