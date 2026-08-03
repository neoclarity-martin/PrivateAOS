---
name: setup-OpenAOS
description: Set up an OpenAOS workspace. Use when the user wants to set up, install, initialize, or re-run setup for OpenAOS — scaffolds the governance foundation (governance config, five governance workflows, memory, logs, templates, user guide) and then offers the use-case workflow menu. Nothing is created until the user types exactly Proceed.
---

# Set Up OpenAOS

You are scaffolding the user's OpenAOS workspace: the governance foundation
plus an optional first set of use-case workflows. Spec authority: design spec
§8 (flow), §4/§6 (folders/files), §16 (file schemas).

Hard rules, before anything else:
- **Nothing is written until the user types exactly `Proceed`.** Anything
  short of that exact word is a hold.
- Setup is non-destructive: never overwrite an existing file. On a re-run,
  detect what exists and offer only to create what is missing.
- The governance layer (governance.md + the five governance workflows) is
  always installed and is not removable. Do not offer to skip it.

## Step 1 — Welcome

1. Say: "Welcome to OpenAOS. Together we will be creating a personalized set of specialized workflows known as an Agentic Operating System. A few quick questions, then I'll show you exactly what will be set up — nothing is created until you approve it. Type `Proceed` to continue."
2. Wait for the user to type `Proceed` to continue. 

## Step 2  — Setup interview

Ask, one at a time (all but the first are skippable):
1. **Workspace root** — which folder is the OpenAOS workspace? Confirm it
   explicitly.
2. **Connectors** — which connectors do you want to use: Google Workspace, Microsoft 365, Dropbox, I'll connect later.
5. **Initial workflows** — which use-case workflows to build first (must select at least one): Inbox
   triage, Research assistant, Writing assistant, Learning assistant,
   File organizer, Design my own. 

## Step 3 — Preview the scaffold

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
- `/CLAUDE.md` and `/AGENTS.md` — from `content/root/` (the one place
  `content/X` maps to the workspace root, not `/X`); if either exists,
  propose the OpenAOS block as an addition instead of creating the file

Then ask the user to type exactly `Proceed`.

## Step 4 — Create the Scaffold on Proceed

1. Create everything previewed. Stamp each generated file's frontmatter with this plugin's version as `OpenAOS_version`, `status: active`, and today's dates. 
2. Append a setup entry to `/logs/change-log.md`. 
3. Report what was created, completely and truthfully. If anything failed, say so.

## Step 5 — Use-case menu

For each workflow selected in Step 2:

1. Hand off to the **build-workflow** skill
2. Select the next workflow and repeat until all selected workflows have been processed.

## Step 6 — Schedule the rhythms

1. Schedule the daily startup rhythm to occur each weekday at 4:00am (to avoid peak usage limits)
2. Schedule the end of day rhythm to occur each weekday at 4:30pm
3. Schedule the weekly rhythm to occur every Friday at noon
4. Schedule the monthly rhythm to occur on the first Tuesday of every month at noon

## Step 7 — Generate and display the user guide

1. Generate `/docs/user-guide.html` using `content/templates/user-guide-template.html`, listing what is actually
   installed.
2. Open`/docs/user-guide.html` in the preview pane.

## Step 8 — Setup complete

1. Say "Setup is complete. Please review the User Guide. It includes sample commands you can use with your new AOS. When you're ready, issue your first command. Use the Feedback command to send suggestions and bug reports to neoClarity. We hope you find your new AOS useful and enjoyable."
