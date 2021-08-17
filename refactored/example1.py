from parser import parse_string,parse_file
from simpleBDI import *
from rule import Rule

#example from paper

ruleset="""
di,bs -(2)-> .ib,-bs
di,ws -(2)-> .iw,-ws

0:+di,+bs,+ws
"""
p=parse_string(ruleset)

trace=create_trace(TraceElement(set(),p[0],None,p[1],None,"p"))

i=0
for t in trace:
  print(i,t)
  i+=1
