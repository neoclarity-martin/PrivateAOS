## Planning mode rules

- Planning mode is active when the user's message begins with "Planning mode" or "pmode".
- While in planning mode:
  - Claude must always show it's reasoning
  - Claude should offer options and a recommendation when an issue is identified
  - Claude must NOT create, edit, rename, move, or delete any files.
  - Claude may only read files, research, and present a proposed plan.
  - Claude must wait for the user to type exactly: Proceed — before making any changes.

- Refining, adjusting, or approving a plan in conversation is NOT a "Proceed". Only the exact word counts.

## Commonly used files and folders

"design spec" = "/design-spec/openaos-design-specification.md"
"runbook" = "/design-spec/openaos-packaging-runbook.md"
"feature-specs" = "/internal-only/feature-specs"

Any file in or under the `/design-spec/` folder is considered a component of the design spec (source of truth), not a generated/rendered copy — this includes `workflow-catalog.yaml`, `workflow-specs/*`, and `setup-interview.md`, not just the main specification document.

## Include the standard AGENTS.md file

@AGENTS.md
