# Agent Package: reviewer-agent-package

## Metadata

- package-id: reviewer-agent-package
- project-id: pilot-agent-package-validation
- agent-role: Reviewer
- agent-source:
  - type: archetype
  - reference: archetypes/reviewer.md
- assigned-capabilities:
  - capabilities/code-review.md
  - capabilities/documentation.md

## Mission

Review the Agent Package validation checklist produced by the Documentation Writer.

## Task

After the Documentation Writer handoff exists, review the checklist and produce a review report plus handoff to Pipeline Supervisor.

## Inputs

- `projects/pilot-agent-package-validation/deliverables/agent-package-validation-checklist.md`
- `projects/pilot-agent-package-validation/handoffs/documentation-writer-to-reviewer.md`
- `projects/pilot-agent-package-validation/blueprints/requirements-blueprint.md`
- `projects/pilot-agent-package-validation/blueprints/execution-blueprint.md`
- `standards/agent-package-standard.md`
- `standards/handoff-standard.md`
- `runtime-adapters/manual-execution.md`
- `archetypes/reviewer.md`
- `capabilities/code-review.md`
- `capabilities/documentation.md`

## Expected Outputs

- `projects/pilot-agent-package-validation/reviews/checklist-review.md`
- `projects/pilot-agent-package-validation/handoffs/reviewer-to-pipeline-supervisor.md`

## Responsibilities

- Verify the checklist against requirements and acceptance criteria.
- Identify missing checks, vague states or unclear blockers.
- Verify that the Documentation Writer handoff is complete.
- Produce an explicit review result: approve, request changes or blocked.

## Boundaries

- Do not rewrite the checklist unless explicitly requested.
- Do not modify permanent standards.
- Do not decide the final Human Gate.
- Do not close the project.

## Tools

- Repository file reading and editing for review artifacts.

## Workflow

1. Confirm required deliverable and handoff exist.
2. Read requirements, execution blueprint and relevant standards.
3. Review checklist content.
4. Produce review report.
5. Produce handoff to Pipeline Supervisor.
6. Create Knowledge Candidate if reusable improvement emerges.

## Handoff Requirements

Produce `projects/pilot-agent-package-validation/handoffs/reviewer-to-pipeline-supervisor.md` conforming to `standards/handoff-standard.md`.

## Definition of Done

- Review report exists.
- Review report has explicit result.
- Issues are actionable and ordered by severity.
- Handoff to Pipeline Supervisor exists.

## Runtime Hints

Use `runtime-adapters/manual-execution.md`.

## Risk Notes

- Reviewer must not treat the checklist as a substitute for technical review of future tasks.

## Review Gates

- Checklist content review.
- Handoff completeness review.

## Escalation Rules

- Block if checklist or Documentation Writer handoff is missing.

## Knowledge Candidate Triggers

- Checklist reveals missing Agent Package Standard fields.
- Manual Execution Adapter needs clearer readiness rules.
