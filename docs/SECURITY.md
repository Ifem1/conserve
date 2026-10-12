# Threat model and failure boundaries

## Protected assets

- Immutable proposal meaning and recipient identities.
- Conservation certificate integrity.
- Status and assent histories.
- Unique consumption of the exact declared source set.
- User-facing distinction between claim-relative semantic proof and legal authorization.

## Adversaries

1. Malicious creator attempts to drop a parent duty or smuggle a new right into a child duty.
2. Malicious leader fabricates a positive verdict or swaps support indices.
3. Malicious assignee or third party attempts to assent for another address.
4. Creator changes conditions after collecting signatures.
5. Creator tries to certify identical source sets multiple times under two case IDs.
6. Attacker embeds prompt injection inside a parent or child text.
7. Overlapping exclusive rights are split into two apparently distinct descriptions.
8. Replay of a certificate by a downstream consumer.
9. Expired case finalized late.

## Controls

- Input is strict JSON: no unknown keys, unique IDs, bounded arrays, bounded lengths, normative kind whitelist, valid nonzero 20-byte recipient address.
- No edit path after case creation. `source_hash` protects all material fields. Signed assent is a blockchain transaction sent by each assignee; it cannot be copied by a different caller.
- Each semantic review calls a leader prompt AND an independently produced validator prompt. Both outputs must agree on status and exact supporting term indexes. The result enters state **after** consensus only.
- Every review index is immutable once committed. A proposer cannot harvest repeat verdicts from the same snapshot; opening a new version is explicit.
- Rights must be grounded in parents; all original terms must survive across children. Exclusive-child pairs must all be disjoint.
- Exact source-root consumption is atomic with successful finalization. Second finalization with same canonical root fails.
- A downstream consumer checks finalized status AND case-specific `final_hash`, not just the owner's word.
- Expiry is read from GenLayer's transaction timestamp (`gl.message.raw.datetime` / fallback message_raw), not local system time.

## What is *not* secured

**Source authenticity.** `propose()` is a self-declared charter. A creator may falsely assert source rights. Conserve does not search for external signatures. A downstream payment/authorization application must independently authenticate that authority.

**Paraphrased multi-case double allocation.** The root guard detects identical canonical source snapshots by the *same creator*. Different spelling, accounts, or partial source-set extraction can bypass this comparison. Do not describe the guard as global semantic double-spend protection.

**Independent validator correctness.** Re-running semantics on independent models is stronger than format checks, not absolute logical soundness. Ambiguity returns non-eligibility; inference disagreements must not mint a positive result. Adversarial StudioNet evidence is required before claiming reliable model behaviour.

**External legal discharge.** This is not a legal agreement, novation, assignment or agency proof. The original party may remain bound under applicable law. Recipient consent covers the self-declared on-chain candidate text only.

**External overlapping rights.** Only overlapping exclusive child rights inside the case are checked. External obligations and rights are not comprehensively discovered.

**Economic custody.** No payments, financial settlement or entitlement withdrawals exist in Conserve. Third-party consuming contracts own their own execution/replay security.

## Live security checks observed on stable 61999 (2026-10-12)

- A live five-report source with a four-report child was classified `WEAKENED`; an unrelated unrestricted client-record right was `UNSUPPORTED`.
- Two identical exclusive grants to separate recipients were classified `OVERLAP`; distinct Lagos/Abuja grants were classified `DISJOINT` and finalized after two distinct assents.
- An unrelated signer and a nominated signer using a wrong source hash could not assent. A valid assent succeeded; withdrawing it left the case OPEN and finalization failed.
- A live short-expiry case was rejected after expiry with `CONSERVE: case expired`.
- An identical creator/source root was rejected on second finalization; a final case could not be finalized again.
- The deployed consumer called the live `is_conserved_for` view, allowed the exact pinned action once, rejected a wrong action and unauthorized caller, and rejected replay.

See `docs/LIVE_PROBE.md` for transaction hashes and receipt outcomes. These probes establish observed contract behavior for these inputs; they do not establish universal model correctness.

## Not live-proven

- A malicious leader deliberately returning a fabricated positive verdict against an independent validator.
- Malformed/partial support vectors, embedded prompt injection, and non-atomic term handling in live consensus.
- External source authenticity, complete historical rights discovery, legal authority, or legal discharge.

