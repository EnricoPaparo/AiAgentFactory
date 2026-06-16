# Agent Package Validation Checklist

## Purpose

Use this checklist before running an Agent Package with the Manual Execution Adapter. It validates operational readiness, not the final technical quality of the task output.

## Validation Inputs

- Agent Package path:
- Project workspace:
- Execution Blueprint path:
- Manual Execution Adapter path: `runtime-adapters/manual-execution.md`
- Validator:
- Validation date:

## Required Package Fields

Mark the package `blocked` if any required field is missing or unreadable.

| Check | Result | Notes |
|---|---|---|
| `package-id` exists, is unique within the project and uses kebab-case. |  |  |
| `project-id` matches the project workspace. |  |  |
| `agent-role` is explicit. |  |  |
| `agent-source` identifies an existing archetype or an ad hoc definition in the Execution Blueprint. |  |  |
| `assigned-capabilities` lists concrete capability file paths. |  |  |
| `mission` states the agent objective for this project. |  |  |
| `task` is specific and verifiable. |  |  |
| `inputs` lists all artifacts the agent must read before work. |  |  |
| `expected-outputs` lists concrete deliverable or handoff paths. |  |  |
| `responsibilities` define what the agent must do. |  |  |
| `boundaries` define what the agent must not do. |  |  |
| `tools` identify available or forbidden tools. |  |  |
| `workflow` gives the minimum execution order. |  |  |
| `handoff-requirements` state the required handoff target and standard. |  |  |
| `definition-of-done` contains checkable completion conditions. |  |  |

## Source And Capability Checks

| Check | Result | Notes |
|---|---|---|
| Every `agent-source` reference exists and is readable. |  |  |
| Every assigned capability exists and is readable. |  |  |
| Assigned capabilities are relevant to the task. |  |  |
| Capability instructions do not conflict with package boundaries. |  |  |
| Runtime hints do not override the Manual Execution Adapter or make strategy decisions. |  |  |

## Input Readiness Checks

Mark the package `blocked` if a required input file is missing. Mark it `incomplete` if an input exists but is ambiguous enough to need correction before execution.

| Check | Result | Notes |
|---|---|---|
| Execution Blueprint exists and matches the package `project-id`. |  |  |
| Requirements and Solution Blueprints listed by the package exist, if required by the task. |  |  |
| Standards listed by the package exist and are readable. |  |  |
| Required prior handoffs exist, if the package depends on upstream work. |  |  |
| Input paths are specific enough for an operator to locate them without guessing. |  |  |

## Output And Boundary Checks

| Check | Result | Notes |
|---|---|---|
| Each expected output has a concrete file path or artifact name. |  |  |
| Expected outputs are allowed by the package boundaries. |  |  |
| The package does not require modifying permanent standards unless explicitly approved by the project workflow. |  |  |
| The package does not assign downstream review or closure work to the current agent. |  |  |
| Out-of-scope work is visible in `boundaries` or escalation rules. |  |  |

## Human Gate Checks

Check all Human Gate files in the project workspace before operational work starts.

| Check | Result | Notes |
|---|---|---|
| All Human Gate files are identified. |  |  |
| Each gate status is one of the allowed Human Gate states. |  |  |
| Any `Pending` gate has a clear `blocking-scope`. |  |  |
| No `Pending` gate blocks the current agent task. |  |  |
| If a `Pending` gate blocks the current task, execution is stopped and status is `blocked`. |  |  |
| Gates with `Changes Requested`, `Rejected` or `Expired` are handled according to their return or escalation instructions. |  |  |

## Handoff Readiness Checks

| Check | Result | Notes |
|---|---|---|
| Required handoff recipient is explicit. |  |  |
| Handoff path is concrete. |  |  |
| Handoff must conform to `standards/handoff-standard.md`. |  |  |
| Handoff can identify produced output, involved files, decisions, open issues and residual risks. |  |  |
| Next action after handoff is assignable to a role or agent. |  |  |
| Review gates, if present, identify the reviewer role and artifacts to review. |  |  |

## Definition Of Done Checks

| Check | Result | Notes |
|---|---|---|
| Each Definition of Done item can be verified locally or by the named reviewer. |  |  |
| Required outputs and handoffs are included in the Definition of Done. |  |  |
| Required verification evidence is named, or the reason it is not applicable is clear. |  |  |
| Completion does not depend on a final project closure gate unless the package is responsible for closure. |  |  |

## Final Validation State

Choose exactly one state.

| State | Use When |
|---|---|
| `ready` | All required fields, inputs, source references, capabilities, Human Gate checks, output paths, handoff requirements and Definition of Done checks pass. No `Pending` Human Gate blocks this task. |
| `incomplete` | The package is mostly executable but has correctable gaps such as unclear wording, weak verification criteria, incomplete notes or non-blocking ambiguity. Execution should wait for correction unless the Pipeline Supervisor accepts the risk. |
| `blocked` | A required input/source/capability is missing or unreadable, a `Pending` Human Gate blocks the task, the task contradicts boundaries, expected outputs are not identifiable, or the package cannot be executed without making new strategy or scope decisions. |

## Blocking Versus Correctable Issues

- Blocking issues prevent Manual Execution from starting.
- Correctable issues should be fixed in the Agent Package or project files before execution but do not necessarily indicate a process stop if the Pipeline Supervisor explicitly accepts the risk.
- If a reusable standard, adapter, capability or archetype improvement is discovered, create a Knowledge Candidate instead of editing permanent knowledge directly.
