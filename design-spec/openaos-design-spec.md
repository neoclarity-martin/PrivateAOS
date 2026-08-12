---
title: OpenAOS Design Specification
file_type: design_spec
project: OpenAOS
created_date: 2026-06-02
last_updated: 2026-08-02
openaos_version: 3.2.0
status: design_ready_for_generation
important_constraint: Do not generate actual OpenAOS files unless the user explicitly types exactly Proceed.
---

# OpenAOS Design Specification

---

# 3.0 Rewrite Frame — Minimal, Workflow-First OpenAOS

> **Status of this block (rewrite complete, 2026-07-17):** This section is
> the authoritative frame of the 3.0 Minimal design; the body below now
> implements it in full (Phases B–H of the rewrite, feature spec
> `internal-only/feature-specs/3.0-create-minimal-openaos.md`). The
> pre-rewrite 2.x spec is preserved at git tag `spec-v2.4.2`.

## Goal

Claude Cowork makes Claude accessible to non-technical users, but leaves them
on their own to turn that access into workflows that are actually good —
well-designed, tailored to their situation, and safe to run against their real
files. **OpenAOS exists to close that gap.** Its purpose is to
**collaboratively build the most useful, most user-friendly workflow for each
of a non-technical user's core use cases**, through a guided interview that
embeds AI best practices the user doesn't have to know; to let the user
**refine any workflow just as easily**, through the same collaborative
interview style; and to keep all of it **safe by default** (nothing
destructive without explicit `Proceed`) and **improving over time** (an easy
channel to send feedback back to the project team). Everything else is
scaffolding in service of that goal.

## Guiding Principle

**A generative core, guarded — nothing more.** The reason a non-technical
user adopts OpenAOS is the promise of a genuinely good, tailored workflow for
the handful of things they actually do. So the whole system is exactly three
things:

1. **Use-case workflow builders** — guided interviews that co-design a
   tailored, best-practice workflow for each core use case.
2. **Workflow refinement** — the same collaborative interview, pointed at an
   existing workflow, to improve it.
3. **Guardrails** — the `Proceed` safety gate, durable memory, review rhythms,
   and a feedback-to-team channel that make those workflows trustworthy.

The builders include a **custom builder** that co-designs brand-new workflows
for the user's own domain — so OpenAOS is not limited to the use cases we
anticipated. This is what turns OpenAOS from "a handful of useful workflows"
into "a way to bring AI into whatever the user actually does to create
value," and is arguably its highest-leverage capability.

Value to the user is the primary objective. Everything that does not directly
serve it — the multi-agent roster, the Pro tier, tiered versioning, DDD
relationship semantics, the factory/instance split — is removed, from both
this spec and the artifacts it generates.

## Core Model

The Minimal OpenAOS design, in full:

- **Workflows.** The unit of value. Two families:
  - *Use-case workflows* — five predefined ones, each authored by a builder
    interview: **inbox triage** (classify, route, and act on inbox items),
    **research assistant** (scoped, source-disciplined research), **writing
    assistant** (drafting/editing keyed to the user's voice), **learning
    assistant / tutor** (guided learning with understanding checks), and
    **file organizer** (file cleanup — inbox-triage for files).
  - *Governance workflows*: daily-startup, end-of-day, weekly-review,
    monthly-review, and feedback submission.
- **Workflows vs. skills (definition).** *Workflows* are user-owned
  artifacts: scaffolded into the user's workspace, tailored to their
  situation, covered by the drift invariant, and refinable via
  `refine-workflow`. *Skills* (`setup-openaos`, `build-workflow`,
  `refine-workflow`) are plugin-owned machinery: shipped identical to every
  user and changed only by plugin updates — never user-refinable.
- **Governance config.** A single standing-rules file,
  `/governance/governance.md`: the `Proceed` safety gate, the permission
  model, and memory boundaries. Standing rules live here; runnable procedures
  are workflows.
- **Builder interview** — the `build-workflow` skill: a guided interview that
  co-designs a tailored workflow. One engine, two modes: **instantiate** one
  of the five predefined use cases, or **design-new** — co-author a
  brand-new, domain-specific workflow from the user's own activity. Both
  embed AI best practices and are value-first; token efficiency is a
  secondary, never-gating consideration. Both produce a workflow that is
  refinable via `refine-workflow`.
- **Refinement interview** — the `refine-workflow` skill: reads an existing
  workflow, asks what's not working, previews a diff, rewrites on `Proceed`.
- **Setup** — the `setup-openaos` skill: scaffolds the shared foundation
  (memory, logs, governance config, governance workflows, user guide) on
  install, then presents the use-case menu and hands off to `build-workflow`.
  Zero use-case workflows at setup is valid — every workflow is
  interview-authored, so nothing generic is ever scaffolded.
- **Memory & safety.** Durable `/memory` and `/logs`; the definition-vs-data
  drift invariant (kept, simplified): data files accumulate and are never
  overwritten; workflow/config definition files change only via the
  refinement interview or a plugin update, each `Proceed`-gated.
- **Distribution.** One artifact: the **OpenAOS** Claude plugin, generated
  directly from this spec. No factory, no instance concept. A single
  `openaos_version` is the only version fact.

Removed from the spec entirely: the five governance *agents* as separate
agents, the ten-agent optional roster, the Pro tier and tier concept,
`spec_version`/`catalog_version`/`compatible_aos_versions` multi-track
versioning (a single `openaos_version` remains), the DDD relationship
vocabulary and typed collaboration edges, the factory-vs-instance guard and
layout, and all sections that exist only to serve those. The exact deletions
are enumerated in the removal manifest
(`internal-only/feature-specs/implemented/3.0-removal-manifest.md`).

---

## Purpose of This Document

This document is the consolidated design specification for **OpenAOS**.

This document is a design artifact only. It does **not** authorize creation of actual OpenAOS files.

The assistant must not generate actual OpenAOS files unless the user explicitly types exactly:

```text
Proceed
```

## Required Next-Step Instructions

The assistant continuing from this document must:

```text
- Review the next steps with the user.
- The user may ask additional questions about the design or next steps.
- Wait for the user to enter the exact instruction “Proceed” to generate the OpenAOS files.
```

## Document Set

This specification is maintained as a small set of companion files in this folder:

```text
openaos-design-spec.md                - the canonical design (this file)
openaos-runbook.md                    - packaging and handoff procedure (rewritten in Phase G)
openaos-revision-history.md           - dated revision and consistency-resolution history
workflow-catalog.yaml                 - the Workflow Catalog: structured workflow identity/ownership data (Section 7A)
vocabulary.yaml                       - controlled vocabularies (file_type/status, permissions/actions), source of truth for Sections 3.2-3.4, 15.4-15.5
file-skeletons.yaml                   - ordered section/field skeletons for generated files (Section 16)
setup-interview.md                    - the setup interview script (rewritten in Phase G)
sync-exclusions.md                    - tenet-check exclusions and their dispositions (read by §34 item 13)
vocabulary.schema.json                - JSON Schema for vocabulary.yaml
workflow-catalog.schema.json          - JSON Schema for workflow-catalog.yaml
content/                              - 20 content sources: the canonical bodies for governance.md,
                                        the workflow router, the five governance workflows, and all
                                        eleven templates (§18.7, §35). Byte-identical to their
                                        counterparts under claude-plugin/openaos/.
workflow-specs/                       - the five use-case builder specs (§7B.1), byte-identical to
                                        their plugin counterparts
```

**Stamped set vs. document set.** `check-spec-version.py` stamps 12 of these
files — the three main documents, `workflow-catalog.yaml`, `vocabulary.yaml`,
`file-skeletons.yaml`, `setup-interview.md`, and the five
`workflow-specs/*/spec.md`. The remainder are deliberately unstamped: the
`content/` sources and `sync-exclusions.md` carry no `openaos_version`
frontmatter, and the two JSON Schema files carry no frontmatter at all. The
document set is therefore larger than the stamped set by design; both are
governed by §36.1 step 3 and by the `Proceed` gate, and `CLAUDE.md` treats
every file under `design-spec/` as a component of the specification.

The canonical specification remains the single source of truth (Section 1.6.1); the companion files hold structured data extracted from it for machine enforcement and are governed by the same `Proceed` safety gate. They are design-time **source** artifacts that live with the spec here in `design-spec/` (versioned by `openaos_version`). For the vocabularies these files own, the prose Sections above carry the normative meaning and rules; the data files carry the enumerated tokens, which the prose references rather than restates.

## Revision History

The full revision history of this specification — including all dated Design Consistency Resolution cycles — is maintained in a companion file:

```text
openaos-revision-history.md
```

Entries there are maintained in reverse chronological order (newest first); new entries are added at the top, as rows in a single table (`openaos_version | Date | Change`). The table is a log of completed cycles, not a one-row-per-unique-version index — the same `openaos_version` may appear in consecutive rows when multiple cycles complete against it without a content change, each with its own date and change description.

Every completed §36.1 Design Readiness Review or §36.2 Plugin Generation cycle gets a row, so the file is a single place to see the current state of the spec and the plugin. `openaos_version` increments only when a cycle actually changes the specification (or, for §36.2, the packaged plugin) — a full §36.1 consistency-review cycle is one increment and one consolidated row when it resolves at least one inconsistency, not one per re-read iteration, however many iterations the loop takes. A cycle that completes with no changes (for example, a Design Readiness Review that surfaces no inconsistencies, or a Plugin Generation that produces no diff from the prior run) still gets a row describing that outcome, logged against the current `openaos_version` rather than incrementing it. A structural change (for example, a document restructure) is its own separate increment.

---

# 1. Project Overview

## 1.1 Project Name

Working project name:

```text
OpenAOS Project
```

The generated system is referred to as:

```text
Agentic Operating System
AOS
```

The framework and the plugin share one name, written two ways. The **display
name**, used in all prose, headings, titles, and user-facing text, is:

```text
OpenAOS
```

The **identifier** — the plugin slug, used in `plugin.json` `name`, the
marketplace entry, the repository path `claude-plugin/openaos/`, the plugin
keyword, and the `openaos@neoclarity.ai` address — is lowercase:

```text
openaos
```

These are the same name at different layers, not two conventions. The
identifier form is **not** subject to display-name capitalization: a branding
pass over prose must leave slugs, filenames, paths, frontmatter keys (notably
`openaos_version`), skill names (`setup-openaos`), and code spans untouched.
Widening a capitalization sweep to those is a defect, not a consistency fix —
see the 2026-08-12 revision-history entry for the `OpenAOS_version` case.

There is no factory/instance term split: the plugin scaffolds the user's
workspace directly, and the workspace is simply the user's folder that OpenAOS
operates in.

## 1.2 Target Platform

The current target platform is:

```text
Claude Cowork
```

Portability to other platforms may be considered later, but is outside the current design scope.

## 1.3 Overall Purpose

OpenAOS should help a non-technical user collaboratively create the most useful, most user-friendly workflow for each of their core use cases — markdown-based workflows plus the memory, governance config, templates, and logs that make them trustworthy.

The builder is intended to be:

```text
A reusable template others could adopt.
```

It should not be only a one-off personal productivity setup, although it should work well for personal productivity.

## 1.4 What OpenAOS Ultimately Produces

The specification generates exactly one artifact: the **OpenAOS** Claude
plugin. Installed, the plugin scaffolds the user's workspace (memory, logs,
governance config, governance workflows, user guide) and provides the builder
and refinement skills that author the user's workflows. There is no separate
factory package and no separate instance concept. Distribution mechanics are
specified in Section 28 (rewritten in Phase G).

## 1.5 Build Process Philosophy

The build process should feel like a combination of:

```text
Executive coach
Friendly collaborator
```

The builder should:

```text
- Explain concepts in coach mode when needed.
- Switch to collaborator mode when making design choices.
- Recommend sensible defaults.
- Ask for approval on important design decisions.
- Move forward with documented assumptions for low-risk details.
- Defer to the user’s wishes.
```

## 1.6 Design Principles and Goals

This section states the principles and goals that motivate the rest of this specification. Section 2 and beyond define *how* OpenAOS behaves; this section defines *why*. When a future design decision is ambiguous, it should be resolved in favor of these principles. They are normative, not aspirational.

### 1.6.1 Design Spec as the Single Source of Truth

OpenAOS is generated from this design specification, not the other way around. The spec is canonical; the framework, the builder files, the plugin package, and any outward-facing description of the project are all **renderings** of it.

```text
- Every builder, workflow schema, workflow, and config traces back to a decision
  recorded here.
- When the spec and a generated artifact disagree, the spec wins and the
  artifact is corrected.
- Outward-facing material (README, pitch, user guide) derives from the spec so
  that documentation and marketing cannot silently drift away from the design.
```

This is what makes the system auditable and reproducible: anyone can regenerate the plugin from the spec and get the same result.

### 1.6.2 Governance Before Productivity

Safety, memory, and quality review must exist before any productive work happens. Setup scaffolds the governance config and governance workflows before any use-case workflow is built. Productivity is additive; governance is foundational. A user cannot end up with a fast, capable, ungoverned system.

### 1.6.3 Single Responsibility at Every Level

Each workflow owns exactly one activity, with explicit boundaries; the system avoids a catch-all procedure that does everything (Section 2.1). The same discipline applies to files: one file, one purpose, scope recoverable from its path. This keeps the system legible to non-technical users and extensible without redesign.

### 1.6.4 Non-Destructive and Approval-Gated by Default

The system prefers actions that cannot lose work. Workflows create, append, or ask rather than overwrite, delete, move, or bulk-modify (Section 2.4). Anything consequential is gated behind a single, unambiguous approval signal — the user typing exactly `Proceed` (Section 3.1) — and approval is specific to the action described, never a standing grant (Section 2.5). The goal is that a user can trust OpenAOS with real work without fear that it will quietly damage their files.

### 1.6.5 Standardization and Extensibility

Uniform schemas — workflow definitions, configs, memory, logs (Sections 15, 16) — let new workflows be added without inventing new formats. The one `build-workflow` engine (Section 12) covers both the predefined use cases and, via its design-new mode, any domain the user brings, so the collection is extensible by design rather than by exception.

### 1.6.7 Self-Documenting and Self-Improving

The system explains itself and improves itself on a cadence. Setup generates a plain-language user guide (Section 16.6). The governance workflows running from daily through monthly keep the system operationally clean, structurally healthy, and aligned with the user's actual goals (Section 17). Any workflow can be improved at any time through the refinement interview. Maintenance is a built-in behavior, not a manual afterthought.

### 1.6.8 Built for Non-Technical Users, Portable Across Platforms

The primary user is non-technical and the primary interface is conversational: setup is an interview, workflows are invoked by intent-matched trigger phrases, and the only exact-string command is `Proceed` (Sections 1.5, 16.6). The target platform is Claude Cowork, but because the entire system is plain markdown, it is portable to Claude Code and adaptable to other LLMs. The design avoids platform-specific mechanisms wherever a portable one exists.

### 1.6.10 Open Source

The project is released openly on Github. Openness reinforces key principles that make external contribution tractable: a single-source-of-truth spec, standardized schemas, and self-documenting output.

The project is hosted at:

```text
https://github.com/neoClarity-AI/OpenAOS
```

The contribution model follows directly from Section 1.6.1 (design spec as the single source of truth). The repository accepts pull requests **only against the design specification**. The Claude plugin is not accepted as a direct contribution; it is regenerated and published by neoClarity from the approved spec, so that quality and safety can be maintained and every released artifact provably traces back to a reviewed design. Although you can generate your own plugin, the way to change the "official" neoClarity plugin is to change the spec.

### 1.6.11 Goals (Summary)

```text
G1. Give non-technical users a genuinely good, tailored workflow for each of
    their core use cases — and a builder for any domain they bring.
G2. Keep the system safe and trustworthy by default (governance-first,
    non-destructive, approval-gated).
G3. Keep the design auditable and reproducible (spec as single source of truth).
G4. Keep the system extensible without redesign (standardized schemas, one
    builder engine, refinable workflows).
G5. Stay portable across Claude Cowork, Claude Code, and other LLMs.
G6. Be self-documenting and self-maintaining.
G7. Be open source and contributor-friendly.
```

---

# 2. Core Architectural Principles

## 2.1 Single Responsibility Principle

The system should follow the **Single Responsibility Principle**.

Each workflow should have a clear purpose, inputs, outputs, boundaries, and approval gates.

The system should avoid creating a bloated catch-all workflow that does everything.

Single responsibility and non-overlap are verified, not merely asserted: the Workflow Catalog (§7A) records each workflow's `domains_owned` and `artifacts_owned`, and the catalog validation (§27) is the enforcement surface for this principle.

## 2.4 Non-Destructive by Default

The system should prefer non-destructive actions.

Workflows should create new files, append to logs, create dated or versioned copies, or ask for clarification when the safest action is unclear.

No workflow may delete, overwrite, rename, move, archive, or bulk-modify files without explicit approval.

## 2.5 Approval Is Action-Specific

User permission applies only to the specific action described.

```text
- Permission to modify one file does not imply permission to modify other files.
- Permission to perform one overwrite does not imply permission for future overwrites.
- Permission to proceed with a batch action applies only to the listed files and changes.
```

---

# 3. Global Safety and Approval Rules

## 3.1 Global File Safety Rule

```text
Never delete, overwrite, rename, move, archive, or bulk-modify files unless the user has given explicit permission.

When a workflow proposes one of these actions, it must first:

1. Explain exactly what action it wants to take.
2. Identify the affected file or files.
3. Explain why the action is recommended.
4. Explain the likely consequence of the action.
5. Ask the user to type exactly: Proceed

If the user does not type Proceed, the workflow must not take the action.

The workflow may suggest safer alternatives, such as copying the file, creating a backup, appending new content, or creating a new versioned file instead of modifying the original.
```

## 3.2 Actions Requiring Explicit Approval

The actions that always require approval are the controlled list `approval_required_actions` in `design-spec/vocabulary.yaml` (source of truth). Each entry carries a stable `id` and its human-readable `label`; where an action has a scoped exception — for example, moving items into `/inbox/processed` under the user-approved inbox-triage workflow is pre-authorized as part of that workflow (Section 31) — the exception is carried on that entry's `note` field, not flattened away. These are the Level 2 actions of the §3.4 model.

The user must type exactly:

```text
Proceed
```

## 3.3 Safe Autonomous Actions

Workflows may autonomously perform low-risk actions — the controlled list is `safe_autonomous_actions` in `design-spec/vocabulary.yaml` (source of truth). These are the Level 1 actions of the §3.4 model.

This is allowed only when the action does not overwrite, delete, move, rename, archive, publish, send, spend money, or expose private information.

## 3.4 Permission Levels

The AOS uses a three-level permission model — the levels, their stable names, and their one-line meanings are `permission_levels` in `design-spec/vocabulary.yaml` (source of truth): Level 1 `safe-autonomous`, Level 2 `approval-required`, Level 3 `prohibited`. Level 1 actions are `safe_autonomous_actions` (§3.3) and Level 2 actions are `approval_required_actions` (§3.2). Level 3 is defined by exclusion — any action that is neither Level 1 nor an approved Level 2 action — and so is recorded as `prohibited_actions: {defined_by: exclusion}` rather than an enumerated token set.

# 4. Top-Level Workspace Folder Structure

Setup scaffolds this structure in the user's workspace (final layout confirmed
in Phase G):

```text
/[workspace]
  /governance
  /workflows
  /memory
  /logs
  /templates
  /docs
  /outputs
  /inbox
    /processed
  /archive
```

`/outputs` is the root-level home for **standalone workflow deliverables** —
artifacts that are not configs, definitions, memory, or logs. It sits at the
root because deliverables are user-facing, not system plumbing. Rules:

```text
- §14.8 classification: /outputs is DATA — never touched by a plugin update.
  Writing a new file there is Level 1 safe-autonomous (§3.3); modifying or
  archiving an existing output follows the normal §3 rules.
- Naming: [slug]-<date>, with the appropriate extension for the artifact
  type (§29) — for example /outputs/weekly-review-2026-07-22.html.
```

# 6. Global Files

During setup, the `setup-openaos` skill should create these global files when
authorized (the foundation; use-case workflows are added only by the builder
interview):

```text
/governance/governance.md
/governance/workflow-router.md
/memory/user-profile.md
/memory/preferences.md
/memory/people.md
/memory/decisions.md
/logs/decision-log.md
/logs/change-log.md
/logs/feedback-log.md
/workflows/daily-startup.md
/workflows/end-of-day.md
/workflows/weekly-review.md
/workflows/monthly-review.md
/workflows/feedback.md
/templates/decision-entry-template.md
/templates/approval-request-template.md
/templates/memory-entry-template.md
/templates/daily-startup-report-template.html
/templates/end-of-day-carryover-template.html
/templates/weekly-review-report-template.html
/templates/monthly-review-report-template.html
/templates/inbox-triage-report-template.html
/templates/organizer-report-template.html
/templates/learning-assistant-report-template.html
/docs/user-guide.html
```

# 7A. Workflow Catalog

*(Cut to Minimal in Phase B; renamed in Phase C, repopulated in Phases D–E.)*

The catalog data file (`workflow-catalog.yaml`) is the structured registry of workflow identity and
ownership data, extracted from this specification for machine enforcement.
The five §17 governance workflows are entries of `kind: governance` (added in
Phase D); the predefined use-case workflows are added as `kind: use-case`
entries in Phase E. Mechanical
validation keeps: domain existence against the vocabulary (V1) and pairwise
disjointness of owned domains (V3) and owned artifacts (V4); validators must
not require a non-empty roster. The DDD relationship vocabulary, typed
collaboration edges, and their validator checks (V2, V5, V14) are removed.

---

# 7B. Use-Case Workflow Specs

The five predefined use-case workflows are the value spine of OpenAOS. None
is ever scaffolded generically: each is authored into the user's workspace by
the `build-workflow` engine's **instantiate** mode (Section 12), driven by
that use case's builder spec.

| Workflow (slug) | Purpose |
|---|---|
| Inbox triage (`inbox-triage`) | Classify, route, and act on inbox items |
| Research assistant (`research-assistant`) | Scoped, source-disciplined research |
| Writing assistant (`writing-assistant`) | Drafting/editing keyed to the user's voice |
| Learning assistant (`learning-assistant`) | Guided learning with understanding checks |
| File organizer (`organizer`) | File cleanup — inbox triage for files |

## 7B.1 Builder Spec Files

Each use case has one builder spec at
`design-spec/workflow-specs/[slug]/spec.md` (file_type `workflow_spec`).
Builder specs are design-time source artifacts, versioned with the spec and
shipped inside the plugin for the instantiate mode to consume. Ordered
section skeleton (enumerated as `workflow_spec` in
`design-spec/file-skeletons.yaml`):

```text
## Purpose                    what the workflow is for; who benefits
## Situation Interview        the §7B.2 question script — elicits the user's
                              real context so the result is tailored
## Baked-In Best Practices    the use-case-specific techniques the generated
                              workflow encodes by default (§12 contract, b)
## Default Skeleton           use-case guidance for each §16.3 workflow
                              section, adapted per interview answers
## Notes                      constraints, common pitfalls, refinement hints
```

## 7B.2 Interview Script Schema

Interview questions (here and in `setup-interview.md`) use this YAML question
schema, carried over from 2.x:

```yaml
- id: kebab-case-question-id
  ask: The question, phrased for a non-technical user.
  type: choice | text
  options: [only for choice]
  default: a sensible default, or none
  skippable: yes | no
  when: always | condition
  captures: what the answer feeds in the generated workflow
```

Scripts are short (roughly four to eight questions), ask about the user's
situation rather than about AI, and every answer must visibly shape the
generated workflow — a question whose answer changes nothing is removed.

---

# 8. Plugin Skills and Setup Flow

OpenAOS ships exactly three skills. Skills are plugin-owned machinery
(Core Model): identical for every user, changed only by plugin updates,
never user-refinable. Everything user-owned is a workflow.

```text
setup-openaos    — scaffolds the foundation and presents the use-case menu
build-workflow   — the builder engine (Section 12): one engine, two modes
refine-workflow  — the refinement engine (Section 13)
```

## 8.1 The setup-openaos Flow

Run once after install (and re-runnable safely — 8.2):

```text
1. Welcome & interview — display the welcome message, wait for the user to
   type exactly Proceed to acknowledge it, then run the setup interview
   (design-spec/setup-interview.md is the source definition). This
   acknowledgment gate is separate from, and does not replace, the §3.1
   write gate at step 3: it gates only the start of the interview, and no
   file is created by passing it.
2. Preview the scaffold — list every folder (§4) and file (§6) that will be
   created, explicitly noting that nothing exists yet and nothing is
   overwritten.
3. Create on Proceed — scaffold the §4 folders and §6 files, shipping the
   plugin's `content/` verbatim: governance.md per §16.1 (including the
   shipped "Output reports render as HTML" Local Rule); workflow-router.md
   per §16.11, carrying the five governance rows; the five governance
   workflows per §17 and the §16.3 schema; memory and log data files created
   empty (or seeded from
   the interview — never fabricated); the §18 templates — the three
   interaction templates (§18.3, §18.5, §18.6) plus all seven §18.2 HTML
   report templates (the four governance ones plus inbox-triage, organizer,
   and learning-assistant, shipped upfront regardless of which use cases are
   selected in step 4); /CLAUDE.md and /AGENTS.md per §16.10; the User Guide
   generated per §16.6. Log setup to /logs/change-log.md.
4. Use-case menu — present the five §7B use cases plus the design-new
   option, and hand off to build-workflow for each selection. Zero
   selections is valid: every use-case workflow is interview-authored, so
   nothing generic is ever scaffolded.
5. Schedule the rhythms — create scheduled runs for the cadences the
   rhythm-optin answer selected, using the default times: daily-startup each
   weekday 04:00, end-of-day each weekday 16:30, weekly-review Fridays 12:00,
   monthly-review the first Tuesday of each month 12:00. Defaults only —
   the user may change any time, and declining scheduling never uninstalls a
   governance workflow (§16.1). Scheduling creates no definition file and so
   does not engage the §14.8 drift invariant.
6. Generate and show the User Guide — write /docs/user-guide.html from the
   §16.6 template, listing what was actually installed (never the full
   catalog), and open it for the user.
7. Close — confirm setup is complete and direct the user to the User Guide
   for sample commands; show where things live, how to run a workflow, how
   to refine one, and how to send feedback (§17.5).
```

## 8.2 Re-Run Behavior

Setup is non-destructive and idempotent: on a re-run it detects the existing
foundation, never overwrites a data file (§14.8), and offers only to create
what is missing — each creation previewed and `Proceed`-gated. Repairing or
updating an existing definition file is `refine-workflow`'s or the plugin
update's job (§14.4), not setup's.

---

# 9. (Removed — merged into Section 8)

*(2.x build-flow content cut in Phase B; see Section 8.)*

---

# 12. The build-workflow Engine

The `build-workflow` skill is the one builder engine: a guided interview that
co-designs a tailored, best-practice workflow with the user. One engine, two
modes:

```text
- instantiate  — build one of the five predefined use cases (§7B), driven by
                 that use case's builder spec.
- design-new   — co-author a brand-new, domain-specific workflow from the
                 user's own activity, driven by the §12.3 pattern library.
```

Both modes produce the same thing: a user-owned workflow file at
`/workflows/[slug].md`, conforming to the §16.3 workflow schema and §15.3
frontmatter, written only on exact `Proceed`, and refinable afterward via
`refine-workflow` — a design-new workflow is indistinguishable from an
instantiated one.

## 12.1 Builder-Interview Contract

Every builder interview, in either mode, is defined by three elements:

**(a) Situation elicitation.** Questions (§7B.2 schema) that surface the
user's real context — their material, their volume, what "good" looks like,
where mistakes are costly — so the workflow is tailored, not generic. The
engine never asks the user about AI techniques; it asks about their
situation and applies the techniques itself. Elicitation also reads
`/memory/user-profile.md` where it exists, including any work-platform
preference (§20.1). The platform informs the **wording** of generated steps —
naming the user's own tools rather than generic ones — and nothing else: it
selects no branch, changes no step sequence, and never causes a workflow to
assume a live connection to that platform exists.

**(b) Baked-in best practices.** The techniques the generated workflow
encodes by default: in instantiate mode, the use case's Baked-In Best
Practices section (§7B.1); in design-new mode, patterns selected from the
§12.3 library. Best practices are defaults the user benefits from without
knowing they exist; the interview may tune them but never silently drops a
safety-relevant one (anything protecting the §3 rules).

**(c) Token-efficiency as a secondary guideline.** Generated workflows avoid
needless context re-reading and process material in sensible passes — but
this never gates authoring and never compromises workflow quality.
Delivering maximum user value is primary; token efficiency is a secondary
consideration only.

## 12.2 Engine Flow (both modes)

```text
1. Elicit    — run the situation interview ((a) above; in design-new mode,
               the §12.4 activity elicitation).
2. Propose   — present the proposed workflow structure in plain language:
               what it will do, the steps, where it will pause for approval.
               Iterate with the user until it fits.
3. Preview   — show the complete drafted workflow file.
4. Write on Proceed — write /workflows/[slug].md only when the user types
               exactly Proceed (§3.1); anything short is a hold. Append the
               workflow's row to /governance/workflow-router.md (§16.11) on
               the same Proceed. Log the creation to /logs/change-log.md.
5. Hand off  — offer a first run, and name refine-workflow as the way to
               adjust it later.
```

Guardrails: the engine writes exactly one new workflow file, its router row,
and its log entry per build — it never edits other workflows or memory as a
side effect (§14.8).

**The router exception (3.2).** Appending the workflow's row to
`/governance/workflow-router.md` is the one governance-file write
build-workflow is authorized to make. It is narrow by construction: append a
single new row, never edit or remove an existing one, never touch any other
part of the file or any other file under `/governance/`. The write is Level 1
(§3.3 — appending to a file, creating nothing destructive) and rides the same
`Proceed` that writes the workflow. The exception exists because trigger
authority now lives only in the router (§16.3): a workflow written without its
row is unreachable, so the row is part of creating the workflow, not a side
effect of it. A build that produced a workflow file but no row would be
incomplete (§27).

The other exception is §12.5: when
the report-output condition is met, the build also writes one new
`/templates/[slug]-report-template.html` (design-new mode only —
instantiate mode's use-case templates are already shipped at setup, §8.1,
and are referenced, never (re)written). A build that would overwrite an
existing workflow file is Level 2 twice over: it requires the overwrite
approval *and* the engine recommends `refine-workflow` instead. Generated
workflows must carry their approval gates in the §16.3 Approval Gates
section, consistent with governance.md.

## 12.3 General AI-Pattern Library (design-new mode)

Design-new has no fixed use-case contract, so element (b) draws from this
library of general patterns, applied to whatever domain the user describes:

```text
- Task decomposition        — break the activity into small, checkable steps.
- Checkpoint / confirm      — pause and confirm before consequential steps.
- Non-destructive by default— propose, copy, or append rather than change;
                              destructive steps go behind the Proceed gate.
- Capture-then-critique     — produce a draft, then critique and revise it
                              against the user's stated standard.
- Understanding checks      — verify comprehension before building on it.
- Source discipline         — separate what the source says from what is
                              inferred; cite; never fabricate.
- Batch similar items       — group like items and process them in one pass.
- Classify before acting    — decide what an item is before doing anything
                              to it.
```

The library is guidance, not a checklist: the engine applies the patterns
that fit the activity and omits the rest.

## 12.4 Design-New Mode

The design-new interview:

```text
1. Elicit the activity — what the user does, what "good" looks like, the
   steps they take today, the inputs and outputs, and where mistakes are
   costly.
2. Propose a workflow structure — apply the §12.3 patterns to the activity;
   explain the proposal in the user's own terms.
3. Preview the drafted workflow.
4. Write on Proceed — as a normal §16.3 workflow definition.
```

This is the capability that lets users bring AI into their own
value-creating work, not just the activities OpenAOS shipped with. Its
outputs are ordinary user-owned workflows: covered by the drift invariant
and refinable via `refine-workflow`.

## 12.5 Report-Output Scaffolding

One condition decides whether a workflow gets a fixed HTML report template
(§18.2):

```text
When the workflow's Outputs are a recurring, structured, user-facing
report — the same shape every run, meant to be read as a summary — it gets
a matching /templates/[slug]-report-template.html (embedding the §18.1
canonical CSS verbatim), Outputs/Steps wired to it, and an
/outputs/[slug]-<date>.html path. This is the default; an explicit opt-out
is offered for a genuinely one-off workflow.

When Outputs are free-form content (prose, drafted messages) or a shape the
user selects per run (a research brief vs. a comparison table), no
template — the workflow's Outputs section says so in plain language
instead.
```

The condition is already decided for every **instantiate**-mode use case:
inbox-triage, organizer, and learning-assistant meet it; research-assistant
and writing-assistant do not (§18.2 table). Their three fixed templates are
shipped once, upfront, by **setup-openaos** (§8.1) alongside the four
governance templates — not scaffolded per build — so instantiating one of
these use cases only wires the workflow's Outputs/Steps to the
already-shipped template; it never writes a template file (§12.2
guardrails). In **design-new** mode there is no pre-shipped template to
point at, so the engine applies the condition itself during Propose: when
met, it writes the one new `/templates/[slug]-report-template.html` as part
of that build (the §12.2 exception) and wires Outputs/Steps to it; when not
met, or when the user opts out, it writes none.

---

# 13. The refine-workflow Engine

The `refine-workflow` skill is the one sanctioned way a workflow definition
changes in place (§14.8). It is the same collaborative interview style as
`build-workflow`, pointed at an existing workflow instead of a blank one:
read it, ask what's not working, preview a diff, rewrite on `Proceed`.

Refinement is generic — one engine for every workflow in `/workflows`,
whether it began as an instantiated use case, a design-new original, or a
governance workflow (within the §13.3 limits). It never needs to know how
the workflow was built: the workflow file itself is the whole input.

## 13.1 Refinement Interview

```text
1. Select & read — identify the target workflow file; read it in full and
   restate, in plain language, what it currently does.
2. Elicit the friction — ask what's not working, in situation terms: where
   the workflow's output disappoints, where it asks too much or too little,
   what changed in the user's situation. Recent run evidence (log entries,
   outputs) may be offered as prompts, never as accusations.
3. Propose the change — describe the smallest revision that fixes the
   friction, in the user's terms, and name anything the change trades away.
   The §12.1 contract applies to the revision: tailored to the situation,
   best practices kept, token efficiency secondary.
4. Preview a diff — show current vs. proposed, marked so a non-technical
   user can see exactly what changes and what stays.
5. Rewrite on Proceed — apply the revision only when the user types exactly
   Proceed; anything short is a hold, and a hold leaves the file untouched.
   Update last_updated, and log the refinement to /logs/change-log.md.
```

## 13.2 Refinement Rules

```text
- One workflow per session: a refinement session edits exactly one workflow
  definition file, its row in /governance/workflow-router.md when that row's
  triggers change, plus its change-log entry — nothing else (§14.8).
- Triggers live in the router: when a refinement changes when the workflow
  should run — a new cadence, a widened or narrowed scope, a rename — the
  matching router row (§16.11) is updated in the same session and shown in
  the same previewed diff, so the user approves the workflow and its triggers
  together. A refinement that changes only how the workflow works leaves the
  row untouched. Editing that one row is the only governance-file write this
  skill makes; rows for other workflows are never touched.
- Smallest change that works: prefer revising the flagged sections over
  wholesale rewrites; a rewrite is proposed only when the user's situation
  has genuinely outgrown the structure, and is named as such in the preview.
- Approval gates are load-bearing: a refinement may add or tune approval
  gates, but a change that removes or weakens one must be called out
  explicitly in the preview — never buried in a larger diff.
- No silent scope creep: if the friction points at a different activity than
  the workflow covers, recommend build-workflow (design-new) for the new
  activity instead of stretching this one.
- Refinement targets workflows: governance.md Local Rules changes and
  template changes follow the same preview-diff-Proceed pattern, but the
  skill's scope is /workflows files.
```

## 13.3 Refining Governance Workflows

Governance workflows are refinable like any other — cadence, inputs, output
shape, and emphasis may all be tailored — within the §16.1 non-removable
boundary: a refinement must not delete a governance workflow, remove its
approval gates, bypass the §17.5 scrub-preview-Proceed sequence, or weaken
the §3 rules it enforces. A requested change that would cross that boundary
is declined with the reason, and the nearest compliant alternative is
offered.

## 13.4 Batch Refinement Mode

The §13.2 default — one workflow per session — covers the common case: a
single workflow's friction. It does not fit a cross-cutting policy change
that touches many workflows plus governance.md at once (for example,
standardizing report output across every report-producing workflow). Batch
mode is the sanctioned exception, not a replacement for the default:

```text
1. Elicit upfront — which workflows are in scope, how to backfill any
   workflow not yet conforming to the new policy, and (when relevant) the
   shared structure being introduced (e.g., a template family). One
   elicitation covers the whole batch, not one per file.
2. Propose one consolidated diff — every affected file's change, shown
   together, so the user reviews the policy change once rather than
   file-by-file.
3. Rewrite on a single Proceed — one exact-word approval authorizes the
   whole consolidated diff. Anything short of it leaves every file
   untouched.
4. Log per file — each changed file still gets its own dated Change Notes
   / change-log entry (§14.8); batching the approval never batches the
   audit trail.
```

Every §13.2 rule still applies per file (approval gates stay load-bearing,
governance workflows stay within the §13.3 boundary); batch mode changes
only how the interview and the approval gate are structured, not what is
allowed to change.

---

# 14. Versioning and Update Policy

## 14.1 Single Version Track

The specification and everything generated from it share one version fact —
`openaos_version`.
There is no separate catalog version and no per-instance version track.
`check-spec-version.py` enforces that all design-spec files agree on the
single version.

## 14.2 Per-File Version Metadata

Each generated definition file should record, in its YAML frontmatter, the `openaos_version` it was rendered from.

Example:

```yaml
---
title: Weekly Review Workflow
openaos_version: 1.0.5
last_updated: 2026-06-11
---
```

## 14.4 Update Modes

The only update path is a **plugin update** (§28). It has exactly two
surfaces, split by the §14.8 classification:

```text
- Plugin-owned machinery (skills, packaged specs and templates inside the
  plugin) — replaced wholesale by the update; the user's workspace is not
  touched by this replacement.
- Workspace definition files (governance config, governance workflows,
  templates, the User Guide projection) — the update may PROPOSE revisions:
  each changed file is previewed as a diff and applied only on Proceed,
  file by file. A declined proposal leaves the file as it is.
- Workspace data files — never touched by an update, without exception.
```

User-authored use-case and design-new workflows are never force-updated: an
update may at most suggest a refinement session. There is no downgrade
machinery; recovering an older state is a user-level file operation.

## 14.8 Definition Files, Data Files, and the Drift Invariant

A user's workspace is a living system: its files change after setup. To keep that change controllable, every file in the workspace is one of two kinds.

**Definition file.** A file that defines behavior: workflow definitions in `/workflows`, the governance config, the workflow router (§16.11), and templates in `/templates`. Use-case workflows are interview-authored and tailored, so definition files are not all spec-renderings — but they change only through sanctioned paths: the builder interview (creation, §12), the refinement interview (`refine-workflow`, §13 — the one sanctioned way a definition file changes in place), or a plugin update, each `Proceed`-gated. No workflow run edits a definition file as a side effect.

**Data file.** A file whose content accumulates from operation and the user's input. *Test: regenerating this file would destroy information the user relies on.* Data files are created once at setup (empty or seeded) and never overwritten by a plugin update; workflows append to and maintain them under the normal non-destructive and approval rules (Sections 2.4, 3). Examples: everything in `/memory`, `/logs`, `/outputs`, `/inbox`, and `/archive`.

**Projections.** A regenerable view built from definitions plus named data inputs (for example the User Guide, Section 16.6) is treated as a **definition file** for update purposes (safe to regenerate), with its data inputs stored separately as data files.

**The drift invariant.** Workflow runs write data files; definition files change only via the sanctioned, `Proceed`-gated paths above. This bounds drift to data (which is supposed to grow) and keeps definitions deliberate, so an update or refinement is a clean, reviewed change rather than a three-way merge.

**Governance application.** Everything under `/governance/` — `governance.md` and `workflow-router.md` — and the five §17 governance workflows are definition files, with two extra rules: every governance change also appends a dated entry to governance.md's Change Notes and to `/logs/change-log.md` (§16.1), and the sanctioned paths may revise but never remove them — the governance layer itself is not removable (§16.1).

The router is the one governance file with sanctioned writers beyond `refine-workflow` and a plugin update: `build-workflow` appends a row per §12.2. This is a deliberate, bounded widening of the invariant, not an exception to it — a row is appended only as part of a `Proceed`-gated workflow creation, never by a workflow *run*, so definitions still change only deliberately.

---

# 15. YAML Frontmatter Standards

## 15.3 Other Generated Markdown File Frontmatter

All generated markdown files should include lightweight YAML frontmatter.

Example:

```yaml
---
title: Weekly Review Workflow
file_type: workflow
openaos_version: 1.0.5
created_date: 2026-06-02
last_updated: 2026-06-02
---
```

## 15.4 Controlled `file_type` Vocabulary

The controlled `file_type` tokens are `file_type` in `design-spec/vocabulary.yaml` (source of truth). The meaning of each type and its per-file assignments are normative here in the prose below.

`design_spec` applies to this design specification itself (`openaos-design-spec.md`), the source document OpenAOS is generated from. It is the one source/design artifact in the vocabulary; the other types all describe generated files.

`project_instructions` applies to the root project instruction files (`/CLAUDE.md` and `/AGENTS.md`) scaffolded at the workspace root (Section 16.10).

`change_log` applies to the workspace change log (`/logs/change-log.md`). `feedback_log` applies to the feedback staging log (`/logs/feedback-log.md`, Section 16.7) — a data file per Section 14.8.

File-type assignments by file:

```text
config        /governance/governance.md

router        /governance/workflow-router.md; the routing table that maps
              user prompts to workflow files (Section 16.11)

memory        /memory/user-profile.md, /memory/preferences.md,
              /memory/people.md, /memory/decisions.md

decision_log  /logs/decision-log.md

workflow      every file in /workflows (governance and use-case)

template      every file in /templates

documentation /docs/user-guide.html (HTML metadata is carried via meta
              tags or an HTML comment rather than YAML frontmatter)

project_instructions
              /CLAUDE.md and /AGENTS.md (workspace root)

catalog       design-spec/workflow-catalog.yaml; see Section 7A

interview_script
              design-spec/setup-interview.md; the setup interview script

workflow_spec design-spec/workflow-specs/[slug]/spec.md; the use-case
              builder specs (Section 7B.1)
```

## 15.5 Controlled Status Vocabulary

The controlled `status` tokens (file, template, workflow, or other artifact) are `status` in `design-spec/vocabulary.yaml` (source of truth): `draft`, `active`, `deprecated`, `archived`. The 2.x `agent_status` lifecycle vocabulary is removed.

The controlled `status` values govern generated files. This design specification itself (file_type `design_spec`) is a source/design artifact, not a generated file, and its `status` field tracks design-phase lifecycle; it is exempt from the controlled artifact-status values.

Casing: in YAML frontmatter, the `status` field must use the lowercase controlled values. Display tables and prose may use human-readable capitalized forms (for example, `Active`) for readability.

## 15.6 Date Format

All frontmatter dates should use ISO format:

```text
YYYY-MM-DD
```

Use timestamps only when there is a specific need to track time of day.

---

# 16. Generated File Schemas by File Type

## 16.1 Governance Config Schema

`/governance/governance.md` (file_type `config`) is the single standing-rules
file of the workspace: the `Proceed` safety gate, the permission model, memory
boundaries, and escalation-to-user rules, in one place. Standing rules live
here; runnable procedures are workflows (Section 17). It folds together the
load-bearing rules of the 2.x Security and Memory agents and the 2.x global
permissions seed (old §16.11) — the coverage of that fold is verified by the
Phase D governance coverage table.

Canonical body: `design-spec/content/governance/governance.md`; this section
is its contract (meaning, governing rule, and the `vocabulary.yaml`
action-list linkage). The plugin copy is byte-identical (§28.1, §18.7).

Generation rules:

```text
- governance.md restates nothing the spec does not say: its Proceed Gate
  section renders §3.1, its Permission Model section renders §3.2–§3.4 (the
  action lists come from vocabulary.yaml, the source of truth), its Memory
  section renders §20.2–§20.3, its Workflows section renders the §14.8/§13
  rule that `/workflows` files change only via refine-workflow or a plugin
  update, its Logs section renders the §19 append-only rule for `/logs`, and
  its Escalation section renders the §3 escalation-to-user rules.
  Workspace-specific tightening (never loosening) is recorded in the Local
  Rules section, not by editing the rendered sections.
- Tools and integrations follow a default-deny rule: a tool or integration
  the user has not explicitly approved is treated as approval-required
  (Level 2) the first time a workflow wants to use it; the grant is recorded
  in Local Rules with a dated Change Notes entry.
- governance.md is a definition file (§14.8): it changes only via a
  `Proceed`-gated refinement or a plugin update, and every change appends a
  dated entry to its Change Notes section and to /logs/change-log.md.
- The governance layer is not removable: setup always installs everything
  under `/governance/` — this file and the §16.11 workflow router — plus the
  five §17 governance workflows, and no sanctioned path deletes or disables
  them. Removing the router would leave every workflow unreachable, so it
  sits inside the boundary rather than beside it.
- Setup ships one Local Rule by default, "Output reports render as HTML":
  the daily-startup, weekly-review, monthly-review, and end-of-day reports,
  plus the inbox-triage, organizer, and learning-assistant reports when
  those use-case workflows are built, render as HTML per §18.2, saved to
  `/outputs` as a `.html` file; logs and memory are unaffected and stay
  markdown. It is recorded as a dated Local Rules entry (with its own Change
  Notes entry) like any other shipped default — not silently assumed.
```

Frontmatter (§15.3) plus this ordered section skeleton (enumerated as
`governance_config` in `design-spec/file-skeletons.yaml`):

```markdown
---
title: Governance
file_type: config
openaos_version: [version]
created_date: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: active
---
# Governance

## Purpose
[what this file is; standing rules vs. runnable workflows]

## The Proceed Gate
[§3.1 rendered: the protected actions, the five-element approval request,
the exact-word rule — anything short of the exact word `Proceed` is a hold]

## Permission Model
[§3.2–§3.4 rendered: the three levels; the Level 1 and Level 2 action lists
from vocabulary.yaml; Level 3 defined by exclusion; the tool/integration
default-deny rule]

## Memory
[§20.2–§20.3 rendered: the four memory files and their scopes; what is
memory-worthy; sensitive entries require explicit approval]

## Workflows
[workflow files in /workflows change only via refine-workflow or a plugin
update, never as a side effect of running one]

## Logs
[logs in /logs accumulate under these rules and are never regenerated or
overwritten]

## Escalation to the User
[when a workflow must stop and ask: approval-required actions, ambiguity
with material consequences, external communication, publishing, spending,
sensitive information, or irreversible changes; failed actions are reported
when relevant and logged when they affect future behavior]

## Local Rules
[workspace-specific tightening the user has approved; ships with one default
entry, "Output reports render as HTML" (see generation rules above)]

## Change Notes

### YYYY-MM-DD — [change]
[dated, append-only record of every governance change]
```

## 16.2 Memory File Schema

Memory files should follow:

```markdown
# [Memory Name]

## Purpose

## Scope

## What Belongs Here

## What Does Not Belong Here

## Memory Entries

## Review / Cleanup Notes
```

Entries under `## Memory Entries` use this dated entry block — the seven §20.3 fields, embedded by `/templates/memory-entry-template.md` (§18.6):

```markdown
### YYYY-MM-DD — [Entry Title]

**Type:** [preference | fact | decision | person | project | learning]
**Summary:**
**Source:**
**Confidence:** [high | medium | low]
**Owner:** [workflow or user]
**Review Date:** YYYY-MM-DD
**Notes:**
```

## 16.3 Workflow File Schema

Canonical bodies of the five governance workflows:
`design-spec/content/workflows/*.md`; this section and §17.1–§17.5 are their
contract (meaning and governing rule). The plugin copies are byte-identical
(§28.1, §18.7).

**No `When to Use` section (3.2).** A workflow file states what it does, not
when to reach for it. Trigger authority belongs solely to the Workflow Router
(§16.11): a workflow's example prompts live in exactly one file, so there is
no second place to keep in sync and no incentive to load a workflow just to
find out whether it applies. Removing the section is what makes the router
authoritative rather than advisory.

Workflow files should follow:

```markdown
# [Workflow Name]

## Purpose

## Inputs

## Outputs

## Steps

## Decision Points

## Approval Gates

## Escalation Triggers

## Completion Criteria
```

## 16.4 Template File Schema

Template files should follow:

```markdown
# [Template Name]

## Purpose

## When to Use

## Template

## Completion Checklist

## Notes
```

## 16.5 Decision Log Schema

Decision logs should be append-only, with newest entries at the top.

```markdown
# [Decision Log Name]

## Log Rules

- Add newest entries at the top.
- Do not delete prior entries.
- Corrections should be added as new entries.
- Do not silently rewrite history.

## Entries

### YYYY-MM-DD — [Decision Title]

**Decision:**  
**Context:**  
**Reasoning:**  
**Approved By:**  
**Impacted Files:**  
**Follow-Up Needed:**  
```

## 16.6 User Guide Schema

`/docs/user-guide.html` (file_type `documentation`) is the workspace's
plain-language manual, written for a non-technical reader. It is a §14.8
**projection**: regenerated from the current definitions (governance config,
installed workflows) plus one data input — its embedded change log — which is
preserved verbatim across regenerations. It is generated at setup (§8.1),
regenerated by the monthly review (§17.4), and may be regenerated after any
build or refinement.

Generation rules (normative):

```text
- Linked table of contents is mandatory; every TOC entry resolves to an
  anchor in the document and every section anchor appears in the TOC.
- The embedded change log is newest-on-top and carried forward unchanged;
  regeneration appends its own entry.
- The safety section must state the exact-command contrast: `Proceed` is the
  only exact-word command in the system; everything else is conversation.
- The guide documents what is actually installed — it lists the user's real
  workflows by name, not the hypothetical roster.
```

Content sections, in order: What OpenAOS Is; Your Workflows (the installed
list); Building a Workflow (the §12 modes, in user terms); Refining a
Workflow (§13); The Proceed Gate and Safety Model (§3, §16.1); Governance
Rhythms (§17); Memory and What Gets Remembered (§20); Sending Feedback
(§17.5); Change Log.

Canonical body: `design-spec/content/templates/user-guide-template.html`;
this section is its contract. The packaged template is
`content/templates/user-guide-template.html` in the plugin, a byte-identical
copy (§28.1, §18.7).

## 16.7 Feedback Log Schema

The feedback staging log (`/logs/feedback-log.md`, file_type `feedback_log`, §15.4) — a **data file** per §14.8: created once (empty) at setup, never overwritten by a plugin update, appended by the feedback workflow. Staged entries work offline; nothing leaves the machine without scrubbing and `Proceed`.

```markdown
---
title: Feedback Log
file_type: feedback_log
---
# Feedback Log

## Log Rules

- Append-only; entries are never deleted (mark discarded instead).
- Every outbound send requires the feedback workflow's scrub step + Proceed (§3.2).

## Entries

### YYYY-MM-DD — [Title]

**Type:** bug | enhancement
**Status:** captured | staged | sent | discarded
**Scrub:** pending | done (date)
**Summary:** [what was observed or proposed, scrubbed of names, file
content, and memory quotes before send]
**Sent:** date | —
```

## 16.8 Change Log Entry Schema

Entries in `/logs/change-log.md` (file_type `change_log`, a data file per §14.8) use this schema:

```markdown
### YYYY-MM-DD — [Change Title]

**Change:** [what changed]
**Made By:** [workflow, refinement interview, plugin update, or user]
**Files Affected:** [paths]
```

## 16.10 Workspace-Root Scaffold Files

Setup provisions `/CLAUDE.md` and `/AGENTS.md` (file_type
`project_instructions`) at the workspace root from the plugin's
`content/root/` (§28), non-destructively: if either file already exists, setup
never overwrites it — it proposes the OpenAOS block as an addition, applied
only on `Proceed`.

```text
/CLAUDE.md  — session entry point: names the workspace as an OpenAOS
              workspace and includes /AGENTS.md.
/AGENTS.md  — standing instructions for any AI agent in the workspace:
              read /governance/governance.md before consequential actions;
              the Proceed gate summary (exact word, anything short is a
              hold); the governance layer is not removable; workflows live
              in /workflows and change only via refine-workflow or a plugin
              update; and a Workflow routing section importing
              @governance/workflow-router.md (§16.11).
```

The routing import is what makes the router load at session start: CLAUDE.md
imports AGENTS.md, AGENTS.md imports the router. Agents therefore arrive with
the routing table but *not* with any workflow body — the point of the pattern.

**Imports use the relative form, never a leading slash.** Write
`@governance/workflow-router.md`, not `@/governance/workflow-router.md`. An
`@path` import resolves relative to the file containing it; a leading slash
makes the path absolute and resolves it against the *filesystem* root, not the
workspace root, so the import silently loads nothing. The failure is invisible
— no error is raised, and an agent that reads the file on demand later still
appears to work — which makes it worth stating here and checking mechanically
(§18.7, VC13). The same rule applies to every `@path` in a root scaffold, not
just the router.

These files carry pointers, not rules: the standing rules live in
governance.md (§16.1), so the root files stay small and stable.

Canonical bodies: `design-spec/content/root/{CLAUDE.md,AGENTS.md}`; this
section is their contract (the required anchors checked by §18.7). The plugin
copies live at `content/root/` and are byte-identical (§28.1).

**Content→workspace mapping exception.** Every other `content/X` in the
plugin maps to workspace `/X`. `content/root/` maps to the workspace **root**
(`/`), not `/root` — the setup behavior described above. This is the one
place the `content/X → /X` model does not hold; it is recorded here and in
`setup-openaos` so it is not mistaken for drift.

## 16.11 Workflow Router Schema

`/governance/workflow-router.md` (file_type `router`) is the routing table an
agent consults to decide which workflow to load. It exists so that answering
"which workflow is this?" costs one small file rather than every workflow file
in `/workflows`. It is loaded at session start through the §16.10 import chain
(`/CLAUDE.md` → `/AGENTS.md` → the router), so routing is available before the
first prompt is read.

```markdown
# Workflow Router

## Purpose

## Routes
```

**Format.** `Routes` is a two-column markdown table — `Example Prompts` and
`File to Load`, one row per workflow. Markdown table over YAML or JSON: the
data is flat and uniform, and a table carries the least structural overhead
per row of the three, which matters for a file loaded into every session.

```text
| Example Prompts | File to Load |
|---|---|
| "run my daily startup", "start my day" | /workflows/daily-startup.md |
```

**Matching rule (stated in the file's own Purpose section, for the agent that
reads it).** The prompts are illustrative, not exact commands: match on
meaning, load the single most likely workflow, and ask the user for
clarification when nothing matches — never guess, and never load several
workflows to compare them.

**Ownership.** Scaffolded by `setup-openaos` with the five §17 governance
rows. `build-workflow` appends a row when it creates a workflow (§12.2);
`refine-workflow` updates a row when triggers change (§13.2). Those two skills
are the only sanctioned writers, matching the §14.8 rule for workflow
definitions themselves. The router is a `/governance/*` file and is therefore
part of the non-removable governance layer (§17).

Canonical body: `design-spec/content/governance/workflow-router.md`; this
section is its contract. The plugin copy is byte-identical (§28.1, §18.7).

---

# 17. Governance Workflows

Every workspace includes exactly five governance workflows, scaffolded at
setup (Section 6) and defined here. They are the runnable half of governance:
`/governance/governance.md` (§16.1) holds the standing rules; these workflows
carry the operating rhythms and the feedback channel. They absorb the
load-bearing content of the 2.x operating rhythms (old Section 25) and the
2.x Review and Feedback agents.

Canonical bodies: `design-spec/content/workflows/{daily-startup,end-of-day,
weekly-review,monthly-review,feedback}.md`; §17.1–§17.5 are their contract
(purpose, review question, inputs/outputs, and governing rule). The plugin
copies are byte-identical (§28.1, §18.7).

Common rules:

```text
- Each file follows the §16.3 workflow schema and lives at the path listed in
  file-skeletons.yaml `workflows:` (source of truth for the enumerable
  fields: paths, purposes, review questions, and the startup-brief
  categories).
- Governance workflows are definition files (§14.8) and part of the
  non-removable governance layer (§16.1): a plugin update may revise them,
  and refinement may tailor their inputs and outputs, but no sanctioned path
  deletes them or removes their approval gates.
- Runs write data files only (logs, memory, outputs) under the normal §3
  rules; a governance workflow never edits a definition file as a side
  effect.
- Cadences are suggestions the user approves at setup (daily, daily,
  weekly, monthly); any run can also be invoked on demand.
- Each has a row in the §16.11 workflow router, shipped with the router at
  setup rather than authored per workspace. The rows are the only record of
  what invokes these workflows; the workflow files themselves carry no
  `When to Use` section (§16.3).
```

## 17.1 Daily Startup Workflow

`/workflows/daily-startup.md`. Review question: **What matters today?**

Help the user start the day by reviewing priorities, commitments, inbox
items, and recently processed inbox items. The run produces a startup brief
that opens with the four inbox `brief_categories` in file-skeletons.yaml, in
order — items processed, items still unresolved, where items were promoted
to, and items requiring user approval (Section 31) — and closes with two
further sections, "What matters today" (the review question) and
"Completion". The full ordered section list is the `html_report_daily_startup`
skeleton in file-skeletons.yaml. Rendered as HTML using
`/templates/daily-startup-report-template.html` (§18.2), saved to
`/outputs/daily-startup-<date>.html`.

## 17.2 End-of-Day Workflow

`/workflows/end-of-day.md`. Review question: **What changed today, and what
must not be lost?**

Capture what changed today, unresolved obligations, decisions made,
follow-ups needed, and next-day carryover. Decisions surfaced here are
recorded via the §18.3 decision entry template (staying markdown in
`/logs/decision-log.md` — logs are append-only, not reports); the carryover
note feeds the next daily startup, rendered as HTML using
`/templates/end-of-day-carryover-template.html` (§18.2), saved to
`/outputs/end-of-day-<date>.html`.

## 17.3 Weekly Review Workflow

`/workflows/weekly-review.md`. Review question: **What needs follow-up
soon?**

Review commitments, decisions, unresolved items, workflow performance, stale
memory signals, and next-week priorities. The weekly review keeps the
workspace operationally clean and prevents loose ends from becoming forgotten
obligations. Memory receives a lightweight review here (§20.3); items that
look stale are flagged for the monthly review, not silently changed. The
follow-up list is rendered as HTML using
`/templates/weekly-review-report-template.html` (§18.2), saved to
`/outputs/weekly-review-<date>.html`.

Workflow performance review is observational: if a workflow produced friction
this week, the run suggests a `refine-workflow` session (§13) — a
suggestion only, never an unprompted edit.

## 17.4 Monthly Review Workflow

`/workflows/monthly-review.md`. Review questions: **What is stale, misplaced,
or structurally messy? Is the whole system still aimed at the right goals?**

Review memory hygiene (the deeper §20.3 pass), workflow quality, permission
boundaries and tool grants (governance.md Local Rules and Change Notes),
structural clutter, and cleanup needs; and review whether the system is still
aimed at the right goals and whether the installed workflows still support
the user's priorities. The monthly review keeps the workspace structurally
healthy and aligned with larger goals, so it doesn't stay well-maintained but
aimed at outdated priorities. The health report is rendered as HTML using
`/templates/monthly-review-report-template.html` (§18.2), saved to
`/outputs/monthly-review-<date>.html`.

The monthly review also:

```text
- Regenerates the User Guide (/docs/user-guide.html, §16.6) as a projection,
  preserving its embedded change log. The User Guide stays HTML at its own
  fixed path and is unaffected by the §18.2 report templates.
- Runs the feedback self-examination: reviews recent friction, errors, and
  preferences for enhancement candidates and presents them for
  accept / edit / discard; accepted items enter the §17.5 feedback flow.
- May suggest building a use-case workflow for an observed gap, or refining
  or archiving one that no longer earns its place. Anti-nagging rule
  (normative): a declined suggestion is logged and not re-raised until the
  next monthly review or a material change in usage pattern. Archiving is
  Level 2 and never touches the governance layer.
```

## 17.5 Feedback Workflow

`/workflows/feedback.md`. The upstream feedback channel to the project team.

Flow (each step gates the next):

```text
1. Capture — record the bug report or suggestion as a feedback-log entry
   (§16.7), status `captured`.
2. Scrub — remove names, file contents, memory quotes, and anything
   identifying; keep only what the project team needs to act.
3. Preview — show the user exactly what would be sent, marked scrubbed.
4. Send on Proceed — email openaos@neoclarity.ai; anything short of the
   exact word is a hold. Record the outcome in the entry's Sent field.
5. Offline fallback — if sending is unavailable, stage the entry in
   /logs/feedback-log.md as `staged` and prompt the user to send manually.
```

Nothing leaves the machine without scrub + preview + `Proceed`. This is the
privacy boundary of the whole system and is not weakened by refinement.

---

# 18. Global Templates

Every generated AOS should include these global templates.

## 18.1 Canonical Report CSS

Every §18.2 HTML report template embeds this exact CSS block verbatim inside
its own `<style>` tag — one canonical palette and card system, so a style
update touches one place (this section) and is carried into every template
by copy, not by reference (§18.2's templates must open standalone, with no
external stylesheet, per the non-destructive/self-contained rule). Reports
are HTML; logs (`/logs/*.md`) and memory (`/memory/*.md`) are unaffected and
stay markdown.

```css
:root {
  --accent: #2563eb; --success: #16a34a; --warning: #d97706; --danger: #dc2626; --muted: #6b7280;
  --bg: #f8fafc; --card-bg: #ffffff; --border: #e2e8f0; --text: #1e293b;
}
body { font-family: system-ui, sans-serif; max-width: 46rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; color: var(--text); background: var(--bg); }
header.report-header { border-bottom: 2px solid var(--border); padding-bottom: 1rem; margin-bottom: 1.5rem; }
header.report-header h1 { margin: 0 0 0.25rem; font-size: 1.5rem; }
.question { color: var(--accent); font-weight: 600; margin: 0.25rem 0 0.5rem; }
.meta { color: var(--muted); font-size: 0.9rem; }
.meta span { margin-right: 1.25rem; }
.card { background: var(--card-bg); border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 8px; padding: 1rem 1.25rem; margin-bottom: 1rem; }
.card h2 { margin-top: 0; font-size: 1.05rem; }
.card.warn { border-left-color: var(--warning); }
.card.danger { border-left-color: var(--danger); }
.card.success { border-left-color: var(--success); }
.card.muted { border-left-color: var(--muted); }
.badge { display: inline-block; font-size: 0.75rem; font-weight: 600; padding: 0.15em 0.6em; border-radius: 999px; margin-left: 0.5em; }
.badge-warn { background: #fef3c7; color: #92400e; }
.badge-danger { background: #fee2e2; color: #991b1b; }
.badge-success { background: #dcfce7; color: #166534; }
p.none, li.none { color: var(--muted); font-style: italic; }
code { background: #f1f5f9; padding: 0.1em 0.35em; border-radius: 4px; font-size: 0.9em; }
table { border-collapse: collapse; width: 100%; }
th, td { text-align: left; padding: 0.35em 0.6em; border-bottom: 1px solid var(--border); font-size: 0.95em; }
footer { color: var(--muted); font-size: 0.85rem; margin-top: 2rem; border-top: 1px solid var(--border); padding-top: 1rem; }
```

Card color meaning (normative across every §18.2 template): `accent` /
unclassed = neutral or informational; `warn` = needs attention or a
proposal awaiting `Proceed`; `danger` = urgent, at-risk, or a governance
concern; `success` = completed or processed; `muted` = empty, flagged-only,
or declined. Empty sections render as `<p class="none">None.</p>` rather
than being omitted, so the fixed section order stays visible.

## 18.2 HTML Report Templates

Retires the 2.x `status-report-template.md`: every recurring, structured,
user-facing workflow report ships as a self-contained HTML file instead
(card layout, color-coded per §18.1, the §18.1 CSS embedded verbatim), so it
opens standalone in a browser with no external dependency. This is a
Local Rule shipped by default (§16.1) — the governance layer records it,
not this section alone.

Seven fixed templates ship in `content/templates/` (governance four +
end-of-day, plus the three use-case workflows whose output is a recurring
structured report rather than free-form content):

| Template file | Workflow | Rendered path |
|---|---|---|
| `daily-startup-report-template.html` | daily-startup (§17.1) | `/outputs/daily-startup-<date>.html` |
| `end-of-day-carryover-template.html` | end-of-day (§17.2) | `/outputs/end-of-day-<date>.html` |
| `weekly-review-report-template.html` | weekly-review (§17.3) | `/outputs/weekly-review-<date>.html` |
| `monthly-review-report-template.html` | monthly-review (§17.4) | `/outputs/monthly-review-<date>.html` |
| `inbox-triage-report-template.html` | inbox-triage (§7B) | `/outputs/inbox-triage-<date>-<run>.html` (inbox-triage may run more than once a day) |
| `organizer-report-template.html` | organizer (§7B) | `/outputs/organizer-<date>.html` |
| `learning-assistant-report-template.html` | learning-assistant (§7B) | `/outputs/learning-assistant-<date>.html` |

Each template's `<section class="card ...">` order matches its workflow's
Outputs section exactly (empty sections say "None", never omitted); a
`<!-- -->` comment block at the top of each file documents which section
maps to which workflow step and the card-color meaning for that template.
Two use-case workflows are deliberately excluded: research-assistant's
output shape is user-chosen at build time (§7B, no fixed template — see
its builder spec Notes), and writing-assistant's deliverable is prose, not
a structured report.

Canonical bodies: `design-spec/content/templates/*-report-template.html`;
this section is their contract (which template serves which workflow, the
rendered path, and the card-section order). The plugin copies are
byte-identical (§28.1, §18.7).

Generation rules:

```text
- setup-openaos ships all seven fixed templates into /templates at setup
  (§8.1) — the governance four plus inbox-triage, organizer, and
  learning-assistant — regardless of which use-case workflows the user
  actually builds that session; build-workflow's instantiate mode only
  wires the workflow's Outputs/Steps to the already-shipped file (§12.5),
  it never writes one.
- build-workflow's design-new mode is the one path that writes a new
  template file: when the §12.5 condition is met for a custom workflow, it
  scaffolds that workflow's own /templates/[slug]-report-template.html as
  part of the build.
- Every template is a definition file (§14.8): shipped or scaffolded fixed,
  updated only by a plugin update or (for a design-new template)
  refine-workflow — never hand-edited outside that.
```

## 18.3 Decision Entry Template

Create:

```text
/templates/decision-entry-template.md
```

Purpose:

```text
Provide a standard format for recording decisions in global or workflow-level decision logs.
```

This template embeds the §16.5 decision-log entry block; it defines no new schema of its own.

Canonical body: `design-spec/content/templates/decision-entry-template.md`;
this section is its contract. The plugin copy is byte-identical (§28.1, §18.7).

## 18.5 Approval Request Template

Create:

```text
/templates/approval-request-template.md
```

Purpose:

```text
Standardize how workflows ask the user to approve Level 2 actions requiring Proceed.
```

The request must explain the proposed action, affected files, reason, consequence, and ask the user to type exactly `Proceed`.

Body skeleton (the five §3.1 elements as labeled fields):

```markdown
**Proposed Action:**
**Affected Files:**
**Reason:**
**Consequence:**
**Approval:** type exactly `Proceed` to authorize
```

Canonical body: `design-spec/content/templates/approval-request-template.md`;
this section is its contract. The plugin copy is byte-identical (§28.1, §18.7).

## 18.6 Memory Entry Template

Create:

```text
/templates/memory-entry-template.md
```

Purpose:

```text
Standardize how important preferences, facts, decisions, people, projects, and workflow learnings are recorded.
```

This template embeds the §16.2 dated memory entry block (the seven §20.3 fields); it defines no new schema of its own.

Canonical body: `design-spec/content/templates/memory-entry-template.md`;
this section is its contract. The plugin copy is byte-identical (§28.1, §18.7).

## 18.7 Content Source Validation

The files under `design-spec/content/` are the canonical bodies of everything
the plugin ships verbatim (§35), and they are meant to be **hand-edited
directly**. Structural validation is therefore normative, not optional:
`scripts/validate-content.py` checks the criteria below, and it must pass
before a spec change or plugin regeneration is considered complete (§27, §34).

**All markdown templates** (governance, the §16.11 workflow router, the five
workflows, the three §18.3 / §18.5 / §18.6 interaction templates):

```text
- Valid YAML frontmatter carrying title, file_type, openaos_version,
  created_date, last_updated, status; file_type exists in vocabulary.yaml and
  matches the file's expected type; openaos_version is a valid version on the
  single track and never ahead of the current spec version (§14.2: a file
  records the version it was rendered from, so an unchanged file may lag).
- ## section headings present, non-empty, and in the exact order of the
  file's file-skeletons.yaml skeleton — none missing, extra, empty, or
  reordered.
- Required in-section markers present where the skeleton's `required_markers`
  enumerates them (e.g. governance Permission Model must carry its Level 1 /
  Level 2 / Level 3 leads, which are bold leads rather than ### headings).
```

**governance.md specifically:**

```text
- Permission Model Level 1 and Level 2 action lists equal vocabulary.yaml —
  the consistency guard against the rendered text freezing out of date.
- The default "Output reports render as HTML" Local Rule is present (§16.1).
```

**workflow-router.md specifically:**

```text
- The Routes section carries the two-column table header, and every row's
  `File to Load` resolves to a real content/workflows/*.md file.
- Every shipped governance workflow has exactly one row — no workflow left
  unroutable, no row pointing at a workflow that does not exist.
- No workflow file carries a `When to Use` section (§16.3): trigger authority
  is the router's alone, so a second copy is drift by definition.
```

**Root scaffolds specifically:**

```text
- No `@path` import uses the absolute form (`@/...`): a leading slash
  resolves against the filesystem root rather than the workspace root, so the
  import silently loads nothing (§16.10, VC13).
- Every `@path` import resolves to a real file — either the sibling scaffold
  (`@AGENTS.md`) or a content source under design-spec/content/.
```

**Workflow files specifically:**

```text
- The Outputs section names a real content/templates/*-report-template.html
  file and an /outputs/[slug]-<date>.html path (report-producing workflows).
- Report section order matches the workflow's brief_categories in
  file-skeletons.yaml where those are defined.
```

**HTML templates** (the seven §18.2 reports plus the §16.6 user guide):

```text
- Parses as well-formed HTML and is self-contained: no external stylesheet,
  script, font, or image references and no CSS @import.
- The seven §18.2 reports embed the §18.1 canonical CSS verbatim; the §16.6
  user guide is a document, not a card report, so it carries its own embedded
  layout CSS instead.
- Report <section class="card …"> <h2> order equals the file's html_report_*
  sections list (a heading may trail a badge span); card classes drawn only
  from {accent or unclassed, warn, danger, success, muted}; the top-of-file
  <!-- --> mapping comment is present; empty sections use <p class="none">.
- The user guide's <h2> order equals its file-skeletons user_guide sections.
```

**Root scaffolds** (`content/root/CLAUDE.md`, `content/root/AGENTS.md`) — not
standard templates:

```text
- No YAML-frontmatter or section-skeleton check: they open with an HTML
  comment and carry pointers, not the §16.4 schema. Instead the §16.10
  required anchors are confirmed — CLAUDE.md names the workspace and includes
  @AGENTS.md; AGENTS.md contains the Proceed-gate summary, the
  governance-layer-not-removable statement, and the rule that workflows change
  only via refine-workflow or a plugin update. The anchor phrases are listed
  in file-skeletons.yaml `root_scaffold:`.
```

**Tree completeness:**

```text
- design-spec/content/ contains exactly the expected set of files — none
  missing, no orphans — and each has a byte-identical copy under the plugin's
  content/ (§28.1, §36.2 step 4).
- No live reference to the retired status-report-template.md. Historical
  records of the retirement itself (the governance Change Notes entry) are
  expected and exempt.
```

---

# 19. Logging Model

## 19.1 Global Logs

The workspace should maintain:

```text
/logs/decision-log.md
/logs/change-log.md
/logs/feedback-log.md
```

Global logs should capture:

```text
- System-wide decisions
- Major configuration changes
- Setup and workflow-authoring history
- Workflow changes
- Permission policy changes
```

## 19.3 Must-Log Categories

Workflows should log these events:

```text
- Important user preferences
- Configuration decisions
- Permission changes
- Files created
- Files modified with approval
- Workflows created or changed
- Important assumptions
- Errors or failed actions
```

Logs should not capture every trivial action. They should preserve decisions that affect future behavior.

---

# 20. Global Memory Files and Governance

## 20.1 Required Global Memory Files

Every workspace should include:

```text
/memory/user-profile.md
/memory/preferences.md
/memory/people.md
/memory/decisions.md
```

`/memory/user-profile.md` may carry a **work-platform preference** seeded by
the setup interview (§8.1 step 1) — the platform the user does most of their
work in. It is one instance of the general memory capture `memory-seeds`
already performs, pre-optioned because the answer is high-value and easy to
state. Its one consumer is `build-workflow` (§12.1(a)), which reads it during
situation elicitation. The user may change or clear it like any other memory
entry.

## 20.2 Memory File Boundaries

```text
/memory/user-profile.md
Stores durable, user-approved facts about the user that help OpenAOS personalize assistance. Avoid sensitive personal attributes unless explicitly approved.

/memory/preferences.md
Stores durable user preferences about communication style, workflows, defaults, formatting, decision-making, tools, and collaboration.

/memory/people.md
Stores relevant people, roles, relationship context, communication preferences, and collaboration notes. Avoid sensitive personal details unless explicitly approved.

/memory/decisions.md
Captures durable decisions that affect future behavior, user preferences, permissions, workflows, and defaults. The decision log remains the authoritative chronological record.
```

## 20.3 Memory Governance Rules

```text
- Information is memory-worthy only if durable, useful, relevant to the system, and likely to improve future assistance.
- Do not store trivial one-time facts, short-lived temporary details, sensitive personal attributes unless explicitly approved, inappropriate third-party private information, or raw notes better suited for /inbox.
- Sensitive memory entries require explicit user approval.
- Memory entries should include Type, Summary, Source, Confidence, Owner, Review Date, and Notes.
- Memory should receive lightweight review during weekly review and deeper hygiene review monthly.
- Stale memory should not be silently deleted; it should be marked stale, superseded, corrected with a new entry, or archived only with approval.
```

---

# 27. Validation and QA

Approved decisions:

```text
- A complete setup must include the required folders, the governance config,
  the workflow router (Section 16.11), the five governance workflows, the
  required global files (Section 6), and the User Guide. Zero use-case
  workflows at setup is valid.
- A complete workflow build must include the workflow definition file
  (Section 16.3), its router row (Section 16.11), and a change-log entry;
  the builder previews the workflow and its row and writes both only on
  Proceed. A workflow without a row is unreachable and therefore incomplete.
- The weekly and monthly review workflows audit generated files for
  completeness, consistency, permissions, and memory hygiene.
- Catalog validation (Section 7A: V1, V3, V4) must pass before a spec change
  or a plugin regeneration is considered complete; validators accept an
  empty use-case roster.
- Content-source validation (Section 18.7) must pass before a spec change or
  a plugin regeneration is considered complete, alongside the catalog,
  vocabulary, and version validators. The files under design-spec/content/
  are hand-editable, so their structure is checked mechanically rather than
  assumed.
```

---

# 28. Distribution

Distribution is plugin-only: one artifact, the **OpenAOS** Claude plugin,
generated directly from this specification per the packaging runbook
(Section 33). There is no factory package and no instance concept — the
plugin, once installed, scaffolds the user's workspace (§8) and runs the
builders.

## 28.1 Plugin Layout

```text
claude-plugin/openaos/
  .claude-plugin/plugin.json      manifest: name `openaos`, version synced
                                  to openaos_version, description, author
  skills/setup-openaos/SKILL.md   the §8.1 setup flow
  skills/build-workflow/SKILL.md  the §12 engine (both modes)
  skills/refine-workflow/SKILL.md the §13 engine
  workflow-specs/[slug]/spec.md   the five §7B builder specs, byte-identical
                                  to their design-spec/workflow-specs sources
  content/governance/governance.md      the §16.1 config (setup source),
                                        byte-identical to its
                                        design-spec/content/ source
  content/governance/workflow-router.md the §16.11 routing table (setup
                                        source), byte-identical copy
  content/workflows/[slug].md           the five §17 governance workflows,
                                        byte-identical copies
  content/templates/*.md|*.html         the §18 templates + the §16.6
                                        user-guide template, byte-identical
                                        copies
  content/root/{CLAUDE.md,AGENTS.md}    the §16.10 root scaffolds,
                                        byte-identical copies
  README.md                       install + quick start
```

## 28.2 Packaging Rules

```text
- Everything in the plugin is rendered from this spec (§1.6.1); the runbook
  (Section 33) is the procedure, and regeneration must be reproducible.
- plugin.json version equals openaos_version — the single version fact.
- The packaged workflow-specs are copies: byte-identical to the design-spec
  sources, verified at packaging (empty diff).
- The whole of content/ follows the same rule: byte-identical to
  design-spec/content/, verified at packaging (empty diff, §36.2 step 4).
  Spec→plugin is a copy, not a re-render.
- The plugin repo path claude-plugin/openaos/ is what
  .claude-plugin/marketplace.json publishes as its source.
- The feedback address baked into the packaged feedback workflow is
  openaos@neoclarity.ai (verified live before release).
- Install → run setup-openaos. Update → §14.4 modes. Uninstall leaves the
  user's workspace untouched (everything user-owned lives there, not in the
  plugin).
```

---


# 29. Naming and Slug Rules

Approved decisions:

```text
- Use lowercase kebab-case for generated folder and file slugs.
- Strip or replace special characters.
- Do not use spaces in generated folder names.
- Preserve human-readable names in frontmatter and headings.
- Handle duplicates by appending a short numeric suffix, such as -2 or -3.
- Standalone deliverables in /outputs use [slug]-<date> with the appropriate
  extension for the artifact type (for example .html for §18.2 reports, .md
  for markdown deliverables). Grouping by workflow keeps a workflow's runs
  adjacent when the folder is sorted by name.
```

---

# 30. Archive Policy

Approved decisions:

```text
- /archive stores retired, superseded, obsolete, or historical materials.
- Archiving requires explicit approval because it moves files.
- Archived files or folders should be dated when useful.
- Prefer copying to archive over moving when preserving active context is important.
- A retired workflow definition is archived (with approval), never deleted; its /outputs deliverables are preserved (data per Section 14.8).
- Archiving or restoring a workflow should be logged in /logs/decision-log.md and /logs/change-log.md, and requires explicit approval with Proceed.
```

---

# 31. Inbox Policy

Approved decisions:

```text
- /inbox is for raw notes, unresolved items, imported material, quick captures, and items awaiting routing.
- /inbox should be reviewed during daily startup when relevant and during weekly review by default.
- Inbox items should be promoted to memory, decisions, outputs, or archive according to the inbox-triage use-case workflow (when built) or on user request.
- Inbox items should not be deleted after processing unless explicitly approved.
- Processed inbox items should be moved to /inbox/processed to avoid duplicate processing.
- Moving an item to /inbox/processed is treated as part of normal inbox processing and should be allowed if the user has approved the inbox-triage workflow. This is the sole pre-authorized exception to the move-approval rule in Section 3.2.
- The daily startup workflow should include a startup brief section summarizing recently processed inbox items, distinguishing items processed, items still unresolved, where items were promoted to, and items requiring user approval.
```

---

# 32. Output Style Standards

Approved decisions:

```text
- Generated files should be detailed enough to be useful but not bloated.
- Workflow instructions should use direct imperative language.
- Use must/should/may consistently: must for requirements, should for strong defaults, may for optional behavior.
- Include examples in workflow definition files and important templates.
- Templates should include placeholders plus brief guidance, not long sample completed entries unless useful.
```

---

# 33. Generation Runbook

The packaging procedure lives in a companion file (rewritten as the plugin packaging runbook in Phase G):

```text
openaos-runbook.md
```

The `Proceed` safety gate is unchanged: actual plugin file generation remains blocked until the user types exactly `Proceed`, per the Purpose section above and the runbook.
