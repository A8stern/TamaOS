# Agent architecture

TamaOS uses small project skills as specialist roles. `AGENTS.md` contains rules that apply broadly; skills load only when their domain is relevant.

## Roles

### Primary agent

Owns the user request, scope, integration, permissions, and final result. It decides whether a specialist is useful and verifies specialist output before it becomes project truth.

### TamaOS Engineer

Invoke `$tamaos-engineer` for engineering-system questions: repository structure, harness, CI, GitHub workflow, toolchains, architectural decision process, and reliability.

Its skill lives at `.agents/skills/tamaos-engineer/`. Its system map is maintained in the repository so another session can reconstruct the engineering environment without relying on chat history.

### Hardware engineer

Invoke `$tamaos-hardware-engineer` for physical components, datasheets, pin and voltage evidence, power distribution, GPIO selection, wiring tables, measurements, and peripheral bring-up.

It owns the electrical contract and physical verification, not firmware implementation. It must distinguish observed, specified, seller-claimed, and assumed facts; a diagram remains planned until the exact assembly is tested.

### Common code agent

Invoke `$tamaos-code` for language-independent implementation behavior: acceptance criteria, affected callers, minimal complete changes, tests, and handoff into review. Pair it with the applicable language skill.

Every committed change must use `$tamaos-code-review` before push. It is only the coordinator; three distinct read-only reviewers each invoke a different installed review skill with non-overlapping ownership:

- `$tamaos-review-correctness`: behavior and regressions;
- `$tamaos-review-architecture`: boundaries and structural cost;
- `$tamaos-review-verification`: evidence and non-functional risk.

The reviewers inspect the same commit independently, do not see one another's reports, and may not substitute one general review for the three required skills. Local evidence records the skill name as well as the reviewer identity. Evidence plus `make ci` is enforced by `make prepush`; CI does not perform agent review. Upstream provenance is recorded in [review-skill-sources.md](review-skill-sources.md).

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
