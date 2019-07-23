from env import *
from human import *
from rule_parser import readfile
from rule_parser_human import readfile as h_readfile
import sys



if __name__=="__main__":
    kb=KB()
    hmm=HUMAN_KB()
    (rs,ev)=readfile(sys.argv[1])
    (hrs,hev)=h_readfile(sys.argv[2])
    public_trace = []
    for r in rs:
        kb.rules.add(r)
    for r in hrs:
        hmm.rules.add(r)
    for i in range(0,100):
        trace_point = [];
        trace_point.append(i);
        if ev.get(i)!=None:
            for e in ev.get(i):
              e.apply(kb,trace_point)
        if hev.get(i)!=None:
            for e in hev.get(i):
              e.apply(hmm,trace_point)
        kb.tick(trace_point)
        hmm.tick(trace_point)
#print(kb)
        public_trace.append(trace_point)
        #for t in kb.trace:
        #print(t)
        #for t in hmm.trace:
    #print(t)
    print(public_trace)

