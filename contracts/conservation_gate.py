# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Small optional consumer demonstrating a genuine typed Conserve IC view gate.

This is an integration fixture, NOT a frontend and NOT the main submission.
"""
from genlayer import *


@gl.contract_interface
class IConserve:
    class View:
        def is_conserved_for(self, case_id: u256, expected_final_hash: str) -> bool: ...


class ConservationGate(gl.Contract):
    conserve: Address
    operator: Address
    case_id: u256
    expected_final_hash: str
    expected_action_hash: str
    consumed: bool

    def __init__(self, conserve: Address, operator: Address,
                 case_id: u256, expected_final_hash: str, expected_action_hash: str):
        if len(expected_final_hash) != 64 or len(expected_action_hash) != 64:
            raise gl.vm.UserError('expected 32-byte hashes')
        self.conserve = conserve
        self.operator = operator
        self.case_id = case_id
        self.expected_final_hash = expected_final_hash
        self.expected_action_hash = expected_action_hash
        self.consumed = False

    @gl.public.write
    def consume(self, action_hash: str) -> bool:
        if gl.message.sender_address != self.operator:
            raise gl.vm.UserError('not operator')
        if self.consumed:
            raise gl.vm.UserError('already consumed')
        if action_hash != self.expected_action_hash:
            raise gl.vm.UserError('different action')
        if not IConserve(self.conserve).view().is_conserved_for(self.case_id, self.expected_final_hash):
            raise gl.vm.UserError('conservation not finalized or hash mismatch')
        self.consumed = True
        return True

    @gl.public.view
    def get_status(self) -> dict:
        return {'consumed': self.consumed,
                'case_id': int(self.case_id),
                'final_hash': self.expected_final_hash,
                'action_hash': self.expected_action_hash}
