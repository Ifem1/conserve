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
2. **Deterministic protocol:** one-way statuses; strict cardinality and text bounds; immutable snapshots; no review retry or verdict shopping; every original parent preserved; every child grounded; all overlapping exclusive-child pairs disjoint; all assignees consented; source root not already spent; owner finalizes; expiry checked using transaction time; final hash includes case ID, source, reviews, and consents.

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

`contracts/conservation_gate.py` is a tiny *optional* contract-only example. After a live case is FINAL, deploy `ConservationGate(conserve_address, operator, case_id, final_hash, expected_action_hash)`. Its one-shot `consume(action_hash)` calls the **live Conserve contract** through a typed IC view, checks exact final hash and exact action hash, and blocks replay. There is no UI, no wallet adapter, and no backend.

## Proof status (observed 2026-10-12)

- Python compilation passed; 35 tests passed, including 6 GenLayer Direct Mode tests and the mocked contract-logic/consumer suite. The Direct Mode environment required the Windows stdin cleanup workaround in `tests/conftest.py`.
- Both contracts passed `genvm-lint` 0.11.0 check, semantic validation, and schema generation with target `GENVM_VERSION=v0.2.12`.
- Repository-local `genlayer@0.39.1` was installed and verified. `npm run check:network` confirmed `eth_chainId=61999` at the required RPC.
- Main contract was redeployed from the user-provided funded throwaway signer: `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`; deployment transaction `0xa9cb64cd055eefc4b8dae5a34ea4b3e0add2857a4944270a00b9fc5b9d819553` reached `FINALIZED` with execution `SUCCESS`. Source parity was verified; SHA-256 `470bcdbb1c66f6e8ca109aab1ae3f5b1d74ee2edc55a682d7eaa92927d8b1e09`. The earlier deployment `0x59B81DC93C24339030A6e10f10eD35d81aa274F1` remains on chain and has the same verified source.
- A live successful case finalized with exact recipient assent; a second disjoint exclusive-right case with two assignees also finalized. Live weakened/unsupported semantic, wrong signer/hash, withdrawal, overlap, expiry, and replay probes produced their expected outcomes. The optional consumer performed a successful typed IC-to-IC read and one-shot consume; wrong action, unauthorized caller, and replay were rejected.
- **Publication in progress:** Ifem1 GitHub authentication is verified; the initial commit, push, and Actions run are pending. The observed live transaction matrix and any unsupported scenarios are recorded in [`docs/LIVE_PROBE.md`](docs/LIVE_PROBE.md).

These live transactions demonstrate contract behavior on the observed stable network; they do not authenticate self-declared real-world legal authority. See [`docs/SECURITY.md`](docs/SECURITY.md) for that boundary.

## Stable network and pinned tooling

```text
Network        studionet (stable)
Chain ID       61999 / 0xF22F
RPC            https://studio.genlayer.com/api
Explorer       https://explorer-studio.genlayer.com
Local CLI      genlayer@0.39.1 (not global 0.40.x)
GenVM target   v0.2.12 (verify against hosted 61999 before claiming compatibility)
GitHub target  https://github.com/Ifem1/conserve (Ifem1 authentication verified; publication in progress)
```

Install CLI **locally**, not globally: `npm install --no-audit --no-fund` then `npm run verify:cli`. A generated `package-lock.json` is included. Use `npm ci` on subsequent installs. Use `npm run check:network` to query actual `eth_chainId` before deploying. Use the package's local `npm run deploy:main` wrapper, never global `genlayer deploy`.

See [`docs/STUDIONET_61999.md`](docs/STUDIONET_61999.md), [`docs/LIVE_PROBE.md`](docs/LIVE_PROBE.md), and [`docs/SECURITY.md`](docs/SECURITY.md).

## Scope limitations

Conserve certifies the **internal preservation** of a creator-declared source set, not real-world legal authority, valid signatures on source instruments, delivery, performance, or enforceability in any jurisdiction. It has no escrow, GEN transfer, price allocation, owner override, or upgrade key. The anti-double-certification guard consumes the exact canonical `(creator, source-terms)` root on finalization; it cannot prevent someone changing source wording, using a second identity, or misrepresenting their real authority. Consumer systems must separately authenticate original source rights/mandates if their application requires it.

**Licence:** MIT.
