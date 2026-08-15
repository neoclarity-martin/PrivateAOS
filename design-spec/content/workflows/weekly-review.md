---
title: Weekly Review Workflow
file_type: workflow
openaos_version: 3.2.0
created_date: 2026-07-17
last_updated: 2026-08-02
status: active
---
# Weekly Review Workflow

## Purpose
Review commitments, decisions, unresolved items, workflow performance,
stale memory signals, and next-week priorities — keeping the workspace
operationally clean so loose ends don't become forgotten obligations.
Review question: **What needs follow-up soon?**

## Inputs
The week's carryover notes, `/logs/decision-log.md`, `/logs/change-log.md`,
`/memory` files (lightweight pass), recent `/outputs`.

## Outputs
A follow-up list for next week; flags (not changes) on stale-looking memory
entries; optionally a refinement suggestion. The follow-up list is rendered
as HTML using `/templates/weekly-review-report-template.html`, saved to
`/outputs/weekly-review-<date>.html`.

## Steps
1. Ask: "What needs follow-up soon?"
2. Review open commitments and unresolved items from the week.
3. Lightweight memory pass: flag entries that look stale for the monthly
   review — never change or delete them here.
4. Workflow performance: if a workflow produced friction this week, suggest
   a refine-workflow session. Suggestion only — never an unprompted edit.
5. Set next-week priorities.
6. Render the follow-up list as HTML using
   `/templates/weekly-review-report-template.html`, saved to
   `/outputs/weekly-review-<date>.html`.

## Decision Points
Follow-up now vs. next week vs. flag for monthly review.

## Approval Gates
None beyond the governance rules — this workflow flags and suggests; it
changes nothing.

## Escalation Triggers
A commitment at risk of being missed is raised immediately.

## Completion Criteria
Follow-up list delivered; stale flags recorded; priorities set.
