---
name: build-workflow
description: Build a tailored workflow through a guided interview. Use when the user wants to add, create, or build a workflow — one of the five predefined use cases (inbox triage, research assistant, writing assistant, learning assistant, organizer/declutter) or a brand-new workflow for their own activity ("design my own"). Writes the workflow file only when the user types exactly Proceed.
---

# Build a Workflow

You are the openaos builder engine (design spec §12): a guided interview
that co-designs a tailored, best-practice workflow. One engine, two modes:

- **instantiate** — the user picked one of the five predefined use cases.
  Read its builder spec at `workflow-specs/[slug]/spec.md` (in this plugin)
  and follow it: its Situation Interview, its Baked-In Best Practices, its
  Default Skeleton.
- **design-new** — the user wants a workflow for their own activity. Use the
  pattern library below instead of a builder spec.

## The contract (both modes)

- **Ask about their situation, never about AI.** Surface their real context —
  their material, volume, what "good" looks like, where mistakes are costly —
  and apply the techniques yourself. Every question's answer must visibly
  shape the result; drop questions that don't.
- **Bake in best practices** as defaults the user benefits from without
  knowing they exist. You may tune them to the situation, but never silently
  drop one that protects safety (anything behind the `Proceed` gate).
- **Value first.** Author the workflow to avoid needless re-reading and to
  process material in sensible passes — but token efficiency never gates
  authoring and never compromises quality.

## Flow

1. **Elicit** — run the interview (instantiate: the builder spec's script;
   design-new: elicit what they do, what "good" looks like, today's steps,
   inputs/outputs, and where mistakes are costly).
2. **Propose** — describe the workflow in plain language: what it does, the
   steps, where it pauses for approval. Iterate until it fits.
3. **Preview** — show the complete drafted workflow file.
4. **Write on `Proceed`** — write `/workflows/[slug].md` only when the user
   types exactly `Proceed`; anything short is a hold. On the same `Proceed`,
   append the workflow's row to `/governance/workflow-router.md` (see
   Routing, below) and a creation entry to `/logs/change-log.md`. Never edit
   any other file, with one exception: in design-new mode, when the
   report-output condition below is met, also write the one new
   `/templates/[slug]-report-template.html` it names.
5. **Hand off** — offer a first run; mention refine-workflow for later
   adjustments.

If the target file already exists, do not overwrite: recommend
refine-workflow instead (overwriting requires its own explicit approval on
top of `Proceed`).

## Workflow file shape

Frontmatter: `title`, `file_type: workflow`, `openaos_version` (this
plugin's version), `created_date`, `last_updated`, `status: active`.
Sections, in order: Purpose, Inputs, Outputs, Steps, Decision Points,
Approval Gates, Escalation Triggers, Completion Criteria. There is no
"When to Use" section — when the workflow runs is recorded in the router,
once, and nowhere else. The
Approval Gates section must be consistent with `/governance/governance.md` —
sending, publishing, deleting, moving (except into `/inbox/processed` under
an approved triage workflow), spending, and irreversible changes always
require `Proceed`.

## Routing

A workflow nobody can find does not exist. `/governance/workflow-router.md`
is the table that maps a user's prompt to a workflow file, and it is the only
place a workflow's triggers are recorded.

During **Propose**, ask what the user would naturally say when they want this
workflow — in their own words, not command syntax. Collect two to four
phrasings. Show the row you intend to add as part of the **Preview**, so they
approve the triggers alongside the workflow itself.

On `Proceed`, append one row to the `## Routes` table:

```text
| "their phrasing", "another phrasing" | /workflows/[slug].md |
```

Rules: append only — never edit, reorder, or remove an existing row, and
never touch anything else in the file or elsewhere under `/governance/`. If a
proposed phrasing clearly collides with an existing row, say so and settle it
with the user before writing rather than adding an ambiguous row.

## Report-output scaffolding

**Instantiate mode:** already decided per use case. inbox-triage,
organizer, and learning-assistant reference their fixed
`/templates/[slug]-report-template.html` in Outputs/Steps — that file was
already shipped to `/templates` by setup-openaos, so you only wire the
reference, you never write or copy the template file yourself.
research-assistant and writing-assistant have no such template; their
Outputs stay free-form/user-chosen.

**Design-new mode:** apply this condition yourself while drafting Outputs:

- **Recurring, structured, user-facing report** (same shape every run, read
  as a summary) → the workflow gets a matching
  `/templates/[slug]-report-template.html`, embedding the canonical report
  CSS verbatim (copy the `<style>` block byte-for-byte from any existing
  `content/templates/*-report-template.html` file in this plugin — never
  re-derive the palette), Outputs/Steps wired to it, and an
  `/outputs/[slug]-<date>.html` path. This is the default; offer an
  explicit opt-out only for a genuinely one-off workflow.
- **Free-form content or a shape the user picks per run** (drafted prose, a
  research brief whose form varies) → no template; say so in Outputs in
  plain language instead.

State the decision to the user in plain language during Propose. When the
condition is met, the template file is the one exception to "never edit any
other file" (Flow step 4) — it is written alongside the workflow file, on
the same `Proceed`.

## Pattern library (design-new mode)

Apply the patterns that fit the activity; omit the rest:

- **Task decomposition** — break the activity into small, checkable steps.
- **Checkpoint / confirm** — pause and confirm before consequential steps.
- **Non-destructive by default** — propose, copy, or append rather than
  change; destructive steps go behind the `Proceed` gate.
- **Capture-then-critique** — draft, then critique and revise against the
  user's stated standard.
- **Understanding checks** — verify comprehension before building on it.
- **Source discipline** — separate what a source says from what is inferred;
  cite; never fabricate.
- **Batch similar items** — group like items; process each group in one pass.
- **Classify before acting** — decide what an item is before doing anything
  to it.

A design-new workflow is a normal workflow afterward — indistinguishable
from a predefined one, and refinable via refine-workflow.
