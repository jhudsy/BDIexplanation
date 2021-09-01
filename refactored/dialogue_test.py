import sys
from BDIparser import parse_string,parse_file
from simpleBDI import *
from participant import *
from dialogue import *


def test1():
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


    a1=Participant(trace)
    a2=Participant(trace)

    wa=WhyNotAction("ib",3,a1)
    d=Dialogue(wa,a1,a2)
    lm=d.gather_responses_to_open_moves()
    while len(lm)!=0:
        print(str(lm[0]))
        d.make_move(lm[0])
        lm=d.gather_responses_to_open_moves()

test1()