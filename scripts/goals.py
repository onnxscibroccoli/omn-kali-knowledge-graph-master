#!/usr/bin/env python3
"""Goal capture CLI; no model, deployment or event replay side effects."""
import argparse,json,sys
from pathlib import Path
from goals_registry import validate_registry,evaluate_goal,add_goal,save_registry
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();subs=ap.add_subparsers(dest='command',required=True)
 for name in ('validate','status','add'):
  sub=subs.add_parser(name);sub.add_argument('--registry',type=Path,default=ROOT/'goals/universal.json')
  if name=='add':sub.add_argument('--request',type=Path,required=True);sub.add_argument('--expected-revision',type=int,required=True)
 args=ap.parse_args()
 try:
  r=json.loads(args.registry.read_text());errors=validate_registry(r)
  if errors:raise ValueError('invalid registry')
  if args.command=='add':
   g=json.loads(args.request.read_text());out=add_goal(r,g,args.expected_revision)
   if out!=r:save_registry(args.registry,out,args.expected_revision)
   print('GOAL REQUEST SAVED');return 0
  if args.command=='status':
   from render_goals import public_projection
   print(json.dumps(public_projection(r),indent=2));return 0
  print('GOALS OK');return 0
 except (OSError,ValueError,KeyError,TypeError,AttributeError):print('GOALS INVALID: check input or revision; no changes committed',file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
