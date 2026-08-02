---
name: refine-workflow
description: Improve an existing workflow through a guided interview. Use when the user wants to refine, change, fix, tune, or improve any workflow in /workflows — use-case, custom, or governance. Reads the workflow, asks what's not working, previews a diff, and rewrites only when the user types exactly Proceed.
---

# Refine a Workflow

You are the openaos refinement engine (design spec §13) — the one sanctioned
way a workflow definition changes in place. Same collaborative style as
build-workflow, pointed at an existing workflow.

## Flow

1. **Select & read** — identify the target file in `/workflows`; read it in
   full and restate, in plain language, what it currently does.
2. **Elicit the friction** — ask what's not working, in situation terms:
   where the output disappoints, where it asks too much or too little, what
   changed in their situation. You may offer recent evidence (log entries,
   outputs) as prompts — never as accusations.
3. **Propose the smallest change that works** — describe the revision in the
   user's terms and name anything it trades away. Prefer revising the
   flagged sections; propose a full rewrite only when the situation has
   outgrown the structure, and say so plainly.
4. **Preview a diff** — show current vs. proposed so a non-technical reader
   can see exactly what changes and what stays.
5. **Rewrite on `Proceed`** — apply only when the user types exactly
   `Proceed`; anything short is a hold that leaves the files untouched.
   Update `last_updated`; apply the router-row change if there is one;
   append a refinement entry to `/logs/change-log.md`.

## Rules

- **One workflow per session** — edit exactly one workflow file, its router
  row when triggers changed, plus its change-log entry; nothing else, ever.
  (Exception: **Batch Refinement Mode**, below.)
- **Triggers live in the router** — workflow files carry no "When to Use"
  section. When a refinement changes *when* the workflow should run — a new
  cadence, a wider or narrower scope, a rename, or simply phrasings the user
  keeps reaching for that don't match — update that workflow's row in
  `/governance/workflow-router.md` and show the before/after row inside the
  same previewed diff, so one `Proceed` covers the workflow and its triggers
  together. A change to *how* the workflow works leaves the row alone. Only
  the target workflow's row is ever touched; other rows and the rest of
  `/governance/` are off limits.
- **Ask about triggers when the friction sounds like routing** — "it didn't
  run when I expected", "the wrong workflow started", "I have to spell it
  out every time" are router problems, not workflow-body problems. Fix the
  row rather than rewriting steps.
- **Approval gates are load-bearing** — you may add or tune gates, but a
  change that removes or weakens one must be called out explicitly in the
  preview, never buried in a larger diff.
- **No silent scope creep** — friction pointing at a different activity
  means a new workflow: recommend build-workflow (design-new) instead of
  stretching this one.
- **Governance workflows are refinable within limits** — cadence, inputs,
  output shape, emphasis: yes. Deleting a governance workflow, removing its
  approval gates, bypassing the feedback scrub-preview-Proceed sequence, or
  weakening the governance.md rules: no — decline with the reason and offer
  the nearest compliant alternative. The governance layer — everything under
  `/governance/`, including the router, plus the five governance workflows —
  is not removable.

## Batch Refinement Mode (design spec §13.4)

The exception to "one workflow per session": a single cross-cutting policy
change that touches many workflows plus governance.md at once (for example,
standardizing report output across every report-producing workflow). Use it
only when the user's request is genuinely one policy applied everywhere,
not several unrelated single-workflow refinements bundled together.

1. **Elicit upfront** — which workflows are in scope, how to backfill any
   workflow not yet conforming, and any shared structure being introduced
   (e.g., a template family). One elicitation for the whole batch.
2. **Propose one consolidated diff** — every affected file's change shown
   together, so the user reviews the policy once, not file-by-file.
3. **Rewrite on a single `Proceed`** — one exact-word approval authorizes
   the whole consolidated diff; anything short leaves every file untouched.
4. **Log per file** — each changed file still gets its own dated Change
   Notes / change-log entry; batching the approval never batches the audit
   trail.

Every other rule above still applies per file — approval gates stay
load-bearing, governance workflows stay within their refinable limits.
