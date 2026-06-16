# Artifact Index: ceramirycs

## Core Artifacts

| Artifact | Path | Status | Notes |
|---|---|---|---|
| Initial request | `input/initial-request.md` | Completed | Preserved user idea. |
| Factory state | `factory-state.json` | Active | Waiting for final delivery approval. |
| Project status | `project-status.md` | Active | Human-readable status. |
| Requirements Blueprint | `blueprints/requirements-blueprint.md` | Approved | Gate `approve-requirements`. |
| Solution Blueprint | `blueprints/solution-blueprint.md` | Approved | Gate `approve-solution-blueprint`. |
| Execution Blueprint | `blueprints/execution-blueprint.md` | Approved | Gate `approve-execution-plan`. |
| Site deliverable | `deliverables/site/` | Completed | Static two-page site. |
| Site review | `reviews/site-review.md` | Completed | Reviewer output. |
| Pipeline supervisor report | `reviews/pipeline-supervisor-report.md` | Completed | Pre-final gate check. |

## Approved Summaries

| Summary | Source | Gate | Status |
|---|---|---|---|
| `summaries/requirements-summary.md` | `blueprints/requirements-blueprint.md` | `approve-requirements` | Approved |
| `summaries/solution-summary.md` | `blueprints/solution-blueprint.md` | `approve-solution-blueprint` | Approved |
| `summaries/execution-summary.md` | `blueprints/execution-blueprint.md` | `approve-execution-plan` | Approved |

## Runtime Packets

| Packet | Agent package | Status |
|---|---|---|
| `runtime-packets/website-builder.json` | `generated-agents/website-builder-agent-package.md` | Used |
| `runtime-packets/site-reviewer.json` | `generated-agents/site-reviewer-agent-package.md` | Used |

## Run Records

| Record | Action | Status |
|---|---|---|
| `run-records/` | operational audit trail | Ready |

## Open Gate

- `human-gates/approve-final-delivery.md`: Pending; blocks project closure.
