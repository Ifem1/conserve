"""Unit checks for the optional one-shot external Conserve view consumer."""
import importlib.util
import sys
from pathlib import Path
import pytest
from conftest import A, B


def load(mod,monkeypatch):
    path=Path(__file__).resolve().parents[1]/'contracts'/'conservation_gate.py'
    spec=importlib.util.spec_from_file_location('local_conservation_gate',path)
    consumer=importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules,'local_conservation_gate',consumer)
    spec.loader.exec_module(consumer)
    return consumer


def wire(consumer,allowed=True):
    class View:
        def is_conserved_for(self,case_id,hash):
            assert case_id==3
            return allowed and hash=='a'*64
    class Gate:
        def view(self):return View()
    consumer.IConserve=lambda address: Gate()
    return consumer.ConservationGate(A,A,3,'a'*64,'b'*64)


def test_consumer_one_shot(mod,monkeypatch):
    consumer=load(mod,monkeypatch)
    gate=wire(consumer)
    with pytest.raises(Exception,match='different action'):
        gate.consume('c'*64)
    assert gate.consume('b'*64)
    assert gate.get_status()['consumed'] is True
    with pytest.raises(Exception,match='already consumed'):
        gate.consume('b'*64)


def test_consumer_requires_owner_and_finalized_source(mod,monkeypatch):
    consumer=load(mod,monkeypatch)
    gate=wire(consumer,allowed=False)
    with pytest.raises(Exception,match='not finalized'):
        gate.consume('b'*64)
    gate=wire(consumer)
    consumer.gl.message.sender_address=B
    with pytest.raises(Exception,match='not operator'):
        gate.consume('b'*64)


def test_consumer_rejects_bad_commitment(mod,monkeypatch):
    consumer=load(mod,monkeypatch)
    with pytest.raises(Exception,match='32-byte'):
        consumer.ConservationGate(A,A,3,'short','b'*64)
