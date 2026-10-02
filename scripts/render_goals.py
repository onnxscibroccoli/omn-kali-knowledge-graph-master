#!/usr/bin/env python3
"""Render validated public goals. Private inventories never become public artifacts."""
import argparse,hashlib,json,re,sys
from pathlib import Path
from goals_registry import validate_registry,evaluate_goal
ROOT=Path(__file__).resolve().parents[1]
def _opaque(value):return 'private-'+hashlib.sha256(value.encode()).hexdigest()[:12]
def public_projection(r:dict)->dict:
 errors=validate_registry(r)
 if errors:raise ValueError('invalid registry')
 repos={x['id']:x for x in r['repositories']};private={x['id'] for x in r['repositories'] if x['visibility']=='private'}
 hidden={g['id'] for g in r['goals'] if g['ownerRepositoryId'] in private}
 names=[x['fullName'] for x in r['repositories'] if x['id'] in private]+list(hidden)
 names+= [c['id'] for g in r['goals'] if g['id'] in hidden for c in g['acceptanceCriteria']]
 def scrub(value):
  for name in sorted(names,key=len,reverse=True):value=value.replace(name,'Private reference')
  value=re.sub(r'https?://\S+|(?<!\S)/(?:\S+)|[A-Za-z]:[\\/]\S+','[reference withheld]',value)
  return value
 out=[];placeholders=set()
 for g in sorted(r['goals'],key=lambda x:x['id']):
  if g['id'] in hidden:continue
  deps=[_opaque(d) if d in hidden else d for d in g['dependencies']];placeholders.update(d for d in deps if d.startswith('private-'))
  ev=evaluate_goal(r,g['id'])
  out.append({'id':g['id'],'title':scrub(g['title']),'owner':repos[g['ownerRepositoryId']]['fullName'],'status':ev['effectiveStatus'],'dependencies':deps,'nextAction':scrub(g['nextAction']),'criteria':[dict(c,id=scrub(c['id'])) for c in ev['criteria']]})
 for pid in sorted(placeholders):out.append({'id':pid,'title':'Private dependency','owner':'Private repository','status':'NOT_PROVEN','dependencies':[],'nextAction':'Review privately','criteria':[]})
 return {'schema':'omnikali.public-goals/v1','revision':r['revision'],'goals':out}
def _safe(text):return re.sub(r'[\x00-\x1f"`<>|\\]',' ',str(text)).strip()
def render_goals(r:dict)->dict[str,str]:
 p=public_projection(r);goals=p['goals'];nodes={g['id']:'n'+str(i) for i,g in enumerate(goals)}
 mermaid=['flowchart TD'];md=['# Universal goals','',f'Registry revision: {r["revision"]}. Generated from `goals/universal.json`.','', '| Goal | Owner | Evidence status | Next action |','|---|---|---|---|'];speech=['Universal goals. Registry revision '+str(r['revision'])+'.']
 for g in goals:
  title=_safe(g['title']);mermaid.append(f'  {nodes[g["id"]]}["{title}: {g["status"]}"]')
  md.append('| '+ ' | '.join(_safe(x) for x in [g['id']+' — '+g['title'],g['owner'],g['status'],g['nextAction']])+' |')
  speech.append(f'{g["owner"]} owns goal {g["id"]}: {title}. Evidence status is {g["status"]}.')
  for c in g['criteria']:speech.append(f'Criterion {c["id"]} requires {c["requiredScope"]} evidence. Its result is {c["status"]}.')
  for dep in g['dependencies']:
   mermaid.append(f'  {nodes[g["id"]]} --> {nodes[dep]}');speech.append(f'Goal {g["id"]} depends on goal {dep}.')
  speech.append('Next action: '+_safe(g['nextAction'])+'.')
 md+=['','```mermaid',*mermaid,'```','','The narrative accompanies this diagram. Implementation, test proof and live proof are separate.']
 return {'graph/universal-goals.mmd':'\n'.join(mermaid)+'\n','docs/UNIVERSAL_GOALS.md':'\n'.join(md)+'\n','docs/UNIVERSAL_GOALS_NARRATIVE.txt':'\n'.join(speech)+'\n'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--registry',type=Path,default=ROOT/'goals/universal.json');ap.add_argument('--check',action='store_true');args=ap.parse_args()
 try:
  out=render_goals(json.loads(args.registry.read_text()))
  for relative,text in out.items():
   path=ROOT/relative
   if args.check:
    if not path.exists() or path.read_text()!=text:raise ValueError('generated output drift')
   else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
  print('GOAL VIEWS OK');return 0
 except (OSError,ValueError,KeyError,TypeError):print('GOAL VIEWS INVALID',file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
