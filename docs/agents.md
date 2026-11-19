# Agent architecture

TamaOS uses small project skills as specialist roles. `AGENTS.md` contains rules that apply broadly; skills load only when their domain is relevant.

## Roles

### Primary agent

Owns the user request, scope, integration, permissions, and final result. It decides whether a specialist is useful and verifies specialist output before it becomes project truth.

### TamaOS Engineer

Invoke `$tamaos-engineer` for engineering-system questions: repository structure, harness, CI, GitHub workflow, toolchains, architectural decision process, reliability, and hardware bring-up procedure.

Its skill lives at `.agents/skills/tamaos-engineer/`. Its system map is maintained in the repository so another session can reconstruct the engineering environment without relying on chat history.

### Future common code agent

Will own language-independent implementation behavior: understanding acceptance criteria, changing code, testing, reviewing, and handing work back to the engineer for integration. It does not exist yet.

### Future language agents

Will add only language-specific knowledge and commands. The first planned language role is Rust. A language agent must use the common code contract and the project `.harness` adapter rather than creating another workflow.

## Delegation contract

A specialist assignment should include:

- concrete outcome;
- bounded scope and non-goals;
- relevant sources;
- expected evidence or artifact;
- permission boundaries for writes and external actions.

Specialists should not edit overlapping files in parallel. The primary agent owns integration.

## Knowledge boundaries

- Rules that should affect nearly every repository task belong in `AGENTS.md`.
- Role-specific decision guidance belongs in that role's `SKILL.md`.
- Detailed role knowledge belongs in the skill's `references/` directory.
- Product and engineering facts remain in their canonical repository documents and are linked, not copied into every role.
- Temporary progress belongs in GitHub issues and pull requests.
