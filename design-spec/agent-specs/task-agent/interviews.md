---
title: Task Agent — Agent Interviews
file_type: interview_script
slug: task-agent
spec_version: 2.4.1
---
# Task Agent — Interviews

## Initialization Interview

```yaml
- id: task-structure
  ask: How do you want tasks structured (priority, due date, source)?
  type: text
  default: priority + due date + source, per the standard task list structure
  skippable: yes
  when: always
  captures: task-config.md task structure

- id: at-risk
  ask: What counts as "at risk", and when should it be surfaced?
  type: text
  default: due within 48 hours and not started; surfaced in the daily startup brief (§17.1)
  skippable: yes
  when: always
  captures: task-config.md at-risk rules

- id: handoffs
  ask: Which handoffs matter (Calendar for time, Project Manager for projects, Automation for recurring)?
  type: text
  default: all three, when the target agent is installed (§23)
  skippable: yes
  when: always
  captures: task-config.md collaboration rules
```

## Update Interview

No questions — no migration required at this release.
