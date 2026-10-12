"""Runtime-level contract checks using GenLayer's real Direct Mode VM."""

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GOOD_PARENT = {"verdict": "PRESERVED", "supports": [0]}
GOOD_CHILD = {"verdict": "GROUNDED", "supports": [0]}


def warp(direct_vm, timestamp):
    direct_vm.warp(timestamp)
    # genlayer-test 0.29.2 updates sender/value but leaves raw.datetime stale.
    import sys
    gl = sys.modules.get("genlayer.gl")
    if gl is not None and getattr(gl, "message_raw", None) is not None:
        gl.message_raw["datetime"] = timestamp


def proposal(owner, assignee, expires_at, *, parent_text=None, child_text=None,
             parent_kind="DUTY", child_kind="DUTY"):
    assignee_address = "0x" + assignee.hex() if isinstance(assignee, bytes) else str(assignee)
    source = [{"id": "p1", "kind": parent_kind,
               "text": parent_text or "The provider must deliver five signed reports by 31 December."}]
    child = [{"id": "c1", "kind": child_kind,
              "text": child_text or "The replacement provider must deliver five signed reports by 31 December.",
              "assignee": assignee_address}]
    case_id = owner.propose("Service assignment", "Preserve report delivery", json.dumps(source),
                            json.dumps(child), expires_at)
    return case_id


def accept_same_verdicts(direct_vm, case, case_id):
    direct_vm.mock_llm(r"PARENT CONSERVATION", json.dumps(GOOD_PARENT))
    direct_vm.mock_llm(r"CHILD AUTHORIZATION", json.dumps(GOOD_CHILD))
    case.review_parent(case_id, 0)
    case.review_child(case_id, 0)


def test_direct_vm_finalizes_frozen_consented_case(direct_vm, direct_deploy,
                                                   direct_alice, direct_bob):
    warp(direct_vm, "2026-10-12T00:00:00Z")
    case = direct_deploy(str(ROOT / "contracts" / "conserve.py"), sdk_version="v0.2.12")
    direct_vm.sender = direct_alice
    case_id = proposal(case, direct_bob, int(datetime(2026, 10, 13, tzinfo=timezone.utc).timestamp()))
    source_hash = case.get_case(case_id)["source_hash"]
    accept_same_verdicts(direct_vm, case, case_id)
    direct_vm.sender = direct_bob
    case.accept_assignment(case_id, source_hash)
    direct_vm.sender = direct_alice
    final_hash = case.finalize(case_id, source_hash)
    assert case.is_conserved_for(case_id, final_hash)
    assert case.get_certificate(case_id)["status"] == 2


def test_direct_vm_rejects_malicious_leader_and_keeps_review_pending(
        direct_vm, direct_deploy, direct_alice, direct_bob):
    warp(direct_vm, "2026-10-12T00:00:00Z")
    case = direct_deploy(str(ROOT / "contracts" / "conserve.py"), sdk_version="v0.2.12")
    direct_vm.sender = direct_alice
    case_id = proposal(case, direct_bob, int(datetime(2026, 10, 13, tzinfo=timezone.utc).timestamp()),
                       child_text="The replacement provider must deliver four reports by 31 December.")
    direct_vm.mock_llm(r"LEADER ASSESS PARENT CONSERVATION", json.dumps(GOOD_PARENT))
    direct_vm.mock_llm(r"INDEPENDENT VERIFY PARENT CONSERVATION",
                       json.dumps({"verdict": "WEAKENED", "supports": []}))
    case.review_parent(case_id, 0)
    assert direct_vm.run_validator() is False
    # Direct Mode captures validators for explicit execution but does not
    # emulate chain rollback; live consensus rejection remains a separate proof.


def test_direct_vm_enforces_withdrawable_consent_expiry_and_root_replay(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    warp(direct_vm, "2026-10-12T00:00:00Z")
    case = direct_deploy(str(ROOT / "contracts" / "conserve.py"), sdk_version="v0.2.12")
    direct_vm.sender = direct_alice
    expiry = int(datetime(2026, 10, 13, tzinfo=timezone.utc).timestamp())
    case_id = proposal(case, direct_bob, expiry)
    source_hash = case.get_case(case_id)["source_hash"]
    accept_same_verdicts(direct_vm, case, case_id)
    direct_vm.sender = direct_bob
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("not a nominated assignee"):
        case.accept_assignment(case_id, source_hash)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("source hash mismatch"):
        case.accept_assignment(case_id, "0" * 64)
    case.accept_assignment(case_id, source_hash)
    case.withdraw_acceptance(case_id, source_hash)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("assignee consents incomplete"):
        case.finalize(case_id, source_hash)
    direct_vm.sender = direct_bob
    case.accept_assignment(case_id, source_hash)
    direct_vm.sender = direct_alice
    final_hash = case.finalize(case_id, source_hash)
    replay_id = proposal(case, direct_bob, expiry)
    replay_hash = case.get_case(replay_id)["source_hash"]
    accept_same_verdicts(direct_vm, case, replay_id)
    direct_vm.sender = direct_bob
    case.accept_assignment(replay_id, replay_hash)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("source set already consumed"):
        case.finalize(replay_id, replay_hash)
    assert case.is_conserved_for(case_id, final_hash)


def test_direct_vm_rejects_expired_case_and_malformed_proposal(
        direct_vm, direct_deploy, direct_alice, direct_bob):
    warp(direct_vm, "2026-10-12T00:00:00Z")
    case = direct_deploy(str(ROOT / "contracts" / "conserve.py"), sdk_version="v0.2.12")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("terms must be valid JSON"):
        case.propose("Bad", "Bad", "not json", "[]", 1791763200)
    expiry = int(datetime(2026, 10, 13, tzinfo=timezone.utc).timestamp())
    expired = proposal(case, direct_bob, expiry)
    warp(direct_vm, "2026-10-14T00:00:00Z")
    with direct_vm.expect_revert("case expired"):
        case.review_parent(expired, 0)


def test_direct_vm_blocks_omission_expansion_and_exclusive_overlap(
        direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    warp(direct_vm, "2026-10-12T00:00:00Z")
    case = direct_deploy(str(ROOT / "contracts" / "conserve.py"), sdk_version="v0.2.12")
    direct_vm.sender = direct_alice
    expiry = int(datetime(2026, 10, 13, tzinfo=timezone.utc).timestamp())

    weakened_id = proposal(
        case, direct_bob, expiry,
        child_text="The replacement provider must deliver four reports by 31 December.")
    direct_vm.mock_llm(r"PARENT CONSERVATION", json.dumps({"verdict": "WEAKENED", "supports": []}))
    case.review_parent(weakened_id, 0)
    direct_vm.mock_llm(r"CHILD AUTHORIZATION", json.dumps(GOOD_CHILD))
    case.review_child(weakened_id, 0)
    assert case.get_case(weakened_id)["parent_reviews"][0]["status"] == 3
    weakened_hash = case.get_case(weakened_id)["source_hash"]
    direct_vm.sender = direct_bob
    case.accept_assignment(weakened_id, weakened_hash)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("missing or non-preserved parent"):
        case.finalize(weakened_id, weakened_hash)

    direct_vm.clear_mocks()
    expanded_id = proposal(case, direct_bob, expiry, child_kind="RIGHT",
                           child_text="The recipient may access all client records.")
    direct_vm.mock_llm(r"PARENT CONSERVATION", json.dumps(GOOD_PARENT))
    case.review_parent(expanded_id, 0)
    direct_vm.mock_llm(r"CHILD AUTHORIZATION", json.dumps({"verdict": "EXPANDED", "supports": []}))
    case.review_child(expanded_id, 0)
    assert case.get_case(expanded_id)["child_reviews"][0]["status"] == 2
    expanded_hash = case.get_case(expanded_id)["source_hash"]
    direct_vm.sender = direct_bob
    case.accept_assignment(expanded_id, expanded_hash)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("missing or ungrounded child"):
        case.finalize(expanded_id, expanded_hash)

    direct_vm.clear_mocks()
    sources = [{"id": "p1", "kind": "EXCLUSIVE_RIGHT",
                "text": "The owner has an exclusive right to distribute the product in market A."}]
    children = [
        {"id": "c1", "kind": "EXCLUSIVE_RIGHT", "text": "Exclusive product distribution in market A.",
         "assignee": "0x" + direct_bob.hex()},
        {"id": "c2", "kind": "EXCLUSIVE_RIGHT", "text": "Exclusive product distribution in market A.",
         "assignee": "0x" + direct_charlie.hex()},
    ]
    overlap_id = case.propose("Exclusive grants", "Avoid duplicate exclusivity", json.dumps(sources),
                              json.dumps(children), expiry)
    direct_vm.mock_llm(r"PARENT CONSERVATION", json.dumps({"verdict": "PRESERVED", "supports": [0, 1]}))
    case.review_parent(overlap_id, 0)
    direct_vm.mock_llm(r"CHILD AUTHORIZATION", json.dumps(GOOD_CHILD))
    case.review_child(overlap_id, 0)
    case.review_child(overlap_id, 1)
    direct_vm.mock_llm(r"EXCLUSIVITY", json.dumps({"verdict": "OVERLAP"}))
    case.review_exclusive_pair(overlap_id, 0)
    assert case.get_case(overlap_id)["exclusive_reviews"][0]["status"] == 2
    overlap_hash = case.get_case(overlap_id)["source_hash"]
    direct_vm.sender = direct_bob
    case.accept_assignment(overlap_id, overlap_hash)
    direct_vm.sender = direct_charlie
    case.accept_assignment(overlap_id, overlap_hash)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("exclusive overlap or missing review"):
        case.finalize(overlap_id, overlap_hash)


def test_direct_vm_consumer_calls_typed_conserve_view_and_blocks_replay(
        direct_vm, direct_deploy, direct_alice, direct_bob):
    from gltest.direct.sdk_loader import setup_sdk_paths
    contract_path = str(ROOT / "contracts" / "conservation_gate.py")
    setup_sdk_paths(Path(contract_path), "v0.2.12")
    from genlayer.py.types import Address
    conserve_address = Address(bytes.fromhex("44" * 20))
    operator = Address(direct_bob)
    action_hash = "b" * 64
    expected_final_hash = "a" * 64
    observed = []
    view_allowed = [False]

    def view_hook(vm, request):
        call = request["CallContract"]
        observed.append(call)
        assert call["address"].as_bytes == conserve_address.as_bytes
        assert call["calldata"] == {"method": "is_conserved_for",
                                     "args": [3, expected_final_hash]}
        return bytes([ResultCode.RETURN]) + calldata.encode(view_allowed[0])

    warp(direct_vm, "2026-10-12T00:00:00Z")
    gate = direct_deploy(contract_path, conserve_address,
                         operator, 3, expected_final_hash, action_hash,
                         sdk_version="v0.2.12")
    from genlayer.py import calldata
    from genlayer.py.public_abi import ResultCode
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("not operator"):
        gate.consume(action_hash)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("different action"):
        gate.consume("c" * 64)
    direct_vm._gl_call_hook = view_hook
    with direct_vm.expect_revert("not finalized or hash mismatch"):
        gate.consume(action_hash)
    view_allowed[0] = True
    assert gate.consume(action_hash) is True
    assert len(observed) == 2  # one fail-closed read and one successful read
    with direct_vm.expect_revert("already consumed"):
        gate.consume(action_hash)


