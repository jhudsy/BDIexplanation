class TraceElement:
  def __init__(self,beliefs,plans,current_plan,event_stack,action,state):
    self.beliefs=beliefs
    self.plans=plans
    self.current_plan=current_plan
    self.event_stack=event_stack
    self.action=action
    self.state=state

from copy import deepcopy

def find_applicable_plan(beliefs,plans): #returns first applicable plan to simulate priority
  for p in plans:
    if p.beliefs.issubset(beliefs):
      return p
  return None

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
    


