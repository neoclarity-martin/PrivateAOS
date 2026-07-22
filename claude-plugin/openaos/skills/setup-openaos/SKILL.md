---
name: setup-openaos
description: Set up an openaos workspace. Use when the user wants to set up, install, initialize, or re-run setup for openaos — scaffolds the governance foundation (governance config, five governance workflows, memory, logs, templates, user guide) and then offers the use-case workflow menu. Nothing is created until the user types exactly Proceed.
---

# Set Up openaos

You are scaffolding the user's openaos workspace: the governance foundation
plus an optional first set of use-case workflows. Spec authority: design spec
§8 (flow), §4/§6 (folders/files), §16 (file schemas).

Hard rules, before anything else:
- **Nothing is written until the user types exactly `Proceed`.** Anything
  short of that exact word is a hold.
- Setup is non-destructive: never overwrite an existing file. On a re-run,
  detect what exists and offer only to create what is missing.
- The governance layer (governance.md + the five governance workflows) is
  always installed and is not removable. Do not offer to skip it.

## Step 1 — Welcome & interview

Say: "Welcome to openaos. A few quick questions, then I'll show you exactly
what will be set up — nothing is created until you approve it."

Ask, one at a time (all but the first are skippable):
1. **Workspace root** — which folder is the openaos workspace? Confirm it
   explicitly.
2. **Work focus** — what kind of work do they most want help with? (Shapes
   the menu emphasis; with approval, seeds /memory/user-profile.md.)
3. **Rhythms** — which check-in cadences to schedule: all / daily only /
   weekly+monthly only / none for now. All five governance workflows are
   installed regardless; this sets only the active cadences.
4. **Memory seeds** — any people, tools, or preferences to remember from the
   start? Default: seed empty. Never fabricate a memory entry.
5. **First workflows** — which use-case workflows to build first: Inbox
   triage, Research assistant, Writing assistant, Learning assistant,
   Organizer / declutter, Design my own — or none yet (perfectly valid).

## Step 2 — Preview the scaffold

List every folder and file that will be created, and state that nothing
exists yet and nothing will be overwritten:

Folders: `/governance /workflows /memory /logs /templates /docs /outputs
/inbox /inbox/processed /archive`

Files:
- `/governance/governance.md` — from `content/governance/governance.md`
- `/workflows/daily-startup.md`, `end-of-day.md`, `weekly-review.md`,
  `monthly-review.md`, `feedback.md` — from `content/workflows/`
- `/memory/user-profile.md`, `preferences.md`, `people.md`, `decisions.md` —
  empty per the memory schema (or seeded per step 1, each seed shown)
- `/logs/decision-log.md`, `change-log.md`, `feedback-log.md` — empty
- `/templates/decision-entry-template.md`, `approval-request-template.md`,
  `memory-entry-template.md` — from `content/templates/`
- `/templates/daily-startup-report-template.html`,
  `end-of-day-carryover-template.html`,
  `weekly-review-report-template.html`,
  `monthly-review-report-template.html`,
  `inbox-triage-report-template.html`, `organizer-report-template.html`,
  `learning-assistant-report-template.html` — all seven HTML report
  templates, from `content/templates/`, shipped upfront regardless of which
  use-case workflows are selected in step 4 (build-workflow only wires an
  instantiated use case to its already-shipped template; it never writes
  one)
- `/docs/user-guide.html` — generated from
  `content/templates/user-guide-template.html`, listing what is actually
  installed
- `/CLAUDE.md` and `/AGENTS.md` — from `templates/`; if either exists,
  propose the openaos block as an addition instead of creating the file

Then ask the user to type exactly `Proceed`.

## Step 3 — Create on Proceed

Create everything previewed. Stamp each generated file's frontmatter with
this plugin's version as `openaos_version`, `status: active`, and today's
dates. Append a setup entry to `/logs/change-log.md`. Report what was
created, completely and truthfully — if anything failed, say so.

## Step 4 — Use-case menu

For each workflow selected in step 1 (or if the user now wants one), hand
off to the **build-workflow** skill — one build session per workflow. Zero
workflows is fine; nothing generic is ever scaffolded.

## Step 5 — Close

Show the user: where things live, how to run a workflow ("run my daily
startup"), how to change one ("refine my inbox triage workflow" →
refine-workflow), and how to send feedback (the feedback workflow — scrubbed
and previewed; nothing is emailed without `Proceed`). Point to
`/docs/user-guide.html` for all of this in plain language.
