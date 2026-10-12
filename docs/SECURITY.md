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
5. Creator tries to certify identical source sets multiple times under two case IDs, changing term IDs or source order.
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
- Source roots hash the creator and an order-independent multiset of normative kind plus exact source text under `CONSERVE_SOURCE_V2`; term IDs are excluded and duplicate occurrences are retained. Root consumption is atomic with successful finalization.
- Per-case `source_hash` remains exact and includes ordered source objects, IDs, candidates, signers, purpose, title, and expiry. Reviews, assents, and final certificates remain case-bound.
- A downstream consumer checks finalized status AND case-specific `final_hash`, not just the owner's word.
- Expiry is read from GenLayer's transaction timestamp (`gl.message.raw.datetime` / fallback message_raw), not local system time.

## What is *not* secured

**Source authenticity.** `propose()` is a self-declared charter. A creator may falsely assert source rights. Conserve does not search for external signatures. A downstream payment/authorization application must independently authenticate that authority.

**Paraphrased multi-case double allocation.** The root guard detects the same creator's source kind/text multiset independent of order and IDs. Different spelling or paraphrasing, different creator identities, or partial source-set extraction can bypass this comparison. Do not describe the guard as global semantic double-spend protection.

**Independent validator correctness.** Re-running semantics on independent models is stronger than format checks, not absolute logical soundness. Ambiguity returns non-eligibility; inference disagreements must not mint a positive result. Adversarial StudioNet evidence is required before claiming reliable model behaviour.

**External legal discharge.** This is not a legal agreement, novation, assignment or agency proof. The original party may remain bound under applicable law. Recipient consent covers the self-declared on-chain candidate text only.

**External overlapping rights.** Only overlapping exclusive child rights inside the case are checked. External obligations and rights are not comprehensively discovered.

**Economic custody.** No payments, financial settlement or entitlement withdrawals exist in Conserve. Third-party consuming contracts own their own execution/replay security.

## Live security checks observed on stable 61999 (2026-10-12)

- A live five-report source with a four-report child was classified `WEAKENED`; an unrelated unrestricted client-record right was `UNSUPPORTED`.
- Two identical exclusive grants to separate recipients were classified `OVERLAP`; distinct Lagos/Abuja grants were classified `DISJOINT` and finalized after two distinct assents.
- An unrelated signer and a nominated signer using a wrong source hash could not assent. A valid assent succeeded; withdrawing it left the case OPEN and finalization failed.
- A live short-expiry case was rejected after expiry with `CONSERVE: case expired`.
- On corrected main `0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488`, reversed source order with renamed IDs produced the same multiset root but a different immutable case hash; after full reviews and assent, replay finalization was FINALIZED / ERROR and left no certificate.
- Historical consumer proof called the then-live `is_conserved_for` view on previous main `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`; it does not establish integration against corrected main `0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488`.

See `docs/LIVE_PROBE.md` for transaction hashes and receipt outcomes. These probes establish observed contract behavior for these inputs; they do not establish universal model correctness.

## Not live-proven

- A malicious leader deliberately returning a fabricated positive verdict against an independent validator.
- Malformed/partial support vectors, embedded prompt injection, and non-atomic term handling in live consensus.
- External source authenticity, complete historical rights discovery, legal authority, or legal discharge.

