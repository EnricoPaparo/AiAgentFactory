# Agent Package: knowledge-evolution-human-gate-reviewer-input

## Metadata

- package-id: knowledge-evolution-human-gate-reviewer-input
- project-id: pilot-agent-package-validation
- agent-role: Knowledge Evolution
- agent-source:
  - type: permanent-agent
  - reference: agents/knowledge-evolution/knowledge-evolution.md
- assigned-capabilities:
  - capabilities/documentation.md

## Mission

Evaluate the proposed Knowledge Candidate about explicitly including `standards/human-gate-standard.md` in Reviewer Agent Packages when Human Gate semantics are part of the review scope.

## Task

Review `projects/pilot-agent-package-validation/knowledge-candidates/explicit-human-gate-standard-input-for-reviewers.md`, decide whether it should be accepted, rejected or sent back for revision, update the candidate decision fields, and produce a handoff to the Human Maintainer.

## Inputs

- `agents/knowledge-evolution/knowledge-evolution.md`
- `standards/knowledge-candidate-standard.md`
- `standards/agent-package-standard.md`
- `standards/human-gate-standard.md`
- `runtime-adapters/codex.md`
- `runtime-adapters/manual-execution.md`
- `projects/pilot-agent-package-validation/knowledge-candidates/explicit-human-gate-standard-input-for-reviewers.md`
- `projects/pilot-agent-package-validation/generated-agents/reviewer-agent-package.md`
- `projects/pilot-agent-package-validation/handoffs/documentation-writer-to-reviewer.md`
- `projects/pilot-agent-package-validation/reviews/checklist-review.md`
- `projects/pilot-agent-package-validation/handoffs/reviewer-to-pipeline-supervisor.md`
- `archetypes/reviewer.md`
- `agents/knowledge-compiler/knowledge-compiler.md`

## Expected Outputs

- Updated `projects/pilot-agent-package-validation/knowledge-candidates/explicit-human-gate-standard-input-for-reviewers.md`
- `projects/pilot-agent-package-validation/handoffs/knowledge-evolution-to-maintainer.md`

## Responsibilities

- Verify that the candidate is concrete, evidenced and generalizable.
- Decide candidate status according to `standards/knowledge-candidate-standard.md`.
- If accepted, identify exact integration targets and proposed change type.
- Preserve the distinction between local project evidence and permanent knowledge.
- Produce a handoff explaining the decision and next action.

## Boundaries

- Do not modify permanent standards, agents, archetypes, capabilities or runtime adapters.
- Do not integrate the candidate automatically.
- Do not change prior pilot outputs, review reports or handoffs.
- Do not decide unrelated Knowledge Candidates.
- Do not close or reopen the pilot project.

## Tools

- Repository file reading and editing for the candidate and handoff only.

## Workflow

1. Read the Knowledge Evolution permanent agent definition.
2. Read the Knowledge Candidate Standard.
3. Read the candidate and all evidence files.
4. Evaluate utility, risk, generalizability and impact.
5. Update the candidate status, review notes, decision and integration target.
6. Produce handoff to Human Maintainer with recommended next action.

## Handoff Requirements

Produce `projects/pilot-agent-package-validation/handoffs/knowledge-evolution-to-maintainer.md` conforming to `standards/handoff-standard.md`.

## Definition of Done

- Candidate has a non-Pending status.
- Candidate review notes explain the decision.
- Candidate decision is explicit and justified.
- Candidate integration target is specific if accepted.
- Handoff to Human Maintainer exists.
- No permanent knowledge files are modified.

## Runtime Hints

Use `runtime-adapters/codex.md` and `runtime-adapters/manual-execution.md`.

## Risk Notes

- The candidate may be useful but too broad if applied to every Reviewer package.
- The recommended integration should be conditional: only when Human Gate semantics are part of the review scope.

## Review Gates

- Human Maintainer reviews the Knowledge Evolution handoff before any permanent integration.

## Escalation Rules

- Block if the candidate file or evidence files are missing.
- Block if deciding the candidate requires modifying permanent knowledge immediately.

## Knowledge Candidate Triggers

None. This package evaluates an existing Knowledge Candidate.
