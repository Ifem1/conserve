# Live StudioNet proof matrix — observed 2026-10-12

Mocked logic tests, GenLayer Direct Mode tests, and the live multi-validator matrix have run. Direct Mode complements but does not replace the live evidence below. The implementation was pushed to `Ifem1/conserve` on `main` at commit `80bef1f944912331bc2b426b2926de7b48dfe1ec`; GitHub Actions run [38310472813](https://github.com/Ifem1/conserve/actions/runs/38310472813) passed.

## Observed deployment and live results

- CLI: repository-local `genlayer@0.39.1`; network alias `studionet`; RPC `https://studio.genlayer.com/api`; `eth_chainId=0xF22F` (61999).
- Current main contract: `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`; deployment transaction `0xa9cb64cd055eefc4b8dae5a34ea4b3e0add2857a4944270a00b9fc5b9d819553` reached `FINALIZED`, leader execution `SUCCESS`.
- Earlier deployment `0x59B81DC93C24339030A6e10f10eD35d81aa274F1` (transaction `0x4e4a828ac01341d8befef89922964aa7395577b039360ca8da257d3183dcfc4a`) remains deployed with the same source.
- Main source SHA-256: `470bcdbb1c66f6e8ca109aab1ae3f5b1d74ee2edc55a682d7eaa92927d8b1e09`; live `npm run verify:deployed-source` matched exact source bytes.
- Successful main lifecycle: case 1, final hash `d5a190b4fa066ec59aee69aae3a0f7e31992e3ef1f546391ca53178efc7c4531`; full parent and child reviews, exact recipient assent, and finalization all executed successfully.
- Two-assignee disjoint exclusive case 5 also finalized successfully; its parent support set included both children, both children were grounded, pair verdict was `DISJOINT`, and both assignees consented.
- Consumer `0x98cC7Cb84A63814cb6B3f61A6a2301Adad19894d`, deployment tx `0xf294030ca40d506e614d6ea7cd2af25adfeb34e0f18af9526f976ad6e7b7879d`; deployed source exactly matches `contracts/conservation_gate.py`, SHA-256 `2f27194fdda516b68e2c3869d748821bfa25faf7ec0630604d1ca12c3adeb237`.
- The consumer’s valid consume called the live typed Conserve view and succeeded; on-chain `get_status` returns `consumed: true`. Wrong action, unauthorized caller, and replay were rejected.
- Initial malformed proposal probe `0xb18969faa715152ebecb46d5e84cab6d3d7883f6816986ad0c4498044b6ccc61` reached `FINALIZED` with leader execution `ERROR`: CLI 0.39.1 parsed JSON arrays as array calldata rather than JSON text strings. No case was created. A typed SDK call was then used for all subsequent live tests.
- A valid recipient assent was once attempted with a mistyped source hash missing its last character; it correctly failed (`0x83ef60659598cdbe653cd17fd4049d871b973342413f67ab2c15220bbd64503e`). The exact hash was then read from chain and assent succeeded in `0x11b01b7c839b9982c46a4eb1797f43a5b7f399c22fa55c7843208b52fa6f8221`.
- GitHub Actions run [38310472813](https://github.com/Ifem1/conserve/actions/runs/38310472813) on the initial source commit passed all steps: hosted GenVM lint, Python compilation, fixed target checks, and 35 mocked plus Direct Mode tests.

## Transaction evidence

All transaction hashes below were queried from the configured stable RPC. Application writes reached `FINALIZED`; `SUCCESS` means the leader execution succeeded, and `ERROR` is an expected reject only where stated. Validator maps are in the corresponding transaction records; they generally show agreeing votes with some idle validators.

| Probe | Transaction(s) | Finalized outcome |
|---|---|---|
| Current main deployment | `0xa9cb64cd055eefc4b8dae5a34ea4b3e0add2857a4944270a00b9fc5b9d819553` | SUCCESS; contract `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66` |
| Case 1 proposal / parent / child | `0xbcc3692a97defe332c6080860e1ea67bd19ef14ac9e0c9dd7b9e077f4cc14bde`; `0x6985ea913172ba8f231f7fe42323387826860012f47ccfa2f7b2bd192e976120`; `0xf260cb7129d83cdb9614d991108a022dd7cf3e4a90eaa3270ab735bdfe8a28f0` | All SUCCESS; parent `PRESERVED`, child `GROUNDED` |
| Case 1 wrong signer / wrong source hash | `0xbebb84adeef91af49b974cffb923279b83ac04f1869506ecf65a29cb8a0c7435`; `0xccc26c5517ac9e898e7212e574efe0f23878ee4ed6b79d5bfa4d2ea6ba31fc98` | Both ERROR; neither assented |
| Case 1 exact assent / finalization | `0x11b01b7c839b9982c46a4eb1797f43a5b7f399c22fa55c7843208b52fa6f8221`; `0x87409790f39ee86c30885e737f72a6f8889e139bd893094cb74747c619bf7e9c` | Both SUCCESS; certificate status 2, final hash `d5a190b4fa066ec59aee69aae3a0f7e31992e3ef1f546391ca53178efc7c4531` |
| Case 2 reduced quantity | `0x5ce7d5ccb46a589e0c1050c19e94a7fd241e8c683ef212bdc0392314c6340e86`; `0xb10b6e7dde13773cb862a4118ba4985fb4592c94143fa61f4b4af5e602851521` | Proposal and review SUCCESS; parent verdict `WEAKENED` |
| Case 3 unsupported right | `0x8c4bd66100279a6514498bb10999500fb3bbd26e4f47472bf85f7138442e2a3b`; `0x7eef9c8b871b736f6c4958fe8520fdfeb6f7df331eb227c2d4b72ffc4f4d9a2f` | Proposal and review SUCCESS; child verdict `UNSUPPORTED` |
| Case 4 overlapping exclusive rights | `0x3c618dcdfe763d4acfd39384a8686cb7698f92a3e929c5b7c86eb86132b80cec`; `0xd6270e94605e6c6bc8953db03db022fa45598911ccb307b7b07299de22cc4da8` | Both SUCCESS; pair verdict `OVERLAP` |
| Case 5 disjoint exclusive rights, 2 assignees | `0x523c630adfc7edc27f9386e016c6e6f2a0d6ed9d31658458e0a15c9454cbf0fc`; `0x4558c695d16f0c57bb2d623c806aec6e3b55e5a45a562561e5a99439b3a98417`; `0x1f9c2a9559b7c63919f60f3c045ee55c0b6a2818a2030c3cb038410746340a5f`; `0x020f3d63b1b305fd874203bbda858c42747a24565cea00c1d3a053aeae6dc9d3`; `0x11e48553a730eb3f257bc9389da88ef42494c675556923c3ae65f2279b9d4793`; `0x87048660a3ebd06fb2bde5dfc98ecf5b4edc4b3e84e33fc0c394afda2879e781`; `0xe9f323f1595ae01dbab5ef6e1b9d365f6da88cd28d1e340b8e15bfd355bd27ff`; `0x8ad865f72327cffa2420636be076874e7640036578d075ebfaf4cb2c57c678bc` | All SUCCESS; parent PRESERVED, both children GROUNDED, pair DISJOINT, both assents accepted; final hash `1da4beb227f9bfc646667e94e9a53f4ec634024cdc4face2798b96ca46b91fa0` |
| Case 6 assent withdrawal | `0xe7df2c5a9807ca4ece1ad85858e8fd76f2f96c8b4560b23d0fb52c6fdfb8c3d0`; `0xec63b373d763f365b0c1cacf71b328395c6f208f7555b62a072c55b9dacb2011`; `0xde0722844e1523a9aeb99ec6ec3ad05fff1e8e85047c7d8d540991cbbb5b4a08`; `0xf434b00d3b23916285748600ae394c95fdb1913ea918a3eb95ea95c10b25f038`; `0xd7f74baaf54c7a408c37128db20b671fac5a4497cf358d3411ae9613a43cdb19`; `0x8cf52248398cce6f7b8d2975b46c73b83163c57688efb64d1a83a65b081a6ae9` | Proposal/reviews/assent/withdraw SUCCESS; finalization ERROR; acceptance list empty, case remains OPEN |
| Case 7 duplicate source root | `0x9fc31f40d206e979623fc9b49c8dea2221b2e84f0d58001a2acd755631525bc2`; `0x9e8f07a4fe2f7c2cb0433a2d70479dbe60dd097fe8100f95eef2dc5bc068578e`; `0x076d410d71bca55b598bb97455d93c631ba57c1faf397da443019b88438e678e`; `0x1e7df422a34a9df5815015930a5a45a33bccef58f19b790fd45c210886542129`; `0xa5f875594a0ac63733ebe51c722199e049c5134d2ab961f9575faff04c41a001` | Proposal/reviews/assent SUCCESS; finalization ERROR because root already consumed |
| Second finalization of case 1 | `0x72fc8b7b3742d63f0b518348463933f7731d19dbc0d49ac84dad0bb8b49a8335` | ERROR; already-final case cannot finalize again |
| Case 8 expiry | `0xf063438b0c438e6404931c06944901af63e09e79ada103697dcd27facfe16b7d` (proposal); `0x0ef21a9bd454577a5e12f4a2a8216ffa288ec706eca1d741a8797dc026ec9c82` (review) | Proposal SUCCESS; after on-chain expiry review FINALIZED with rollback `CONSERVE: case expired` |
| Consumer deployment | `0xf294030ca40d506e614d6ea7cd2af25adfeb34e0f18af9526f976ad6e7b7879d` | FINALIZED, execution SUCCESS; contract `0x98cC7Cb84A63814cb6B3f61A6a2301Adad19894d`; source parity verified |
| Consumer wrong action / unauthorized caller | `0x72564f8e1ccdfbcf16a551edca8fc6359163848429a917db8c52339962e90295`; `0x530f0034a71f7a9d754ae24c54b1462f3bf28d613295b6700ab28a3ff9383565` | Both FINALIZED, execution ERROR |
| Consumer valid cross-contract consume / replay | `0xa9cdbfe44579054617dcfac89b8ac07564230e6a7178170e040442cfaa928b29`; `0xf0bc4b044e78d3df1b12d9ccfd09f39a5b2abc75d329646a66a3b57568820113` | First returned true / SUCCESS; replay ERROR; `get_status.consumed=true` |

## Before testing

- Confirm local CLI exactly 0.39.1.
- Confirm RPC `https://studio.genlayer.com/api`, chain ID exactly 61999.
- Confirm deployment `FINALIZED` and execution `SUCCESS`, schema matches source.
- Have two distinct funded StudioNet signers available (creator A and assignee B); use a third C for two-assignee scenarios.

## Case 1 — positive single-assignee conservation

Declare source and child atomic norms using the ABI methods or hosted Studio form:

```json
{
  "title":"Service assignment",
  "purpose":"Preserve signed-report delivery obligations across a new provider",
  "sources_json":"[{\"id\":\"p1\",\"kind\":\"DUTY\",\"text\":\"The provider must deliver five signed reports by 31 December.\"}]",
  "candidates_json":"[{\"id\":\"c1\",\"kind\":\"DUTY\",\"text\":\"Replacement provider must deliver five signed reports by 31 December.\",\"assignee\":\"<B_ADDRESS>\"}]"
}
```

Compute an `expires_at` UNIX timestamp in the future (no more than 90 days). `propose(...)` returns case ID. Query `get_case(id)` and save `source_hash`.

Execute `review_parent(id,0)` and `review_child(id,0)` as **finalized transactions**. Any `AMBIGUOUS` result is not a pass and requires a new case. Switch to signer B and call `accept_assignment(id,source_hash)`. Switch to creator A and call `finalize(id,source_hash)`. Confirm `get_certificate` status `2`, 64-char final hash, and `is_conserved_for(id,final_hash) == true`.

## Case 2 — missing obligation

Parent says *five reports*, child says *four*. Confirm `review_parent` produces `WEAKENED` or `OMITTED`, **or** independent consensus disagrees and prevents a state update. In either outcome `finalize` must be impossible.

## Case 3 — new child right / wrong kind

Parent DUTY is unrelated to a child `RIGHT` granting access to client databases. Expected: `EXPANDED`/`UNSUPPORTED`/`WRONG_KIND`/`AMBIGUOUS`, or validator disagreement. No finalization.

## Case 4 — assignee identity

After all semantic checks pass, attempt acceptance from signer C when B is nominated. Must fail. Attempt acceptance with a different source hash from B. Must fail. B consents correctly, then withdraws. Finalize must fail until B reconsents.

## Case 5 — exclusive rights

Parent declares exclusive distribution right over markets A + B. Children assign exclusive A to B and exclusive B to C. Run each child and source review and the pair review. Disjoint outcome may finalize if all other requirements pass. Next, create two overlapping exclusive child grants (same product and territory/channel) and prove `OVERLAP` / `AMBIGUOUS` cannot finalize.

## Case 6 — repeated source set

Open two cases with the identical creator and canonical `sources_json` but distinct child candidates, then properly review/consent. Finalize the first. Finalizing the second must fail on consumed root. Also prove that an already final case cannot be cancelled or re-reviewed.

## Case 7 — actual consumer

After Case 1 is final, deploy `ConservationGate(conserve_address,A,case_id,final_hash,action_hash)` using a fixed 32-byte hex action hash. Call `consume(wrong_hash)` -> reject. `consume(action_hash)` by a non-operator -> reject. `consume(action_hash)` by A -> success/finalized. Repeat -> reject replay. The consumer must call the actual deployed `Conserve` IC view.

## Evidence completeness

The transaction evidence table above replaces the original pending placeholders. It records observed hashes and outcomes; scenarios listed under “Not live-proven” in `docs/SECURITY.md` remain unsupported.

If you cannot reproduce one of these outcomes, do not claim that control is live-proven. Fix only after investigating the precise GenVM/consensus failure.
