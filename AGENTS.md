# Repository instructions for Codex agents

READ `IFEM_CODEX_INSTRUCTIONS.txt` BEFORE ANY OTHER TASK. The user will supply this folder locally after unzipping; do NOT clone a different repo.

- Network: only `studionet` / chain 61999 / RPC `https://studio.genlayer.com/api`.
- CLI: only repository-local `genlayer@0.39.1`; do not invoke global 0.40.x.
- No UI, Next.js app, API backend, Docker requirement, wallet provider, WalletConnect, Snaps, or EVM settlement contracts.
- Main submission: `contracts/conserve.py`. Optional one-shot consumer is `contracts/conservation_gate.py`.
- Preserve the original mechanism, invariants, and strict reject-on-uncertainty boundaries. No model-derived monetary value, recipient, consent or authority.
- Never invent CI passing status, finality, deployment address, validator votes, receipt, source parity or reward score.
- If you find a GenVM compatibility issue, repair and test against stable hosted 61999. Do not change the target to 61997.
- Ifem owns `Ifem1/conserve`; do not try to push to `ometere123`.
