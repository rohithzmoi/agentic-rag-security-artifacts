# Table 1: Qualitative Guarantee Analysis

AFR = Authorization-First Retrieval, Auth = Authorization Correctness, Deleg = Delegation Correctness, Stale = Staleness Risk, Deploy = Deployment Complexity

Legend: ✓ = Yes, ✗ = No, ± = Conditional

| Defense Family | AFR | Auth | Deleg | Stale | Deploy | Notes |
|---|---|---|---|---|---|---|
| D1 Role-Partitioned Indices | ± | ± | — | High | Low | Index proliferation; breaks under dynamic roles and cross-role queries |
| D2 Metadata-Tag Filtering | ± | ± | — | High | Low | Tag expressiveness limits; correctness depends on tag freshness |
| D3 Post-Retrieval Filtering | ✗ | Weak | — | Med | Low | Model already saw data; cannot prove non-influence on reasoning |
| D4 Prompt Constraints | ✗ | Weak | — | — | Low | Bypassable via injection; behavioral control only |
| D5 Tool-Access Controls | — | — | ± | Med | Med | Retrieval path not constrained; helps delegation only |
| D6 AFR-Oriented | ✓ | Strong | Strong | Low | High | Runtime RBAC resolution; satisfies Definition 1-3 |