# Live StudioNet proof matrix — observed 2026-10-12

Mocked logic tests, GenLayer Direct Mode tests, and the live multi-validator matrix have run. Direct Mode complements but does not replace the live evidence below. The implementation was pushed to `Ifem1/conserve` on `main` at commit `80bef1f944912331bc2b426b2926de7b48dfe1ec`; GitHub Actions run [38310472813](https://github.com/Ifem1/conserve/actions/runs/38310472813) passed.

## Corrected current deployment and proof

- Target: stable `studionet`, chain 61999 (`0xF22F`), RPC `https://studio.genlayer.com/api`; local CLI `genlayer@0.39.1`.
- Corrected V2 main: [`0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488`](https://explorer-studio.genlayer.com/address/0x6B8aD73f19b53B1d939d6d52963c99Aa18F1E488). Deploy tx [`0x83e4e1fd39ba7ec6ef6da29e50010c631a60565f745c48d8834cd034b0e862c7`](https://explorer-studio.genlayer.com/tx/0x83e4e1fd39ba7ec6ef6da29e50010c631a60565f745c48d8834cd034b0e862c7): FINALIZED, leader execution SUCCESS, all five validators AGREE. Source SHA-256 `bfb00d856cc80c54d599e2f36ffaff5f1efa3b8e9fd49f1143a289bdcbf98f65`; `npm run verify:deployed-source` passed exact byte parity.
- Root identity is Keccak over owner, `CONSERVE_SOURCE_V2`, and a sorted multiset of `[kind, exact text]` pairs. Source IDs and order are excluded; repeated identical pairs remain repeated. Case `source_hash` still includes the exact ordered source objects and other case fields.

| Fresh V2 proof | Transaction(s) | Observed result |
|---|---|---|
| Case 1 proposal | [`0x3387a986569a257c8924598c193b6b9866cb3cd7538e73b7b5d3c357c7e64313`](https://explorer-studio.genlayer.com/tx/0x3387a986569a257c8924598c193b6b9866cb3cd7538e73b7b5d3c357c7e64313) | FINALIZED / SUCCESS; five AGREE. Case ID 1; source hash `2de5fc7b7c986c1800efa642e3389805eac39d25e09f37802546c354cb47afa1`; root `7cfca1bc4132c5827f8a5dea0d22ceb9963025783251417c5cf920004c68bd3c`. |
| Case 1 parent reviews | [`0x190a55c4752370be9e591a362413a3b79d7000e61ff9cb03e25d988e106f7d84`](https://explorer-studio.genlayer.com/tx/0x190a55c4752370be9e591a362413a3b79d7000e61ff9cb03e25d988e106f7d84); [`0x001e3b9df65a520786439c3de7e5c9fa5431fbea9158f18420a74a9b4fe276aa`](https://explorer-studio.genlayer.com/tx/0x001e3b9df65a520786439c3de7e5c9fa5431fbea9158f18420a74a9b4fe276aa) | Both FINALIZED / SUCCESS, PRESERVED. |
| Case 1 child reviews | [`0x1cd2d122172aa867c2d71f093a5b31df74fefe8458072539c7187f768ba9d75a`](https://explorer-studio.genlayer.com/tx/0x1cd2d122172aa867c2d71f093a5b31df74fefe8458072539c7187f768ba9d75a); [`0x8392922a91ffcca5ed007b4345a4bbd4e6609b97b5d5fc6ab5c97e6080971428`](https://explorer-studio.genlayer.com/tx/0x8392922a91ffcca5ed007b4345a4bbd4e6609b97b5d5fc6ab5c97e6080971428) | Both FINALIZED / SUCCESS, GROUNDED. |
| Case 1 assignee consent | [`0x34de65ac82fb62622f96f35050ea60d81762f2e8a15e8413325b38ec60bfa5e5`](https://explorer-studio.genlayer.com/tx/0x34de65ac82fb62622f96f35050ea60d81762f2e8a15e8413325b38ec60bfa5e5) | FINALIZED / SUCCESS. |
| Case 1 finalization | [`0x056b3c35e57ccbe948643e045febee9c5e94ad7f94207b24da8578b7961121ee`](https://explorer-studio.genlayer.com/tx/0x056b3c35e57ccbe948643e045febee9c5e94ad7f94207b24da8578b7961121ee) | FINALIZED / SUCCESS; five AGREE. Certificate status 2; final hash `d80369388ed1708bffab2afb1800c98e300dcae5c678ceae7df2718e07dd6714`. |
| Case 2 reordered/relabelled proposal | [`0xe6ae1aae958cc94ae654a1e28c3210501eb62e1c16ece41b68eaf682540dbd54`](https://explorer-studio.genlayer.com/tx/0xe6ae1aae958cc94ae654a1e28c3210501eb62e1c16ece41b68eaf682540dbd54) | FINALIZED / SUCCESS; same exact source kinds/texts in reverse order and with renamed IDs. Root matches case 1; exact case source hash `6554440453c200ce5b7969c881eaf8aa95c1a025d416e83944ecb24ba17b58a7` differs. |
| Case 2 parent reviews | [`0xd69ab46155d9361f46d9d8469ac59e34391ce659c8cedd4ee234db1d6fe3a98a`](https://explorer-studio.genlayer.com/tx/0xd69ab46155d9361f46d9d8469ac59e34391ce659c8cedd4ee234db1d6fe3a98a); [`0xbff619289c2aa95dac90610313bbae2de05002c2f5a42992f58d5539cc412d25`](https://explorer-studio.genlayer.com/tx/0xbff619289c2aa95dac90610313bbae2de05002c2f5a42992f58d5539cc412d25) | Both FINALIZED / SUCCESS. |
| Case 2 child reviews | [`0xdae51c75e1e530c604bf8dc4802e650954dd1d0e0f8430c99b91a7c7ef08fa22`](https://explorer-studio.genlayer.com/tx/0xdae51c75e1e530c604bf8dc4802e650954dd1d0e0f8430c99b91a7c7ef08fa22); [`0xcd8e37e9e103c5c4b74e3fe8d4d8ed498548805044af6829689b5d2ec062ec21`](https://explorer-studio.genlayer.com/tx/0xcd8e37e9e103c5c4b74e3fe8d4d8ed498548805044af6829689b5d2ec062ec21) | Both FINALIZED / SUCCESS. |
| Case 2 assignee consent | [`0x099ade90e5decff4a099cc46a5ba7d7e9074cb3ebcd570e378b20a62046067f3`](https://explorer-studio.genlayer.com/tx/0x099ade90e5decff4a099cc46a5ba7d7e9074cb3ebcd570e378b20a62046067f3) | FINALIZED / SUCCESS. |
| Case 2 replay finalization | [`0x999bfa9c3749ba2b5d36d3efd0ccf8eb46b2bd109bc38f765dfe1d3709fec4ef`](https://explorer-studio.genlayer.com/tx/0x999bfa9c3749ba2b5d36d3efd0ccf8eb46b2bd109bc38f765dfe1d3709fec4ef) | FINALIZED / ERROR; certificate read after failure remained status 1 / OPEN with empty final hash. The same root was already consumed by case 1. |

## Superseded deployments and historical proof

- Previous main `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66` and earlier `0x59B81DC93C24339030A6e10f10eD35d81aa274F1` used pre-canonicalization source SHA-256 `470bcdbb1c66f6e8ca109aab1ae3f5b1d74ee2edc55a682d7eaa92927d8b1e09`. They are not the corrected deployment.
- Intermediate canonical-root V1 deployment `0x7f65e0dB391975dfdA93713eB7756F24bC8e2276`, tx `0x2cfc630f0f4c51a4e731e840217e95f5ec4406fd012bfcad8bd835a471e2c31e`, source SHA-256 `0b1ba39e71c1786b0036373e80914a52eb2b0f2eddb5e35a85e907022892079a`, had a separately deployed source hash before the `CONSERVE_SOURCE_V2` domain tag was applied; it is superseded by the V2 address above.
- The older transaction table below is historical evidence against pre-canonicalization main `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`; it must not be cited as replay evidence for the corrected source.
- Historical optional consumer `0x98cC7Cb84A63814cb6B3f61A6a2301Adad19894d` (deploy tx `0xf294030ca40d506e614d6ea7cd2af25adfeb34e0f18af9526f976ad6e7b7879d`) was configured to call that same previous main `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66`, case 1 and its historical final hash. It was not configured to call corrected V2 main.

## Historical transaction evidence on superseded main
### Historical transaction table

All transaction hashes below were queried from the configured stable RPC. Application writes reached `FINALIZED`; `SUCCESS` means the leader execution succeeded, and `ERROR` is an expected reject only where stated. Validator maps are in the corresponding transaction records; they generally show agreeing votes with some idle validators.

| Probe | Transaction(s) | Finalized outcome |
|---|---|---|
| Previous pre-canonicalization main deployment | `0xa9cb64cd055eefc4b8dae5a34ea4b3e0add2857a4944270a00b9fc5b9d819553` | SUCCESS; contract `0x15eCD4d06379D81A6133Af66a4424CDeAE3dfa66` |
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
