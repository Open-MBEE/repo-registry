# WP5f — Decision brief: the first owners and maintainers *(the shape, with a hypothetical example)*

> **HYPOTHETICAL.** This document shows the *shape* of the brief the co-founders will use to choose OpenMBEE's first
> owners and maintainers. Every person in it ("Person A" to "Person F", "Organization X" to "Z") is invented. **It is
> not the proposed decision**, and it recommends, ranks and proposes no one ([WP5f-decisions.md](WP5f-decisions.md),
> "OD5" and "The decision brief's form"). The only real facts in it are the counts under "Today".

## Who decides, and how it is recorded

The co-founders decide, likely from a loose consensus of the most active contributors and the informally defined
leadership group. The supervisor records their decision in [`data/maintainers.yaml`](../data/maintainers.yaml) by a
pull request, where the model checks it (see "Recording it", below). How and when the organization's roles change is
decided later, in its own package ([maintainer-policy.md](../docs/maintainer-policy.md), "How the first owners and
maintainers are chosen").

## What the policies ask

| Provision | What it asks | Where |
|---|---|---|
| Maintainers govern the organization | The maintainers are named in `data/maintainers.yaml`, and this repository's CODEOWNERS lists the same people | Maintainer policy 1; `maintainers-match` |
| A small set of owners | 2 or 3 owners, each a maintainer; the owners check the other maintainers' powers | Maintainer policy 2; `org-few-owners` |
| Enough maintainers, from more than one organization | Five to start, more as needed; from more than one organization, so governance survives any one person or employer leaving | Maintainer policy 3 |
| Governance held openly | Each maintainer makes their organization membership public; nobody is named against their choice | Maintainer policy 4; `governance-roles-named` |
| Verified, where it matters | A code owner of a high-tier repository (today `.github`, governance/graduated) is a maintainer an owner has verified out of band: identity, sanctions, affiliation; published facts with consent | `verified-code-owners` |
| Release authority | For each incubating or graduated tool, a named release authority, credentialed before it acts | Maintainer policy 12, 13 |

## Today *(real counts)*

- The organization has **18 owners**: 2 with public membership, 16 concealed (counted, never named; WP3).
- `data/maintainers.yaml` names **4 people**, as a placeholder.
- No maintainer has a verification recorded (XF-3).

## The facts to weigh *(hypothetical)*

The brief summarizes public activity in the organization's repositories over the last 12 months. It states facts and
draws no conclusion from them. It never shows anyone's membership or role in the organization: who holds the owner
role today is known to the co-founders from the organization's settings, and stays out of this public repository
(WP3 OD1).

| Person *(hypothetical)* | Organization | Public commits and reviews, last 12 months | Areas |
|---|---|---|---|
| Person A | Organization X | 140 | tools (incubating), governance |
| Person B | Organization X | 95 | tools (sandbox), media |
| Person C | Organization Y | 60 | tools (incubating) |
| Person D | Organization Z | 35 | media, website |
| Person E | Organization Y | 20 | research |
| Person F | Organization Z | 5 | governance |

## The choices to make

1. **The maintainers:** who governs (at least five, from more than one organization).
2. **The owners:** 2 or 3 of the maintainers.
3. **Owners who are not kept:** they become members (and maintainers, where chosen), keeping their access through
   teams. The brief lists how many, not who.
4. **Release authorities:** for each incubating or graduated tool, who holds it.
5. **Consent:** each person named agrees to be named publicly; a code owner of a high-tier repository also agrees to
   publish their legal name, country of residence and affiliation, for verification.

## A filled example *(hypothetical: the shape only, not a proposal)*

| Choice | Hypothetical answer |
|---|---|
| Maintainers | Person A, Person B, Person C, Person D, Person E (organizations X, Y and Z) |
| Owners | Person A, Person C |
| Owners not kept | a count only, from the organization's settings (in this example, 16 of 18 owners become members) |
| Release authorities | one per incubating or graduated tool, each a maintainer |
| Consent | each of the five agrees to be named; Persons A and C also publish their facts for verification |

## Recording it

The supervisor records the decision in `data/maintainers.yaml` by a pull request: the maintainers under `maintainers`,
keyed by GitHub user ID with their login and name; the owners under `owners`, each one of those maintainers. The model
checks it: `owners` is empty until the decision is recorded, and then holds 2 or 3 named maintainers
(`scripts/validate.py`). `data/proposed-codeowners` lists the same maintainers (`maintainers-match`).
