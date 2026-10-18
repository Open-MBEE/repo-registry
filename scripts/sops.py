#!/usr/bin/env python3
"""Render each policy's SOP from its data: a view, rendered, never committed (WP5b OD4, answer 6).

Every part of an SOP comes from the policy's YAML (data/policies/<id>.yaml): its name, meaning, what it applies to
(the applicability view), its set-up steps, its automated and attested checks, the attestation entries to copy
(docs/attestations-format.md) and its citations. Nothing in an SOP is written by hand any more.

Links to model files and documents point to the repository on GitHub, so the rendered SOPs read the same in demo
mode (build/demo/sops/) and, later, on the wiki (WP7). Links between views are relative.

Usage: python3 scripts/sops.py [--out build/demo]   (reads build/demo/reports/policy-applicability.yaml)
"""
import argparse
import pathlib
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import model  # noqa: E402
import policies as P  # noqa: E402

REPO = "https://github.com/Open-MBEE/repo-registry/blob/main"
GOVERNANCE_NOTE = {  # how a governance kind reads in prose: who holds it (WP4c); data about the kinds, kept here
    "governance/sandbox": "repo-registry today",
    "governance/incubating": "nothing yet",
    "governance/graduated": "the administration of the Open-MBEE GitHub organization, and repo-registry once it is "
                            "accepted as the canonical source",
}


def kind_phrase(name):
    t, s = name.split("/")
    note = GOVERNANCE_NOTE.get(name)
    return f"{t} at {s}" + (f" ({note})" if note else "")


def attest_block(p, org_policy):
    att = p["checks"].get("attested") or []
    entries = "\n".join(
        f"  - policy: {p['id']}\n    check: {c['id']}\n    attested_by: your-github-username\n    date: YYYY-MM-DD\n"
        "    release: vX.Y.Z           # the release this is made for, or none if there is no release yet" for c in att)
    where = ("the `ATTESTATIONS.yaml` of this repository, `repo-registry`, where the org is governed (the org has no "
             "repository of its own)") if org_policy else "your repository's `ATTESTATIONS.yaml`, at its root"
    who = "a code owner of `repo-registry`" if org_policy else "a code owner of the repository"
    it = "this entry" if len(att) == 1 else "these entries"
    return [f"How to attest: add {it} to {where}, and renew {'it' if len(att) == 1 else 'them'} for each release",
            f"([attestations-format.md]({REPO}/docs/attestations-format.md)). An entry counts only if its `release` "
            "names the release being checked (or `none` before the first release), and the last change to the file "
            f"was committed by {who}. Point to the file from the README: \"Attestations: see `ATTESTATIONS.yaml`.\"",
            "", "```yaml", "attestations:", entries, "```"]


def render(p, in_effect_for):
    pid = p["id"]
    org_policy = in_effect_for == ["governance/graduated"]
    L = [f"# {p['name']}", "",
         f"> **PROVISIONAL** until the maintainers approve the policies. A view, rendered from policy `{pid}` "
         f"([`data/policies/{pid}.yaml`]({REPO}/data/policies/{pid}.yaml)); never edit it by hand.", "",
         " ".join(p["meaning"].split()), "",
         f"**Applies to:** {', '.join(kind_phrase(k) for k in in_effect_for) or 'no kind'}. Your repository's type and "
         f"stage are in [registry.yaml]({REPO}/registry.yaml); the stages are explained in "
         f"[lifecycle-stage-map.md]({REPO}/docs/lifecycle-stage-map.md), and the full table is in "
         "[policy-applicability.md](../policy-applicability.md)."
         + (f" {' '.join(p['applies_note'].split())}" if p.get("applies_note") else ""), ""]
    guidance = p.get("license_guidance")
    if guidance:
        L += ["| Your repository's type | Use | Also accepted |", "|---|---|---|"]
        L += [f"| {t} | {g['use']} | {g['also']} |" for t, g in guidance.items()]
        L.append("")
    L += ["## Set up", ""] + [f"{i}. {step}" for i, step in enumerate(p["setup"], 1)] + [""]
    auto = p["checks"].get("automated") or []
    L += ["## Automated checks", ""]
    if auto:
        L += ["The registry checks these itself. A check it can't read shows as yellow (can't tell), never as off.", ""]
        L += [f"- **{c['id']}**: `{c['reads']}` (needs {c['permission']})" for c in auto]
    else:
        L.append("None. This policy is checked by attestation only.")
    att = p["checks"].get("attested") or []
    L += ["", "## Attested checks", ""]
    if att:
        L += [f"- **{c['id']}**: {' '.join(c['statement'].split())}" for c in att] + [""] + attest_block(p, org_policy)
    else:
        L.append("None.")
    cites = p["cites"]
    fmt = lambda v: v if v == "none" else ", ".join(v)  # noqa: E731
    L += ["", "## Why", "",
          f"- CISA: {fmt(cites['cisa'])} (see `data/sources/cisa-practices.yaml`)",
          f"- NIST SP 800-53: {fmt(cites['nist'])} (see `data/sources/nist-800-53.yaml`)"]
    if cites.get("openssf"):
        L.append(f"- OpenSSF security baseline: {', '.join(cites['openssf'])} "
                 "(see `data/sources/openssf-security-baseline.yaml`)")
    for clause in cites.get("iso12207") or []:
        L.append(f"- ISO/IEC/IEEE 12207:2026 clause {clause} (cited by reference)")
    if p.get("secondary_notes"):
        L.append(f"- {' '.join(p['secondary_notes'].split())}")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="build/demo")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    root, out = pathlib.Path(args.root), pathlib.Path(args.out)
    pols, _ = P.load_policies(root / "data/policies")
    by_policy = yaml.safe_load((out / "reports/policy-applicability.yaml").read_text())["policies"]
    (out / "sops").mkdir(parents=True, exist_ok=True)
    for pid, p in pols.items():
        (out / "sops" / f"{pid}.md").write_text(render(p, by_policy.get(pid, [])))
    print(f"wrote {len(pols)} SOPs to {out / 'sops'}")


if __name__ == "__main__":
    main()
