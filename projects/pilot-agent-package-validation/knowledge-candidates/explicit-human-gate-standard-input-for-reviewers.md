# Knowledge Candidate: explicit-human-gate-standard-input-for-reviewers

## Metadata

- candidate-id: explicit-human-gate-standard-input-for-reviewers
- project-id: pilot-agent-package-validation
- status: Proposed
- proposed-by: Reviewer
- target-area: process rule

## Proposal

When a Reviewer Agent Package must review checklist content that validates Human Gate states or blocking behavior, include `standards/human-gate-standard.md` explicitly in the package inputs.

## Context

During the pilot review, the checklist contained Human Gate status and blocking-scope checks. The upstream handoff asked the Reviewer to verify against `standards/human-gate-standard.md`, but the Reviewer Agent Package input list did not include that standard.

## Motivation

Explicitly listing the Human Gate standard prevents hidden review dependencies and makes Manual Execution preflight stricter. A reviewer who follows only the Agent Package input list should still receive every authoritative standard needed for the assigned review.

## Generalizability

Medium. This applies to reviewer packages for checklist, process, handoff or runtime-adapter outputs where Human Gate behavior is part of the review scope.

## Risk

Low. The rule could add unnecessary input files to reviewer packages that only mention Human Gates incidentally, so it should apply only when Human Gate semantics are part of the review criteria.

## Recommended Action

Knowledge Evolution should evaluate whether to add this as a process rule for Agent Package generation or as guidance in reviewer archetype usage notes.

## Evidence

- `projects/pilot-agent-package-validation/generated-agents/reviewer-agent-package.md`
- `projects/pilot-agent-package-validation/handoffs/documentation-writer-to-reviewer.md`
- `projects/pilot-agent-package-validation/reviews/checklist-review.md`

## Review Notes

Pending Knowledge Evolution review.

## Decision

Pending.

## Integration Target

- `archetypes/reviewer.md`
- Agent Package generation process rules

