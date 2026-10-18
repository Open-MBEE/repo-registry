# Org governance review

> **PROVISIONAL.** WP3 D-1. How the Open-MBEE GitHub organization is governed: every way power over it is held,
> from GitHub's documentation, and what a read-only snapshot shows today. Privacy (WP3 OD1, R-8): only owners whose
> membership is public, and the people the supervisor named, are named. Everyone else is a count.

## What the snapshot shows (2026-10-18)

Taken by `scripts/org_snapshot.py` with the credential of `mzargham` (org role: member).
Stored in `data/snapshots/2026-10-18/org.json`.

| Item | Value |
|---|---|
| Org owners | 18: 2 with public membership (`ablack-jpl`, `aftimg`), 16 concealed (count only) |
| Public members of the org | 5 |
| Teams visible to the credential | 9 |
| Outside collaborators | unreadable with a member's credential (yellow) |
| Installed GitHub Apps | unreadable with a member's credential (yellow) |
| Holders of security manager, CI/CD admin, moderator, App Manager | unreadable with a member's credential (yellow) |
| Org security configurations | unreadable with a member's credential (yellow) |
| Org rulesets | unreadable with a member's credential (yellow) |
| `default_repository_permission` | unreadable with a member's credential (yellow) |
| `members_can_change_repo_visibility` | True |
| `members_can_create_private_repositories` | True |
| `members_can_create_public_repositories` | True |
| `members_can_create_repositories` | True |
| `members_can_create_teams` | True |
| `members_can_delete_repositories` | False |
| `members_can_fork_private_repositories` | False |
| `members_can_invite_outside_collaborators` | True |
| `two_factor_requirement_enabled` | unreadable with a member's credential (yellow) |
| `web_commit_signoff_required` | False |

**What this means.**

- **18 owners is far above OpenSSF's 2 to 3** (baseline TI-3). Every owner has complete administrative access to
  every repository and to the org itself. This is the main finding, and `org-few-owners` is red.
- **Only 2 owners are public,** so who governs OpenMBEE can't be seen from outside. `governance-roles-named` is red.
  The rule isn't ratified yet, and people may step down rather than be named.
- **Members can create public repositories, change repository visibility and invite outside collaborators.** These
  settings keep the org low-friction for research and media, which fits WP0's aims. They are recorded, not judged.
  Restricting outside-collaborator invites to owners is an Enterprise Cloud feature anyway.
- **Much of the governance picture needs an owner's credential:** the two-factor requirement, the base permission,
  outside collaborators, installed apps, holders of the narrower org roles, security configurations and org rulesets.
  These are yellow, never off. The supervisor can obtain the permissions, and the sensing credential is expected gap
  XF-1 (WP6).
- **Activity hints** (last public commit in the org; a hint, never a verdict): `ablack-jpl` 2017-09-25, `aftimg` 2026-10-03; listed maintainers `HuiJun` 2026-10-17, `aftimg` 2026-10-03, `mzargham` 2026-10-05, `rkarban` none found.

## How power over a GitHub organization is held (from GitHub's documentation)

Read 2026-10-18 from docs.github.com. Every URL is `https://docs.github.com` + the path in the key table. Anything the
documentation doesn't state is marked UNCONFIRMED.

Short URL keys used in tables:

| Key | Path |
|---|---|
| ROLES | /en/organizations/managing-peoples-access-to-your-organization-with-roles/roles-in-an-organization |
| PREDEF | /en/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-predefined-organization-roles |
| CUSTORG | /en/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-custom-organization-roles |
| SECMGR | /en/organizations/managing-peoples-access-to-your-organization-with-roles/managing-security-managers-in-your-organization |
| MOD | /en/organizations/managing-peoples-access-to-your-organization-with-roles/managing-moderators-in-your-organization |
| BILL | /en/organizations/managing-peoples-access-to-your-organization-with-roles/adding-a-billing-manager-to-your-organization |
| APPMGR | /en/organizations/managing-programmatic-access-to-your-organization/adding-and-removing-github-app-managers-in-your-organization |
| REPOROLES | /en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization |
| CUSTREPO | /en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/about-custom-repository-roles |
| BASE | /en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/setting-base-permissions-for-an-organization |
| TEAMMAINT | /en/organizations/organizing-members-into-teams/assigning-the-team-maintainer-role-to-a-team-member |
| OUTSIDE | /en/organizations/managing-user-access-to-your-organizations-repositories/managing-outside-collaborators/adding-outside-collaborators-to-repositories-in-your-organization |
| R-ORGS | /en/rest/orgs/orgs |
| R-ORGS-GHEC | /en/enterprise-cloud@latest/rest/orgs/orgs |
| R-MEMBERS | /en/rest/orgs/members |
| R-ORGROLES | /en/rest/orgs/organization-roles |
| R-SECMGR | /en/rest/orgs/security-managers |
| R-CUSTREPO | /en/rest/orgs/custom-roles |
| R-OUTSIDE | /en/rest/orgs/outside-collaborators |
| R-COLLAB | /en/rest/collaborators/collaborators |
| R-TEAMS | /en/rest/teams/teams |
| R-TEAMMEM | /en/rest/teams/members |
| R-REPOS | /en/rest/repos/repos |
| R-PAT | /en/rest/orgs/personal-access-tokens |
| R-ACTIONS | /en/rest/actions/permissions |
| R-RULES | /en/rest/orgs/rules |
| R-SECCONF | /en/rest/code-security/configurations |
| R-HOOKS | /en/rest/orgs/webhooks |
| R-BLOCK | /en/rest/orgs/blocking |
| R-INTER | /en/rest/interactions/orgs |
| FGPAT | /en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens |
| GQL-ORGS | /en/graphql/reference/orgs |
| GQL-USERS | /en/graphql/reference/users |
| PLANS | /en/get-started/learning-about-github/githubs-plans |

## How to read these with `gh api`

- REST: `gh api /orgs/ORG/...` (add `--paginate` for lists). GraphQL: `gh api graphql -f query='...'`.
- Two separate gates apply. (1) The **caller's role** in the org (owner, member, security manager, and so on). (2) The **token's grant**: a classic scope (`read:org`, `admin:org`, `repo`, `read:audit_log`, `admin:org_hook`), or a fine-grained PAT / GitHub App permission (for example Organization "Members: read", Organization "Administration: read", Repository "Administration: read"). The REST page for each endpoint states (1) and the classic scope. FGPAT maps each endpoint to a fine-grained permission.
- A REST response carries an `X-Accepted-GitHub-Permissions` header that says which fine-grained permission the endpoint needs (FGPAT).
- What a caller without permission gets: for most org endpoints the docs list only `404` (and sometimes `403`) as the error code. Docs page R-TEAMS says outright that a missing permission returns 404 on "Check team permissions for a repository". Elsewhere the docs list codes but do not say which one an unauthorized caller gets: **UNCONFIRMED** per endpoint unless stated below.

---

## A. Organization-level roles

The predefined org roles are Member, Moderator, Owner, Billing manager, Security manager, CI/CD admin, and App Manager. The predefined repository-access org roles are All-repository read, triage, write, maintain, and admin. All of these "are available by default in every organization" (PREDEF). An owner chooses owner or member at invitation; the other roles are assigned to existing people (PREDEF). A user or team can hold several org roles (/en/organizations/managing-peoples-access-to-your-organization-with-roles/using-organization-roles).

| Role | What it confers (docs) | Read endpoint and fields | Min. permission to read | Plan | Docs |
|---|---|---|---|---|---|
| **Owner** | "Complete administrative access" (ROLES). From the PREDEF table, owner-only: invite, remove and reinstate members; add/remove people in all teams; promote team maintainers; add collaborators to all repos; access the audit log; delete the org; transfer repos; install and manage Marketplace apps; manage the forking policy, default branch name, default labels and PR-review settings; convert members to outside collaborators; view people with access to a repo; push to all repos. Owners also have admin on every org repo (REPOROLES). | `GET /orgs/{org}/members?role=admin` returns users. Or `GET /orgs/{org}/memberships/{username}` returns `role` (`admin`, `member`, `billing_manager`) and `state`. GraphQL: `organization.membersWithRole` edges carry `role` (`ADMIN`/`MEMBER`). | Members list: Members read (FGPAT). memberships/{username}: "authenticated user must be an organization member" (R-MEMBERS); a non-member caller gets 403 or 404 (both listed; which one applies is **UNCONFIRMED**). | All plans | ROLES, PREDEF, R-MEMBERS, GQL-ORGS, GQL-USERS |
| **Member** | Default non-admin role. Can create repos and teams (unless restricted), see all members and teams, be made team maintainer, hide comments on writable items (PREDEF). | Same as above, `role=member` | Same | All | ROLES, PREDEF |
| **Moderator** | Member plus: block and unblock non-members, set org and repo interaction limits, hide comments in all public org repos. No other extra abilities. At most 10 people or teams (MOD). | `GET /orgs/{org}/organization-roles` lists roles (find the Moderator role id), then `GET /orgs/{org}/organization-roles/{role_id}/users` and `/teams`. | List of roles: org admin, or a custom role with "View organization roles"; classic `admin:org`; FGPAT "Custom organization roles: read". Assignee lists: "must be an administrator for the organization"; classic `admin:org`; FGPAT "Members: read" (R-ORGROLES, FGPAT). Errors listed: 404; 422 "if the organization roles feature is not enabled". | All (predefined) | MOD, R-ORGROLES |
| **Billing manager** | View metered usage, budgets and payment history; manage payment methods; upgrade or downgrade between Free and Team; invite or remove billing managers; manage sponsorships. Cannot access repos, see private members, or appear in the member list (BILL). Cannot be invited at org level if the org is owned by an enterprise (BILL). | `GET /orgs/{org}/memberships/{username}` returns `role: billing_manager`. A dedicated list endpoint for billing managers: **UNCONFIRMED** (none found; `members?role=` accepts only all, admin or member). | Org member (R-MEMBERS) | Free/Team (an enterprise-owned org cannot invite them) | BILL, R-MEMBERS |
| **Security manager** | Read on all repos; write on all security alerts; configure security features at org and repo level, including enabling or disabling GHAS (SECMGR). Also: Dependabot alerts for all repos, the security overview, and secret, code and Dependabot dismissal or bypass review (PREDEF). | `GET /orgs/{org}/organization-roles` then `/organization-roles/{id}/users` and `/teams`. The legacy `GET /orgs/{org}/security-managers` was "closing down ... starting January 1, 2026" (R-SECMGR). | As for Moderator | All (some features need GHAS) | SECMGR, R-SECMGR, R-ORGROLES |
| **CI/CD admin** | "Admin access to manage Actions policies, runners, runner groups, hosted compute network configurations, secrets, variables, and usage metrics" (PREDEF) | organization-roles endpoints as above | As above | **UNCONFIRMED** (PREDEF says "every organization") | PREDEF |
| **App Manager** | Create, edit and delete all org-owned GitHub App registrations (PREDEF). Cannot install or uninstall apps, and cannot list apps on Marketplace (APPMGR). Can also be granted per app. Owners can always manage apps and "are not shown" in the role-assignment view (APPMGR). | organization-roles endpoints for the org-wide role. Per-app managers: **UNCONFIRMED** (no read endpoint found). | As above | All | APPMGR, ROLES |
| **All-repository read/triage/write/maintain/admin** | That repo role on all repos in the org (PREDEF) | organization-roles endpoints; the role object has `base_role`, `source` (`Organization`, `Enterprise`, `Predefined`) and `permissions[]` | As above | **UNCONFIRMED** | PREDEF, R-ORGROLES |
| **Custom organization roles** | Granular org permissions: manage or view custom org and repo roles, org webhooks, OAuth app policy, custom properties, org rulesets, view the audit log, Actions policies/secrets/variables/runners, alert-dismissal and bypass reviews, Copilot metrics. Optionally a base repo role (read through admin) across **all** repos, plus extra repo permissions (that part is public preview). "Organization permissions do not grant read, write, or administrator access to any repositories" (CUSTORG). | Same organization-roles endpoints; `source: Organization` | As above | **Enterprise Cloud only** ("only available to organizations on GitHub Enterprise Cloud", ROLES) | CUSTORG, ROLES |

Notes:
- The roles endpoints return roles, not owners. Owners are read from `members?role=admin` or GraphQL `membersWithRole { edges { role } }`.
- In GraphQL, an `OrganizationMemberEdge` has `hasTwoFactorEnabled`, which "Returns null if information is not available to viewer" (GQL-USERS). `viewerCanAdminister` tells the caller whether it is an owner (GQL-ORGS).
- Enterprise owners: GraphQL `organization.enterpriseOwners` (GQL-ORGS). An enterprise team can give someone indirect membership: see `direct_membership` and `enterprise_teams_providing_indirect_membership` on the memberships endpoint (R-MEMBERS).

## B. Repository-level power across the org

| Item | What it confers | Read endpoint and fields | Min. permission to read | Plan | Docs |
|---|---|---|---|---|---|
| Repo roles (Read < Triage < Write < Maintain < Admin) | Read: pull, fork, open issues, review. Triage: labels, close or assign issues and PRs. Write: push, merge, approve required reviews, manage labels and milestones. Maintain: description, topics, PR-merge config, Pages source, push to protected branches (not under rulesets), interaction limits. Admin: everything in "What admin can do" below (REPOROLES). | `GET /repos/{o}/{r}/collaborators` returns users with `permissions{}` and `role_name` (highest role across repo, team, org and enterprise grants; there is "presently not a way to differentiate between an organization level grant and a repository level grant"). `affiliation=outside\|direct\|all`. `GET /repos/{o}/{r}/collaborators/{u}/permission` returns `permission` (legacy admin, write, read, none; maintain maps to write, triage to read) and `role_name` (includes custom roles). | Collaborators list: write, maintain or admin on the repo, and (for org repos) org membership; classic `read:org`+`repo`; FGPAT Repository "Metadata: read" (R-COLLAB, FGPAT). Check one collaborator: push access (R-COLLAB). | All | REPOROLES, R-COLLAB |
| Grants via teams | A team gets a repo role, and child teams inherit it | `GET /repos/{o}/{r}/teams` lists teams with `permission`. `GET /orgs/{org}/teams/{slug}/repos` lists a team's repos. `GET /orgs/{org}/teams/{slug}/repos/{o}/{r}` checks admin, push, maintain, triage or pull, including inheritance through parent teams. | repo/teams: only teams "visible to the authenticated user"; for public repos, only teams that added the repo explicitly; FGPAT Repository "Administration: read" (R-REPOS, FGPAT). Team-repo check: 404 if the team lacks access, **or** if the repo is private and the caller lacks read or the `repo`/`admin:org` scope (R-TEAMS). | Free includes "Team access controls" (PLANS) | R-REPOS, R-TEAMS |
| Teams and team maintainers | Maintainer: rename the team and change its visibility; add or remove members; assign maintainers; remove the team's repo access; request parent/child changes; code-review and reminder settings (TEAMMAINT) | `GET /orgs/{org}/teams`; `GET /orgs/{org}/teams/{slug}/members` (each member has `role` member or maintainer, and an `inherited` flag); `GET .../memberships/{u}` | Teams "visible to the authenticated user"; FGPAT Organization "Members: read" (R-TEAMS, R-TEAMMEM, FGPAT) | All | TEAMMAINT, R-TEAMMEM |
| Outside collaborators | Non-members with access to one or more repos; cannot join teams; 2FA required if the org requires it (OUTSIDE). Base permission does not apply to them (BASE). | `GET /orgs/{org}/outside_collaborators` (`filter=2fa_disabled\|2fa_insecure`). Per repo: `collaborators?affiliation=outside`. | FGPAT "Members: read". The caller role needed: **UNCONFIRMED** (not stated). | All | R-OUTSIDE, OUTSIDE |
| Base (default) permission | Minimum role for every member on every repo; a higher grant overrides it; internal repos are at least read (BASE) | `GET /orgs/{org}` returns `default_repository_permission` | Owner for "full details" (R-ORGS); which fields are owner-only is **UNCONFIRMED** | All | BASE, R-ORGS |
| Custom repository roles | Inherit Read, Triage, Write or Maintain, plus extra permissions (for example manage webhooks, deploy keys, bypass branch protections, edit repo rules, security alerts); up to 20; any repo admin can assign them (CUSTREPO) | `GET /orgs/{org}/custom-repository-roles`, `/{role_id}`; `GET /orgs/{org}/repository-fine-grained-permissions` | Org admin **or admin of any repo in the org**; classic `admin:org` or `repo` (R-CUSTREPO) | **Enterprise Cloud only** (CUSTREPO) | CUSTREPO, R-CUSTREPO |
| Deploy keys | Anyone holding the private key can read (or write) the repo "even if they're later removed from the organization" (REPOROLES warning) | `GET /repos/{o}/{r}/keys` | FGPAT Repository "Administration: read" (FGPAT) | All | REPOROLES, FGPAT |

**What admin on a repo can do** (REPOROLES table, Admin-only rows): manage individual, team and outside-collaborator access; manage branch protection and repo rulesets; merge on protected branches without approvals; delete issues; change visibility (unless the org restricts it); make it a template; change settings and the default branch; manage webhooks and deploy keys; set the repo forking policy; transfer repos in; delete, transfer out or archive (unless the org restricts it); edit custom property values; create security advisories; manage GHAS access; enable the dependency graph on private repos. Repo admins can also install GitHub Apps on their repos (see C), and they see the `security_and_analysis` block in `GET /repos/{o}/{r}` (R-REPOS).

## C. Apps, OAuth apps, and personal access tokens

| Item | How power is obtained | Read endpoint and fields | Min. permission | Plan | Docs |
|---|---|---|---|---|---|
| GitHub App installations | Owners install apps on the org. By default, repo admins can install an app that requests no org permissions and no "repository administration" permission, and can add their repos to an app already installed. Owners can restrict installation to owners only (/en/apps/using-github-apps/installing-a-github-app-from-a-third-party, /en/organizations/managing-programmatic-access-to-your-organization/limiting-oauth-app-and-github-app-access-requests). App managers cannot install (APPMGR). | `GET /orgs/{org}/installations` returns `installations[]` with `app_slug`, `app_id`, `repository_selection` (`all`/`selected`), `permissions{}`, `events[]`, `suspended_at`, `created_at` | "must be an organization owner"; classic scope given as "admin:read" (sic) (R-ORGS); FGPAT Organization "Administration: read" (FGPAT). Response for a non-owner: **UNCONFIRMED**. | All | R-ORGS, FGPAT |
| App's own view | An installation token sees only the repos granted to it | `GET /installation/repositories` | Installation token (/en/rest/apps/installations) | All | /en/rest/apps/installations |
| OAuth apps | When "OAuth app access restrictions" are on (the default for new orgs), members and outside collaborators cannot authorize OAuth apps on org resources without owner approval (/en/organizations/managing-oauth-access-to-your-organizations-data/about-oauth-app-access-restrictions) | REST endpoint for the OAuth app policy or the approved-app list: **UNCONFIRMED** (none found). A custom org role permission "Manage organization OAuth app policies" exists (CUSTORG). | n/a | All | as cited |
| Fine-grained PAT policy | Owners choose: allow or restrict PAT access (classic and fine-grained); a maximum lifetime (fine-grained default 366 days); approval required (the default) or not. Classic PATs are never subject to approval (/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization). | Policy values: **UNCONFIRMED** (no read endpoint found). Approved tokens: `GET /orgs/{org}/personal-access-tokens`, `/{pat_id}/repositories`. Pending requests: `GET /orgs/{org}/personal-access-token-requests`. | **"Only GitHub Apps can use this endpoint"**; PATs and OAuth tokens cannot (R-PAT, /en/organizations/managing-programmatic-access-to-your-organization/managing-requests-for-personal-access-tokens-in-your-organization) | All | R-PAT |
| SAML SSO credential authorizations | PATs, SSH keys, and OAuth or App user tokens authorized for a SAML org | `GET /orgs/{org}/credential-authorizations` | Owner; classic `read:org` (R-ORGS-GHEC) | **Enterprise Cloud** (SAML) | R-ORGS-GHEC |
| Org webhooks | Get org event payloads (may include repo metadata, CUSTORG) | `GET /orgs/{org}/hooks` | Owner; classic `admin:org_hook`. OAuth apps cannot see hooks they did not create (R-HOOKS). | All | R-HOOKS |

## D. Org settings that bear on security and governance

The fields named below are on `GET /orgs/{org}` (R-ORGS) unless stated. The docs say: "To see the full details about an organization, the authenticated user must be an organization owner"; classic tokens need `admin:org` "to see the full details". **UNCONFIRMED:** which fields are dropped for a non-owner. Assume every governance field may be missing or null.

| Setting | Effect | Read | Min. permission | Plan | Docs |
|---|---|---|---|---|---|
| 2FA requirement | Members and billing managers without 2FA lose access to org resources but keep membership; outside collaborators without 2FA are **removed**. A "secure methods only" variant also exists. | `two_factor_requirement_enabled`; GraphQL `requiresTwoFactorAuthentication`. Per user: `GET /orgs/{org}/members?filter=2fa_disabled\|2fa_insecure` ("only available for organization owners"); same filter on outside_collaborators; GraphQL edge `hasTwoFactorEnabled` (null when not visible). | Owner for full details or filters | All. PLANS lists "Two-factor authentication enforcement" in Free. | /en/organizations/keeping-your-organization-secure/managing-two-factor-authentication-for-your-organization/requiring-two-factor-authentication-in-your-organization, R-ORGS, R-MEMBERS |
| Base permission | See B | `default_repository_permission` | Owner (full details) | All | BASE |
| Repo creation | Whether members and Apps can create repos, and of which type; owners always can. "Private only" is an Enterprise Cloud option. | `members_can_create_repositories`, `members_allowed_repository_creation_type`, `members_can_create_public_/private_/internal_repositories`; `memberships/{u}` → `permissions.can_create_repository`; GraphQL `viewerCanCreateRepositories` | Owner (full details) | All; private-only on Enterprise Cloud | /en/organizations/managing-organization-settings/restricting-repository-creation-in-your-organization |
| Visibility change | Owners only, or any repo admin | `members_can_change_repo_visibility` | Owner (full details) | All | /en/organizations/managing-organization-settings/restricting-repository-visibility-changes-in-your-organization |
| Delete or transfer | Owners only, or members with repo admin | `members_can_delete_repositories` | Owner (full details) | All | /en/organizations/managing-organization-settings/setting-permissions-for-deleting-or-transferring-repositories |
| Private forking | Off by default for new orgs | `members_can_fork_private_repositories`; GraphQL `membersCanForkPrivateRepositories` | Owner (full details) | All | /en/organizations/managing-organization-settings/managing-the-forking-policy-for-your-organization |
| Invite outside collaborators | Default: any repo admin can invite. Restricting this to owners is Enterprise Cloud only. | `members_can_invite_outside_collaborators` | Owner (full details) | Restriction: Enterprise Cloud | /en/organizations/managing-organization-settings/setting-permissions-for-adding-outside-collaborators |
| Other member privileges | Delete issues, create teams, create Pages, view dependency insights, web commit sign-off | `members_can_delete_issues`, `members_can_create_teams`, `members_can_create_pages`, `members_can_view_dependency_insights`, `web_commit_signoff_required`, `deploy_keys_enabled_for_repositories` | Owner (full details) | All | R-ORGS |
| PAT policy | See C | No read endpoint found (**UNCONFIRMED**) | n/a | All | C |
| Org rulesets | Branch, tag and push rules across many repos; only owners can edit org rulesets; repo admins can add repo-level rulesets that aggregate with them | `GET /orgs/{org}/rulesets` (`targets=` filter), `/{id}`, `/{id}/history`; GraphQL `organization.rulesets`. `bypass_actors` "is only returned if the user ... has write access to the ruleset" (R-RULES). | Caller role not stated (**UNCONFIRMED**). FGPAT lists Organization "Administration: **write**" even for these GETs (FGPAT). Custom role: "Manage organization ref update rules and rulesets" (CUSTORG). Errors listed: 404, 500. | **Team or Enterprise** ("For customers on GitHub Team or GitHub Enterprise plans") | /en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization, R-RULES |
| Security configurations | Org-defined bundles of repo security settings, plus defaults for new repos | `GET /orgs/{org}/code-security/configurations`, `/defaults`, `/{id}/repositories`; per repo `GET /repos/{o}/{r}/code-security-configuration`. The legacy `*_enabled_for_new_repositories` fields on GET /orgs are deprecated. | "administrator or security manager"; classic `read:org` (`write:org` for get-one, as documented); FGPAT Organization "Administration: read" (R-SECCONF, FGPAT) | All for free features; GHAS products purchasable on Team and Enterprise Cloud | /en/code-security/securing-your-organization/introduction-to-securing-your-organization-at-scale/about-enabling-security-features-at-scale, R-SECCONF |
| Actions policy | Which repos may use Actions; which actions are allowed; SHA pinning | `GET /orgs/{org}/actions/permissions` → `enabled_repositories` (all/none/selected), `allowed_actions` (all/local_only/selected), `sha_pinning_required`; `.../selected-actions` → `github_owned_allowed`, `verified_allowed`, `patterns_allowed[]` | classic `admin:org`; FGPAT Organization "Administration: read"; caller role not stated (**UNCONFIRMED**; owners or CI/CD admin per PREDEF and CUSTORG) | All; an enterprise policy may override it | R-ACTIONS, /en/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization |
| Default GITHUB_TOKEN permissions | read or write default; whether Actions can approve PRs | `GET /orgs/{org}/actions/permissions/workflow` → `default_workflow_permissions`, `can_approve_pull_request_reviews`. Also fork-PR approval, self-hosted runner settings, retention. | As above | All | R-ACTIONS |
| Audit log | Events from the last 180 days; "Only owners can access" in the UI. A custom role "View organization audit log" exists on Enterprise Cloud. | `GET /orgs/{org}/audit-log` (`phrase`, `include=web\|git\|all`) | Owner; classic `read:audit_log`; 1,750 queries/hour (R-ORGS-GHEC). GraphQL `auditLog` is deprecated, "Removal on 2026-04-01" (GQL-ORGS). | **API: Enterprise Cloud only** ("Organizations that use GitHub Enterprise Cloud can interact with the audit log using the GraphQL API and REST API") | /en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization, R-ORGS-GHEC |
| SAML SSO | Members must authenticate through the IdP; also governs credential authorizations | GraphQL `organization.samlIdentityProvider`, visible to owners, owners' classic PATs with `read:org`/`admin:org`, or Apps with Members read or write (GQL-ORGS). Also `credential-authorizations` (C). | Owner | **Enterprise Cloud only** | /en/organizations/managing-saml-single-sign-on-for-your-organization/about-identity-and-access-management-with-saml-single-sign-on |
| IP allow list | Restricts network access to org resources | GraphQL `ipAllowListEnabledSetting`, `ipAllowListEntries`, `ipAllowListForInstalledAppsEnabledSetting` | **UNCONFIRMED** | Enterprise Cloud (PLANS) | GQL-ORGS, PLANS |
| Blocking and interaction limits | Moderators and owners | `GET /orgs/{org}/blocks`; `GET /orgs/{org}/interaction-limits` | Interaction limits: FGPAT Organization "Administration: read". Blocks: "Blocking users" permission (FGPAT). Caller role **UNCONFIRMED**. | All | R-BLOCK, R-INTER |

## E. Membership visibility (public vs concealed)

| Fact | Detail | Docs |
|---|---|---|
| Default | "By default, your organization membership visibility is set to private"; each user can publicize their own membership | /en/account-and-profile/concepts/organization-membership |
| Who can toggle | Only the user, for themselves: `PUT`/`DELETE /orgs/{org}/public_members/{username}` ("A user cannot publicize the membership for another user"; removal fails if "public visibility is enforced by default") | R-MEMBERS |
| Who sees concealed members | `GET /orgs/{org}/members`: "If the authenticated user is also a member of this organization then both concealed and public members will be returned." PREDEF: "See all organization members and teams" is granted to Owners, Members, Moderators, Security managers and App managers, but **not** Billing managers ("cannot ... See private members", BILL). | R-MEMBERS, PREDEF, BILL |
| What a non-member sees | `GET /orgs/{org}/members` from a non-member returns public members only. **UNCONFIRMED**: the current text states only the member case. `GET /orgs/{org}/public_members` lists public members. | R-MEMBERS |
| Check one user | `GET /orgs/{org}/members/{u}`: **204** if the requester is a member and the user is a member; **404** if the requester is a member and the user is not; **302** (redirect) "if requester is not an organization member". `GET /orgs/{org}/public_members/{u}` checks public membership only. | R-MEMBERS |
| Role and state | `GET /orgs/{org}/memberships/{u}` (requester must be a member) → `role`, `state` (`active`/`pending`), `direct_membership` | R-MEMBERS |
| Pending invitations | `GET /orgs/{org}/invitations` (`role` direct_member, admin, billing_manager or hiring_manager; `invitation_source` member or scim); GraphQL `pendingMembers`. Owner-only per the related invitation endpoints ("must be an organization owner" to see invitations, on the invitation-teams endpoint). | R-MEMBERS, GQL-ORGS |
| Token note | Fine-grained token: Organization "Members: read" covers members, public_members, memberships, outside_collaborators, teams and org-role assignees | FGPAT |

## Notes and caveats

1. A complete owner list needs a caller who can see concealed members (any member). A non-member program sees only public members. The exact behaviour for non-members is UNCONFIRMED (see E).
2. Many governance fields on `GET /orgs/{org}` need an owner caller and an `admin:org` token. The docs do not list which fields a non-owner loses: UNCONFIRMED.
3. Enterprise Cloud only: custom org roles, custom repo roles, SAML SSO and credential authorizations, the audit-log API, restricting outside-collaborator invites to owners, "private-only" repo creation, and the IP allow list. Org rulesets need Team or Enterprise.
4. Removed or closing-down endpoints: `/orgs/{org}/security-managers` (from 2026-01-01; use organization-roles), the GraphQL `auditLog` (removal 2026-04-01), the legacy `/teams/{id}` routes, and the `custom_roles` routes.
5. The PAT inventory and request endpoints work **only for GitHub Apps**. A `gh` user token cannot read them.
6. The `role_name` and `permission` on the collaborator endpoints are the highest effective role. The docs say the API cannot tell whether a grant came from the org or the repo, so attributing a grant needs the team, collaborator and org-role endpoints together.
