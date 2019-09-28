
##########################################
class RuleEffect:
    """The effects of a rule, subclassed by other classes below"""
    def apply(self,kb):
      pass
##########################################

class ExecuteAction(RuleEffect):
  def __init__(self,action):
    super().__init__()
    self.action=action

  def apply(self,kb,public_trace):
      print ("system performs "+self.action);
      s = "s:"+self.action
      public_trace.append(s)

  def __repr__(self):
    return "."+self.action
##########################################

class AddBelief(RuleEffect):
    def __init__(self,belief):
      super().__init__()
      self.belief=belief

    def apply(self,kb,public_trace):
      kb.add_belief(self.belief)

    def __repr__(self):
        return "+"+self.belief
##########################################

class RemoveBelief(RuleEffect):
    def __init__(self,belief):
      super().__init__()
      self.belief=belief

    def apply(self,kb,public_trace):
      kb.remove_belief(self.belief)

    def __repr__(self):
      return "-"+self.belief
##########################################
class AddGoal(RuleEffect):
    def __init__(self,goal):
      super().__init__()
      self.goal=goal


    def apply(self,kb,public_trace):
      kb.add_goal(self.goal)

    def __repr__(self):
      return "+!"+self.goal
##########################################
class RemoveGoal(RuleEffect):
    def __init__(self,goal):
      super().__init__()
      self.goal=goal

    def apply(self,kb,public_trace):
      kb.remove_goal(self.goal)

    def __repr__(self):
      return "-!"+self.goal

##########################################
#######END RULE EFFECT CLASSES############
##########################################



class Rule:
  def __init__(self,beliefs=set(),goals=set(),effects=set()):
    self.beliefs=beliefs
    self.goals=goals
    self.effects=effects

  def __repr__(self):
      s=""
      for b in self.beliefs:
          s+=b+","
      for g in self.goals:
          s+="!"+g+","
      s+=" -> "
      for e in self.effects:
          s+=str(e)+","
      return s

##########################################

class KB:
    def __init__(self):
        self.beliefs=set()
        self.goals=set()
        self.rules=set()
        self.trace=[] #captures the beliefs,goals and rules applied at any point in time
        self.time=0

    def tick(self,public_trace,public_actions):
        """Does a clock tick in the KB. NOT THE ENVIRONMENT!!!"""
        rules=self.find_applicable_rules()
        if len(rules)!=0:
            rule=rules.pop()
        else:
            rule=Rule(set(),set(),set())

        #add action to the trace based on the selected rule. TODO: move to apply
        actions=set()
        for e in rule.effects:
          if e.__class__==ExecuteAction:
            actions.add(e.action)
            public_actions.add(e.action)

        #record the trace, which takes the form of beliefs, goals and applied rule and time stamp
        self.trace.append([set(self.beliefs),set(self.goals),actions,rule,self.time])


        self.execute(rule,public_trace)
        self.goals=self.goals-self.beliefs #remove goals that were achieved
        self.time+=1

    def find_applicable_rules(self):
        app=set()
        for r in self.rules:
            if r.beliefs <= self.beliefs and r.goals <= self.goals:
                app.add(r)
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
