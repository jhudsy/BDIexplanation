from parser import parse_string,parse_file
from simpleBDI import *
from rule import Rule
from participant import *
from dialogue import *

ruleset="""
  hungry,no_food,at_home-(1)-> +go_to_shops
  at_home,go_to_shops -(2)-> .drive,-at_home,+at_shops,-go_to_shops
  no_food,at_shops -(1)-> .buy_food,+go_home,+have_food,-no_food
  go_home -(1)-> .drive,-at_shops,+at_home,-go_home
  hungry,have_food,at_home -(1)-> .eat,-hungry,-have_food,+no_food

  at_shops,need_clothing-(2)->.buy_clothes,-need_clothing

  0:+hungry,+no_food,+at_home,+need_clothing
 24:+hungry
"""
p=parse_string(ruleset,timesteps=31)
print(p[1])

trace=create_trace(TraceElement(set(),p[0],None,p[1],None,"p"))

i=0
for t in trace:
  print(i,t.state,t.beliefs)
  if t.action!=None:
    print(i,t.action)
  i+=1

a1=Participant(trace,"a1")
a2=Participant(trace,"a2")

wa=WhyAction("drive",30,a2,None)
d=Dialogue(wa,a1,a2)
finished=False
while not finished:
    lm=d.gather_responses_to_open_moves()
    i=0
    resp={}
    for i in range(len(lm)):
      print(i,str(lm[i]))
    j=input("response?")
    d.make_move(lm[int(j)])
    lm=d.gather_responses_to_open_moves()
    if len(lm)==0:
      finished=True
