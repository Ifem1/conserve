# Formal invariants and decision table

CONSERVE_V1 deals with **bounded self-declared normative snapshots**. Only atomic propositions are supported. A semantic LLM may help decide entailment, but never mutates protocol state within nondeterministic execution.

## Invariants

Let `P` be 1..4 immutable original atomic terms and `C` be 1..6 immutable recipient-bound candidate atomic terms.

1. `SourceRoot = Keccak256(canonical(owner, sorted_multiset((kind, exact_text) for P), CONSERVE_SOURCE_V2))` is consumed at most once on finalization per creator and exact source kind/text multiset. IDs and submitted order do not affect the root; duplicate occurrences do. Failed/cancelled proposals do not consume it. Cross-identity or paraphrased-source reuse is not prevented.
2. `FrozenCase = Keccak256(canonical(owner, title, purpose, P, C, recipients, expiry))` includes all material proposal fields; no edit method exists.
3. Each `P[i]` has **one immutable reviewed verdict**. It must be `PRESERVED`, with an explicit nonempty set of supporting candidate indices, to finalize. For a parent split across several children, the independent assessment must establish joint entailment, not mere thematic similarity.
4. Each `C[j]` has **one immutable reviewed verdict**. It must be `GROUNDED` to finalize. An expanded right, unsupported new right, wrong normative kind, compound child or uncertain child permanently blocks that case.
5. For each pair of `EXCLUSIVE_RIGHT` children, `pair_review` must equal `DISJOINT`; `OVERLAP`, `AMBIGUOUS` or `PENDING` prevents finalization. This only compares child exclusive rights within a single case, not pre-existing external rights.
6. All distinct child assignees must explicitly approve the exact `FrozenCase` hash; acceptance is withdrawable until finalization and frozen thereafter.
7. Only the creator can finalize/cancel. Expired proposals cannot finalize or be further reviewed/assented. An expired proposal is permanently ineligible even if stored status remains OPEN.
8. Only `FINAL` case is consumable; `final_hash = Keccak256(canonical(case_id, source_hash, review_hash, domain_tag))` binds case identity, terms, consensus results and signers.
9. Every consensus validator independently reclassifies the same frozen input and compares both substantive status **and supporting indexes**. Malformed output or disagreement causes nondeterministic failure without state change.
10. No method transfers GEN, executes an external financial action, claims independent authority, or grants a right not explicitly within the declaration.

## Finalization predicate

```text
valid =
    status == OPEN
    AND now <= expiry
    AND msg.sender == case.owner
    AND provided_hash == source_hash
    AND every parent_review == PRESERVED
    AND every child_review == GROUNDED
    AND every exclusive_pair_review == DISJOINT
    AND accepted_signers == required_signers
    AND source_root not previously spent
```

`result_hash` encodes all audit vectors; the final hash is domain separated. No administrator can bypass any conjunct.

## Status matrix

| Semantic result | Stored as | Eligible for FINAL? |
|---|---|---|
| Parent preserved | `PRESERVED` | Yes for that parent |
| Parent weakened/omitted/ambiguous | `WEAKENED`/`OMITTED`/`AMBIGUOUS` | No |
| Child grounded and atomic | `GROUNDED` | Yes for that child |
| Child expanded/unsupported/non-atomic/mislabeled/ambiguous | corresponding permanent result | No |
| Exclusive pair disjoint | `DISJOINT` | Yes for that pair |
| Exclusive pair overlap/ambiguous | `OVERLAP`/`AMBIGUOUS` | No |
| Assignee refused/withdrew | missing assent | No |
| Exact source previously conserved | `root spent` | No |
| Case expired | expired precondition | No |

### Avoided false positives

- Superficially equivalent language must not hide a shorter deadline, different scope, expanded permission, new exception, weaker prohibition, wrong obligor, or reduced quantity.
- Independent children may jointly cover a split source: compare the **union**, not only one-to-one pairs.
- Repeating the same exclusive right with a new ID or recipient triggers pairwise overlap rather than automatic acceptance.
- Support indices are materially checked, not ignored as free-form prose.
- A downstream contract pins the final certificate hash and exact action hash, not a mutable "latest case" pointer.

### Deliberate limits

`Conserve` is a statement-relative proof, not a general satisfiability theorem. It cannot prove actual signatory authority, authenticity of an external contract, completeness of the creator's historical commitments, or safe division of external economic entitlements absent external binding. Independent models can agree incorrectly. High-value consumers should require a separate authenticated source/identity layer and handle consensus rejection by opening a corrected new case, rather than retrying a bad immutable one.
