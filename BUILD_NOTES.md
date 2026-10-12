# Verification and deployment record (2026-10-12)

## Local validation

- Repository-local CLI is `genlayer@0.39.1`; `npm run verify:cli` passed.
- `npm run check:network` verified `eth_chainId=0xf22f` from `https://studio.genlayer.com/api`.
- `python -m py_compile contracts/conserve.py contracts/conservation_gate.py` passed.
- `python -m pytest -q tests` passed: 35 tests, including 6 GenLayer Direct Mode tests.
- `GENVM_VERSION=v0.2.12 genvm-lint check`, semantic validation, and schema generation passed for both contracts with `genvm-lint` 0.11.0.
- `npm install --no-audit --no-fund` generated the committed-intended `package-lock.json`; `npm run verify:deployed-source` confirms exact main source parity.

## Stable StudioNet deployments

- Main: `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`, transaction `0xa9cb64cd055eefc4b8dae5a34ea4b3e0add2857a4944270a00b9fc5b9d819553`, FINALIZED / execution SUCCESS. Source SHA-256 `470bcdbb1c66f6e8ca109aab1ae3f5b1d74ee2edc55a682d7eaa92927d8b1e09`.
- Earlier same-source main deployment: `0x59B81DC93C24339030A6e10f10eD35d81aa274F1`, transaction `0x4e4a828ac01341d8befef89922964aa7395577b039360ca8da257d3183dcfc4a`.
- Optional consumer: `0x98cC7Cb84A63814cb6B3f61A6a2301Adad19894d`, transaction `0xf294030ca40d506e614d6ea7cd2af25adfeb34e0f18af9526f976ad6e7b7879d`, FINALIZED / execution SUCCESS. Local and deployed source SHA-256 `2f27194fdda516b68e2c3869d748821bfa25faf7ec0630604d1ca12c3adeb237`.
- Main positive lifecycle, semantic rejection matrix, expiry/replay guards, two-assignee disjoint split, and consumer cross-contract/replay probes are listed in `docs/LIVE_PROBE.md`.

## Publication status

The target repository is `Ifem1/conserve`; the initial source commit `80bef1f944912331bc2b426b2926de7b48dfe1ec` is pushed to `main`. GitHub Actions run [38310472813](https://github.com/Ifem1/conserve/actions/runs/38310472813) passed hosted GenVM lint, Python compilation, target checks, and all 35 mocked and Direct Mode tests. The final documentation update is being published separately.

The underlying source and signer inputs are self-declared; this contract does not authenticate real-world legal authority or source authenticity.
