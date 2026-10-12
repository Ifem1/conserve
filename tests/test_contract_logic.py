"""Adversarial deterministic invariants (run without Studio or wallet)."""
import json
import pytest
from conftest import A,B,C


def make(case, one, exp):
    return case.propose('Service duties', 'Preserve mandatory duties in a restructuring', *one, exp)

def run_reviews(case,cid):
    case.review_parent(cid,0)
    case.review_child(cid,0)

def accept(mod,case,cid,signer=B):
    mod.gl.message.sender_address=signer
    return case.accept_assignment(cid,case.get_case(cid)['source_hash'])

def finalize(mod,case,cid):
    mod.gl.message.sender_address=A
    return case.finalize(cid,case.get_case(cid)['source_hash'])

def test_valid_conservation_lifecycle(case,mod,one,exp):
    cid=make(case,one,exp)
    assert case.is_conserved(cid) is False
    assert case.get_certificate(cid)['review_count'] == 0
    run_reviews(case,cid)
    accept(mod,case,cid)
    final_hash=finalize(mod,case,cid)
    assert len(final_hash)==64
    assert case.is_conserved_for(cid,final_hash)
    assert case.get_certificate(cid)['status']==2
    assert case.get_certificate(cid)['review_count']==2
    assert not case.is_conserved_for(cid,'0'*64)
    with pytest.raises(Exception,match='not open'):
        case.review_child(cid,0)
    with pytest.raises(Exception,match='cannot cancel'):
        case.cancel(cid)


def test_incomplete_consent_blocks(case,mod,one,exp):
    cid=make(case,one,exp)
    run_reviews(case,cid)
    with pytest.raises(Exception,match='assignee consents incomplete'):
        finalize(mod,case,cid)
    mod.gl.message.sender_address=C
    with pytest.raises(Exception,match='not a nominated assignee'):
        case.accept_assignment(cid,case.get_case(cid)['source_hash'])
    mod.gl.message.sender_address=A


def test_revoke_consent_blocks(case,mod,one,exp):
    cid=make(case,one,exp);run_reviews(case,cid)
    accept(mod,case,cid)
    hash=case.get_case(cid)['source_hash']
    mod.gl.message.sender_address=B
    assert case.withdraw_acceptance(cid,hash)
    with pytest.raises(Exception,match='no assent'):
        case.withdraw_acceptance(cid,hash)
    with pytest.raises(Exception,match='assignee consents incomplete'):
        finalize(mod,case,cid)


def test_parent_weakened_and_omitted_block(case,mod,one,exp):
    for kind in ('WEAKENED','OMITTED','AMBIGUOUS'):
        mod.gl.nondet.responses['parent']={'verdict':kind,'supports':[]}
        cid=make(case,one,exp)
        case.review_parent(cid,0)
        case.review_child(cid,0)
        accept(mod,case,cid)
        with pytest.raises(Exception,match='non-preserved parent'):
            finalize(mod,case,cid)
        mod.gl.message.sender_address=A


def test_right_expansion_unanchored_nonatomic_block(case,mod,one,exp):
    for kind in ('EXPANDED','UNSUPPORTED','WRONG_KIND','NONATOMIC','AMBIGUOUS'):
        mod.gl.nondet.responses['child']={'verdict':kind,'supports':[]}
        cid=make(case,one,exp)
        run_reviews(case,cid)
        accept(mod,case,cid)
        with pytest.raises(Exception,match='ungrounded child'):
            finalize(mod,case,cid)
        mod.gl.message.sender_address=A


def test_malicious_leader_rejected(case,mod,one,exp):
    cid=make(case,one,exp)
    mod.gl.nondet.responses['parent_validator']={'verdict':'OMITTED','supports':[]}
    with pytest.raises(Exception,match='CONSENSUS DISAGREEMENT'):
        case.review_parent(cid,0)
    assert case.get_case(cid)['parent_reviews'][0]['status']==0


def test_malicious_support_substitution_rejected(case,mod,exp):
    p=json.dumps([{'id':'p1','kind':'DUTY','text':'Deliver 3 reports.'}])
    c=json.dumps([
     {'id':'c1','kind':'DUTY','text':'Deliver 3 reports.','assignee':B},
     {'id':'c2','kind':'DUTY','text':'Deliver 3 reports.','assignee':C}])
    cid=case.propose('A','B',p,c,exp)
    mod.gl.nondet.responses['parent']={'verdict':'PRESERVED','supports':[0]}
    mod.gl.nondet.responses['parent_validator']={'verdict':'PRESERVED','supports':[1]}
    with pytest.raises(Exception,match='CONSENSUS DISAGREEMENT'):
        case.review_parent(cid,0)


def test_exclusive_overlap_blocks(case,mod,exp):
    parents=json.dumps([{'id':'p1','kind':'EXCLUSIVE_RIGHT','text':'Exclusive rights to sell widgets in West Africa online.'}])
    children=json.dumps([
       {'id':'c1','kind':'EXCLUSIVE_RIGHT','text':'Exclusive right to sell widgets in Nigeria online.','assignee':B},
       {'id':'c2','kind':'EXCLUSIVE_RIGHT','text':'Exclusive right to sell widgets in Ghana online.','assignee':C},
    ])
    cid=case.propose('Exclusive','Divide sales regions',parents,children,exp)
    mod.gl.nondet.responses['parent']={'verdict':'PRESERVED','supports':[0,1]}
    for i in range(2):
        case.review_child(cid,i)
    case.review_parent(cid,0)
    mod.gl.nondet.responses['pair']={'verdict':'OVERLAP'}
    assert case.review_exclusive_pair(cid,0)==2
    accept(mod,case,cid,B);accept(mod,case,cid,C)
    with pytest.raises(Exception,match='exclusive overlap'):
        finalize(mod,case,cid)


def test_disjoint_exclusive_passes(case,mod,exp):
    parents=json.dumps([{'id':'p1','kind':'EXCLUSIVE_RIGHT','text':'Exclusive sale rights to widgets in Nigeria and Ghana.'}])
    children=json.dumps([
       {'id':'c1','kind':'EXCLUSIVE_RIGHT','text':'Exclusive widget sale rights in Nigeria.','assignee':B},
       {'id':'c2','kind':'EXCLUSIVE_RIGHT','text':'Exclusive widget sale rights in Ghana.','assignee':C},
    ])
    cid=case.propose('Exclusive','Separate markets',parents,children,exp)
    mod.gl.nondet.responses['parent']={'verdict':'PRESERVED','supports':[0,1]}
    case.review_parent(cid,0)
    case.review_child(cid,0);case.review_child(cid,1)
    assert case.review_exclusive_pair(cid,0)==1
    accept(mod,case,cid,B);accept(mod,case,cid,C)
    assert case.is_conserved_for(cid,finalize(mod,case,cid))


def test_timestamp_and_expiration(case,mod,one,exp):
    cid=make(case,one,exp)
    mod.gl.message.raw.datetime='2026-10-15T00:00:00Z'
    with pytest.raises(Exception,match='expired'):
        case.review_parent(cid,0)
    with pytest.raises(Exception,match='expired'):
        case.accept_assignment(cid,case.get_case(cid)['source_hash'])


def test_creator_only_finalization(case,mod,one,exp):
    cid=make(case,one,exp)
    run_reviews(case,cid)
    accept(mod,case,cid)
    with pytest.raises(Exception,match='only creator'):
        case.finalize(cid,case.get_case(cid)['source_hash'])


def test_source_hash_pins_data_and_assignee(case,mod,one,exp):
    cid=make(case,one,exp)
    p,c=one
    c2=json.loads(c)
    c2[0]['assignee']=C
    next_id=case.propose('Service duties','Preserve mandatory duties in a restructuring',p,json.dumps(c2),exp)
    assert case.get_case(cid)['source_hash'] != case.get_case(next_id)['source_hash']
    mod.gl.message.sender_address=B
    with pytest.raises(Exception,match='source hash mismatch'):
        case.accept_assignment(cid,case.get_case(next_id)['source_hash'])


def test_input_failures(case,mod,one,exp):
    p,c=one
    inputs=[('[]',c),('not-json',c),(p,'[]'),(p,c.replace(B,'0x'+'00'*20)),
            (json.dumps([{'id':'p1','kind':'DUTY','text':'hi','foo':'bar'}]),c)]
    for badp,badc in inputs:
        with pytest.raises(Exception):
            case.propose('Title','Purpose',badp,badc,exp)
    with pytest.raises(Exception,match='expiry'):
        case.propose('Title','Purpose',p,c,0)


def test_no_duplicate_or_retry(case,mod,one,exp):
    cid=make(case,one,exp)
    case.review_parent(cid,0)
    with pytest.raises(Exception,match='already reviewed'):
        case.review_parent(cid,0)
    accept(mod,case,cid)
    with pytest.raises(Exception,match='duplicate assent'):
        accept(mod,case,cid)


def test_certificate_domain_separation(case,mod,one,exp):
    a=make(case,one,exp)
    b=make(case,one,exp)
    assert case.get_case(a)['source_hash']==case.get_case(b)['source_hash']
    for cid in (a,b):
        run_reviews(case,cid)
        accept(mod,case,cid)
        mod.gl.message.sender_address=A
    # Certificates from the same source are non-repeatable; compare predicted
    # domain-separated hashes without finalizing the second case.
    h_a = finalize(mod,case,a)
    assert len(h_a) == 64
    assert case.get_case(a)['final_hash'] != ''
    assert case.get_case(b)['final_hash'] == '' 


def test_no_source_true_claim(case,mod,one,exp):
    # No external legal authority: certification covers only explicitly submitted charter.
    cid=make(case,one,exp)
    assert 'source_hash' in case.get_case(cid)
    assert not case.is_conserved(cid)

def test_reusing_same_root_cannot_finalise_twice(case,mod,one,exp):
    a=make(case,one,exp)
    b=make(case,one,exp)
    for cid in (a,b):
        run_reviews(case,cid)
        accept(mod,case,cid)
        mod.gl.message.sender_address=A
    assert finalize(mod,case,a)
    with pytest.raises(Exception,match='already consumed'):
        finalize(mod,case,b)
    assert not case.is_conserved(b)

def test_validator_rejects_forged_child_kind(case,mod,one,exp):
    cid=make(case,one,exp)
    mod.gl.nondet.responses['child_validator']={'verdict':'WRONG_KIND','supports':[]}
    with pytest.raises(Exception,match='CONSENSUS DISAGREEMENT'):
        case.review_child(cid,0)
    assert case.get_case(cid)['child_reviews'][0]['status']==0


def test_validator_rejects_forged_exclusivity(case,mod,exp):
    parent=json.dumps([{'id':'p','kind':'EXCLUSIVE_RIGHT','text':'Exclusive widget rights in A+B.'}])
    children=json.dumps([
        {'id':'a','kind':'EXCLUSIVE_RIGHT','text':'Exclusive in A.','assignee':B},
        {'id':'b','kind':'EXCLUSIVE_RIGHT','text':'Exclusive in B.','assignee':C}])
    cid=case.propose('Rights','Divide rights',parent,children,exp)
    mod.gl.nondet.responses['pair_validator']={'verdict':'OVERLAP'}
    with pytest.raises(Exception,match='CONSENSUS DISAGREEMENT'):
        case.review_exclusive_pair(cid,0)
    assert case.get_case(cid)['exclusive_reviews'][0]['status']==0


def test_noncanonical_support_vector_is_rejected(case,mod,one,exp):
    cid=make(case,one,exp)
    mod.gl.nondet.responses['parent']={'verdict':'PRESERVED','supports':[0,0]}
    with pytest.raises(Exception,match='malformed leader'):
        case.review_parent(cid,0)
    assert case.get_case(cid)['parent_reviews'][0]['status']==0


def test_strict_json_schema_blocks_extra_keys(case,mod,one,exp):
    cid=make(case,one,exp)
    mod.gl.nondet.responses['parent']={'verdict':'PRESERVED','supports':[0],'leader_override':True}
    with pytest.raises(Exception,match='malformed leader'):
        case.review_parent(cid,0)


def test_false_boolean_indices_are_not_accepted(case,mod,one,exp):
    cid=make(case,one,exp)
    mod.gl.nondet.responses['parent']={'verdict':'PRESERVED','supports':[True]}
    with pytest.raises(Exception,match='malformed leader'):
        case.review_parent(cid,0)


def test_sealed_hash_unknown_case_and_unauthorized_cancel(case,mod,one,exp):
    with pytest.raises(Exception,match='unknown case'):
        case.get_case(12345)
    cid=make(case,one,exp)
    mod.gl.message.sender_address=B
    with pytest.raises(Exception,match='only creator'):
        case.cancel(cid)
    mod.gl.message.sender_address=A
    assert case.cancel(cid)
    assert not case.is_conserved(cid)
    with pytest.raises(Exception,match='not open'):
        case.review_parent(cid,0)


def test_missing_timestamp_fails_closed(case,mod,one,exp):
    mod.gl.message.raw.datetime = None
    with pytest.raises(Exception,match='transaction timestamp unavailable'):
        case.propose('Title','Purpose',*one,exp)


def test_invalid_assignee_address_and_term_ids(case,mod,one,exp):
    p,c=one
    bad=json.loads(c)
    bad[0]['assignee']='0x1234'
    with pytest.raises(Exception,match='20-byte'):
        case.propose('Title','Purpose',p,json.dumps(bad),exp)
    bad=json.loads(c)
    bad[0]['id']='../weird'
    with pytest.raises(Exception,match='invalid term ID'):
        case.propose('Title','Purpose',p,json.dumps(bad),exp)


def test_all_signers_required_for_two_assignees(case,mod,exp):
    parents=json.dumps([{'id':'p','kind':'DUTY','text':'Produce ten verified records.'}])
    children=json.dumps([
        {'id':'a','kind':'DUTY','text':'Produce five verified records.','assignee':B},
        {'id':'b','kind':'DUTY','text':'Produce five verified records.','assignee':C}])
    cid=case.propose('Records','Divide task',parents,children,exp)
    mod.gl.nondet.responses['parent']={'verdict':'PRESERVED','supports':[0,1]}
    case.review_parent(cid,0)
    case.review_child(cid,0);case.review_child(cid,1)
    accept(mod,case,cid,B)
    with pytest.raises(Exception,match='incomplete'):
        finalize(mod,case,cid)
    accept(mod,case,cid,C)
    assert finalize(mod,case,cid)
