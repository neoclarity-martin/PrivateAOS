---
title: Writing Agent — Agent Interviews
file_type: interview_script
slug: writing-agent
spec_version: 2.4.1
---
# Writing Agent — Interviews

## Initialization Interview

```yaml
- id: content-kinds
  ask: What kinds of content will this agent draft, and for what audiences?
  type: text
  default: none
  skippable: no
  when: always
  captures: writing-config.md scope

- id: voice
  ask: What voice, tone, and formatting conventions should drafts follow?
  type: text
  default: learn from the user's existing writing; confirm before first external use
  skippable: yes
  when: always
  captures: writing memory (voice/style preferences); /memory/preferences.md when global

- id: research-input
  ask: Should research come from the Research Agent when installed (§23)?
  type: boolean
  default: yes
  skippable: yes
  when: always
  captures: writing-config.md collaboration rules
```

## Update Interview

No questions — no migration required at this release.
