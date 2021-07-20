from rules import *

class KB:
    def __init__(self):
        self.beliefs=set()
        self.goals=set()
        self.rules=[]
        self.trace=[] #captures the beliefs,goals and rules applied at any point in time
        self.time=0
        
    def percieve(self, belief_changes, trace_point):
        add_beliefs = set();
        removed_beliefs = set();
        if belief_changes != None:
            for e in belief_changes:
                if (isinstance(e, AddBelief)):
                    add_beliefs.add(e.belief)
                if (isinstance(e, RemoveBelief)):
                    removed_beliefs.add(e.belief)
            e.apply(self, trace_point)
        self.trace.append([set(self.beliefs),set(self.goals),set(add_beliefs),set(removed_beliefs),set(),Perception(),self.time])
        self.time += 1

    def tick(self,public_trace,public_actions):
        """Does a clock tick in the KB. NOT THE ENVIRONMENT!!!"""
        rules=self.find_applicable_rules()
        if len(rules)!=0:
            rule=rules.pop()
        else:
            rule=Rule(set(),set(),set())
            
        self.trace.append([set(self.beliefs),set(self.goals),set(),set(),set(),rule,self.time])
        self.time += 1

        #add action to the trace based on the selected rule. TODO: move to apply
        actions=set()
        add_beliefs = set();
        removed_beliefs = set();
        for e in rule.effects:
            if e.__class__==ExecuteAction:
                actions.add(e.action)
                public_actions.add(e.action)
            if (isinstance(e, AddBelief)):
                add_beliefs.add(e.belief)
            if (isinstance(e, RemoveBelief)):
                removed_beliefs.add(e.belief)

        self.execute(rule,public_trace)
        self.goals=self.goals-self.beliefs #remove goals that were achieved
        #record the trace, which takes the form of beliefs, goals and applied rule and time stamp
        self.trace.append([set(self.beliefs),set(self.goals),set(add_beliefs),set(removed_beliefs),actions,Rule(set(),set(),set()),self.time])

        self.time+=1

    def find_applicable_rules(self):
        app=[]
        for r in self.rules:
            if r.beliefs <= self.beliefs and r.goals <= self.goals:
                app.append(r)
        return app

    def execute(self,rule,public_trace):
        if rule==None:
            return
        #print("executing rule ", rule)
        for e in rule.effects:
            e.apply(self,public_trace)

    def add_goal(self,g):
        self.goals.add(g)

    def remove_goal(self,g):
        self.goals.discard(g)

    def add_belief(self,b):
        self.beliefs.add(b)

    def remove_belief(self,b):
        self.beliefs.discard(b)

    def __repr__(self):
        return "Beliefs: "+str(self.beliefs)+" Goals: "+str(self.goals)
        
    def name(self):
        return "robot"
  ##########################################
