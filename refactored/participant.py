from copy import deepcopy
from simpleBDI import TraceElement


class Participant:
    """A participant consists of their own trace, the other's trace and a set of (negative) constraints they have on
    the other, both on their trace and on priorities between plans. We assume that the plan library is static and can
    always refer to trace[0].plans, other[0].plans and other_constraints_trace[0].plans for these.

    Important: things in other_constraints_trace are negative constraints. If a belief appears here, it is *not* a
    belief for the other.
  """

    #trace: list[TraceElement]

    def __init__(self, trace):
        self.trace = trace

        self.other = deepcopy(trace)
        for i in range(len(trace)):
            self.other[i].beliefs = []
            self.other[i].plans = []
            self.other[i].current_plan = None
            for j in range(len(self.other[i].event_stack)):
                self.other[i].event_stack[j] = None
            self.other[i].action = None

        self.other_constraints_trace = deepcopy(self.other)
        self.other_constraints_priorities = []

    def plans(self):
        return self.trace[0].plans

    def other_plans(self):
        return self.other[0].plans

    def other_constraints_plans(self):
        return self.other_constraints_trace.plans

    def find_inconsistencies(self):
        """returns any inconsistency(ies) detected between self.trace, self.other/self.other_constraints"""
        pass
