---
title: Memory Agent — Agent Interviews
file_type: interview_script
slug: memory-agent
spec_version: 2.4.1
---
# Memory Agent — Interviews

## Initialization Interview

```yaml
- id: memory-seeds
  ask: Any durable user facts or preferences to seed the global memory files with?
  type: text
  default: none — seed empty, never fabricate
  skippable: yes
  when: always
  captures: /memory global files initial entries (§20.1)

- id: sensitive-categories
  ask: Are there categories of information you consider sensitive, requiring approval before storage?
  type: text
  default: standard §20.3 sensitivity rules unchanged
  skippable: yes
  when: always
  captures: memory-config.md sensitivity rules (coordinated with Security Agent)

- id: review-cadence
  ask: Preferred memory review cadence beyond the default weekly-light / monthly-deep?
  type: choice
  options: [default (weekly light, monthly deep), lighter, heavier]
  default: default (weekly light, monthly deep)
  skippable: yes
  when: always
  captures: memory-config.md review cadence (§17.8, §20.3)
```

## Update Interview

No questions — no migration required at this release.
