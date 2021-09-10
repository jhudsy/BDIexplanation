from lark import Lark, Transformer
from rule import *

parser = Lark(r"""
STRING: /([a-zA-Z_][a-zA-Z0-9_]*)/
NUMBER: /(0|[1-9][0-9]*)/
COMMENT: /#[^\n]*/

ruleset: rules events
rules: (rule)*
events: (event)*

rule: beliefs "-(" priority ")->" effects
priority: NUMBER
beliefs: [belief ("," belief)*]
belief: STRING
effects: [effect ("," effect)*]
effect: addbelief | rembelief | action
action: "."STRING
addbelief:  "+" belief
rembelief: "-" belief

event: NUMBER ":" effects
%import common.WS
%ignore WS
%ignore COMMENT
""", start='ruleset')


class RulesTransformer(Transformer):

    def ruleset(self, args):
        # return rules and events
        return args

    def rules(self, args):
        return args

    def events(self, args):
        ev = {}
        # return a time->event map
        for e in args:
            ev[e.time] = e
        return ev

    def rule(self, args):
        # arg[0]: set of beliefs,
        # arg[1]: priority
        # arg[2]: [belief,action] effects
        return Rule(args[0], args[2], args[1])

    def beliefs(self, args):
        return set(args)

    def priority(self, args):
        return args[0]

    def belief(self, args):
        return args[0]

    def addbelief(self, args):
        return AddBelief(args[0])

    def rembelief(self, args):
        return RemBelief(args[0])

    def action(self, args):
        return ExecuteAction(args[0])

    def effects(self, args):
        return set(args)

    def effect(self, args):
        return args[0]

    def event(self, args):
        return Event(args[0], args[1])

    def NUMBER(self, args):
        return int(args)

    def STRING(self, args):
        return str(args)



def event_time_to_event_stack(events,**kwargs):
    """time in event list is 3 times shorter than time here so we include extra Nones to take care of that. Alternatively, the timesteps parameter can be used to explicitly set the trace length"""
    timesteps=kwargs.get("timesteps",4+max(events)*3)
    event_stack = [None] * timesteps # make event stack the length of the last event + 4 to include an extra cycle of action and
    # last perception event

    for i in range(len(event_stack)):
        if i % 3 == 0 and events.get(i , None) is not None:
            event_stack[i] = events[i]

    return event_stack


def parse_string(string,**kwargs):
    """parses a string. N.B., adds a null plan of the form []-(0)->[]"""
    (plans, events) = RulesTransformer().transform(parser.parse(string))
    plans.append(Rule(set(), set(), 0))
    return (plans, event_time_to_event_stack(events,**kwargs))


def parse_file(filename,**kwargs):
    with open(filename, 'r') as myfile:
        data = myfile.read()
        return parse_string(data,**kwargs)
