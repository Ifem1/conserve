# Independent-review packet — observed status 2026-10-12

## Classification

- **Category:** reusable standalone GenLayer Intelligent Contract, no frontend
- **Core primitive:** consent-bound semantic obligation/right conservation under one-to-many / many-to-many restructuring
- **Primary contract:** `contracts/conserve.py`
- **Optional integration fixture:** `contracts/conservation_gate.py`
- **Target:** stable StudioNet 61999, local CLI 0.39.1

## GenLayer indispensable work

For each original atomic norm, validators independently establish whether the *entire* proposed child set preserves its meaning. For each child, they independently establish correct normative type and that no right or exception is invented. For each potential conflicting exclusive-right pair, they determine semantic overlap. The leader and validator independently answer with the exact same verdict and support-index set before the result can become contract state. Models never decide signatures, certificate eligibility, exclusivity bookkeeping, identity, expiry, economics, or status transitions.

## Deterministic reusable guarantee

A certificate is available only when original norms all survive, proposed norms all have authorization basis, no two child exclusive grants overlap, every nominated assignee assents, and the same creator has not consumed the identical source kind/text multiset (order-independent, IDs excluded, duplicate occurrences retained). Consumers use `is_conserved_for(case_id, final_hash)` as a strict version-pinned gate.

## What to attach to submission

- source commit, immutable source SHA-256, deployed contract address, explorer link;
- exact compiler/linter/GenVM/CLI compatibility versions;
- adversarial unit test report **and actual Direct Mode test output** separately;
- StudioNet finalized successful lifecycle and negative tests;
- proof of a real typed cross-contract consumer read and replay block;
- explicit scope statement: self-declared source snapshot, not legal source authentication;
- all open risks and unsupported features identified in `SECURITY.md`.

## Current verification record

- Python compilation passed; 37 tests passed, including 7 Direct Mode cases; mocked tests are identified separately.
- GenVM: `genvm-lint` 0.11.0 check, semantic validation, and schema generation passed for both contracts targeting v0.2.12.
- CLI/network: repository-local CLI 0.39.1 verified; stable RPC chain ID 61999 verified.
- Corrected main deployment `0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488`, deployment tx `0x83e4e1fd39ba7ec6ef6da29e50010c631a60565f745c48d8834cd034b0e862c7`, FINALIZED / execution SUCCESS with five AGREE votes. Source SHA-256 `bfb00d856cc80c54d599e2f36ffaff5f1efa3b8e9fd49f1143a289bdcbf98f65` matched deployed bytes.
- Fresh live case 1 finalized with certificate hash `d80369388ed1708bffab2afb1800c98e300dcae5c678ceae7df2718e07dd6714`. Reordered and relabelled case 2 had the same canonical root and a different exact case hash; its fully reviewed and consented finalization was FINALIZED / ERROR and left it OPEN.
- Optional consumer `0x98cC7Cb84A63814cb6B3f61A6a2301Adad19894d` was deployed against previous main `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`; its historical tests are not evidence against corrected main.
- Correction commit `bbde8c2da3e15943064ade91d1af8ea072de514f` is published on `main`; [GitHub Actions run 38317072266](https://github.com/Ifem1/conserve/actions/runs/38317072266) passed. Full live evidence is in `docs/LIVE_PROBE.md`.

The correction's local and live proof work is complete to the recorded evidence. No external reviewer acceptance is claimed.

## Draft short description (edit after truth-checking live proof)

Conserve is a contract-only GenLayer primitive for safely restructuring a declared set of obligations and rights. Independent validators assess whether each original atomic term survives the complete proposed child set, whether each new child is grounded without invented rights, and whether exclusive child grants are disjoint. A deterministic, consent-bound state machine issues one hash-pinned certificate only when all semantic and signer conditions hold; other Intelligent Contracts can gate actions against it. It does not claim to authenticate the underlying real-world agreement or transfer legal rights.
