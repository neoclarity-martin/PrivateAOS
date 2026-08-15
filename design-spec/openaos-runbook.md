---
title: OpenAOS Packaging Runbook
file_type: design_spec
project: OpenAOS
openaos_version: 3.2.1
created_date: 2026-06-02
last_updated: 2026-08-15
status: design_ready_for_generation
important_constraint: Do not generate actual OpenAOS files unless the user explicitly types exactly Proceed.
---

# OpenAOS Packaging Runbook

Part of the OpenAOS Design Specification document set. The canonical design
is in `openaos-design-spec.md` (Sections 1–32); this file holds the
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
- Sync ordering: within any cycle, §36.3 (plugin → spec) runs before §36.2
  (spec → plugin). The two directions are never concurrently live, so there is
  no "which side is authoritative" question and no conflict resolution to do.
- The §36.3 tenet-check gate applies to all plugin → spec reflection, without
  exception. A change that violates a fundamental design tenet is not
  reflected; it is reported, logged, and left to the user to decide.
- §36.3 is a *drafting* path for maintainers and contributors alike. The only
  route by which a change reaches `main` is a spec change with a plugin
  regenerated from it. Spec prose produced by a §36.3 draft is reviewed and
  owned by its author, not attributed to the tool.
```

## 33.1 Fundamental Design Tenets (sync gate)

Drawn from what is already normative elsewhere in the design, restated here as
the checklist §36.3 step 2 applies. A plugin-side change that violates any of
these is never reflected into the spec.

```text
1. Scope discipline (Guiding Principle; the Frame's removed-concepts
   paragraph). The system is exactly three things: use-case workflow builders,
   workflow refinement, and guardrails. A plugin edit that adds scope beyond
   that — new capabilities, new agent roles, or the reappearance of anything
   the Frame lists as removed — cannot be reflected. The Frame paragraph is
   the normative authority for what "removed" means; the removal manifest it
   cites enumerates the deletions as non-normative detail.
2. Governance layer is not removable (spec §14.8, §16.1). No plugin edit may
   weaken, bypass, or remove the Proceed safety gate, governance.md,
   workflow-router.md, or the five governance workflows. Sanctioned paths may
   revise them; nothing may remove them.
3. Skills vs. workflows boundary (Core Model). Skills (setup-openaos,
   build-workflow, refine-workflow) are plugin-owned and never user-refinable;
   workflows are user-owned and refinable. This tenet resists mechanical
   checking: any skill-file change touching the refinability boundary surfaces
   for human review regardless of the automated verdict.
4. Drift invariant (spec §14.8). Definition files change only through
   sanctioned, Proceed-gated paths; workflow runs never edit a definition file
   as a side effect. A plugin edit that introduces a new unsanctioned write
   path violates this even if the change itself seems reasonable.
5. Single-artifact distribution (Core Model). One plugin, one openaos_version,
   generated from one spec. No new artifact types, no new version tracks.
```

The tenet check is a judgment call and is deliberately **not** mechanized into
CI. CI enforces the byte-identity invariant, which is what makes an unreflected
plugin edit unable to reach `main`; the tenet check stays a §36.3 step and a
maintainer review responsibility.

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
[ ] §8.1 and setup-openaos/SKILL.md agree step-for-step, in both directions
    (a spec-side step absent from the skill is a finding, and so is a
    skill-side step absent from the spec).
[ ] File schemas (§16), skeletons (file-skeletons.yaml), and templates (§18)
    agree.
[ ] Catalog, vocabulary, and version validators pass (§27).
[ ] Content sources (design-spec/content/) are well-formed and complete
    (§18.7); validate-content.py passes.
[ ] workflow-specs/ is byte-identical between design-spec/ and the plugin;
    validate-workflow-specs.py passes.
[ ] The three plugin skills pass their spec-anchor checks (§35 authored
    bucket); validate-skills.py passes.
[ ] No unreflected direct edits remain in claude-plugin/openaos/skills/ —
    §36.3 has been run since the last skill edit and §36.2 since that
    (scripts/sync-state.py check is clean).
[ ] Every tenet-check exclusion in design-spec/sync-exclusions.md carries a
    disposition. An `open` entry is recorded as a finding on the §36.1 step 4
    issue list, which gates finalization; it clears by recording any
    disposition, including an explicit decision not to act.
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

**Direction and authority.** Every source above is spec-authoritative — the spec
wins at every commit boundary — but the two buckets move differently:

```text
content/, workflow-specs/    Mechanical. Byte-identical copies, no
                              interpretation. Move spec → plugin in §36.2 and
                              plugin → spec in §36.3. Enforced by
                              validate-content.py (VC2) and
                              validate-workflow-specs.py (WS1–WS2).
skills/*/SKILL.md            Authored from §8.1, §12, §13 — and the plugin copy
                              may be edited directly as a *drafting surface*.
                              §36.3 reflects such an edit back into
                              §8.1/§12/§13, the author reviews and owns the
                              resulting spec prose, and §36.2 then regenerates
                              the skill file from the spec. The plugin edit is
                              scaffolding that gets round-tripped away.
```

§36.3 is the sanctioned path back. It is a drafting aid, not a second route to
`main`: what is proposed is always a spec change, with the plugin regenerated
from it (§33).

# 36. Workflows

## 36.1 Design Readiness Review

1. Choose mode: **full** (all §34 items) or **incremental** (items whose
   underlying sections changed since the last completed review's baseline
   `openaos_version`, per git diff). Mechanical checks always run in full.
2. Mechanical checks: run `scripts/validate-workflow-catalog.py`,
   `scripts/validate-vocabulary.py`, `scripts/check-spec-version.py`,
   `scripts/validate-content.py`, `scripts/validate-workflow-specs.py`, and
   `scripts/validate-skills.py`; all must pass.
3. Verify the §34 checklist over the document set (spec, this runbook,
   revision history, workflow-catalog.yaml, vocabulary.yaml,
   file-skeletons.yaml, setup-interview.md, workflow-specs/*,
   design-spec/content/*, sync-exclusions.md).
4. Record all completeness, safety, and consistency findings on one issue
   list; the list gates finalization. **A tenet-check exclusion in
   `design-spec/sync-exclusions.md` whose disposition is still `open` is a
   finding on this list** — an unresolved conflict between a plugin-side change
   and a fundamental design tenet is a decision the project owes itself, and it
   clears by recording any disposition, including an explicit decision not to
   act. It does not block the review from running, only from finalizing.
5. Resolve findings (each spec change `Proceed`-gated) and repeat steps 2–4
   until a clean pass.
6. Finalize: add a revision-history row and confirm `status:
   design_ready_for_generation` across the stamped set. Increment
   `openaos_version` only if the specification changed.

## 36.2 Plugin Generation

1. Precondition: a completed §36.1 review at the current `openaos_version`.
2. Read spec §28 and render every §35 source into `claude-plugin/openaos/`.
   **Baseline guard, before rendering each `skills/*/SKILL.md`:** compare the
   existing plugin file against the recorded sync baseline
   (`scripts/sync-state.py check`). If it matches, regenerate as normal. If it
   differs, a plugin-side hand-edit is unreflected — **stop, name the file, and
   direct the user to §36.3**, which must run first (§33 ordering rule). This
   preserves the spec → plugin flow for skills while making it impossible for a
   generation to clobber an unreflected edit. Where no baseline exists (fresh
   clone), the comparison is unavailable, so confirm with the user before
   overwriting an existing skill file. `content/*` and `workflow-specs/*` render
   spec → plugin unconditionally; they are copies, and §36.3 has already run.
3. Preview: list every file to be created and, separately, every existing
   file that would be overwritten. Generate only on exact `Proceed`.
4. Validate the result: `plugin.json` well-formed with `name` and `version`
   equal to `openaos_version`; the three SKILL.md files pass
   `scripts/validate-skills.py` (SK1–SK5 — present and correctly named, `name`
   and `description` frontmatter, spec citations resolving and each skill citing
   its governing §8/§12/§13, in-skill file references resolving, Proceed gate
   present; prose fidelity to §8.1/§12/§13 remains a review judgment, not a
   script's);
   `workflow-specs/` byte-identical to the design-spec sources (empty diff,
   `scripts/validate-workflow-specs.py`);
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
6. Update the sync baseline: `python scripts/sync-state.py record`.

## 36.3 Spec Sync (Plugin → Spec)

Triggered by the phrase **"Using the runbook, sync the design spec with the
plugin."** No precondition — this workflow exists specifically to capture ad hoc
direct edits made to the plugin. It runs *before* §36.2 in any cycle (§33), and
it restores equality; it never changes the packaged framework.

The four mechanical validators are **not** run as a precondition. A precondition
run would block syncing the very drift that broke them. They run at step 7.

1. **Detect scope.** Diff `claude-plugin/openaos/` against its spec-derived
   counterparts, in two buckets:
   - *Mechanical* — `content/*` and `workflow-specs/*`, by byte comparison
     (`scripts/sync-plugin-to-spec.py` with no `--apply`, and
     `scripts/validate-content.py` / `scripts/validate-workflow-specs.py` for
     the same view from the other side).
   - *Authored* — `skills/*/SKILL.md` against spec §8.1, §12, and §13.

   Scope is narrowed using the sync state file where present
   (`scripts/sync-state.py status`); where absent, the full comparison runs —
   noisy once, never wrong. If neither bucket shows drift, report "nothing to
   sync" and stop.
2. **Tenet check.** For every changed file in both buckets, check the change
   against the five fundamental design tenets in §33.1. Anything that fails is
   excluded from this sync, reported by name and violated tenet, and appended to
   `design-spec/sync-exclusions.md` with disposition `open`, which makes it a
   finding on the next §36.1 issue list until decided (§34). Nothing is ever
   silently dropped. Tenet 3
   in particular resists mechanical checking: any skill-file change touching the
   refinability boundary is surfaced for human review regardless.
3. **Mechanical sync.** For tenet-passing mechanical files, copy the plugin
   version onto its `design-spec/` counterpart verbatim
   (`scripts/sync-plugin-to-spec.py --apply`, passing `--exclude` for each
   tenet-check exclusion).
4. **Authored reflection.** For tenet-passing skill changes, draft the
   corresponding §8.1/§12/§13 update, preserving spec-only material (rationale,
   cross-references) that the terser skill file does not carry, and flagging
   anything ambiguous rather than guessing. **The draft is a starting point the
   author is expected to review and edit, not an output to be accepted as
   written** — the author owns the spec language that results (§33).
5. **Combined preview.** List every spec file this would touch, both buckets
   together, plus the tenet-check exclusions, before writing anything.
6. **Proceed gate.** One gate for the whole batch; write only on exact
   `Proceed`.
7. **Validate.** Re-run `scripts/validate-content.py`,
   `scripts/validate-workflow-specs.py`, `scripts/validate-skills.py`,
   `scripts/validate-workflow-catalog.py`, `scripts/validate-vocabulary.py`, and
   `scripts/check-spec-version.py`; then `python scripts/sync-state.py record`.
8. **Revision history.** Add a row: "Spec sync from plugin: [files]." **No
   automatic `openaos_version` bump** — a bump is made only if the user directs
   one during the preview/review step.
9. **Close the round trip.** Direct the user to §36.2 to regenerate the plugin
   from the now-updated spec.

# 37. Release Steps (manual)

```text
- Smoke-test per the feature spec: install fresh; run setup-openaos;
  instantiate one use case; design-new one custom workflow; refine it;
  run the feedback workflow to preview (no send).
- Verify the openaos@neoclarity.ai mailbox is live.
- Publish via .claude-plugin/marketplace.json.
```
