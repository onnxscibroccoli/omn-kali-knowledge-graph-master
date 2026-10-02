import copy, sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from goals_registry import validate_registry, evaluate_goal

def fixture():
 return {'schema':'omnikali.universal-goals/v1','revision':0,'repositories':[{'id':'1','fullName':'owner/repo','visibility':'public','currentBindings':{'codeSha':'a'*40,'transportContractHash':'b'*64}}], 'goals':[{'id':'G1','title':'Goal','requestKey':'request-1','requestedAt':'2026-10-02T17:00:00Z','requestedBy':'user','sourceRequestRef':'request:1','ownerRepositoryId':'1','affectedRepositories':['1'],'capability':'browser','targetArchitecture':'independent','dependencies':[],'acceptanceCriteria':[{'id':'C1','description':'artifact verified','requiredScope':'INTEGRATION'}],'implementationRefs':[],'evidenceRefs':[],'status':'IMPLEMENTED','blockers':[],'nextAction':'verify','revision':0,'supersedes':[]}], 'evidence':[], 'audit':[]}
def proof(r,result='PASS',scope='INTEGRATION'):
 e={'id':'E1','repositoryId':'1','codeSha':'a'*40,'transportContractHash':'b'*64,'criterionId':'C1','scope':scope,'timestamp':'2026-10-02T17:00:00Z','result':result,'scenario':'test','environmentId':'isolated','artifactRef':'artifact:1','artifactSha256':'c'*64,'provenanceVerified':True}
 r['evidence']=[e];r['goals'][0]['evidenceRefs']=['E1'];return e
class RegistryTests(unittest.TestCase):
 def test_valid(self): self.assertEqual(validate_registry(fixture()),[])
 def test_duplicate_ids_rejected(self):
  r=fixture();r['goals']*=2;self.assertTrue(validate_registry(r))
 def test_dangling_owner_rejected(self):
  r=fixture();r['goals'][0]['ownerRepositoryId']='missing';self.assertTrue(validate_registry(r))
 def test_dependency_cycle_rejected(self):
  r=fixture();r['goals'][0]['dependencies']=['G1'];self.assertTrue(validate_registry(r))
 def test_repository_rename_preserves_owner(self):
  r=fixture();r['repositories'][0]['fullName']='owner/renamed';self.assertEqual(validate_registry(r),[])
 def test_unknown_status_rejected(self):
  r=fixture();r['goals'][0]['status']='SHIPPED';self.assertTrue(validate_registry(r))
 def test_empty_acceptance_cannot_claim_proven(self):
  r=fixture();r['goals'][0].update(status='TEST_PROVEN',acceptanceCriteria=[]);self.assertTrue(validate_registry(r))
 def test_malformed_roots_rejected(self):
  for r in [None,[],{}, {'schema':'omnikali.universal-goals/v1','goals':[None]}]: self.assertTrue(validate_registry(r))
 def test_proof_promotes(self):
  r=fixture();proof(r);self.assertEqual(evaluate_goal(r,'G1')['effectiveStatus'],'TEST_PROVEN')
 def test_skipped_job_not_proof(self):
  r=fixture();proof(r,'SKIPPED');self.assertNotEqual(evaluate_goal(r,'G1')['effectiveStatus'],'TEST_PROVEN')
 def test_missing_artifact_not_proof(self):
  r=fixture();proof(r)['artifactRef']='';self.assertNotEqual(evaluate_goal(r,'G1')['effectiveStatus'],'TEST_PROVEN')
 def test_stale_code_not_proof(self):
  r=fixture();proof(r)['codeSha']='d'*40;self.assertEqual(evaluate_goal(r,'G1')['effectiveStatus'],'REGRESSED')
 def test_changed_transport_not_proof(self):
  r=fixture();proof(r)['transportContractHash']='d'*64;self.assertEqual(evaluate_goal(r,'G1')['effectiveStatus'],'REGRESSED')
 def test_unit_scope_cannot_prove_live(self):
  r=fixture();r['goals'][0]['acceptanceCriteria'][0]['requiredScope']='LIVE';proof(r,scope='UNIT');self.assertNotEqual(evaluate_goal(r,'G1')['effectiveStatus'],'LIVE_PROVEN')
 def test_regression_preserves_history(self):
  r=fixture();proof(r)['invalidatedAt']='2026-10-03T00:00:00Z';original=copy.deepcopy(r);self.assertEqual(evaluate_goal(r,'G1')['effectiveStatus'],'REGRESSED');self.assertEqual(r,original)
 def test_later_failure_blocks_prior_pass(self):
  r=fixture();e=copy.deepcopy(proof(r));e.update(id='E2',result='FAIL',timestamp='2026-10-03T00:00:00Z');r['evidence'].append(e);r['goals'][0]['evidenceRefs'].append('E2');self.assertNotEqual(evaluate_goal(r,'G1')['effectiveStatus'],'TEST_PROVEN')
 def test_foreign_criterion_rejected(self):
  r=fixture();proof(r)['criterionId']='OTHER';self.assertTrue(validate_registry(r))
 def test_unverified_provenance_not_proof(self):
  r=fixture();proof(r)['provenanceVerified']=False;self.assertNotEqual(evaluate_goal(r,'G1')['effectiveStatus'],'TEST_PROVEN')
 def test_equal_time_failure_blocks(self):
  r=fixture();e=copy.deepcopy(proof(r));e.update(id='E2',result='FAIL');r['evidence'].append(e);r['goals'][0]['evidenceRefs'].append('E2');self.assertNotEqual(evaluate_goal(r,'G1')['effectiveStatus'],'TEST_PROVEN')
if __name__=='__main__': unittest.main()
