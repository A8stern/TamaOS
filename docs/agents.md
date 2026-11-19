# Agent architecture

TamaOS uses small project skills as specialist roles. `AGENTS.md` contains rules that apply broadly; skills load only when their domain is relevant.

## Roles

### Primary agent

Owns the user request, scope, integration, permissions, and final result. It decides whether a specialist is useful and verifies specialist output before it becomes project truth.

### TamaOS Engineer

Invoke `$tamaos-engineer` for engineering-system questions: repository structure, harness, CI, GitHub workflow, toolchains, architectural decision process, reliability, and hardware bring-up procedure.

Its skill lives at `.agents/skills/tamaos-engineer/`. Its system map is maintained in the repository so another session can reconstruct the engineering environment without relying on chat history.

### Common code agent

Invoke `$tamaos-code` for language-independent implementation behavior: acceptance criteria, affected callers, minimal complete changes, tests, and handoff into review. Pair it with the applicable language skill.

Every committed change must use `$tamaos-code-review` before push. That skill coordinates three distinct read-only reviewers with non-overlapping ownership:

- correctness: behavior and regressions;
- architecture: boundaries and change cost;
- verification-risk: evidence and non-functional risk.

The reviewers inspect the same commit independently and do not see one another's reports. Local evidence plus `make ci` is enforced by `make prepush`; CI does not perform agent review.

### Future language agents

Will add only language-specific knowledge and commands. The first planned language role is Rust. A language agent must use the common code contract and the project `.harness` adapter rather than creating another workflow.

### Proposed architecture agent

Should own cross-component design exploration, alternatives, ADR recommendations, and dependency boundaries. It should not own CI/toolchains (engineer), implementation (code agent), or language idioms (language agent).

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
