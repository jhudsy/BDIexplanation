from lark import Lark, Transformer
from rule import *

parser= Lark(r"""
STRING: /([a-zA-Z_][a-zA-Z0-9_]*)/
NUMBER: /(0|[1-9][0-9]*)/
COMMENT: /#[^\n]*/

ruleset: rules events
rules: (rule)*
events: (event)*

rule: beliefs "-(" priority ")->" effects
priority: NUMBER
beliefs: [belief ("," belief)*]
belief: STRING
effects: [effect ("," effect)*]
effect: addbelief | rembelief | action
action: "."STRING
addbelief:  "+" belief
rembelief: "-" belief

event: NUMBER ":" effects
%import common.WS
%ignore WS
%ignore COMMENT
""",start='ruleset')

class RulesTransformer(Transformer):

  def ruleset(self,args):
    #return rules and events
    return args

  def rules(self,args):
    return args
  
  def events(self,args):
    ev={}
    #return a time->event map
    for e in args:
      ev[e.time]=e
    return ev


  def rule(self,args):
    #arg[0]: set of beliefs,
    #arg[1]: priority
    #arg[2]: [belief,action] effects
    return Rule(args[0],args[2],args[1])

  def beliefs(self,args):
    return set(args)

  def priority(self,args):
    return args[0]

  def belief(self,args):
    return args[0]

  def addbelief(self,args):
    return AddBelief(args[0])

  def rembelief(self,args):
    return RemBelief(args[0])

  def action(self,args):
    return ExecuteAction(args[0])

  def effects(self,args):
    return set(args)

  def effect(self,args):
    return args[0]
    
  def event(self,args):
    return Event(args[0],args[1])

  def NUMBER(self,args):
    return int(args)
  
  def STRING(self,args):
    return str(args)

"""time in event list is 3 times shorter than time here so we include extra Nones to take care of that"""
def event_time_to_event_stack(events):
  event_stack=[None]*(4+max(events)*3) #make event stack the length of the last event + 4 to include an extra cycle of action and last perception event
  
  for i in range(len(event_stack)):
    if i%3==0 and events.get(i//3,None)!=None:
      #print(i,events[i//3],len(event_stack))
      event_stack[i]=events[i//3]

  return event_stack

def parse_string(string):
  (plans,events)=RulesTransformer().transform(parser.parse(string))
  return (plans,event_time_to_event_stack(events))

def parse_file(f):
  with open(filename,'r') as myfile:
    data=myfile.read()
    return parse_string(data)

#test a simple string
#s="""tsm -(1)-> -tsm,+gal
#       st,as,gal -(1)-> +aw, -as, .m1
#       st,aw,gal -(2)-> +at,-aw,-gal,+gts,.m2
#       al,gts -(3)-> -gts,.d
#       0:+st
#       6:+as,+gal
#  """

#print(parse_string(s))
