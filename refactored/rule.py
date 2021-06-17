class Effect:
  #does an in-place update of the passed trace element
  def execute_effect(self,trace_element):
    pass
  
  def __init__(self,param):
    self.parameter=param

class AddBelief(Effect):
  def execute_effect(self,trace_element):
    trace_element.beliefs.add(self.parameter)

class RemBelief(Effect):
  def execute_effect(self,trace_element):
    trace_element.beliefs.discard(self.parameter)

class ExecuteAction(Effect):
  def execute_effect(self,trace_element):
    trace_element.action=trace_element

class Event:
  def __init__(self,time,effects):
    self.time=time
    self.effect=effects

class Rule:
  def __init__(self,beliefs,effects):
    self.beliefs=beliefs
    self.effects=effects
  
  def executed_actions(self):
    return set(map(lambda x: x.parameter, filter(lambda x:x.__class__==ExecuteAction,self.effects)))
  
  def added_beliefs(self):
    return set(map(lambda x: x.parameter, filter(lambda x:x.__class__==AddBelief,self.effects)))
  
  def removed_beliefs(self):
    return set(map(lambda x: x.parameter, filter(lambda x:x.__class__==RemBelief,self.effects)))

