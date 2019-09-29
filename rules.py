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
      print ("human expects "+self.action)
      s = "h:"+self.action
      public_trace.append(s)
      
  def effect_equals(self, effect):
    if (isinstance(effect, ExecuteAction)):
        return self.action == effect.action
    return False

  def __repr__(self):
    return "."+self.action
##########################################

class AddBelief(RuleEffect):
    def __init__(self,belief):
      super().__init__()
      self.belief=belief

    def apply(self,kb,public_trace):
      kb.add_belief(self.belief)

    def effect_equals(self, effect):
      if (isinstance(effect, AddBelief)):
          return self.belief == effect.belief
      return False

    def __repr__(self):
        return "+"+self.belief
##########################################

class RemoveBelief(RuleEffect):
    def __init__(self,belief):
      super().__init__()
      self.belief=belief

    def apply(self,kb,public_trace):
      kb.remove_belief(self.belief)

    def effect_equals(self, effect):
      if (isinstance(effect, RemoveBelief)):
          return self.belief == effect.belief
      return False

    def __repr__(self):
      return "-"+self.belief
##########################################
class AddGoal(RuleEffect):
    def __init__(self,goal):
      super().__init__()
      self.goal=goal

    def effect_equals(self, effect):
      if (isinstance(effect, AddGoal)):
          return self.goal == effect.goal
      return False

    def apply(self,kb,public_trace):
      kb.add_goal(self.goal)

    def __repr__(self):
      return "+!"+self.goal
##########################################
class RemoveGoal(RuleEffect):
    def __init__(self,goal):
      super().__init__()
      self.goal=goal

    def effect_equals(self, effect):
      if (isinstance(effect, RemoveGoal)):
          return self.goal == effect.goal
      return False

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
    
  def rule_equals(self, rule):
    for b in self.beliefs:
        if (not b in rule.beliefs):
            return False
    for g in self.goals:
        if (not g in rule.goals):
            return False
    for e in self.effects:
        not_present = True
        for e2 in rule.effects:
            if (e.effect_equals(e2)):
                not_present = False
                break;
        if (not_present):
            return False
    for b in rule.beliefs:
        if (not b in self.beliefs):
            return False
    for g in rule.goals:
        if (not g in self.goals):
            return False
    for e in rule.effects:
        not_present = True
        for e2 in self.effects:
             if (e.effect_equals(e2)):
                 not_present = False
                 break;
        if (not_present):
             return False
    return True
    
  def in_rule_list(self, rule_list):
    for rule in rule_list:
        if (self.rule_equals(rule)):
            return True
    return False

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

