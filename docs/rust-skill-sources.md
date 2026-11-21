# Rust skill sources

The TamaOS Rust review skills are project-scoped adaptations. Their lane ownership and schema come from the TamaOS review contract; the Rust-specific review knowledge was selected from these public sources after inspecting the pinned content.

| TamaOS skill | Upstream skill | Pinned commit | License | Adaptation |
|---|---|---|---|---|
| `tamaos-rust-review-correctness` | [`po4yka/rust-skills` — `rust-review`](https://github.com/po4yka/rust-skills/tree/d9ab525a6566b687980d3b4c05b97a197802876a/skills/rust-review) | `d9ab525a6566b687980d3b4c05b97a197802876a` | BSD-3-Clause | Retains Rust semantic/soundness review and narrows it to concrete correctness defects. |
| `tamaos-rust-review-architecture` | [`full-stack-skills/rust-skills` — `rust-api-design`](https://github.com/full-stack-skills/rust-skills/tree/b8a6af74af28ee86b8cbbbc3075cde0b31a5155e/skills/rust-api-design) | `b8a6af74af28ee86b8cbbbc3075cde0b31a5155e` | Apache-2.0 | Uses Rust public-contract and type-safety guidance under the TamaOS architecture clearance. |
| `tamaos-rust-review-verification` | [`full-stack-skills/rust-skills` — `rust-testing`](https://github.com/full-stack-skills/rust-skills/tree/b8a6af74af28ee86b8cbbbc3075cde0b31a5155e/skills/rust-testing) | `b8a6af74af28ee86b8cbbbc3075cde0b31a5155e` | Apache-2.0 | Uses Rust-native test/build evidence and excludes design and demonstrated behavior bugs. |

The upstream skills are not executed directly and their scripts/examples are not vendored. Review upstream changes before updating a pinned commit.
