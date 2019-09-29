from lark import Lark
from human import *

parser= Lark(r"""

STRING: /[a-zA-Z_]\w*/
NUMBER: /[0-9_]\w*/
COMMENT: /#[^\n]*/

ruleset: (rule)* (event)*
rule: body "->" effects
body: _beliefs [ _goals ]
_beliefs: [belief ("," belief)*]
belief: STRING
_goals: "!"goal ("," goal)*
goal: STRING
effects: [_effect ("," _effect)*]
_effect: addbelief | rembelief | addgoal | remgoal | action
action: "."STRING
addbelief:  "+"belief
rembelief: "-"belief
addgoal:  "+!"goal
remgoal:  "-!"goal

event: NUMBER ":" _effect

%import common.WS
%ignore WS
%ignore COMMENT

""",start='ruleset')

def readfile(filename):

  ruleset=[]
  events={}
  with open(filename,'r') as myfile:
    data=myfile.read()

  o=parser.parse(data)

  for r in o.find_data("rule"):
    beliefs=set()
    goals=set()
    effects=set()

    body=list(r.find_data("body"))[0]
    for belief in body.find_data("belief"):
      beliefs.add(belief.children[0].value)
    for goal in body.find_data("goal"):
      goals.add(goal.children[0].value)
    for a in r.find_data("addbelief"):
      effects.add(AddBelief(a.children[0].children[0].value))
    for a in r.find_data("addgoal"):
      effects.add(AddGoal(a.children[0].children[0].value))
    for a in r.find_data("rembelief"):
      effects.add(RemoveBelief(a.children[0].children[0].value))
    for a in r.find_data("remgoal"):
      effects.add(RemoveGoal(a.children[0].children[0].value))
    for a  in r.find_data("action"):  
      effects.add(ExecuteAction(a.children[0].value))
    ruleset.append(Rule(beliefs,goals,effects))


  for e in o.find_data("event"):
      time=int(e.children[0])

      if events.get(time)==None:
          events[time]=set()

      if e.children[1].data=="addbelief":
          events[time].add(AddBelief(e.children[1].children[0].children[0].value))
      if e.children[1].data=="addgoal":
          events[time].add(AddGoal(e.children[1].children[0].children[0].value))
      if e.children[1].data=="rembelief":
          events[time].add(RemoveBelief(e.children[1].children[0].children[0].value))
      if e.children[1].data=="remgoal":
          events[time].add(RemoveGoal(e.children[1].children[0].children[0].value))
  return (ruleset,events)
