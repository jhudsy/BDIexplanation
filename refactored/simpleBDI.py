class TraceElement:
  def __init__(self,beliefs,plans,current_plan,event_stack,action,state):
    self.beliefs=beliefs
    self.plans=plans
    self.current_plan=current_plan
    self.event_stack=event_stack
    self.action=action
    self.state=state

from copy import deepcopy

"""Highly inefficient implementation, but finds all plans of top priority which are applicable and returns a random one of these"""
def find_applicable_plan(beliefs,plans): 
  gathered_plans=set()
  gathered_priority=-1
  for p in plans:
    if p.beliefs.issubset(beliefs):
      if p.priority>gathered_priority:  #we've found a higher priority plan, flush gathered plans
         gathered_plans=set()
         gathered_plans.add(p)
         gathered_priority=p.priority
      elif p.priorty==gathered_priority: #same priority, add plan
         gathered_plans.add(p)
  if len(gathered_plans)==0:
    return None
  return random.choice(gathered_plans)

def do_perception(last_trace_element):
  if last_trace_element.state!="p":
    raise Exception("Incorrect state, expected p got",last_trace_element.state)
  
  new_trace_element=copy.deepcopy(last_trace_element)
  if len(new_trace_element.event_stack)==0:
    return None #end of execution
  
  current_event=new_trace_element.event_stack.pop()
    
  for e in current_event: #NB needs to be empty container for this to work
    e.execute_effect(new_trace_element)

  new_trace_element.state="s"
  return new_trace_element

def do_selection(last_trace_element):
  if last_trace_element.state!="s":
    raise Exception("Incorrect state, expected s got",last_trace_element.state)
  
  new_trace_element=copy.deepcopy(last_trace_element)
  if len(new_trace_element.event_stack)==0:
    raise Exception("Unexpected empty stack")
  
  new_trace_element.event_stack.pop() #remove null element as we are not doing perception

  plan=find_applicable_plan(new_trace_element.beliefs,new_trace_element.plans)
  new_trace_element.current_plan=plan
  new_trace_element.state="e"
  return new_trace_element

def do_execution(last_trace_element):
  if last_trace_element.state!="s":
    raise Exception("Incorrect state, expected s got",last_trace_element.state)
  
  new_trace_element=copy.deepcopy(last_trace_element)
  if len(new_trace_element.event_stack)==0:
    raise Exception("Unexpected empty stack")
  
  new_trace_element.event_stack.pop() #remove null element as we are not doing perception

  beliefs=new_trace_element.beliefs
  for e in new_trace_element.current_plan.effects:
    e.execute_effect(new_trace_element)
  new_trace_element.state="p"
  return new_trace_element

#initial_state should be (set(),plans,None,event_stack,none,"p")
def create_trace(initial_state):
  trace=[initial_state]
  while True:
    trace.append(do_perception(trace[-1]))
    if trace[-1]==None:
      return trace
    trace.append(do_selection(trace[-1]))
    trace.append(do_execution(trace[-1]))
    


