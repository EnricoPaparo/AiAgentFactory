# Bootstrap Execution Blueprint: ceramic-cozy-landing

## Requirements Source

projects/ceramic-cozy-landing/input/initial-request.md

## Solution Source

None. This bootstrap blueprint exists only to run the Requirement Analyst before a Solution Blueprint exists.

## Execution Goal

Produce a Requirements Blueprint from the initial user request.

## Required Agents

- Requirement Analyst: clarify project goal, requirements, constraints, assumptions, ambiguities, out of scope and acceptance criteria.

Sorgenti:

- Requirement Analyst: permanent agent `agents/requirement-analyst/requirement-analyst.md`.

## Agent Inputs

- Requirement Analyst:
  - `projects/ceramic-cozy-landing/input/initial-request.md`
  - `agents/requirement-analyst/requirement-analyst.md`
  - `standards/requirements-blueprint-standard.md`
  - `standards/handoff-standard.md`
  - `standards/human-gate-standard.md`
  - `projects/ceramic-cozy-landing/human-gates/approve-requirements.md`

## Agent Outputs

- Requirement Analyst:
  - `projects/ceramic-cozy-landing/blueprints/requirements-blueprint.md`
  - `projects/ceramic-cozy-landing/handoffs/requirement-analyst-to-architect.md`

## Workflow

1. Execute Requirement Analyst Agent Package with Codex Runtime Adapter.
2. Requirement Analyst creates Requirements Blueprint.
3. Requirement Analyst creates handoff to Architect.
4. Human Maintainer reviews `approve-requirements` before Solution Blueprint generation.

## Handoffs

- Requirement Analyst to Architect.

## Review Gates

- Requirements completeness review by Human Maintainer through Human Gate.

## Human Gates

- approve-requirements:
  - status: Pending
  - blocking-scope: solution blueprint generation
  - decision-owner: Human Maintainer

## Completion Criteria

- Requirements Blueprint exists and conforms to `standards/requirements-blueprint-standard.md`.
- Requirement Analyst handoff exists and conforms to `standards/handoff-standard.md`.
- No architecture or stack decisions are introduced by Requirement Analyst.

## Escalation Rules

- Block if the initial request is missing.
- Block if a Human Gate `Pending` applies to the current task.
- Record subjective visual interpretation as assumptions or ambiguities.

## Runtime Preferences

Use `runtime-adapters/codex.md`.

## Knowledge Candidate Plan

Create Knowledge Candidate only if the requirements process reveals reusable improvements to standards, agents, archetypes, capability or runtime adapter.
