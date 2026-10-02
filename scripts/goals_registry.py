"""Canonical goals validation and evidence evaluation. No execution side effects."""
from __future__ import annotations
import re
from datetime import datetime
STATUSES={'PLANNED','IN_PROGRESS','BLOCKED','IMPLEMENTED','TEST_PROVEN','LIVE_PROVEN','REGRESSED','RETIRED'}
SCOPES={'UNIT','INTEGRATION','LIVE','RECONSTRUCTION'}
RESULTS={'PASS','FAIL','NOT_PROVEN','NOT_APPLICABLE','SKIPPED'}
HEX40=re.compile(r'^[a-f0-9]{40}$');HEX64=re.compile(r'^[a-f0-9]{64}$')
GOAL_STRINGS=('id','title','requestKey','requestedAt','requestedBy','sourceRequestRef','ownerRepositoryId','capability','targetArchitecture','status','nextAction')
GOAL_LISTS=('affectedRepositories','dependencies','acceptanceCriteria','implementationRefs','evidenceRefs','blockers','supersedes')
def immutable_artifact(v):
 if not isinstance(v,str):return False
 return bool(re.fullmatch(r'artifact:[A-Za-z0-9_.-]+|sha256:[a-f0-9]{64}|https://github\.com/[^/]+/[^/]+/actions/runs/[0-9]+/artifacts/[0-9]+',v))

def _text(v): return isinstance(v,str) and bool(v.strip())
def _timestamp(v):
 try:
  d=datetime.fromisoformat(v.replace('Z','+00:00'));return d.timestamp() if d.tzinfo else None
 except (ValueError,TypeError,AttributeError): return None
def _revision(v): return type(v) is int and v>=0

def validate_registry(r: dict)->list[str]:
 errors=[]
 if not isinstance(r,dict): return ['registry must be an object']
 if r.get('schema')!='omnikali.universal-goals/v1': errors.append('unsupported schema')
 if not _revision(r.get('revision')): errors.append('invalid revision')
 for k in ('repositories','goals','evidence','audit'):
  if not isinstance(r.get(k),list): errors.append(f'{k} must be a list')
 if errors: return sorted(errors)
 def indexed(items,label):
  out={}
  for x in items:
   if not isinstance(x,dict) or not _text(x.get('id')): errors.append(f'{label}: invalid object/id');continue
   if x['id'] in out: errors.append(f'{label}: duplicate id {x["id"]}')
   out[x['id']]=x
  return out
 repos=indexed(r['repositories'],'repository');goals=indexed(r['goals'],'goal');evidence=indexed(r['evidence'],'evidence');keys=set()
 for repo in repos.values():
  if not _text(repo.get('fullName')) or not isinstance(repo.get('visibility'),str) or repo.get('visibility') not in {'public','private'}:errors.append('invalid repository metadata')
  b=repo.get('currentBindings')
  if not isinstance(b,dict) or not HEX40.fullmatch(str(b.get('codeSha',''))) or not HEX64.fullmatch(str(b.get('transportContractHash',''))):errors.append('invalid repository bindings')
 for g in goals.values():
  name=g['id']
  for k in GOAL_STRINGS:
   if not _text(g.get(k)): errors.append(f'{name}: missing {k}')
  for k in GOAL_LISTS:
   if not isinstance(g.get(k),list): errors.append(f'{name}: invalid {k}')
  if not isinstance(g.get('status'),str) or g.get('status') not in STATUSES:errors.append(f'{name}: invalid status')
  if not _revision(g.get('revision')) or _timestamp(g.get('requestedAt')) is None:errors.append(f'{name}: invalid revision/timestamp')
  if not isinstance(g.get('ownerRepositoryId'),str) or g.get('ownerRepositoryId') not in repos:errors.append(f'{name}: dangling owner')
  key=g.get('requestKey')
  if isinstance(key,str) and key in keys:errors.append(f'{name}: duplicate request key')
  keys.add(key if isinstance(key,str) else None)
  for field,target in [('affectedRepositories',repos),('dependencies',goals),('supersedes',goals),('evidenceRefs',evidence)]:
   if isinstance(g.get(field),list):
    for x in g[field]:
     if not isinstance(x,str) or x not in target:errors.append(f'{name}: dangling {field}')
  criteria=g.get('acceptanceCriteria',[])
  if isinstance(criteria,list):
   ids=[]
   for c in criteria:
    if not isinstance(c,dict) or not _text(c.get('id')) or not _text(c.get('description')) or not isinstance(c.get('requiredScope'),str) or c.get('requiredScope') not in SCOPES:errors.append(f'{name}: invalid criterion');continue
    ids.append(c['id'])
   if len(ids)!=len(set(ids)):errors.append(f'{name}: duplicate criterion')
   if not ids: errors.append(f'{name}: acceptance criteria required')
   for eid in g.get('evidenceRefs',[]) if isinstance(g.get('evidenceRefs'),list) else []:
    if isinstance(eid,str) and eid in evidence:
     e=evidence[eid]
     if e.get('criterionId') not in ids or e.get('repositoryId')!=g.get('ownerRepositoryId'):errors.append(f'{name}: foreign criterion/owner evidence')
 for e in evidence.values():
  if not isinstance(e.get('result'),str) or e.get('result') not in RESULTS or not isinstance(e.get('scope'),str) or e.get('scope') not in SCOPES or not isinstance(e.get('repositoryId'),str) or e.get('repositoryId') not in repos:errors.append('invalid evidence result/scope/owner')
  for k in ('criterionId','scenario','environmentId'):
   if not _text(e.get(k)):errors.append(f'evidence: missing {k}')
  if _timestamp(e.get('timestamp')) is None:errors.append('invalid evidence timestamp')
  if not HEX40.fullmatch(str(e.get('codeSha',''))) or not HEX64.fullmatch(str(e.get('transportContractHash',''))):errors.append('invalid evidence binding')
  if e.get('artifactSha256') and not HEX64.fullmatch(str(e['artifactSha256'])):errors.append('invalid artifact hash')
  if 'invalidatedAt' in e and _timestamp(e['invalidatedAt']) is None:errors.append('invalid invalidation timestamp')
  if type(e.get('provenanceVerified',False)) is not bool:errors.append('invalid provenance flag')
 visiting=set();visited=set()
 def visit(gid):
  if gid in visiting:errors.append('dependency cycle');return
  if gid in visited:return
  visiting.add(gid)
  ds=goals[gid].get('dependencies',[])
  if isinstance(ds,list):
   for d in ds:
    if isinstance(d,str) and d in goals:visit(d)
  visiting.remove(gid);visited.add(gid)
 for gid in goals:visit(gid)
 if not errors:
  for g in goals.values():
   if g['status'] in {'TEST_PROVEN','LIVE_PROVEN'}:
    actual=evaluate_goal(r,g['id'])['effectiveStatus']
    if actual not in {'TEST_PROVEN','LIVE_PROVEN'} or (g['status']=='LIVE_PROVEN' and actual!='LIVE_PROVEN'):errors.append(f'{g["id"]}: unsupported proof claim')
 return sorted(set(errors))

def evaluate_goal(r:dict,goal_id:str,_seen=None)->dict:
 seen=set(_seen or ())
 if goal_id in seen:raise ValueError('dependency cycle')
 seen.add(goal_id)
 g=next(x for x in r['goals'] if x['id']==goal_id)
 repo=next(x for x in r['repositories'] if x['id']==g['ownerRepositoryId']);binding=repo['currentBindings']
 records=[e for e in r['evidence'] if e['id'] in g['evidenceRefs']]
 criteria=[];regressed=False
 for c in g['acceptanceCriteria']:
  es=[e for e in records if e.get('criterionId')==c['id'] and e.get('repositoryId')==g['ownerRepositoryId']]
  matching=[e for e in es if e.get('codeSha')==binding['codeSha'] and e.get('transportContractHash')==binding['transportContractHash']]
  sufficient={'UNIT':SCOPES,'INTEGRATION':{'INTEGRATION','LIVE','RECONSTRUCTION'},'LIVE':{'LIVE'},'RECONSTRUCTION':{'RECONSTRUCTION'}}[c['requiredScope']]
  suitable=[e for e in matching if e.get('scope') in sufficient]
  latest=max((_timestamp(e.get('timestamp')) or 0 for e in matching),default=None)
  current=[e for e in matching if (_timestamp(e.get('timestamp')) or 0)==latest]
  def verified(e):return e.get('scope') in sufficient and e.get('result')=='PASS' and e.get('provenanceVerified') is True and immutable_artifact(e.get('artifactRef')) and bool(HEX64.fullmatch(str(e.get('artifactSha256','')))) and not e.get('invalidatedAt')
  passed=bool(current) and all(verified(e) for e in current)
  invalidated=any(e.get('result')=='PASS' and (e.get('invalidatedAt') or e not in matching) for e in es)
  failed=any(e.get('result')=='FAIL' for e in current)
  regressed |= (invalidated or failed) and not passed
  criteria.append({'id':c['id'],'status':'PASS' if passed else 'NOT_PROVEN','requiredScope':c['requiredScope']})
 status=g['status']
 if status!='RETIRED':
  if regressed:status='REGRESSED'
  elif criteria and all(c['status']=='PASS' for c in criteria): status='LIVE_PROVEN' if all(c['requiredScope']=='LIVE' for c in criteria) else 'TEST_PROVEN'
  elif status in {'TEST_PROVEN','LIVE_PROVEN'}:status='IMPLEMENTED'
 unmet=[d for d in g['dependencies'] if evaluate_goal(r,d,seen)['effectiveStatus'] not in {'TEST_PROVEN','LIVE_PROVEN'}]
 if unmet and status in {'TEST_PROVEN','LIVE_PROVEN'}:status='BLOCKED'
 return {'goalId':goal_id,'effectiveStatus':status,'criteria':criteria,'blockers':g['blockers']+(['acceptance evidence NOT_PROVEN'] if any(c['status']!='PASS' for c in criteria) else [])+['dependency NOT_PROVEN: '+d for d in unmet]}

def add_goal(registry:dict,goal:dict,expected_revision:int)->dict:
 import copy
 if registry['revision']!=expected_revision:raise ValueError('revision conflict')
 for old in registry['goals']:
  if old['requestKey']==goal['requestKey']:
   if old!=goal:raise ValueError('conflicting request key')
   return copy.deepcopy(registry)
 result=copy.deepcopy(registry);result['goals'].append(copy.deepcopy(goal));result['revision']+=1
 result['audit'].append({'revision':result['revision'],'action':'goal.added','goalId':goal['id'],'requestKey':goal['requestKey']})
 if validate_registry(result):raise ValueError('invalid goal request')
 return result

def save_registry(path,registry:dict,expected_revision:int)->None:
 import fcntl,json,os,tempfile
 from pathlib import Path
 path=Path(path);errors=validate_registry(registry)
 if errors:raise ValueError('invalid registry')
 with path.with_suffix(path.suffix+'.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  current=json.loads(path.read_text())
  if current.get('revision')!=expected_revision:raise ValueError('revision conflict')
  if registry['revision']!=expected_revision+1:raise ValueError('next revision required')
  if registry['audit'][:len(current['audit'])]!=current['audit']:raise ValueError('audit history changed')
  # This bounded writer implements addition only, so the audit must describe exactly it.
  old_ids={g['id'] for g in current['goals']}
  added=[g for g in registry['goals'] if g['id'] not in old_ids]
  if len(added)!=1 or registry['goals'][:-1]!=current['goals'] or registry['goals'][-1]!=added[0]:raise ValueError('unsupported goal mutation')
  expected={'revision':registry['revision'],'action':'goal.added','goalId':added[0]['id'],'requestKey':added[0]['requestKey']}
  if registry['audit'][len(current['audit']):]!=[expected]:raise ValueError('audit entry mismatch')
  if registry['repositories']!=current['repositories'] or registry['evidence']!=current['evidence']:raise ValueError('unsupported metadata mutation')
  tmp=None
  try:
   with tempfile.NamedTemporaryFile(mode='w',dir=path.parent,prefix='.'+path.name+'.',delete=False) as fh:
    tmp=fh.name;json.dump(registry,fh,indent=2,sort_keys=True);fh.write('\n');fh.flush();os.fsync(fh.fileno())
   os.replace(tmp,path);tmp=None
   fd=os.open(path.parent,os.O_RDONLY)
   try:os.fsync(fd)
   finally:os.close(fd)
  finally:
   if tmp is not None:os.unlink(tmp)
