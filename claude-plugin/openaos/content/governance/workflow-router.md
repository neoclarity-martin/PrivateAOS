---
title: Workflow Router
file_type: router
openaos_version: 3.2.0
created_date: 2026-08-02
last_updated: 2026-08-02
status: active
---
# Workflow Router

## Purpose
This table is how an agent decides which workflow to load. It is the single
place a workflow's triggers are recorded — workflow files themselves no
longer carry a "When to Use" section, so there is nothing to keep in sync.

The prompts in the left column are **examples, not exact commands**. Real
prompts will be worded differently. Match on meaning, pick the single most
likely workflow, and load only that file. If nothing matches, ask the user
what they want rather than guessing or loading several workflows to compare.

Rows are added by `build-workflow` when a workflow is created and updated by
`refine-workflow` when its triggers change. This file is part of the
governance layer and is not removable.

## Routes

| Example Prompts | File to Load |
|---|---|
| "run my daily startup", "start my day", "what matters today?" | /workflows/daily-startup.md |
| "wrap up the day", "end of day", "what changed today?" | /workflows/end-of-day.md |
| "do a weekly review", "what needs follow-up soon?", "next week" | /workflows/weekly-review.md |
| "do a monthly review", "monthly cleanup", "is this still aimed right?" | /workflows/monthly-review.md |
| "report a bug", "send feedback", "I have a suggestion" | /workflows/feedback.md |
