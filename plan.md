---
title: DDD Improvement Cycle 1 — Implementation Plan
file_type: plan
created_date: 2026-07-15
status: awaiting_proceed
scope: Relationship + trigger vocabularies for the Agent Catalog (formerly proposals P2+P3)
important_constraint: Do not implement unless the user explicitly types exactly Proceed.
---

# DDD Improvement Cycle 1 — Implementation Plan

Adds two Domain-driven-design-derived concepts to the design spec while keeping existing AOS vocabulary: a **collaboration relationship taxonomy** (DDD context-mapping relationships) and a **controlled trigger vocabulary** (DDD domain events) for `collaborates_with` edges. This is the hardest of the queued DDD cycles because it changes the §7A.3 catalog schema, all 15 catalog entries, the JSON Schema, and the validation checks.

Deferred to later cycles: context map projection, consolidated glossary file, and design-principles grounding notes (strategic classification + DDD correspondence appendix).

## Decisions Already Made (2026-07-15)

| # | Decision | Resolution |
|---|---|---|
| D1 | Trigger field shape | Replace `"on": string` with required `trigger: <token>` + optional `note: string` |
| D2 | Relationship field | Required on every `collaborates_with` edge |
| D3 | Relationship vocabulary | AOS-native tokens (`informs`, `requests`, `conforms-to`, `gated-by`) + DDD aliases documented in a glossary table |
| D4 | Trigger token derivation | Derive from existing catalog `"on":` prose + §17 workflow triggers + §24 escalation causes; one token per distinct event, no speculative tokens (est. 12–20) |
| D5 | Enforcement | Full closed-enum enforcement in `catalog.schema.json` and V-checks; new token = catalog edit + `catalog_version` bump |
| D6 | Global escalation edges (P3, 2026-07-15) | Kept as a documented global rule (catalog header comments + §24); the 4 §24-cause tokens (`permission-conflict`, `privacy-risk`, `sensitive-memory-question`, `routing-conflict`) join the V14 carve-out alongside workflow tokens |
| D7 | Reciprocal-edge relationships (2026-07-15) | Pairs match by trigger token; sending side carries `requests`/`informs`, receiving (`handoff-from`) side carries `conforms-to` (§18.4 handoff format) — so `conforms-to` has real uses and V14 covers relationships |
| D8 | Catalog `spec_version` timing (2026-07-15) | Set to anticipated 2.4.0 during P3; P7 confirms |
| D9 | Inbox combined escalation (2026-07-15) | Split into two edges (`ownership-unclear`, `priority-conflict`) — total edges now 43 |

## Relationship Token Semantics (normative once implemented)

| Token | Meaning | DDD equivalent | Example |
|---|---|---|---|
| `informs` | Producer publishes; consumer reads, no change authority | Supplier / published language | Review Agent → Security Agent audit findings |
| `requests` | Consumer may propose changes; owner decides | Customer/Supplier | Chief of Staff → Security Agent tool-matrix change recommendation (§22); Feedback Agent upstream channel |
| `conforms-to` | Consumer adopts the owner's format/rules as-is | Conformist | Agents conforming to Memory Agent's memory-entry schema, §18.4 handoff template |
| `gated-by` | Interaction passes through the owner's approval boundary; owner can block | (no direct DDD term; nearest: anti-corruption layer / gatekeeper) | Tool use gated by Security's tool access matrix; retirement gated by user `Proceed` |

Semantic implications (candidates for later V-checks, not in this cycle's scope): a `requests` edge implies a feedback path; a `conforms-to` edge implies migration handling in the owner's §7B.3 Update section; `gated-by` edges must correspond to §3.2 approval-required actions.

## Implementation Steps (in execution order)

### P1. Define the vocabularies (spec §7A.6 + trigger inventory)

1. Inventory every `"on":` string in `design-spec/agent-catalog.yaml` (all 15 entries, including comment-modeled escalation edges), the §17.1–17.8 workflow triggers, and the §24 escalation causes.
2. Mint one kebab-case token per distinct event (target 12–20; every token must have ≥1 using edge). Expected candidates: `permission-conflict`, `privacy-risk`, `routing-conflict`, `priority-conflict`, `matrix-change-recommended`, `catalog-validation-complete`, `daily-startup`, `end-of-day`, `weekly-review`, `monthly-review`, `inbox-item-received`, `project-kickoff`, `decision-captured`, `memory-review`, `handoff-created`, `agent-built`, `feedback-captured`, `enhancement-candidate`. Final list comes from the inventory, not this guess.
3. Add to §7A.6 catalog file shape, under `vocabulary:`:
   - `relationships: [informs, requests, conforms-to, gated-by]`
   - `triggers: [<derived list>]`
4. State the versioning rule: adding a relationship or trigger token is a catalog edit (`catalog_version` bump), mirroring the existing rule for `domains`.

### P2. Change the edge schema (spec §7A.3)

Replace the `collaborates_with` entry schema with:

```yaml
collaborates_with:
  - agent: slug                       # must resolve to a real slug (V5)
    direction: handoff-to | handoff-from | escalates-to
    relationship: informs | requests | conforms-to | gated-by   # REQUIRED; from vocabulary.relationships
    trigger: <token>                  # REQUIRED; from vocabulary.triggers
    note: string                      # OPTIONAL; nuance only, never the sole carrier of meaning
```

The `"on":` field is removed. Update the §7A.3 comment about YAML `on` quoting accordingly (no longer needed). Update the §7A.2 controlled-vocabulary rule to name all three vocabularies (domains, relationships, triggers).

### P3. Update all 15 catalog entries (design-spec/agent-catalog.yaml)

1. For every edge on every entry: map its former `"on":` prose to a `trigger:` token and assign a `relationship:`; move residual nuance into `note:`.
2. Reciprocity: ensure every `handoff-to` has a matching `handoff-from` with the **same trigger token** on the counterpart entry (this is what makes V5 mechanical).
3. Convert comment-modeled edges (e.g. "all agents escalate-to security-agent") consistently — either keep as a documented global rule or materialize as explicit edges; decide during implementation and record in the revision history (flag: this is the one known sub-decision left open).
4. Bump `catalog_version` (MINOR) and set `spec_version` to the new spec version from P6.

### P4. Extend validation (spec §7A.5, §27 + derived CI artifacts)

1. **V5 (extended):** every edge's `agent` resolves; `relationship` and `trigger` are members of their vocabularies; reciprocal edges match by trigger token, not prose reading.
2. **V14 (new):** every `vocabulary.relationships` and `vocabulary.triggers` token is used by at least one edge (no dead tokens).
3. Update `design-spec/catalog.schema.json`: closed enums for `relationship` and `trigger` (enum list generated from the vocabulary — keep the schema a *rendering* per §1.6.1/§7A.5), required-field additions, removal of `on`.
4. Note in §7A.5 that `scripts/validate-catalog.py` must cover the extended V5 surface and V14. (The script lives in the GitHub repo, not this workspace; the spec text records the requirement.)

### P5. Add the relationship glossary table (spec §7A)

Add a short subsection (proposed: **§7A.7 Relationship Vocabulary**) containing the token-semantics table above, including the DDD-equivalent column (decision D3). Note that this table will migrate into the consolidated glossary when that later cycle lands.

### P6. Downstream touch points and cross-references

1. **§18.4 Handoff Summary:** the `Trigger` field uses `vocabulary.triggers` tokens (same event language across catalog, workflows, logs).
2. **§23 Agent Collaboration Rules / §24 Escalation Model:** add cross-references stating that collaboration edges are typed by `relationship` and `trigger` per §7A.3/§7A.6–7A.7; no change to the approved decisions themselves.
3. **§7.4 governance projection:** verify no wording changes needed (it renders catalog identity, not edges; expected no-op — confirm).

### P7. Versioning and history

1. Bump `spec_version` in the main spec frontmatter (MINOR — additive schema change) and update `last_updated`.
2. Propagate `spec_version` to `agent-catalog.yaml` header.
3. Add one consolidated row to `design-spec/aos-factory-revision-history.md` (top of table): new `spec_version` | date | summary of this cycle (one row for the whole cycle per the revision-history rules).

### P8. Verification pass

1. Re-read changed sections for internal consistency (§7A.2/7A.3/7A.5/7A.6/7A.7, §18.4, §23, §24).
2. Validate `agent-catalog.yaml` against the updated `catalog.schema.json` (run a local jsonschema check in the sandbox).
3. Manually check V5 reciprocity and V14 no-dead-tokens across the finished catalog.
4. Confirm no remaining `"on":` fields anywhere in spec or catalog (grep).

## Files Touched

| File | Change |
|---|---|
| `design-spec/aos-factory-design-specification.md` | §7A.2, §7A.3, §7A.5, §7A.6, new §7A.7, §18.4, §23, §24 cross-refs, frontmatter version |
| `design-spec/agent-catalog.yaml` | vocabularies, all 15 entries' edges, version headers |
| `design-spec/catalog.schema.json` | enums, required fields, remove `on` |
| `design-spec/aos-factory-revision-history.md` | one new row |

## Implementation Progress Checklist

Mark items as work completes; the cycle is done only when P8 passes and the revision-history row is logged.

- [x] **P1 — Vocabularies defined** (2026-07-15)
  - [x] Trigger inventory completed (catalog `"on":` prose + §17 + §24) — mapping table in scratchpad `p1-trigger-inventory.md`; all 42 `"on":` fields accounted for
  - [x] Final trigger token list minted — 29 tokens: 8 workflow-sourced (§17) + 21 edge/§24-sourced. Per user decision (2026-07-15), workflow tokens are first-class without a using edge (V14 carve-out in P4); priority-conflict variants normalized to one token with nuance in `note:`
  - [x] §7A.6 updated with `relationships` and `triggers` vocabularies
  - [x] Vocabulary versioning rule stated (incl. workflow-token carve-out)
- [x] **P2 — Edge schema changed (§7A.3)** (2026-07-15)
  - [x] New edge schema in place (`relationship`, `trigger`, `note`; `on` removed)
  - [x] §7A.2 rule extended to all three vocabularies
- [x] **P3 — Catalog entries updated (all 15)** (2026-07-15)
  - [x] Open item resolved: global rule kept, not explicit edges (D6)
  - [x] 5 governance entries converted
  - [x] 10 productive entries converted (incl. D9 edge split; 43 edges total)
  - [x] Reciprocity by trigger token verified entry-by-entry (scripted check: 16 pairs, 0 unmatched, 0 dead tokens, all 4 relationships used)
  - [x] `catalog_version` (1.3.0) and `spec_version` (2.4.0, per D8) headers bumped
- [x] **P4 — Validation extended** (2026-07-15)
  - [x] V5 extension text in §7A.5 (vocabulary membership + reciprocity by trigger token)
  - [x] V14 added (with §7A.6 carve-out; §27 line updated to "V1-V8 and V14")
  - [x] `catalog.schema.json` updated (relationship/trigger closed enums, required fields, `note` optional, `on` removed; vocabulary block requires all three lists) — catalog validated against it (15 agents, pass)
  - [x] `validate-catalog.py` requirement noted in §7A.5 (reciprocity-by-trigger + V14 incl. carve-out)
- [x] **P5 — §7A.7 Relationship Vocabulary table added** (2026-07-15; incl. DDD-equivalent column, deferred-V-check note, glossary-migration note)
- [ ] **P6 — Downstream touch points**
  - [ ] §18.4 Trigger field references `vocabulary.triggers`
  - [ ] §23/§24 cross-references added
  - [ ] §7.4 confirmed no-op
- [ ] **P7 — Versioning and history**
  - [ ] Spec frontmatter `spec_version` + `last_updated` bumped
  - [ ] Revision-history row added
- [ ] **P8 — Verification pass**
  - [ ] Consistency re-read of all changed sections
  - [ ] Catalog validates against updated JSON Schema (sandbox run)
  - [ ] V5 reciprocity + V14 no-dead-tokens checked
  - [ ] Grep confirms no remaining `"on":` fields

## Open Item

- ~~P3 step 3: represent "all agents escalate-to security-agent" as a global rule or explicit per-entry edges~~ — resolved 2026-07-15 as D6 (global rule + V14 carve-out).

## Approval

No changes are made until the user types exactly: `Proceed`
