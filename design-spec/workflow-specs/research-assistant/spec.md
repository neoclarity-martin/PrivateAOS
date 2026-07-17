---
title: Research Assistant — Builder Spec
file_type: workflow_spec
slug: research-assistant
openaos_version: 3.0.0
---
# Research Assistant — Builder Spec

## Purpose

Scoped, source-disciplined research: turn a question into a cited,
trustworthy answer the user can act on, with findings kept separate from
interpretation.

## Situation Interview

```yaml
- id: research-subjects
  ask: What do you usually need to research? (markets, technical topics, people/organizations, purchases, background for writing)
  type: text
  default: none
  skippable: no
  when: always
  captures: domain framing throughout; example scopes in When to Use

- id: source-preferences
  ask: Are there sources you trust or ones to avoid?
  type: text
  default: none — general source-quality rules apply
  skippable: yes
  when: always
  captures: the source-selection rules in Steps

- id: output-form
  ask: What form should results take? (a short brief, a detailed report, a comparison table, talking points)
  type: choice
  options: [short brief, detailed report, comparison table, talking points]
  default: short brief
  skippable: yes
  when: always
  captures: the Outputs section and the /outputs deliverable format

- id: depth-vs-speed
  ask: When they conflict, do you prefer a fast partial answer or a slower thorough one?
  type: choice
  options: [fast partial, slower thorough]
  default: fast partial, flagging what was not covered
  skippable: yes
  when: always
  captures: the stop rule in Completion Criteria

- id: mistake-cost
  ask: Where would a research mistake cost you most? (acting on a wrong fact, missing an option, stale information)
  type: text
  default: none
  skippable: yes
  when: always
  captures: which verification steps are strengthened
```

## Baked-In Best Practices

```text
- Narrow the scope first: restate the question and the boundaries, and
  confirm them before searching (checkpoint pattern).
- Source discipline: cite every load-bearing claim; separate what a source
  says from what is inferred; never fabricate a source or a quote.
- Findings before synthesis: gather and record findings first, then
  interpret in a clearly separate section.
- Mark confidence and gaps: say what is uncertain, what conflicts, and what
  was not covered.
- Prefer primary and recent sources; note the date of time-sensitive facts.
```

## Default Skeleton

Per §16.3 section: **Inputs** — the question, scope boundaries, and any
user-supplied material. **Steps** — restate/confirm scope, gather findings
with citations, then synthesize into the chosen output form. **Decision
Points** — when to stop (the depth-vs-speed rule), when a conflict warrants
deeper checking. **Approval Gates** — none beyond §3 (research is read-only;
publishing or sending a result is Level 2). **Outputs** — dated deliverable
in /outputs (§4). **Completion Criteria** — question answered within scope,
claims cited, gaps stated.

## Notes

The failure mode to design against is fluent, uncited synthesis — plausible
text with no traceable support. The findings/synthesis separation is the
main guard; keep it even in the "short brief" form.
