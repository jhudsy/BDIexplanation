class Move:
  def __init__(self,parent,player):
    self.closed=False
    self.parent=parent
    self.player=player
  
  def is_valid(self,me,op,constraints):
    """Me, op, constraints are traces - arrays of trace elements."""
    pass
  
  def check_closure(self):
    pass

  def effect(self,me,op,constraints):
    """N.B., me,op,constraints are traces but represent the me,op and constraints of the other player. That is me is the other player, op is myself and constraints are constraints on op (i.e., me). This is in contrast to check valid."""
             pass

class WhyAction(Move):
  def __init__(self,action,time):
    self.action=action
    self.time=time

  def is_valid(self,me,op,constraints):
    return me[self.time].stage=="e"
  
  def check_closure(self,dialogue):
    for d in dialogue:
      if d==Didnt(action,time) or (d.__class__=="Assert" and
                                   d.time=self.time-1 and
                                   ExecuteAction(self.action) in d.plan)
        return True
    return False

class WhyNotAction(Move):
  def __init__(self,action,time):
    self.action=action
    self.time=time
  
  def is_valid(self,me,op,constraints):
    return me[self.time].stage=="e"
  
  def check_closure(self,dialogue):
    for d in dialogue:
      if d==Did(action,time) or d==Why(action,time):
        return True
    return False

class WhyPlan(Move):
  def __init__(self,plan,time):
    self.plan=plan
    self.time=time

  def is_valid(self,me,op,constraints):
    return op[self.time].plan==plan #possible bug in paper regarding not checking phase? 
  
  def check_closure(self,dialogue):
    beliefs=set(self.plan.beliefs)
    for d in dialogue:
      if d.__class__=="Assert" and d.end_time==self.time-1:
        beliefs.remove(d.belief)
    return len(beliefs)==0

class WhyBelief(Move):
  def __init__(self,belief,time):
    self.belief=belief
    self.time=time
  
  def is_valid(self,me,op,constraints):
    return self.belief in op[self.time].beliefs
  
  def check_closure(self,dialogue):
    for d in dialogue:
      if d==Percept(AddBelief(self.belief),self.time):
        return True
      if d.__class__=AssertPlan and d.time=self.time-1 and AddBelief(self.belief) in d.plan.effects:
        return True
    return False

class WhyNotBelief(Move):
  def __init__(self,belief,time):
    self.belief=belief
    self.time=time
  
  def is_valid(self,me,op,constraints):
    return not(self.belief in op[self.time].beliefs)
  
  def check_closure(self,dialogue):
    for d in dialogue:
      if d==Percept(RemBelief(self.belief),self.time):
        return True
      if d.__class__=AssertPlan and d.time=self.time-1 and RemBelief(self.belief) in d.plan.effects:
        return True
    return False

class AssertPlan(Move):
  def __init__(self,plan,time):
    self.plan=plan
    self.time=time
  
  def is_valid(self,me,op,constraints):
    if not me[self.time].stage=="s":
      return False
    if not me[self.time].current_plan==self.plan:
      return False

    #now check whether following a whyAction, whyBelief or whyNotBelief
    
    for m in dialogue.moves:
      if not m.closed and m.__class__==WhyAction and m.action in self.plan.executed_actions():
        return True
      if not m.closed and m.__class__==WhyBelief and m.belief in self.plan.added_beliefs():
        return True
      if not m.closed and m.__class__==WhyNotBelief and m.belief in self.plan.removed_beliefs():
        return True
    return False
  
  def check_closure(self,dialogue):
    for d in dialogue:
      if d==WhyPlan(self.plan,self.time) or (d.__class__==AssertPlan and d.time==self.time) or d==AcceptPlan(self.plan,self.time) or d==NotInLibrary(self.plan) or (d.__class__==Precedence and d.plan==self.plan):
        return True
    return False
  
  def effect(self,me,op,constraints):
    op[self.time].plan=self.plan
    for d in dialogue:
      if d.__class__==AssertPlan and d.time==self.time:
        constraints[self.time]=self.plan


