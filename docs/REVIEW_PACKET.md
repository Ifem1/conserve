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

A certificate is available only when original norms all survive, proposed norms all have authorization basis, no two child exclusive grants overlap, every nominated assignee assents, and no identical creator/source term set has already been certified. Consumers use `is_conserved_for(case_id, final_hash)` as a strict version-pinned gate.

## What to attach to submission

- source commit, immutable source SHA-256, deployed contract address, explorer link;
- exact compiler/linter/GenVM/CLI compatibility versions;
- adversarial unit test report **and actual Direct Mode test output** separately;
- StudioNet finalized successful lifecycle and negative tests;
- proof of a real typed cross-contract consumer read and replay block;
- explicit scope statement: self-declared source snapshot, not legal source authentication;
- all open risks and unsupported features identified in `SECURITY.md`.

## Current verification record

- Python compilation: passed.
- Automated tests: 35 passed, including 6 Direct Mode cases; mocked tests are identified separately in the test suite.
- GenVM: `genvm-lint` 0.11.0 check, semantic validation and schema generation passed for both contracts targeting v0.2.12.
- CLI/network: local CLI 0.39.1 verified; stable RPC chain ID 61999 verified.
- Current main deployment: `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`, transaction `0xa9cb64cd055eefc4b8dae5a34ea4b3e0add2857a4944270a00b9fc5b9d819553`, FINALIZED / execution SUCCESS. Main source SHA-256 `470bcdbb1c66f6e8ca109aab1ae3f5b1d74ee2edc55a682d7eaa92927d8b1e09` matched deployed bytes. Earlier same-source deployment `0x59B81DC93C24339030A6e10f10eD35d81aa274F1` remains deployed.
- Main live evidence includes successful case 1 finalization (hash `d5a190b4fa066ec59aee69aae3a0f7e31992e3ef1f546391ca53178efc7c4531`), weakened-parent rejection, unsupported-right rejection, overlapping-exclusive rejection, a successful two-assignee disjoint split, wrong-signer and wrong-hash rejection, withdrawal-blocked finalization, expiry rejection, duplicate-root rejection, and second-finalization rejection.
- Optional consumer `0x98cC7Cb84A63814cb6B3f61A6a2301Adad19894d`, deployment transaction `0xf294030ca40d506e614d6ea7cd2af25adfeb34e0f18af9526f976ad6e7b7879d`, passed byte parity with local consumer SHA-256 `2f27194fdda516b68e2c3869d748821bfa25faf7ec0630604d1ca12c3adeb237`. Wrong action, unauthorized caller, successful typed cross-contract consumption, and replay rejection were observed.
- Publication in progress: GitHub authentication as Ifem1 is verified, and the target `main` branch is empty. The initial commit, push, and CI run are pending. The full transaction matrix is in `docs/LIVE_PROBE.md`.

The contract and live proof work is complete to the recorded matrix. **Publication is in progress; no CI or reviewer acceptance is claimed yet.**

## Draft short description (edit after truth-checking live proof)

Conserve is a contract-only GenLayer primitive for safely restructuring a declared set of obligations and rights. Independent validators assess whether each original atomic term survives the complete proposed child set, whether each new child is grounded without invented rights, and whether exclusive child grants are disjoint. A deterministic, consent-bound state machine issues one hash-pinned certificate only when all semantic and signer conditions hold; other Intelligent Contracts can gate actions against it. It does not claim to authenticate the underlying real-world agreement or transfer legal rights.
