# Knowledge Candidate: explicit-human-gate-standard-input-for-reviewers

## Metadata

- candidate-id: explicit-human-gate-standard-input-for-reviewers
- project-id: pilot-agent-package-validation
- status: Integrated
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

Accepted by Knowledge Evolution on 2026-06-16.

The candidate is concrete, evidenced and appropriately scoped. The pilot evidence shows a real hidden dependency: the Reviewer Agent Package required review of Human Gate states and blocking behavior, and the upstream handoff explicitly asked for verification against `standards/human-gate-standard.md`, but that standard was not listed in the Reviewer package inputs.

Utility is high for package executability because a runtime adapter expects the Agent Package input list to be sufficient for preflight. Generalizability is medium rather than universal: the rule should apply only when Human Gate semantics are part of the review criteria, not whenever a project merely contains a Human Gate. Risk is low if integrated as conditional package-generation guidance.

## Decision

Integrated.

Knowledge Evolution accepted this as a reusable process rule, and the Human Maintainer approved integration into permanent knowledge. Future Reviewer Agent Packages should explicitly include `standards/human-gate-standard.md` when the review scope requires validating Human Gate states, blocking scope, waiting behavior, or downstream execution constraints.

The integration is conditional, not universal: the Human Gate Standard is required only when Human Gate semantics are part of the assigned review scope.

## Integration Target

- `agents/knowledge-compiler/knowledge-compiler.md`: add conditional package-generation guidance so Knowledge Compiler includes `standards/human-gate-standard.md` in Reviewer Agent Package inputs when Human Gate semantics are part of the assigned review scope.
- `archetypes/reviewer.md`: add a usage note or input expectation that Human Gate Standard is required when a Reviewer evaluates Human Gate status, blocking behavior or gate-driven workflow readiness.

## Integration Evidence

Integrated on 2026-06-16:

- `agents/knowledge-compiler/knowledge-compiler.md` now requires standards needed for task verification to be included in Agent Package inputs and specifically calls out Reviewer packages that evaluate Human Gate semantics.
- `archetypes/reviewer.md` now lists required standards as expected inputs and requires `standards/human-gate-standard.md` when reviewing Human Gate behavior.
