# Execution Blueprint: pilot-agent-package-validation

## Requirements Source

projects/pilot-agent-package-validation/blueprints/requirements-blueprint.md

## Solution Source

projects/pilot-agent-package-validation/blueprints/solution-blueprint.md

## Execution Goal

Produrre e revisionare una checklist markdown per validare Agent Package prima dell'esecuzione manuale.

## Required Agents

- Documentation Writer: produce il deliverable documentale e handoff.
- Reviewer: verifica il deliverable rispetto a requisiti, standard e handoff.

Sorgenti:

- Documentation Writer: archetype `archetypes/documentation-writer.md`.
- Reviewer: archetype `archetypes/reviewer.md`.

## Agent Inputs

- Documentation Writer:
  - `projects/pilot-agent-package-validation/blueprints/requirements-blueprint.md`
  - `projects/pilot-agent-package-validation/blueprints/solution-blueprint.md`
  - `projects/pilot-agent-package-validation/blueprints/execution-blueprint.md`
  - `standards/agent-package-standard.md`
  - `standards/human-gate-standard.md`
  - `standards/handoff-standard.md`
  - `runtime-adapters/manual-execution.md`
  - `capabilities/documentation.md`
- Reviewer:
  - Documentation Writer handoff.
  - Checklist deliverable.
  - Requirements Blueprint.
  - Agent Package Standard.
  - Manual Execution Adapter.
  - `capabilities/code-review.md`
  - `capabilities/documentation.md`

## Agent Outputs

- Documentation Writer:
  - `deliverables/agent-package-validation-checklist.md`
  - `handoffs/documentation-writer-to-reviewer.md`
- Reviewer:
  - `reviews/checklist-review.md`
  - `handoffs/reviewer-to-pipeline-supervisor.md`

## Workflow

1. Execute Documentation Writer Agent Package with Manual Execution Adapter.
2. Documentation Writer creates checklist deliverable.
3. Documentation Writer creates handoff to Reviewer.
4. Execute Reviewer Agent Package with Manual Execution Adapter.
5. Reviewer creates review report.
6. Reviewer creates handoff to Pipeline Supervisor.
7. Pipeline Supervisor checks completion criteria.
8. Human Maintainer approves final delivery gate or requests changes.

## Handoffs

- Documentation Writer to Reviewer.
- Reviewer to Pipeline Supervisor.

## Review Gates

- Checklist content review.
- Handoff completeness review.

## Human Gates

- approve-final-delivery:
  - status: Pending
  - blocking-scope: project closure
  - decision-owner: Human Maintainer

## Completion Criteria

- Checklist deliverable exists.
- Documentation Writer handoff exists.
- Reviewer report exists.
- Reviewer to Pipeline Supervisor handoff exists.
- Final Human Gate is decided.
- Any reusable lesson is captured as Knowledge Candidate.

## Escalation Rules

- Block if a required input file is missing.
- Block if a Human Gate `Pending` applies to the current task.
- Create Knowledge Candidate if an existing standard is unclear or insufficient.

## Parallelization Notes

None. Reviewer waits for Documentation Writer handoff.

## Runtime Preferences

Use `runtime-adapters/manual-execution.md`.

## Knowledge Candidate Plan

Create Knowledge Candidate only if the pilot reveals a reusable improvement to standards, archetypes, capability, adapter or project template.
