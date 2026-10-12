# CONSERVE

**Consensus-certified preservation of obligations and bounded rights during agreement restructuring.**

**Standalone GenLayer Intelligent Contract · Contract-only · No frontend · Stable StudioNet 61999**

> A party may split or reassign a declared bundle of obligations and rights only after every original atomic term is demonstrably preserved, every proposed child term is grounded in the original set, overlapping exclusive rights are ruled out, and every nominated recipient has assented to the exact immutable transformation. The model does not grant rights, decide consent, or issue a certificate by itself.

## Why it exists

Conventional smart contracts can verify arithmetic conservation: `sum(inputs) == sum(outputs)`. Real-world agreements are harder. "Maintain the service for thirty days" can be split or rewritten into apparently equivalent clauses, but a single omitted exception, period, actor, restriction, or exclusivity condition changes what is promised. Conserve attaches an immutable source snapshot to a bounded transformation, uses GenLayer consensus for *semantic coverage*, and makes all final admission checks deterministic.

### Minimal example

**Sources**
- P1 DUTY: `The provider must deliver five signed reports by 31 December.`
- P2 PROHIBITION: `The provider must not disclose client records to third parties.`

**Proposed children**
- C1 DUTY assigned to Provider B: `Provider B must deliver five signed reports by 31 December.`
- C2 PROHIBITION assigned to Provider B: `Provider B must not disclose client records to third parties.`

A case cannot finalize unless each `P*` is independently assessed as `PRESERVED`, each `C*` as `GROUNDED`, all nominated assignees have consented to the **exact source hash**, and any potentially overlapping exclusive rights are independently classified as `DISJOINT`.

A false rewrite such as "deliver *four* reports" or "disclosure *permitted with partners*" must fail conservation. Uncertain semantic cases fail closed.

## Two-layer security model

1. **Semantic consensus:** independent validators re-derive the full verdict and the exact supporting term indexes for each parent/child review. The validator must reject a leader who picks a different verdict or support set. This is not schema-only verification. Inputs are explicitly untrusted, and all LLM calls are inside nondeterministic blocks.
2. **Deterministic protocol:** one-way statuses; strict cardinality and text bounds; immutable snapshots; no review retry or verdict shopping; every original parent preserved; every child grounded; all overlapping exclusive-child pairs disjoint; all assignees consented; order-independent source root not already spent; owner finalizes; expiry checked using transaction time; final hash includes case ID, exact case source, reviews, and consents.

## Interface

Main contract: [`contracts/conserve.py`](contracts/conserve.py), `Conserve()` (no constructor arguments).

| Method | Caller | Purpose |
|---|---|---|
| `propose(title, purpose, sources_json, candidates_json, expires_at)` | any creator | Freeze 1–4 atomic source terms and 1–6 candidate terms; return case ID |
| `review_parent(case_id,index)` | anyone | Consensus checks complete parent conservation by child set |
| `review_child(case_id,index)` | anyone | Consensus checks child term atomicity, kind and no unsupported/new rights |
| `review_exclusive_pair(case_id,pair_index)` | anyone | Consensus checks distinctness of two child exclusive rights |
| `accept_assignment(case_id,source_hash)` | nominated assignee | Consents to precisely that immutable transfer/rewrite |
| `withdraw_acceptance(case_id,source_hash)` | consenting assignee | Withdraws before finalization |
| `finalize(case_id,source_hash)` | creator | Deterministically issues conservation certificate, if all invariants hold |
| `cancel(case_id)` | creator | Cancels an unfinalized case |
| `get_case(case_id)` | anyone | Immutable terms, review matrix, consents, hashes, status |
| `get_certificate(case_id)` | anyone | Compact certificate metadata |
| `is_conserved_for(case_id,final_hash)` | any consumer IC | Exact hash-bound finalized gate |
| `is_conserved(case_id)` | anyone | Basic status (prefer hash-bound API for serious integrations) |

Statuses: `OPEN=1`, `FINAL=2`, `CANCELLED=3`. Only the `FINAL` case is consumable.

### Input schema

`sources_json`: JSON array of `{ "id": "p1", "kind": "DUTY", "text": "..." }`.

`candidates_json`: JSON array of `{ "id": "c1", "kind": "DUTY", "text": "...", "assignee": "0x<20-byte-address>" }`.

Each term must be **atomic** and `kind` is exactly `DUTY`, `PROHIBITION`, `RIGHT`, or `EXCLUSIVE_RIGHT`. For any proposed child right, independent validators must establish that its scope is grounded within the original source rights. The child review rejects mislabeled or compound norms. A parent containing multiple independent norms is ambiguous and cannot be certified as preserved.

**Bounds:** 4 sources, 6 children, 600 characters per term, 700-character purpose, 90-day expiry. Each source/child review is its own consensus transaction; at most 15 distinct exclusive-child pairs require review. This bounds per-call inference costs and lets a reviewer see partial progress on chain. See [`docs/INVARIANTS.md`](docs/INVARIANTS.md).

## How the consumer actually uses it

`contracts/conservation_gate.py` is a tiny *optional* contract-only example. After a live case is FINAL, deploy `ConservationGate(conserve_address, operator, case_id, final_hash, expected_action_hash)`. Its one-shot `consume(action_hash)` calls the **live Conserve contract** through a typed IC view, checks exact final hash and exact action hash, and blocks replay. Historical consumer proof used previous main `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`; it is not evidence against the corrected deployment below. There is no UI, no wallet adapter, and no backend.

Source-root identity hashes a sorted **multiset** of each source term's normative kind and exact text, plus the creator and `CONSERVE_SOURCE_V2` domain. It ignores case-local term IDs and input ordering while preserving duplicate occurrences. `source_hash`, review indices, assignee assent, and final certificates remain bound to the exact immutable case, including its original source order and IDs. The guard does not deduplicate paraphrases or different creator identities.

## Proof status (observed 2026-10-12)

- Python compilation passed; 37 tests passed, including 7 GenLayer Direct Mode tests and the mocked contract-logic/consumer suite. The Direct Mode environment required the Windows stdin cleanup workaround in `tests/conftest.py`.
- Both contracts passed `genvm-lint` 0.11.0 check, semantic validation, and schema generation with target `GENVM_VERSION=v0.2.12`. Repository-local `genlayer@0.39.1` and stable StudioNet chain 61999 were verified.
- Corrected main contract: [`0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488`](https://explorer-studio.genlayer.com/address/0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488); deployment transaction [`0x83e4e1fd39ba7ec6ef6da29e50010c631a60565f745c48d8834cd034b0e862c7`](https://explorer-studio.genlayer.com/tx/0x83e4e1fd39ba7ec6ef6da29e50010c631a60565f745c48d8834cd034b0e862c7) reached `FINALIZED` / execution `SUCCESS` with five AGREE votes. Exact source parity passed; SHA-256 `bfb00d856cc80c54d599e2f36ffaff5f1efa3b8e9fd49f1143a289bdcbf98f65`.
- On this deployment, case 1 finalized with exact recipient assent and certificate hash `d80369388ed1708bffab2afb1800c98e300dcae5c678ceae7df2718e07dd6714`. Case 2 reversed the same source norms and renamed IDs: the root hashes matched, the exact case hashes differed, and after complete reviews and assent the replay finalization reached `FINALIZED` / `ERROR`; its certificate remained OPEN.
- Historical consumer evidence used previous main `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`, not the corrected deployment.
- **Publication pending:** this correction is being committed to [`Ifem1/conserve`](https://github.com/Ifem1/conserve); CI for this correction has not run yet.

These live transactions demonstrate behavior for the recorded inputs; they do not authenticate self-declared real-world legal authority. See [`docs/SECURITY.md`](docs/SECURITY.md) for limits.

## Stable network and pinned tooling

```text
Network        studionet (stable)
Chain ID       61999 / 0xF22F
RPC            https://studio.genlayer.com/api
Explorer       https://explorer-studio.genlayer.com
Local CLI      genlayer@0.39.1 (not global 0.40.x)
GenVM target   v0.2.12 (verify against hosted 61999 before claiming compatibility)
GitHub target  https://github.com/Ifem1/conserve (root-canonicalization correction pending publication)
```

Install CLI **locally**, not globally: `npm install --no-audit --no-fund` then `npm run verify:cli`. A generated `package-lock.json` is included. Use `npm ci` on subsequent installs. Use `npm run check:network` to query actual `eth_chainId` before deploying. Use the package's local `npm run deploy:main` wrapper, never global `genlayer deploy`.

See [`docs/STUDIONET_61999.md`](docs/STUDIONET_61999.md), [`docs/LIVE_PROBE.md`](docs/LIVE_PROBE.md), and [`docs/SECURITY.md`](docs/SECURITY.md).

## Scope limitations

Conserve certifies the **internal preservation** of a creator-declared source set, not real-world legal authority, valid signatures on source instruments, delivery, performance, or enforceability in any jurisdiction. It has no escrow, GEN transfer, price allocation, owner override, or upgrade key. The anti-double-certification guard consumes the same creator's source kind/text multiset on finalization, independent of IDs and order and preserving duplicate occurrences. It cannot prevent paraphrased sources, partial source-set extraction, use of another identity, or misrepresentation of real authority. Consumer systems must separately authenticate original source rights/mandates if their application requires it.

**Licence:** MIT.
