---
title: AOS Factory Design Specification
file_type: design_spec
project: Script to Build Agentic OS Factory
created_date: 2026-06-02
last_updated: 2026-07-16
spec_version: 2.4.2
status: design_ready_for_factory_generation
important_constraint: Do not generate actual AOS Factory files unless the user explicitly types exactly Proceed.
---

# AOS Factory Design Specification

---

# 3.0 Rewrite Frame — Minimal, Workflow-First openaos

> **Status of this block (Phase A):** This section is the authoritative
> destination frame for the 3.0 rewrite (feature spec
> `internal-only/feature-specs/3.0-create-minimal-openaos.md`). Everything
> below it is 2.x content that will be cut to this frame in Phase B and
> renamed in Phase C. Where this frame and the 2.x body conflict, this frame
> wins. The pre-rewrite spec is preserved at git tag `spec-v2.4.2`.

## Goal

Claude Cowork makes Claude accessible to non-technical users, but leaves them
on their own to turn that access into workflows that are actually good —
well-designed, tailored to their situation, and safe to run against their real
files. **openaos exists to close that gap.** Its purpose is to
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
user adopts openaos is the promise of a genuinely good, tailored workflow for
the handful of things they actually do. So the whole system is exactly three
things:

1. **Use-case workflow builders** — guided interviews that co-design a
   tailored, best-practice workflow for each core use case.
2. **Workflow refinement** — the same collaborative interview, pointed at an
   existing workflow, to improve it.
3. **Guardrails** — the `Proceed` safety gate, durable memory, review rhythms,
   and a feedback-to-team channel that make those workflows trustworthy.

The builders include a **custom builder** that co-designs brand-new workflows
for the user's own domain — so openaos is not limited to the use cases we
anticipated. This is what turns openaos from "a handful of useful workflows"
into "a way to bring AI into whatever the user actually does to create
value," and is arguably its highest-leverage capability.

Value to the user is the primary objective. Everything that does not directly
serve it — the multi-agent roster, the Pro tier, tiered versioning, DDD
relationship semantics, the factory/instance split — is removed, from both
this spec and the artifacts it generates.

## Core Model

The Minimal openaos design, in full:

- **Workflows.** The unit of value. Two families:
  - *Use-case workflows* — five predefined ones, each authored by a builder
    interview: **inbox triage** (classify, route, and act on inbox items),
    **research assistant** (scoped, source-disciplined research), **writing
    assistant** (drafting/editing keyed to the user's voice), **learning
    assistant / tutor** (guided learning with understanding checks), and
    **organizer / declutter** (file cleanup — inbox-triage for files).
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
- **Distribution.** One artifact: the **openaos** Claude plugin, generated
  directly from this spec. No factory, no instance concept. A single
  `openaos_version` is the only version fact.

Removed from the spec entirely: the five governance *agents* as separate
agents, the ten-agent optional roster, the Pro tier and tier concept,
`spec_version`/`catalog_version`/`compatible_aos_versions` multi-track
versioning (a single `openaos_version` remains), the DDD relationship
vocabulary and typed collaboration edges, the factory-vs-instance guard and
layout, and all sections that exist only to serve those. The exact deletions
are enumerated in the removal manifest
(`internal-only/feature-specs/3.0-removal-manifest.md`).

---

## Purpose of This Document

This document is the consolidated design specification for the **Agentic Operating System (AOS) Factory**.

This document is a design artifact only. It does **not** authorize creation of actual AOS Factory files.

The assistant must not generate actual AOS Factory files unless the user explicitly types exactly:

```text
Proceed
```

## Required Next-Step Instructions

The assistant continuing from this document must:

```text
- Review the next steps with the user.
- The user may ask additional questions about the design or next steps.
- Wait for the user to enter the exact instruction “Proceed” to generate the AOS Factory files.
```

## Document Set

This specification is maintained as a small set of companion files in this folder:

```text
aos-factory-design-specification.md   - the canonical design (this file)
aos-factory-generation-runbook.md     - packaging and handoff procedure (rewritten in Phase G)
aos-factory-revision-history.md       - dated revision and consistency-resolution history
agent-catalog.yaml                    - the Workflow Catalog: structured workflow identity/ownership data (Section 7A)
vocabulary.yaml                       - controlled vocabularies (file_type/status, permissions/actions), source of truth for Sections 3.2-3.4, 15.4-15.5
file-skeletons.yaml                   - ordered section/field skeletons for generated files (Section 16)
aos-interviews.md                     - the setup interview script (rewritten as setup-interview.md in Phases C/G)
```

The canonical specification remains the single source of truth (Section 1.6.1); the companion files hold structured data extracted from it for machine enforcement and are governed by the same `Proceed` safety gate. They are design-time **source** artifacts that live with the spec here in `design-spec/` (versioned by `spec_version`). For the vocabularies these files own, the prose Sections above carry the normative meaning and rules; the data files carry the enumerated tokens, which the prose references rather than restates.

## Revision History

The full revision history of this specification — including all dated Design Consistency Resolution cycles — is maintained in a companion file:

```text
aos-factory-revision-history.md
```

Entries there are maintained in reverse chronological order (newest first); new entries are added at the top, as rows in a single table (`spec_version | Date | Change`). The table is a log of completed cycles, not a one-row-per-unique-version index — the same `spec_version` may appear in consecutive rows when multiple cycles complete against it without a content change, each with its own date and change description.

Every completed §36.1 Design Readiness Review, §36.2 AOS Factory Generation, or §36.3 Claude Plugin Generation cycle gets a row, so the file is a single place to see the current state of the spec, the factory, and the plugin. `spec_version` increments only when a cycle actually changes the specification (or, for §36.3, the packaged framework) — a full §36.1 consistency-review cycle is one increment and one consolidated row when it resolves at least one inconsistency, not one per re-read iteration, however many iterations the loop takes. A cycle that completes with no changes (for example, a Design Readiness Review that surfaces no inconsistencies, or a Factory/Plugin Generation that produces no diff from the prior run) still gets a row describing that outcome, logged against the current `spec_version` rather than incrementing it. A structural change (for example, a document restructure) is its own separate increment.

---

# 1. Project Overview

## 1.1 Project Name

Working project name:

```text
AOS Factory Project
```

The generated system is referred to as:

```text
Agentic Operating System
AOS
```

The framework and the plugin are both referred to as (Phase C applies this
rename throughout):

```text
openaos
```

There is no factory/instance term split: the plugin scaffolds the user's
workspace directly, and the workspace is simply the user's folder that openaos
operates in.

## 1.2 Target Platform

The current target platform is:

```text
Claude Cowork
```

Portability to other platforms may be considered later, but is outside the current design scope.

## 1.3 Overall Purpose

openaos should help a non-technical user collaboratively create the most useful, most user-friendly workflow for each of their core use cases — markdown-based workflows plus the memory, governance config, templates, and logs that make them trustworthy.

The builder is intended to be:

```text
A reusable template others could adopt.
```

It should not be only a one-off personal productivity setup, although it should work well for personal productivity.

## 1.4 What openaos Ultimately Produces

The specification generates exactly one artifact: the **openaos** Claude
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

This section states the principles and goals that motivate the rest of this specification. Section 2 and beyond define *how* the AOS Factory behaves; this section defines *why*. When a future design decision is ambiguous, it should be resolved in favor of these principles. They are normative, not aspirational.

### 1.6.1 Design Spec as the Single Source of Truth

The AOS Factory is generated from this design specification, not the other way around. The spec is canonical; the factory framework, the builder files, the plugin package, and any outward-facing description of the project are all **renderings** of it.

```text
- Every builder, agent schema, workflow, and config traces back to a decision
  recorded here.
- When the spec and a generated artifact disagree, the spec wins and the
  artifact is corrected.
- Outward-facing material (README, pitch, user guide) derives from the spec so
  that documentation and marketing cannot silently drift away from the design.
```

This is what makes the system auditable and reproducible: anyone can regenerate the factory from the spec and get the same result.

### 1.6.2 Governance Before Productivity

Safety, memory, and quality review must exist before any productive work happens. Setup scaffolds the governance config and governance workflows before any use-case workflow is built. Productivity is additive; governance is foundational. A user cannot end up with a fast, capable, ungoverned system.

### 1.6.3 Single Responsibility at Every Level

Each workflow owns exactly one activity, with explicit boundaries; the system avoids a catch-all procedure that does everything (Section 2.1). The same discipline applies to files: one file, one purpose, scope recoverable from its path. This keeps the system legible to non-technical users and extensible without redesign.

### 1.6.4 Non-Destructive and Approval-Gated by Default

The system prefers actions that cannot lose work. Workflows create, append, or ask rather than overwrite, delete, move, or bulk-modify (Section 2.4). Anything consequential is gated behind a single, unambiguous approval signal — the user typing exactly `Proceed` (Section 3.1) — and approval is specific to the action described, never a standing grant (Section 2.5). The goal is that a user can trust openaos with real work without fear that it will quietly damage their files.

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
https://github.com/neoClarity-AI/Open-AOS-Factory
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

When an agent proposes one of these actions, it must first:

1. Explain exactly what action it wants to take.
2. Identify the affected file or files.
3. Explain why the action is recommended.
4. Explain the likely consequence of the action.
5. Ask the user to type exactly: Proceed

If the user does not type Proceed, the agent must not take the action.

The agent may suggest safer alternatives, such as copying the file, creating a backup, appending new content, or creating a new versioned file instead of modifying the original.
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
- Naming: YYYY-MM-DD-[slug].md, or the appropriate extension (§29).
```

# 6. Global Files

During setup, the `setup-openaos` skill should create these global files when
authorized (the foundation; use-case workflows are added only by the builder
interview):

```text
/governance/governance.md
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
/templates/status-report-template.md
/templates/decision-entry-template.md
/templates/approval-request-template.md
/templates/memory-entry-template.md
/docs/user-guide.html
```

# 7A. Workflow Catalog

*(Cut to Minimal in Phase B; renamed in Phase C, repopulated in Phases D–E.)*

The catalog data file (`agent-catalog.yaml`, renamed `workflow-catalog.yaml`
in the Phase C sweep) is the structured registry of workflow identity and
ownership data, extracted from this specification for machine enforcement.
Until Phases D–E author the governance and use-case workflow definitions, the
roster is legitimately empty — a minimal-but-valid catalog. Mechanical
validation keeps: domain existence against the vocabulary (V1) and pairwise
disjointness of owned domains (V3) and owned artifacts (V4); validators must
not require a non-empty roster. The DDD relationship vocabulary, typed
collaboration edges, and their validator checks (V2, V5, V14) are removed.

---

# 8. Builder Skills and Setup Flow (placeholder — Phases E/G)

*(2.x builder-framework and build-flow content cut in Phase B. Replaced by
the `setup-openaos`, `build-workflow`, and `refine-workflow` plugin skills:
the builder-interview contract is authored in Phase E, the setup flow and
packaging in Phase G, per the 3.0 Rewrite Frame.)*

---

# 9. (Removed — merged into Section 8 placeholder)

*(2.x build-flow content cut in Phase B; see Section 8.)*

---

# 12. Build Engine (placeholder — Phases E/G)

*(2.x generic-build-engine and Build-AOS schemas cut in Phase B. The
`build-workflow` engine — one engine, two modes (instantiate / design-new) —
is authored in Phase E; the `setup-openaos` flow in Phase G.)*

---

# 14. Versioning and Update Policy

## 14.1 Single Version Track

The specification and everything generated from it share one version fact —
currently `spec_version`, renamed `openaos_version` in the Phase C sweep.
There is no separate catalog version and no per-instance version track.
`check-spec-version.py` enforces that all design-spec files agree on the
single version.

## 14.2 Per-File Version Metadata

Each generated definition file should record, in its YAML frontmatter, the `spec_version` it was rendered from.

Example:

```yaml
---
title: Weekly Review Workflow
spec_version: 1.0.5
last_updated: 2026-06-11
---
```

## 14.4 Update Modes (placeholder — Phase G)

*(2.x update-mode content cut in Phase B. The only update path is a plugin
update, specified with distribution in Phase G.)*

## 14.8 Definition Files, Data Files, and the Drift Invariant

A user's workspace is a living system: its files change after setup. To keep that change controllable, every file in the workspace is one of two kinds. (This invariant is restated for governance in Phase D and amended in Phase F to name the refinement interview as the sanctioned in-place edit path.)

**Definition file.** A file that defines behavior: workflow definitions in `/workflows`, the governance config, and templates in `/templates`. Use-case workflows are interview-authored and tailored, so definition files are not all spec-renderings — but they change only through sanctioned paths: the builder interview (creation), the refinement interview, or a plugin update, each `Proceed`-gated. No workflow run edits a definition file as a side effect.

**Data file.** A file whose content accumulates from operation and the user's input. *Test: regenerating this file would destroy information the user relies on.* Data files are created once at setup (empty or seeded) and never overwritten by a plugin update; workflows append to and maintain them under the normal non-destructive and approval rules (Sections 2.4, 3). Examples: everything in `/memory`, `/logs`, `/outputs`, `/inbox`, and `/archive`.

**Projections.** A regenerable view built from definitions plus named data inputs (for example the User Guide, Section 16.6) is treated as a **definition file** for update purposes (safe to regenerate), with its data inputs stored separately as data files.

**The drift invariant.** Workflow runs write data files; definition files change only via the sanctioned, `Proceed`-gated paths above. This bounds drift to data (which is supposed to grow) and keeps definitions deliberate, so an update or refinement is a clean, reviewed change rather than a three-way merge.

---

# 15. YAML Frontmatter Standards

## 15.3 Other Generated Markdown File Frontmatter

All generated markdown files should include lightweight YAML frontmatter.

Example:

```yaml
---
title: Weekly Review Workflow
file_type: workflow
spec_version: 1.0.5
created_date: 2026-06-02
last_updated: 2026-06-02
---
```

## 15.4 Controlled `file_type` Vocabulary

The controlled `file_type` tokens are `file_type` in `design-spec/vocabulary.yaml` (source of truth). The meaning of each type and its per-file assignments are normative here in the prose below.

`design_spec` applies to this design specification itself (`aos-factory-design-specification.md`), the source document the AOS Factory is generated from. It is the one source/design artifact in the vocabulary; the other types all describe factory-generated files.

`project_instructions` applies to the root project instruction files (`/CLAUDE.md` and `/AGENTS.md`) scaffolded at the workspace root (Section 16.10).

`change_log` applies to the workspace change log (`/logs/change-log.md`). `feedback_log` applies to the feedback staging log (`/logs/feedback-log.md`, Section 16.7) — a data file per Section 14.8.

File-type assignments by file:

```text
config        /governance/governance.md

memory        /memory/user-profile.md, /memory/preferences.md,
              /memory/people.md, /memory/decisions.md

decision_log  /logs/decision-log.md

workflow      every file in /workflows (governance and use-case)

template      every file in /templates

documentation /docs/user-guide.html (HTML metadata is carried via meta
              tags or an HTML comment rather than YAML frontmatter)

project_instructions
              /CLAUDE.md and /AGENTS.md (workspace root)

catalog       design-spec/agent-catalog.yaml (renamed workflow-catalog.yaml
              in Phase C); see Section 7A

interview_script
              design-spec/aos-interviews.md (renamed setup-interview.md in
              Phase C); the setup interview script
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

## 16.1 Governance Config Schema (placeholder — Phase D)

*(2.x per-agent config-file schema cut in Phase B. The single standing-rules
file `/governance/governance.md` — `Proceed` gate, permission model, memory
boundaries — is authored in Phase D.)*

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

Workflow files should follow:

```markdown
# [Workflow Name]

## Purpose

## When to Use

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

## 16.6 User Guide Schema (placeholder — Phase G)

*(2.x agent-era user-guide schema cut in Phase B. The plugin's User Guide
template — what workflows are, running the builders, `Proceed` and the safety
model, refinement, governance rhythms, feedback — is authored in Phase G. The
guide remains a §14.8 projection: regenerable from definitions plus its
embedded change log, which is data. The load-bearing 2.x generation rules —
mandatory linked table of contents, embedded newest-on-top change log, the
`Proceed`-is-the-only-exact-command contrast, and the consistency checks that
every TOC entry resolves to an anchor and vice versa — carry forward into the
Phase G authoring.)*

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
**Status:** staged | approved | sent | discarded
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

## 16.10 Workspace-Root Scaffold Files (placeholder — Phase G)

*(2.x CLAUDE.md/AGENTS.md schema cut in Phase B; the plugin's workspace
scaffolding is specified in Phase G.)*


---

# 17. Governance Workflows (placeholder — Phase D)

*(2.x global-workflow content cut in Phase B. Phase D authors the five
governance workflows — `daily-startup`, `end-of-day`, `weekly-review`,
`monthly-review`, and `feedback` — which also absorb the load-bearing content
of the 2.x operating rhythms (old Section 25). The agent-era workflows
(inbox-to-task, project kickoff, decision capture, memory review) are
removed; their surviving concerns are covered by the use-case workflows
authored in Phase E and the memory governance rules of Section 20.)*

---

# 18. Global Templates

Every generated AOS should include these global templates.

## 18.1 Status Report Template

Create:

```text
/templates/status-report-template.md
```

Purpose:

```text
Give the user a concise summary of current priorities, active projects, pending approvals, recent decisions, next actions, and processed inbox items.
```

Body skeleton:

```markdown
## Priorities
## Active Projects
## Pending Approvals
## Recent Decisions
## Next Actions
## Processed Inbox
```

## 18.3 Decision Entry Template

Create:

```text
/templates/decision-entry-template.md
```

Purpose:

```text
Provide a standard format for recording decisions in global, project-level, or agent-level decision logs.
```

This template embeds the §16.5 decision-log entry block; it defines no new schema of its own.

## 18.5 Approval Request Template

Create:

```text
/templates/approval-request-template.md
```

Purpose:

```text
Standardize how agents ask the user to approve Level 2 actions requiring Proceed.
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

## 18.6 Memory Entry Template

Create:

```text
/templates/memory-entry-template.md
```

Purpose:

```text
Standardize how important preferences, facts, decisions, people, projects, and agent learnings are recorded.
```

This template embeds the §16.2 dated memory entry block (the seven §20.3 fields); it defines no new schema of its own.

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

## 20.2 Memory File Boundaries

```text
/memory/user-profile.md
Stores durable, user-approved facts about the user that help openaos personalize assistance. Avoid sensitive personal attributes unless explicitly approved.

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
  the five governance workflows, the required global files (Section 6), and
  the User Guide. Zero use-case workflows at setup is valid.
- A complete workflow build must include the workflow definition file
  (Section 16.3) and a change-log entry; the builder previews the workflow
  and writes it only on Proceed.
- The weekly and monthly review workflows audit generated files for
  completeness, consistency, permissions, and memory hygiene.
- Catalog validation (Section 7A: V1, V3, V4) must pass before a spec change
  or a plugin regeneration is considered complete; validators accept an
  empty use-case roster.
```

---

# 28. Distribution (placeholder — Phase G)

*(2.x distribution and update mechanics cut in Phase B. Distribution is
plugin-only: the openaos Claude plugin, generated directly from this
specification — no factory instance, no multi-format delivery. Specified in
Phase G.)*

---


# 29. Naming and Slug Rules

Approved decisions:

```text
- Use lowercase kebab-case for generated folder and file slugs.
- Strip or replace special characters.
- Do not use spaces in generated folder names.
- Preserve human-readable names in frontmatter and headings.
- Handle duplicates by appending a short numeric suffix, such as -2 or -3.
- Standalone deliverables in /outputs use YYYY-MM-DD-[slug].md (or the
  appropriate extension for the artifact type).
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
- Agent instructions should use direct imperative language.
- Use must/should/may consistently: must for requirements, should for strong defaults, may for optional behavior.
- Include examples in agent instruction files and important templates.
- Templates should include placeholders plus brief guidance, not long sample completed entries unless useful.
```

---

# 33. Generation Runbook

The packaging procedure lives in a companion file (rewritten as the plugin packaging runbook in Phase G):

```text
aos-factory-generation-runbook.md
```

The `Proceed` safety gate is unchanged: actual plugin file generation remains blocked until the user types exactly `Proceed`, per the Purpose section above and the runbook.
