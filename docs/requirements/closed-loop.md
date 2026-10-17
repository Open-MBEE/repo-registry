# Requirements — closed-loop behavior

> **DRAFT.** Nothing here is locked until mzargham says "lock." Columns and sources are defined in
> [design.md](../design.md#requirement-conventions).

This is the intended behavior. It emerges from the design and from the people taking part, so it is measured, not
built. Its columns are ID · intended behavior · measure.

| ID | Intended behavior | Measure |
|---|---|---|
| CL-1 | Violations fall over time as operators act on change requests. (Automatic actuation is deferred to R5.) | Count per run |
| CL-2 | Unknowns fall as people answer attestations. | Count, and the age of open attestations |
| CL-3 | Residual error is visible and has a named owner. | Age by owner |
| CL-4 | Emergent items reach the policy plane. | Open taxonomy-review items |
| CL-5 | Load on humans stays low: one issue per repo × attribute, a cap per run, auto-close when cleared. | Issues opened per run |
| CL-6 | Sensitivity to initial conditions is contained: actuation starts off and is turned on per class, by a governor, after the initial class assignments are reviewed. | Actuation flag history |
| CL-7 | Compute stays small: scheduled sensing in batched calls (about 13 for 183 repos today). | Run time; API calls |
| CL-8 | People find their way by the wiki rather than by asking. | Cold-read navigation tasks; community-manager feedback |
