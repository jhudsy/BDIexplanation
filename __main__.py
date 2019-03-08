from env import *
from rule_parser import readfile
import sys



if __name__=="__main__":
    kb=KB()
    (rs,ev)=readfile(sys.argv[0])
    for r in rs:
        kb.rules.add(r)
    for i in range(0,100):
        if ev.get(i)!=None:
            for e in ev.get(i):
              e.apply(kb)
        kb.tick()
        print(kb)
