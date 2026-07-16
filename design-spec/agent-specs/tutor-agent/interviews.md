---
title: Tutor Agent — Agent Interviews
file_type: interview_script
slug: tutor-agent
spec_version: 2.4.2
---
# Tutor Agent — Interviews

## Initialization Interview

```yaml
- id: learning-goal
  ask: What do you want to learn, and at what level?
  type: text
  default: none
  skippable: no
  when: always
  captures: tutor memory (learning goals)

- id: learning-style
  ask: What learning style and format do you prefer (explanations, practice, worked examples)?
  type: text
  default: mixed — plain-language explanations with worked examples and practice questions (§32)
  skippable: yes
  when: always
  captures: tutor memory (style preferences)

- id: web-search
  ask: Should the agent use web search (if granted in the matrix), or only provided materials?
  type: choice
  options: [provided materials only, web search if granted]
  default: provided materials only
  skippable: yes
  when: always
  captures: tutor-config.md tool use (§22)

- id: progress-tracking
  ask: How should progress be tracked and surfaced?
  type: text
  default: tracked in agent memory; stale or overdue topics surfaced during reviews
  skippable: yes
  when: always
  captures: tutor-config.md progress rules
```

## Update Interview

No questions — no migration required at this release.
