from human import *
from dialogue import *
from rule_parser import readfile
import sys

if __name__=="__main__":
    # kb is the `robot', hmm is the `human'
    kb=KB("robot")
    hmm=KB("human")
    
    # Both are instanted by reading in a file that consists of a program followed by an
    # input trace
    (rs,ev)=readfile(sys.argv[1])
    (hrs,hev)=readfile(sys.argv[2])
    public_trace = []
    actions = set()
    
    # instantiate the two agents with their rules
    for r in rs:
        kb.rules.append(r)
    for r in hrs:
        hmm.rules.append(r)
        
    # We now move through the two input traces (for up to 10 steps)
    for i in range(0,10):
        trace_point = [];
        # Although implemented as an array, a trace point is a tuple of the time step, i
        # Followed by any actions taken
        # e.g., a trace of 10 points can end up looking like
        # [[0], [1], [2], [3], [4, 'robot:move1', 'human:move1'], [5, 'robot:move2'], [6, 'robot:drill'], [7], [8], [9]]
        trace_point.append(i);

        kb.percieve(ev.get(i),trace_point)
        hmm.percieve(hev.get(i),trace_point)
        kb.tick(trace_point,actions)
        hmm.tick(trace_point,actions)

        public_trace.append(trace_point)

    print(public_trace)
    print(hmm.trace)
    print(kb.trace)
    dialogue=Dialogue(hmm,kb,actions,public_trace)
    while (dialogue.can_continue):
        print("\nDIALOGUE TURN:")
        dialogue.move()
        if (dialogue.is_closed()):
            print("\nDIALOGUE CLOSED\n")
            break
    print(dialogue)


