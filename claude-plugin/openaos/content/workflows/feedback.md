---
title: Feedback Workflow
file_type: workflow
openaos_version: 3.0.0
created_date: 2026-07-17
last_updated: 2026-07-17
status: active
---
# Feedback Workflow

## Purpose
Send a bug report or improvement suggestion to the openaos project team —
scrubbed, previewed, and only ever sent with your explicit approval. This
workflow is the privacy boundary of the system: nothing leaves the machine
without scrub + preview + `Proceed`.

## When to Use
Whenever something didn't work or could work better ("I want to report a
bug", "I have a suggestion"), and for candidates accepted during the
monthly review.

## Inputs
Your description of the issue or idea; optionally the relevant run context.

## Outputs
An entry in `/logs/feedback-log.md` (Type, Status, Scrub, Summary, Sent);
if approved, an email to openaos@neoclarity.ai.

## Steps
1. **Capture** — record the feedback as a log entry, status `captured`.
2. **Scrub** — remove names, file contents, memory quotes, and anything
   identifying; keep only what the project team needs to act. Mark the
   entry's Scrub field.
3. **Preview** — show exactly what would be sent, and to whom.
4. **Send on `Proceed`** — email openaos@neoclarity.ai only when you type
   exactly `Proceed`; anything short is a hold. Record the outcome in the
   entry's Sent field.
5. **Offline fallback** — if sending is unavailable, set the entry to
   `staged` and prompt you to send it manually later.

## Decision Points
Whether context details survive the scrub (when in doubt, scrub them out).

## Approval Gates
The send itself — always, with no exception. A hold leaves the entry staged
and nothing sent.

## Escalation Triggers
If the scrubbed preview still contains anything potentially identifying,
stop and ask before proceeding to the send step.

## Completion Criteria
The entry exists in the feedback log with an accurate Status and Sent
field — whether sent, staged, or held.
