# Strict stable StudioNet deployment playbook

This repository is scoped to **StudioNet 61999 (0xF22F)**, RPC `https://studio.genlayer.com/api`, and local repository CLI `genlayer@0.39.1`. **Do not use Studio Dev, Studio Next, chain 61997, or global 0.40.x prerelease tooling.**

## 1. Setup on Ifem's own machine

```bash
# Unzip the archive yourself and open that local conserve/ folder in Codex.
cd conserve
npm install --no-audit --no-fund
npm run verify:cli
python -m venv .venv
# activate the venv on your platform
python -m pip install -r requirements-dev.txt
npm run lint:python
npm run test:logic
```

Once the real dependency tree resolves, commit the generated `package-lock.json`; use `npm ci` on future installs. Do not run `npm install -g genlayer`.

## 2. GenVM static/runtime proof

Install a GenVM linter compatible with the **hosted 61999 GenVM v0.2.12** and run the supported `genvm-lint check` / `lint` / `validate` / `schema` commands for both sources. Verify the actual syntax shown by `genvm-lint --help`; record the version. Run real GenLayer Direct Mode tests of the nonlinear semantic cases, not only CPython mocks. This archive has not run them because these tools are unavailable in its build environment.

## 3. Always verify the effective target

```bash
npm run check:network
./node_modules/.bin/genlayer network set studionet
./node_modules/.bin/genlayer network info
```

The preflight requests the actual `eth_chainId` and fails if it is not 61999. If an RPC does not implement `eth_chainId`, stop and independently verify `net_version` and official network information before changing the preflight. Never bypass the chain guard to deploy.

## 4. Deploy

```bash
npm run deploy:main
```

This wrapper explicitly deploys `contracts/conserve.py` against `https://studio.genlayer.com/api`, using the repository-local CLI. The target is the main Conserve IC; the consumer `contracts/conservation_gate.py` is optional and should be deployed only after a finalized Conserve case exists.

Before creating test cases, verify that the deploy transaction is **FINALIZED**, execution is **SUCCESS**, and the address returned actually contains the expected source (`gen_getContractSchema`/`gen_getContractCode` or CLI `code` command). Avoid treating `ACCEPTED` as finalized.

## 5. Live evidence

Follow [`LIVE_PROBE.md`](LIVE_PROBE.md). Record:

- source commit SHA and SHA-256 of deployed `.py` bytes;
- deployed contract addresses;
- one positive result including every distinct assignee's consent;
- negative runs for omitted/expanded rights, wrong signer, duplicate source root and exclusive overlap;
- consensus-stage evidence showing independent validator votes, not only local mock results;
- optional IC-to-IC consumer gate with one successful commit, one rejection and replay prevention;
- real finalized transaction hash and explorer links for every claim.

No account private key should be committed. `Ifem1/conserve` needs to exist and Ifem must authorize the remote push; the ZIP has deliberately no `.git` remote.

## Source references

- https://docs.genlayer.com/api-references/genlayer-cli — stable CLI 0.39.1
- https://docs.genlayer.com/developers/intelligent-contracts/deploying/network-configuration — `studionet` alias, separate `studio-dev`
- https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle — independent nondet validator comparison
- https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism — storage updates outside nondet blocks
- https://docs.genlayer.com/developers/intelligent-contracts/features/interacting-with-intelligent-contracts — typed IC view consumer
