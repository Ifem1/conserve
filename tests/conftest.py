"""Deterministic contract-logic harness. Not a substitute for GenVM Direct Mode."""
import hashlib
import importlib.util
import json
import sys
import types
import os
import pytest
from datetime import datetime, timezone
from pathlib import Path
import pytest

A = '0x' + '11' * 20
B = '0x' + '22' * 20
C = '0x' + '33' * 20


def pytest_configure(config):
    """Work around genlayer-test 0.29.2's open-stdin unlink bug on Windows."""
    if os.name != 'nt':
        return
    from gltest.direct import loader

    original_load = loader.load_contract_class

    def load_contract_class_windows(contract_path, vm, sdk_version=None):
        deferred_unlinks = []
        unlink = os.unlink

        def unlink_after_stdin_restore(path, *args, **kwargs):
            try:
                return unlink(path, *args, **kwargs)
            except PermissionError:
                deferred_unlinks.append(path)

        try:
            os.unlink = unlink_after_stdin_restore
            return original_load(contract_path, vm, sdk_version)
        finally:
            os.unlink = unlink
            stdin_fd = getattr(vm, '_original_stdin_fd', None)
            if stdin_fd is not None:
                try:
                    os.dup2(stdin_fd, 0)
                    os.close(stdin_fd)
                except OSError:
                    pass
                vm._original_stdin_fd = None
            for path in deferred_unlinks:
                try:
                    unlink(path)
                except FileNotFoundError:
                    pass

    loader.load_contract_class = load_contract_class_windows

class Map(dict):
    @classmethod
    def __class_getitem__(cls, item):
        return cls
    def get_or_insert_default(self, key):
        if key not in self:
            self[key] = types.SimpleNamespace()
        return self[key]

class Array(list):
    @classmethod
    def __class_getitem__(cls, item):
        return cls

class Return:
    def __init__(self, calldata): self.calldata = calldata

class VM:
    class UserError(Exception): pass
    Return = Return
    def run_nondet_unsafe(self, leader_fn, validator_fn):
        response = leader_fn()
        if not validator_fn(Return(response)):
            raise VM.UserError('CONSENSUS DISAGREEMENT')
        return response

class NonDet:
    responses = {}
    def exec_prompt(self, prompt, response_format=None):
        if 'PARENT CONSERVATION' in prompt:
            key = 'parent'
        elif 'CHILD AUTHORIZATION' in prompt:
            key = 'child'
        elif 'EXCLUSIVITY' in prompt:
            key = 'pair'
        else: raise AssertionError(prompt[:100])
        k = key + '_validator' if 'INDEPENDENT VERIFY' in prompt else key
        return self.responses.get(k, self.responses[key])

@pytest.fixture
def mod(monkeypatch):
    fake = types.ModuleType('genlayer')
    fake.TreeMap = Map
    fake.DynArray = Array
    fake.Address = str
    fake.u256 = int
    fake.u8 = int
    fake.allow_storage = lambda cls: cls
    fake.Keccak256 = lambda value: hashlib.sha3_256(value)
    fake.gl = types.SimpleNamespace(
        contract=types.SimpleNamespace(Contract=object),
        Contract=object,
        public=types.SimpleNamespace(write=lambda f:f,view=lambda f:f),
        contract_interface=lambda cls: cls,
        vm=VM(),
        nondet=NonDet(),
        message=types.SimpleNamespace(sender_address=A,raw=types.SimpleNamespace(datetime='2026-10-12T00:00:00Z')),
    )
    monkeypatch.setitem(sys.modules,'genlayer',fake)
    path=Path(__file__).resolve().parents[1]/'contracts'/'conserve.py'
    spec=importlib.util.spec_from_file_location('local_conserve',path)
    module=importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules,'local_conserve',module)
    spec.loader.exec_module(module)
    fake.gl.nondet.responses={
       'parent':{'verdict':'PRESERVED','supports':[0]},
       'child':{'verdict':'GROUNDED','supports':[0]},
       'pair':{'verdict':'DISJOINT'},
    }
    return module

@pytest.fixture
def case(mod):
    return mod.Conserve()

@pytest.fixture
def one():
    p=[{'id':'p1','kind':'DUTY','text':'The provider must deliver five signed reports by 31 December.'}]
    c=[{'id':'c1','kind':'DUTY','text':'The replacement provider must deliver five signed reports by 31 December.','assignee':B}]
    return json.dumps(p),json.dumps(c)

@pytest.fixture
def exp():
    return int(datetime(2026,10,14,tzinfo=timezone.utc).timestamp())
