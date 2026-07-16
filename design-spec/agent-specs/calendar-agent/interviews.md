---
title: Calendar Agent — Agent Interviews
file_type: interview_script
slug: calendar-agent
spec_version: 2.4.1
---
# Calendar Agent — Interviews

## Initialization Interview

```yaml
- id: calendars-scope
  ask: Which calendar(s) should this agent read, and what read scope is approved?
  type: text
  default: none
  skippable: no
  when: always
  captures: calendar-config.md scope; tool-access-matrix.md request row

- id: scheduling-preferences
  ask: What are your scheduling preferences (working hours, focus blocks, buffers)?
  type: text
  default: standard business hours; propose focus blocks; 15-minute buffers
  skippable: yes
  when: always
  captures: calendar memory (scheduling preferences)

- id: conflict-handling
  ask: How should conflicts and double-bookings be handled?
  type: choice
  options: [propose resolution and ask, always ask first]
  default: propose resolution and ask
  skippable: yes
  when: always
  captures: calendar-config.md conflict rules

- id: modification-gate
  ask: Confirm that all calendar modifications, and any change involving other people, require Proceed.
  type: boolean
  default: yes
  skippable: yes
  when: always
  captures: calendar-config.md approval boundaries (§3.2)
```

## Update Interview

No questions — no migration required at this release.
