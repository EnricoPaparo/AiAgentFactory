# Agent Package: documentation-writer-agent-package

## Metadata

- package-id: documentation-writer-agent-package
- project-id: pilot-agent-package-validation
- agent-role: Documentation Writer
- agent-source:
  - type: archetype
  - reference: archetypes/documentation-writer.md
- assigned-capabilities:
  - capabilities/documentation.md

## Mission

Create an operational checklist for validating whether an Agent Package is ready for Manual Execution.

## Task

Produce `projects/pilot-agent-package-validation/deliverables/agent-package-validation-checklist.md` and a handoff to Reviewer.

## Inputs

- `projects/pilot-agent-package-validation/blueprints/requirements-blueprint.md`
- `projects/pilot-agent-package-validation/blueprints/solution-blueprint.md`
- `projects/pilot-agent-package-validation/blueprints/execution-blueprint.md`
- `standards/agent-package-standard.md`
- `standards/human-gate-standard.md`
- `standards/handoff-standard.md`
- `runtime-adapters/manual-execution.md`
- `archetypes/documentation-writer.md`
- `capabilities/documentation.md`

## Expected Outputs

- `projects/pilot-agent-package-validation/deliverables/agent-package-validation-checklist.md`
- `projects/pilot-agent-package-validation/handoffs/documentation-writer-to-reviewer.md`

## Responsibilities

- Produce a practical checklist, not a tutorial.
- Cover required Agent Package fields.
- Include Human Gate readiness checks.
- Include handoff readiness checks.
- Define final validation states: `ready`, `incomplete`, `blocked`.
- Record assumptions, limitations and residual risks in the handoff.

## Boundaries

- Do not modify permanent standards.
- Do not implement automation or scripts.
- Do not create the Reviewer output.
- Do not close the project.
- Do not bypass Human Gate rules.

## Tools

- Repository file editing.
- Existing markdown standards and project files.

## Workflow

1. Read all inputs.
2. Check whether any Human Gate `Pending` blocks this task.
3. Draft the checklist deliverable.
4. Verify the checklist against requirements and Agent Package Standard.
5. Create handoff to Reviewer.
6. If a reusable improvement emerges, create a Knowledge Candidate instead of modifying permanent knowledge.

## Handoff Requirements

Produce `projects/pilot-agent-package-validation/handoffs/documentation-writer-to-reviewer.md` conforming to `standards/handoff-standard.md`.

## Definition of Done

- Checklist deliverable exists.
- Checklist includes required field checks.
- Checklist includes Human Gate checks.
- Checklist includes handoff checks.
- Checklist defines `ready`, `incomplete`, `blocked`.
- Handoff to Reviewer exists.

## Runtime Hints

Use `runtime-adapters/manual-execution.md`.

## Risk Notes

- Risk: checklist duplicates Agent Package Standard too much.
- Risk: checklist validates form but not task quality.

## Review Gates

- Reviewer must verify completeness and usability.

## Escalation Rules

- Block if required standards or blueprints are missing.
- Block if a Human Gate `Pending` applies to this task.

## Knowledge Candidate Triggers

- Missing field in Agent Package Standard.
- Human Gate ambiguity.
- Handoff Standard insufficient for manual execution.
