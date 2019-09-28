from env import *

def why_belief(kb,belief,time):
    """respond with when the rule triggered the belief to become true"""
    if belief not in kb.trace[time][0]:
        return "belief did not hold at time "+str(time)

    for t in range(time,1,-1):
        r=kb.trace[t][2]
        for e in r.effects:
            if e.__class__==AddBelief and e.belief==belief:
                return "Rule "+str(r)+" created the belief at time "+t
        if belief in kb.trace[t][0] and belief not in kb.trace[t-1][0]:
            return "Environment added belief at time "+str(t)
    return "Environment added belief at time 0"

def why_goal(kb,goal,time):
    """respond with when the goal was created to become true and why"""
    if goal not in kb.trace[time][1]:
        return "goal did not hold at time "+str(time)

    for t in range(time,1,-1):
        r=kb.trace[t][2]
        for e in r.effects:
            if e.__class__==AddGoal and e.goal==goal:
                return "Rule "+str(r)+" created the goal at time "+str(t)
        if goal in kb.trace[t][1] and goal not in kb.trace[t-1][1]:
            return "Environment added goal at time "+str(t)
    return "Environment added goal at time 0"

def why_not_hold_belief(kb,belief,time):
    """The user is asking what rule caused the belief to be removed. What we
    seem to be doing is looking for the "temporally proximate cause", that is the rule that most recently
    caused the effect."""
    if belief in kb.trace[time][0]:
        return "belief did hold at time "+str(time)

    for t in range(time,1,-1):
        if belief not in kb.trace[t][0] and belief in kb.trace[t-1][0]:
            r=kb.trace[t-1][2]
            for e in r.effects:
                if e.__class__==RemoveBelief and e.belief==belief:
                    return "Rule "+str(r)+" removed belief at time "+str(t)
            #otherwise environment removed it
            return "Environment removed belief at time "+str(t)
    return "Belief did not hold at time 0"

def why_not_hold_goal(kb,goal,time):
    if goal in kb.trace[time][1]:
        return "goal did hold at time "+str(time)

    for t in range(time,1,-1):
        if goal not in kb.trace[t][1] and goal in kb.trace[t-1][1] and goal in kb.trace[t][0]:
            return "Belief created due to rule "+str(kb.trace[t-1][2])+" removed goal"
        if goal not in kb.trace[t][1] and goal in kb.trace[t-1][1]:
            r=kb.trace[t-1][2]
            for e in r.effects:
                if e.__class__==RemoveGoal and e.goal==goal:
                    return "Rule "+str(r)+" explicitly removed goal at time "+str(t)
        #otherwise environment removed it
            return "Environment removed goal at time "+str(t)
    return "Goal did not hold at time 0"
