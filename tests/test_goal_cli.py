import json,subprocess,sys,tempfile,unittest
from pathlib import Path
from test_goals_registry import fixture
ROOT=Path(__file__).resolve().parents[1]
class CLI(unittest.TestCase):
 def runcli(self,*args):return subprocess.run([sys.executable,str(ROOT/'scripts/goals.py'),*args],cwd='/',text=True,capture_output=True)
 def test_arbitrary_cwd(self):self.assertEqual(self.runcli('validate').returncode,0)
 def test_malformed_json(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';p.write_text('secret malformed')
   out=self.runcli('validate','--registry',str(p));self.assertEqual(out.returncode,1);self.assertNotIn('secret',out.stderr);self.assertNotIn('Traceback',out.stderr)
 def test_missing_file(self):self.assertEqual(self.runcli('validate','--registry','/not-present').returncode,1)
 def test_revision_conflict(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';p.write_text(json.dumps(fixture()));q=Path(td)/'q.json';g=fixture()['goals'][0];g.update(id='G2',requestKey='request-2');q.write_text(json.dumps(g));out=self.runcli('add','--registry',str(p),'--request',str(q),'--expected-revision','5');self.assertEqual(out.returncode,1);self.assertNotIn('Traceback',out.stderr)
 def test_generated_output_drift(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';r=fixture();p.write_text(json.dumps(r));out=subprocess.run([sys.executable,str(ROOT/'scripts/render_goals.py'),'--registry',str(p),'--check'],capture_output=True);self.assertEqual(out.returncode,1)
 def test_cli_add(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'r.json';p.write_text(json.dumps(fixture()));q=Path(td)/'q.json';g=fixture()['goals'][0];g.update(id='G2',requestKey='request-2');q.write_text(json.dumps(g));self.assertEqual(self.runcli('add','--registry',str(p),'--request',str(q),'--expected-revision','0').returncode,0);self.assertEqual(json.loads(p.read_text())['revision'],1)
if __name__=='__main__':unittest.main()
