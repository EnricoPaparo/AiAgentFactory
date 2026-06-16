# Contributing to AiAgentFactory

This document explains how to extend the factory's permanent knowledge: adding capabilities, archetypes, standards, permanent agents, and runtime adapters.

AiAgentFactory follows a **controlled knowledge evolution process**. No change to permanent knowledge should happen without deliberate review. Spontaneous improvements belong in a project's `knowledge-candidates/` folder first.

---

## General Rules

1. **All permanent changes go through review.** Use a Knowledge Candidate during a project run, then promote it via the Knowledge Evolution agent.
2. **Separation of concerns.** Do not put project-specific knowledge in permanent files. Keep temporary work in `projects/<project-id>/`.
3. **No automatic integration.** Even if a change looks obviously correct, it must go through the Knowledge Evolution lifecycle before landing in permanent files.
4. **Minimal but complete.** Every new artifact must satisfy its standard's required fields. Prefer fewer, high-quality files over many shallow ones.
5. **Language.** All documentation is written in **Italian** (existing convention). New contributions must follow the same language.

---

## Naming Conventions

| Type | Convention | Example |
|---|---|---|
| Files and folders | `kebab-case` | `api-security.md`, `knowledge-compiler/` |
| Permanent agents | `agents/<agent-name>/` | `agents/requirement-analyst/` |
| Archetypes | singular noun | `developer.md`, `tester.md` |
| Capabilities | topic or technology | `postgres.md`, `api-security.md` |
| Standards | `<artifact>-standard.md` | `handoff-standard.md` |
| Runtime adapters | runtime name | `claude-code.md`, `langgraph.md` |
| Agent Packages | descriptive pattern | `developer-node-postgres.md` |

---

## How to Add a Capability

A capability is reusable operational knowledge — best practices, checklists, failure modes, risks, and lessons learned for a specific technology, domain, or practice. It is **not** a tutorial.

**Required fields** (defined in `standards/capability-standard.md`):
- Scopo
- Usata da
- Quando si usa
- Contenuto operativo (checklist, pratiche, failure mode, rischi)
- Criteri di revisione
- Limiti

**Steps:**
1. Verify the capability doesn't already exist in `capabilities/`.
2. Create `capabilities/<topic>.md` following `standards/capability-standard.md`.
3. Keep the content operational: checklists and criteria, not generic explanations.
4. If created during a project, save it as a Knowledge Candidate first (`projects/<id>/knowledge-candidates/`), then promote via Knowledge Evolution.

**What belongs in a capability:**
- Specific practices for a technology or domain
- Checklist of things to verify or avoid
- Known failure modes and how to detect them
- Security or performance criteria relevant to the topic

**What does NOT belong in a capability:**
- Generic tutorials or introductions
- Decisions that belong in a blueprint
- Project-specific context

---

## How to Add an Archetype

An archetype is a reusable skeleton for generating temporary agents of a recurring type. It defines role, responsibilities, inputs, outputs, boundaries, and Definition of Done. It does **not** contain specific technical knowledge (that belongs in capabilities).

**Required fields** (follow existing archetypes as reference):
- Scopo
- Natura dell'archetype
- Responsabilità
- Input attesi
- Output attesi
- Limiti
- Capability compatibili
- Handoff richiesto
- Definition of Done
- Failure mode da evitare

**Steps:**
1. Verify the role is genuinely recurring across projects (one-off roles should be ad-hoc agents, not archetypes).
2. Create `archetypes/<role>.md` using existing archetypes as format reference.
3. Do not include project-specific context or technical knowledge in the archetype itself.
4. If created during a project, save it as a Knowledge Candidate first.

---

## How to Add a Runtime Adapter

A runtime adapter defines translation rules from a generic Agent Package to a specific runtime's format and execution model.

**Required sections** (follow `runtime-adapters/manual-execution.md` as reference):
- Scopo
- Quando si usa
- Prerequisiti
- Come tradurre un Agent Package
- Come gestire gli Handoff
- Come gestire i Human Gate
- Anti-pattern da evitare

**Steps:**
1. Create `runtime-adapters/<runtime-name>.md`.
2. The adapter must not contain factory decision logic — it translates, it does not decide.
3. Document all runtime-specific constraints and limitations explicitly.
4. Add the new adapter to the runtime-adapters table in `implementation-status.md`.

---

## How to Update a Standard

Standards are format contracts. Changing them affects all existing and future artifacts that reference them.

**Before changing a standard:**
1. Identify all existing artifacts that follow the standard (search in `projects/`, `agents/`, `archetypes/`).
2. Assess the impact — breaking changes require migrating existing artifacts.
3. Propose the change as a Knowledge Candidate during a project run.
4. Get explicit approval through the Knowledge Evolution agent.

**When changing a standard:**
1. Update the required/optional fields table.
2. Update the format example in the standard.
3. Update the failure mode list if new anti-patterns are identified.
4. Update `implementation-status.md`.

---

## How to Add a Permanent Agent

Permanent agents are governance roles in the factory. Adding one means introducing a new stable responsibility in the factory's core process.

**Required sections** (follow existing agents as reference):
- Identità
- Responsabilità
- Input
- Output
- Limiti
- Workflow
- Definition of Done
- Failure mode da evitare

**Steps:**
1. Verify the role doesn't overlap with an existing permanent agent.
2. Define the agent's single responsibility clearly.
3. Create `agents/<agent-name>/<agent-name>.md`.
4. Update the permanent agents table in `AgentFactory.md` and `implementation-status.md`.
5. New permanent agents require explicit review — propose as Knowledge Candidate first.

---

## Knowledge Candidate Lifecycle

When you identify an improvement during a project:

```text
1. Create the proposal in projects/<project-id>/knowledge-candidates/
   following standards/knowledge-candidate-standard.md

2. Activate the Knowledge Evolution agent to evaluate it

3. If Accepted → Knowledge Evolution integrates it into the correct permanent file(s)

4. If Rejected → reason is recorded in the Knowledge Candidate file; no permanent change

5. Update the Knowledge Candidate status:
   Proposed → Reviewed → Accepted → Integrated
                        → Rejected
```

Never skip this cycle. Even obvious improvements must be evaluated before entering permanent files.

---

## Checklist Before Submitting a Change

- [ ] The change belongs in permanent knowledge (not project-specific)
- [ ] The file follows the correct standard or format reference
- [ ] Naming follows `kebab-case` convention
- [ ] Language is Italian (consistent with existing docs)
- [ ] No overlap with existing permanent agents, archetypes, or capabilities
- [ ] `implementation-status.md` updated if a new artifact was added
- [ ] Change was proposed as a Knowledge Candidate and approved before integration
