import copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from goals_registry import validate_registry,evaluate_goal,save_registry
from render_goals import render_goals
from test_goals_registry import fixture,proof
class Review(unittest.TestCase):
 def test_malformed_fields_return_errors(self):
  for field in ['status','ownerRepositoryId','requestKey']:
   for bad in [[],{}]:
    r=fixture();r['goals'][0][field]=bad;self.assertTrue(validate_registry(r))
 def test_unmet_dependency_blocks_proof(self):
  r=fixture();proof(r);g=copy.deepcopy(r['goals'][0]);g.update(id='G2',requestKey='r2',status='PLANNED',evidenceRefs=[]);r['goals'].append(g);r['goals'][0]['dependencies']=['G2'];self.assertEqual(evaluate_goal(r,'G1')['effectiveStatus'],'BLOCKED')
 def test_transitive_dependency_blocks(self):
  r=fixture();proof(r);g=copy.deepcopy(r['goals'][0]);g.update(id='G2',requestKey='r2',status='PLANNED',evidenceRefs=[]);r['goals'].append(g);r['goals'][0]['dependencies']=['G2'];r['goals'][0]['status']='TEST_PROVEN';self.assertTrue(validate_registry(r))
 def test_mutable_artifact_not_proof(self):
  r=fixture();proof(r)['artifactRef']='https://host/artifacts/latest';self.assertNotEqual(evaluate_goal(r,'G1')['effectiveStatus'],'TEST_PROVEN')
 def test_public_free_text_redacted(self):
  r=fixture();r['goals'][0]['nextAction']='Open /private/inventory.json https://private.test/session';s='\n'.join(render_goals(r).values());self.assertNotIn('/private/inventory.json',s);self.assertNotIn('private.test',s)
 def test_private_id_redacted(self):
  r=fixture();repo=copy.deepcopy(r['repositories'][0]);repo.update(id='2',fullName='secret/private',visibility='private');r['repositories'].append(repo);g=copy.deepcopy(r['goals'][0]);g.update(id='PRIVATE_GOAL',requestKey='r2',ownerRepositoryId='2',affectedRepositories=['2']);r['goals'].append(g);r['goals'][0]['nextAction']='Use PRIVATE_GOAL';s='\n'.join(render_goals(r).values());self.assertNotIn('PRIVATE_GOAL',s)
 def test_unaudited_change_not_saved(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';r=fixture();p.write_text(json.dumps(r));r['revision']=1;r['goals'][0]['title']='Changed'
   with self.assertRaises(ValueError):save_registry(p,r,0)
 def test_seed_ownership_and_blockers(self):
  r=json.loads((Path(__file__).resolve().parents[1]/'goals/universal.json').read_text());goals={g['id']:g for g in r['goals']};repos={x['id']:x['fullName'] for x in r['repositories']};self.assertEqual(repos[goals['ARCH-G11']['ownerRepositoryId']],'onnxscibroccoli/Grasshopper');self.assertTrue(goals['ARCH-G13']['blockers']);self.assertTrue(goals['ARCH-G14']['blockers'])
 def test_later_lower_scope_failure_blocks(self):
  r=fixture();e=copy.deepcopy(proof(r));e.update(id='E2',scope='UNIT',result='FAIL',timestamp='2026-10-03T00:00:00Z');r['evidence'].append(e);r['goals'][0]['evidenceRefs'].append('E2');self.assertNotEqual(evaluate_goal(r,'G1')['effectiveStatus'],'TEST_PROVEN')
 def test_mismatched_audit_rejected(self):
  from goals_registry import add_goal
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';r=fixture();p.write_text(json.dumps(r));g=copy.deepcopy(r['goals'][0]);g.update(id='G2',requestKey='r2');out=add_goal(r,g,0);out['audit'][-1]['goalId']='WRONG'
   with self.assertRaises(ValueError):save_registry(p,out,0)
if __name__=='__main__':unittest.main()
