class Effect:
  #does an in-place update of the passed trace element
  def execute_effect(self,trace_element):
    pass
  
  def __init__(self,param):
    self.parameter=param

  def __eq__(self,other):
    return self.__class__==other.__class__ and self.parameter==other.parameter

  def __hash__(self):
    return hash(hash(self.parameter)+hash(self.__class__.__name__))

class AddBelief(Effect):
  def __str__(self):
    return f"+{self.parameter}"

  def execute_effect(self,trace_element):
    trace_element.beliefs.add(self.parameter)

class RemBelief(Effect):
  def __str__(self):
    return f"-{self.parameter}"
  def execute_effect(self,trace_element):
    trace_element.beliefs.discard(self.parameter)

class ExecuteAction(Effect):
  def __str__(self):
    return f".{self.parameter}"
  def execute_effect(self,trace_element):
    trace_element.action=self.parameter

class Event:
  def __init__(self,time,effects):
    self.time=time
    self.effect=effects

  def __str__(self):
    #return f"{self.time}:{list(str(e) for e in self.effect)}"
    return f"{list(str(e) for e in self.effect)}"

class Rule:
  def __init__(self,beliefs,effects,priority):
    self.beliefs=beliefs
    self.effects=effects
    self.priority=priority

  def __str__(self):
    return f"{list(str(b) for b in self.beliefs)}-({self.priority})->{list(str(e) for e in self.effects)}"
  
  def executed_actions(self):
    return set(map(lambda x: x.parameter, filter(lambda x:x.__class__==ExecuteAction,self.effects)))
  
  def added_beliefs(self):
    return set(map(lambda x: x.parameter, filter(lambda x:x.__class__==AddBelief,self.effects)))
  
  def removed_beliefs(self):
    return set(map(lambda x: x.parameter, filter(lambda x:x.__class__==RemBelief,self.effects)))

  def __eq__(self,other):
    if other.__class__!=self.__class__:
      return False
    return self.beliefs == other.beliefs and self.effects == other.effects and self.priority == other.priority

  def __hash__(self):
    h=sum(map(lambda x: hash(x),self.beliefs))
    h+=sum(map(lambda x: hash(x),self.effects))
    h+=self.priority
    return h