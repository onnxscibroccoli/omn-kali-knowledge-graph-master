import copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from goals_registry import add_goal,save_registry
from test_goals_registry import fixture
class Requests(unittest.TestCase):
 def new(self):
  g=copy.deepcopy(fixture()['goals'][0]);g.update(id='G2',requestKey='request-2',status='PLANNED');return g
 def test_repeated_request_is_idempotent(self):
  r=fixture();g=self.new();out=add_goal(r,g,0);self.assertEqual(add_goal(out,g,1),out);self.assertEqual(len(r['goals']),1)
 def test_conflicting_request_key_rejected(self):
  r=fixture();g=copy.deepcopy(r['goals'][0]);g['title']='different'
  with self.assertRaises(ValueError):add_goal(r,g,0)
 def test_stale_revision_does_not_write(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';r=fixture();p.write_text(json.dumps(r));out=add_goal(r,self.new(),0);save_registry(p,out,0);before=p.read_bytes()
   with self.assertRaises(ValueError):save_registry(p,out,0)
   self.assertEqual(p.read_bytes(),before)
 def test_invalid_goal_never_replaces_file(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';p.write_text(json.dumps(fixture()));before=p.read_bytes();r=fixture();r['goals'][0]['status']='SHIPPED'
   with self.assertRaises(ValueError):save_registry(p,r,0)
   self.assertEqual(p.read_bytes(),before)
 def test_interruption_keeps_valid_old_or_new_registry(self):
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';r=fixture();p.write_text(json.dumps(r));out=add_goal(r,self.new(),0)
   with patch('os.replace',side_effect=OSError('interrupted')):
    with self.assertRaises(OSError):save_registry(p,out,0)
   self.assertEqual(json.loads(p.read_text()),r)
if __name__=='__main__':unittest.main()
