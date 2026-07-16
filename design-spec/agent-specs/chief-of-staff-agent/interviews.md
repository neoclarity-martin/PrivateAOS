---
title: Chief of Staff Agent — Agent Interviews
file_type: interview_script
slug: chief-of-staff-agent
spec_version: 2.4.1
---
# Chief of Staff Agent — Interviews

## Initialization Interview

```yaml
- id: priority-rules
  ask: What are your default prioritization rules?
  type: text
  default: no standing rules — escalate the first conflict and capture the ruling as a preference
  skippable: yes
  when: always
  captures: chief-of-staff memory (priority rules); /memory/preferences.md when global

- id: coordination-preferences
  ask: Any standing coordination preferences (e.g. how much to route vs. handle directly)?
  type: text
  default: push work down to specialized agents; coordinate rather than perform (§2.2, §7.6)
  skippable: yes
  when: always
  captures: chief-of-staff-config.md coordination notes
```

## Update Interview

No questions — no migration required at this release.
