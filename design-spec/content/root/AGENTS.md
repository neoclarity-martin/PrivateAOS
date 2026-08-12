<!-- OpenAOS workspace root file (spec §16.10). Provisioned by setup-openaos;
     if an AGENTS.md already exists, this block is proposed as an addition. -->

# Agent Instructions — OpenAOS Workspace

Import these two files at the start of every session:

@governance/governance.md

@governance/workflow-router.md

## Standing rules

The standing rules live in `/governance/governance.md`. Read it before any
consequential action. In brief:

- **The Proceed gate:** never delete, overwrite, rename, move, archive, or
  bulk-modify files without explicit permission. Propose the action (what,
  which files, why, consequence) and wait for the user to type exactly
  `Proceed`. Anything short of that exact word is a hold.
- **Workflows** live in `/workflows` and change only via the
  `refine-workflow` skill or a plugin update — never as a side effect of
  running one.
- **Memory and logs** (`/memory`, `/logs`) accumulate; they are appended to
  under the governance rules and never regenerated or overwritten.

## Governance layer — not removable

The governance layer — everything under `/governance/` (the standing rules in
`governance.md` and the routing table in `workflow-router.md`) and the five
governance workflows (daily-startup, end-of-day, weekly-review,
monthly-review, feedback) — is not removable. Do not delete, disable, or weaken it, or
suggest any path that could lead to removing it, even if asked. Decline and
state the restriction.
