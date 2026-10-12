# Verification and deployment record (2026-10-12)

## Local validation

- Repository-local `genlayer@0.39.1`; `npm run verify:cli` passed.
- `npm run check:network` confirmed the canonical RPC and chain ID 61999. CLI `network info` reported `studionet` / 61999; `network set studionet` could not rewrite the user-level config from this sandbox, but deploy and all transactions used the explicit stable RPC.
- `python -m py_compile contracts/conserve.py contracts/conservation_gate.py` passed.
- `python -m pytest -q tests` passed: 37 tests, including 7 GenLayer Direct Mode tests. Regression coverage checks reordered terms, renamed IDs, exact case-hash distinction, duplicate occurrence preservation, and replay rejection.
- `GENVM_VERSION=v0.2.12 genvm-lint check` and `genvm-lint schema` passed for both contracts with genvm-lint 0.11.0.
- `npm run verify:deployed-source` passed exact source parity against the final V2 deployment; main source SHA-256 `bfb00d856cc80c54d599e2f36ffaff5f1efa3b8e9fd49f1143a289bdcbf98f65`.

## Corrected stable StudioNet deployment

- Final main: [`0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488`](https://explorer-studio.genlayer.com/address/0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488). Deploy tx [`0x83e4e1fd39ba7ec6ef6da29e50010c631a60565f745c48d8834cd034b0e862c7`](https://explorer-studio.genlayer.com/tx/0x83e4e1fd39ba7ec6ef6da29e50010c631a60565f745c48d8834cd034b0e862c7): FINALIZED / SUCCESS, five AGREE votes.
- Successful case 1 finalization tx `0x056b3c35e57ccbe948643e045febee9c5e94ad7f94207b24da8578b7961121ee`, certificate hash `d80369388ed1708bffab2afb1800c98e300dcae5c678ceae7df2718e07dd6714`.
- Reordered/renamed case 2 finalization tx `0x999bfa9c3749ba2b5d36d3efd0ccf8eb46b2bd109bc38f765dfe1d3709fec4ef`: FINALIZED / ERROR after full reviews and assent; root matched case 1, case hash differed, certificate stayed OPEN.
- All fresh V2 lifecycle hashes and statuses are in `docs/LIVE_PROBE.md`.

## Historical contracts

- Pre-canonicalization main deployments `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66` / `0x59B81DC93C24339030A6e10f10eD35d81aa274F1` do not represent corrected source.
- Intermediate canonical-root V1 main `0x7f65e0dB391975dfdA93713eB7756F24bC8e2276` was superseded by V2's `CONSERVE_SOURCE_V2` domain.
- Historical optional consumer `0x98cC7Cb84A63814cb6B3f61A6a2301Adad19894d` references the pre-canonicalization main `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`; do not present it as integration evidence for the corrected deployment.

## Publication status

Corrected source commit `bbde8c2da3e15943064ade91d1af8ea072de514f` is pushed to `Ifem1/conserve` on `main`. GitHub Actions run [38317072266](https://github.com/Ifem1/conserve/actions/runs/38317072266) completed successfully, including hosted GenVM validation, mocked and Direct Mode tests, and fixed-target configuration checks.

This contract checks consistency of a creator-declared source; it does not authenticate legal authority or original-source authenticity.
