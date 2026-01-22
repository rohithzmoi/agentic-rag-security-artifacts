# Table 2: Representative Deployment Patterns

State Iso. = Isolation of caches, rerankers, and adaptive components across users

Legend: ✓ = Can guarantee, ✗ = Cannot guarantee by construction, ± = Conditional

| Representative Pattern | AFR | Auth | Deleg | State Iso. | Reason |
|---|---|---|---|---|---|
| Role-partitioned indices (per role/domain) | ± | ± | — | ± | AFR only if routing is perfect; breaks under dynamic roles and cross-role querie... |
| Metadata tag filtering at retrieval | ✓/± | ± | — | ± | Candidate set constrained only to the extent tags are correct and fresh; express... |
| Broad retrieve then redact before LLM | ✗ | ✗ | — | ± | Unauthorized chunks may enter intermediate context or reranking; redaction canno... |
| Prompt non-disclosure + output filters | ✗ | ✗ | — | — | Behavioral control only; does not prevent unauthorized context exposure or inter... |
| Tool-scoped agents (OAuth/IAM) with unconstrained retrieval | — | — | ± | ± | Delegation improved for tools but retrieval path remains an ungoverned data acce... |
| AFR PEP gating retrieval candidates against PDP | ✓ | ✓ | ±/✓ | ± | Achieves Eq. 3; auth correctness depends on including all intermediate artifacts... |