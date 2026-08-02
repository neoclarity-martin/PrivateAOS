---
title: OpenAOS Packaging Runbook
file_type: design_spec
project: OpenAOS
openaos_version: 3.2.0
created_date: 2026-06-02
last_updated: 2026-08-02
status: design_ready_for_generation
important_constraint: Do not generate actual openaos files unless the user explicitly types exactly Proceed.
---

# OpenAOS Packaging Runbook

Part of the OpenAOS Design Specification document set. The canonical design
is in `openaos-design-specification.md` (Sections 1–32); this file holds the
review and packaging procedure (Sections 33–37). Section numbering is
preserved from the specification so cross-references continue to resolve.
The `Proceed` safety gate applies in full: no plugin files are generated
until the user types exactly `Proceed`.

(Rewritten in the 3.0 Phase G: the 2.x factory-generation procedure is
replaced by plugin-only packaging per spec §28.)

---

# 33. Design Governance Rules

```text
- The most recent confirmed decisions are authoritative. Where they conflict
  with earlier sections, the later decisions govern.
- A completed decision must be preserved unless the user explicitly changes
  it.
- The full design spec must not be rewritten unless the user explicitly
  requests a consolidated version.
- The revision history and openaos_version follow the format and increment
  rule in the specification's "Revision History" section.
- The governance layer (spec §16.1, §17) is not removable from the design or
  from generated artifacts (AGENTS.md hard rule).
```

# 34. Design Readiness Checklist

Verified by every §36.1 review; each item maps to spec sections:

```text
[ ] Goal, guiding principle, and core model are consistent (Frame).
[ ] Safety and approval rules are complete (§3) and rendered into the
    governance config schema (§16.1).
[ ] The five governance workflows are defined (§17) with catalog entries,
    and each has a workflow-router row (§16.11).
[ ] The five use-case builder specs exist and follow §7B.1 (workflow-specs/).
[ ] The build-workflow contract (§12) and refine-workflow engine (§13) are
    consistent with the drift invariant (§14.8).
[ ] Setup flow (§8) and setup-interview.md agree.
[ ] File schemas (§16), skeletons (file-skeletons.yaml), and templates (§18)
    agree.
[ ] Catalog, vocabulary, and version validators pass (§27).
[ ] Content sources (design-spec/content/) are well-formed and complete
    (§18.7); validate-content.py passes.
[ ] Distribution layout and packaging rules are current (§28).
[ ] The feedback address openaos@neoclarity.ai is live (verified before
    release; spec §28.2).
```

# 35. Generation Scope

The one generated artifact is the plugin at `claude-plugin/openaos/`, laid
out per spec §28.1. Its sources:

```text
skills/*/SKILL.md            authored from §8.1, §12, §13
workflow-specs/              byte-identical copies of design-spec sources
content/                     byte-identical copies of design-spec/content/
                              sources (governance config, the §16.11
                              workflow router, the five
                              governance workflows, the seven §18.2 HTML
                              report templates, the §16.6 user-guide
                              template, the three §18.3/§18.5/§18.6
                              interaction templates, and the two §16.10
                              root scaffolds under content/root/);
                              status-report-template.md retired
.claude-plugin/plugin.json   name openaos; version = openaos_version
README.md                    install + quick start
```

# 36. Workflows

## 36.1 Design Readiness Review

1. Choose mode: **full** (all §34 items) or **incremental** (items whose
   underlying sections changed since the last completed review's baseline
   `openaos_version`, per git diff). Mechanical checks always run in full.
2. Mechanical checks: run `scripts/validate-workflow-catalog.py`,
   `scripts/validate-vocabulary.py`, `scripts/check-spec-version.py`, and
   `scripts/validate-content.py`; all must pass.
3. Verify the §34 checklist over the document set (spec, this runbook,
   revision history, workflow-catalog.yaml, vocabulary.yaml,
   file-skeletons.yaml, setup-interview.md, workflow-specs/*,
   design-spec/content/*).
4. Record all completeness, safety, and consistency findings on one issue
   list; the list gates finalization.
5. Resolve findings (each spec change `Proceed`-gated) and repeat steps 2–4
   until a clean pass.
6. Finalize: add a revision-history row and confirm `status:
   design_ready_for_generation` across the stamped set. Increment
   `openaos_version` only if the specification changed.

## 36.2 Plugin Generation

1. Precondition: a completed §36.1 review at the current `openaos_version`.
2. Read spec §28 and render every §35 source into `claude-plugin/openaos/`.
3. Preview: list every file to be created and, separately, every existing
   file that would be overwritten. Generate only on exact `Proceed`.
4. Validate the result: `plugin.json` well-formed with `name` and `version`
   equal to `openaos_version`; the three SKILL.md files present with `name`
   and `description` frontmatter; in-skill file references resolve;
   `workflow-specs/` byte-identical to the design-spec sources (empty diff);
   all of `content/` byte-identical to `design-spec/content/` (empty diff,
   same rule as `workflow-specs/`);
   `.claude-plugin/marketplace.json` `source` points at
   `./claude-plugin/openaos`; no remaining live reference to the
   retired `status-report-template.md` anywhere in the plugin (the
   governance Change Notes record of its retirement is expected); every report-producing
   workflow (§17.1–§17.4, and inbox-triage/organizer/learning-assistant when
   built) points at a real `content/templates/*-report-template.html` file
   and a `/outputs/[slug]-<date>.html` path; every such HTML template opens
   standalone (embeds the §18.1 CSS inline, no external asset references).
5. Add a revision-history row for the completed generation (no
   `openaos_version` increment unless the packaged framework changed).

# 37. Release Steps (manual)

```text
- Smoke-test per the feature spec: install fresh; run setup-openaos;
  instantiate one use case; design-new one custom workflow; refine it;
  run the feedback workflow to preview (no send).
- Verify the openaos@neoclarity.ai mailbox is live.
- Publish via .claude-plugin/marketplace.json.
```
