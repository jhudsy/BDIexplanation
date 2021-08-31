from participant import Participant
from copy import deepcopy
from rule import AddBelief, RemBelief

class Dialogue:
    p1: Participant
    p2: Participant

    def __init__(self, start_move, player1, player2):
        self.moves = [start_move]
        self.p1 = player1
        self.p2 = player2
        self.to_move = self.p1

    def get_other_player(self, player):
        if player == self.p1:
            return self.p2
        return self.p1

    def make_move(self, move):
        self.moves.append(move)
        for m in self.moves:
            if m is None or m.closed:
                continue
            m.try_close(self)

    def gather_responses_to_open_moves(self):
        lm = []
        for m in self.moves:
            if not m.closed:
                lm+=m.find_legal_moves(self)
        return lm


###############################################################################################################
class Move:

    def __init__(self, player, in_response_to):
        """player is the player making the move. responds_to is the move being responded to. closed is whether the
        move is closed. """
        self.player = player
        self.responds_to = in_response_to
        self.closed = False

    def try_close(self, dialogue):
        """by default a move is closed if it is already closed or there is a response to it. The only exception is
        why_plan(plan,time). We will overload this method there"""
        if self.closed:
            return True
        for m in dialogue.moves:
            if m.responds_to == self:
                self.closed = True
                return True
        return False

    def find_legal_moves(self, dialogue: Dialogue):
        """This returns a collection of legal responses to the current move, based on what is contained in the
        current dialogue. """
        pass

    def update_knowledge_base(self, other: Participant):
        """updates the current player (or typically the other player's) knowledge base given that the move was
        actually made"""
        pass


###############################################################################################################
class WhyNotAction(Move):
    def __init__(self, action, time, player):
        super().__init__(player, None)
        self.action = action
        self.time = time

    def __str__(self):
        return f"{self.player}:Why was action {self.action} not executed at time {self.time}?"

    def find_legal_moves(self, dialogue: Dialogue):
        legal_moves = []
        to_move = dialogue.get_other_player(self.player)
        legal_moves.append(WhyAction(self.action, self.time, to_move, self))
        if self.player.trace[self.time].action == self.action:
            legal_moves.append(DidAction(self.action, self.time, to_move, self))
        return legal_moves


###############################################################################################################
class WhyAction(Move):
    def __init__(self, action, time, player, responds_to):
        super().__init__(player, responds_to)
        self.action = action
        self.time = time

    def __str__(self):
        return f"{self.player}:Why was action {self.action} executed at time {self.time}?"

    def find_legal_moves(self, dialogue: Dialogue):
        legal_moves = []
        to_move = dialogue.get_other_player(self.player)
        if to_move.trace[self.time].action != self.action:
            legal_moves.append(DidntAction(self.action, self.time, to_move, self))
        legal_moves.append(AssertPlan(to_move.trace[self.time - 1].current_plan, self.time - 1, to_move, self))
        return legal_moves


###############################################################################################################
class DidAction(Move):
    def __init__(self, action, time, player, responds_to):
        super().__init__(player, responds_to)
        self.action = action
        self.time = time
        self.closed = True

    def __str__(self):
        return f"{self.player}: Action {self.action} was executed at time {self.time}"

    def find_legal_moves(self, dialogue: Dialogue):
        return []

    def update_knowledge_base(self, other: Participant):
        other.other[self.time].action = self.action


###############################################################################################################
class DidntAction(Move):
    def __init__(self, action, time, player, responds_to):
        super().__init__(player, responds_to)
        self.action = action
        self.time = time
        self.closed = True

    def __str__(self):
        return f"{self.player}: Action {self.action} was not executed at time {self.time}"

    def find_legal_moves(self, dialogue: Dialogue):
        return []

    def update_knowledge_base(self, other: Participant):
        other.other_constraints_trace[self.time].action = self.action


###############################################################################################################
class AssertPlan(Move):
    def __init__(self, plan, time, player, responds_to):
        super().__init__(player, responds_to)
        self.plan = plan
        self.time = time

    def __str__(self):
        return f"{self.player}:Plan {self.plan} was executed at time {self.time}"

    def find_legal_moves(self, dialogue: Dialogue):
        legal_moves = []
        to_move = dialogue.get_other_player(self.player)
        # legal moves are why plan, assert another plan, accept plan, not in library, or precedence.
        # why plan:
        legal_moves.append(WhyPlan(self.plan, self.time, to_move, self))
        # assert another plan if that happened at the same time
        if to_move.trace[self.time].current_plan != self.plan:
            legal_moves.append(AssertPlan(to_move.trace[self.time].current_plan, self.time, to_move, self))
        elif to_move.trace[self.time].current_plan != self.plan:
            legal_moves.append(AcceptPlan(self.plan, self.time, to_move, self))
        if self.plan not in to_move.trace[self.time].plans:
            legal_moves.append(NotInLibrary(self.plan, to_move, self))
        # Precedence is trickier, need to check for a parent assert (which we respond to).
        if self.responds_to.__class__ == AssertPlan and self.responds_to.plan.priority <= self.plan.priority:
            legal_moves.append(Precedence(self.plan, self.responds_to.plan, to_move, self))
        return legal_moves

    def update_knowledge_base(self, other: Participant):
        other.other[self.time].current_plan = self.plan
        if self.responds_to.__class__ == AssertPlan:
            other.other_constraints_trace[self.time].current_plan = self.responds_to.current_plan


###############################################################################################################
class AcceptPlan(Move):
    def __init__(self, plan, time, player, responds_to):
        super().__init__(player, responds_to)
        self.plan = plan
        self.time = time
        self.closed = True

    def __str__(self):
        return f"{self.player}: accepts that plan {self.plan} was executed at time {self.time}"

    def find_legal_moves(self, dialogue):
        return []

    def update_knowledge_base(self, other):
        other.other[self.time].current_plan = self.plan


###############################################################################################################
class NotInLibrary(Move):
    def __init__(self, plan, player, responds_to):
        super().__init__(player, responds_to)
        self.plan = plan
        self.closed = True

    def __str__(self):
        return f"{self.player}: plan {self.plan} is not in the plan library"

    def find_legal_moves(self, dialogue):
        return []

    def update_knowledge_base(self, other):
        other.other_constraints_plans().append(self.plan)


###############################################################################################################
class Precedence(Move):
    def __init__(self, plan, lower_prec_plan, player, responds_to):
        super().__init__(player, responds_to)
        self.plan = plan
        self.lower_prec_plan = lower_prec_plan
        self.closed = True

    def __str__(self):
        return f"{self.player}: plan {self.plan} has equal or higher precendence to plan {self.lower_prec_plan}"

    def find_legal_moves(self, dialogue):
        return []

    def update_knowledge_base(self, other):
        other.other_constraints_priorities.add(self.plan, self.lower_prec_plan)


###############################################################################################################
class WhyPlan(Move):
    def __init__(self, plan, time, player, responds_to):
        super().__init__(player, responds_to)
        self.plan = plan
        self.time = time

    def __str__(self):
        return f"{self.player}: Why was plan {self.plan} executed at time {self.time}?"

    def try_close(self, dialogue):
        bel = deepcopy(self.plan.beliefs)
        for m in dialogue.moves:
            if m.__class__ == AssertBelief and m.end == self.time - 1:
                bel.remove(m.belief)
        if len(bel) == 0:
            self.closed = True
            return True
        return False

    # the legal moves are assertions about beliefs held by the other participant at time t-1 that are in this plan.
    # We could just look at plan beleifs.
    # We prefilter things here based on the other player beliefs to reduce number of choices.
    def find_legal_moves(self, dialogue: Dialogue):
        beliefs_to_prove=self.plan.beliefs
        for m in dialogue.moves:
            if m.__class__==AssertBelief and m.end==self.time-1 and m.belief in beliefs_to_prove:
                beliefs_to_prove=beliefs_to_prove-set([m.belief])

        legal_moves = []
        to_move = dialogue.get_other_player(self.player)
        beliefs = to_move.trace[self.time-1].beliefs
        for b in beliefs_to_prove:
            if b in beliefs:
                for i in range(self.time , -1, -1):
                    if b not in to_move.trace[i].beliefs or i==-1: #problem is we get to 0 as we believed this from beginning
                        legal_moves.append(AssertBelief(b, i + 1, self.time - 1, to_move, self))
        return legal_moves


###############################################################################################################
class AssertBelief(Move):
    def __init__(self, belief, start_time, end_time, player, responds_to):
        super().__init__(player, responds_to)
        self.belief = belief
        self.start = start_time
        self.end = end_time

    def __str__(self):
        return f"{self.player}: asserts that belief {self.belief} held from time {self.start} until at least {self.end}"

    def find_legal_moves(self, dialogue):
        """we can ask why the belief held, or assert that the belief did not hold at some intermediate timepoint. For
        the latter, we consider the time interval in which the belief did not hold (according to the utterer). """
        legal_moves = []
        to_move = dialogue.get_other_player(self.player)
        for i in range(self.start, self.end + 1):
            legal_moves.append(WhyBelief(self.belief, i, to_move, self))

        if self.belief not in to_move.trace[self.end].beliefs:
            for i in range(self.end, 0, -1):
                if self.belief in to_move.trace[i].beliefs:
                    legal_moves.append(AssertNotBelief(self.belief, i, self.end, to_move, self))
                    break

        found_belief = True
        for i in range(self.start, self.end + 1):
            if self.belief not in to_move.trace[i].beliefs:
                found_belief = False
        if found_belief:
            legal_moves.append(AcceptBelief(self.belief, self.start, self.end, to_move, self))
        return legal_moves

    def update_knowledge_base(self, other: Participant):
        for i in range(self.start, self.end + 1):
            other.other[i].beliefs.add(self.belief)


###############################################################################################################
class AssertNotBelief(Move):
    def __init__(self, belief, start_time, end_time, player, responds_to):
        super().__init__(player, responds_to)
        self.belief = belief
        self.start = start_time
        self.end = end_time

    def __str__(self):
        return f"{self.player}: asserts belief {self.belief} does not hold between times {self.start} and {self.end} "

    def find_legal_moves(self, dialogue):
        """legal responses are accept and why"""
        legal_moves = []
        to_move = dialogue.get_other_player(self.player)
        # why is asked about the start time of the belief
        legal_moves.append(WhyNotBelief(self.belief, self.start, to_move, self))
        accept_not_belief = True
        for i in range(self.start, self.end + 1):
            if self.belief in to_move.trace[i].beliefs:
                accept_not_belief = False
                break
        if accept_not_belief:
            legal_moves.append(AcceptNotBelief(self.belief, self.start, self.end, to_move, self))

    def update_knowledge_base(self, other: Participant):
        for i in range(self.start, self.end + 1):
            other.other_constraints_trace[i].beliefs.add(self.belief)


###############################################################################################################
class WhyBelief(Move):
    def __init__(self, belief, time, player, responds_to):
        super().__init__(player, responds_to)
        self.belief = belief
        self.time = time

    def __str__(self):
        return f"{self.player} asks why belief {self.belief} holds at time {self.time}?"

    def find_legal_moves(self, dialogue):
        """legal responses are assert plan at time t-1 and percept"""
        legal_moves = []
        to_move = dialogue.get_other_player(self.player)
        if AddBelief(self.belief) in to_move.trace[self.time - 1].current_plan:
            legal_moves.append(AssertPlan(to_move.trace[self.time - 1].current_plan, self.time - 1, to_move, self))
        if AddBelief(self.belief) in to_move.trace[self.time - 1].event_stack[0]:  # TODO: Check time
            legal_moves.append(PerceptAddBelief(self.belief, self.time, to_move, self))
        return legal_moves  # NB. what if legal moves are empty?


###############################################################################################################
class WhyNotBelief(Move):
    def __init__(self, belief, time, player, responds_to):
        super().__init__(player, responds_to)
        self.belief = belief
        self.time = time

    def __str__(self):
        return f"{self.player} asks why belief {self.belief} holds at time {self.time}?"

    def find_legal_moves(self, dialogue):
        """legal responses are assert plan at time t-1 and percept"""
        legal_moves = []
        to_move = dialogue.get_other_player(self.player)
        if RemBelief(self.belief) in to_move.trace[self.time - 1].current_plan:
            legal_moves.append(AssertPlan(to_move.trace[self.time - 1].current_plan, self.time - 1, to_move, self))
        if RemBelief(self.belief) in to_move.trace[self.time - 1].event_stack[0]:  # TODO: Check time
            legal_moves.append(PerceptRemoveBelief(self.belief, self.time, to_move, self))
        return legal_moves  # NB. what if legal moves are empty?


###############################################################################################################
class AcceptBelief(Move):
    def __init__(self, belief, start_time, end_time, player, responds_to):
        super().__init__(player, responds_to)
        self.belief = belief
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.player} accepts that belief {self.belief} holds between {self.start_time} and {self.end_time}"

    def find_legal_moves(self, dialogue: Dialogue):
        return []

    def update_knowledge_base(self, other: Participant):
        for i in range(self.start_time, self.end_time + 1):
            other.other[i].beliefs.add(self.belief)


###############################################################################################################
class AcceptNotBelief(Move):
    def __init__(self, belief, start_time, end_time, player, responds_to):
        super().__init__(player, responds_to)
        self.belief = belief
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"{self.player} accepts that belief {self.belief} does not hold between {self.start_time} and " \
               f"{self.end_time}"

    def find_legal_moves(self, dialogue: Dialogue):
        return []

    def update_knowledge_base(self, other: Participant):
        for i in range(self.start_time, self.end_time + 1):
            other.other_constraints_trace[i].beliefs.add(self.belief)


###############################################################################################################
class PerceptAddBelief(Move):
    def __init__(self, belief, time, player, responds_to):
        super().__init__(player, responds_to)
        self.belief = belief
        self.time = time

    def __str__(self):
        return f"{self.player} percieved the addition of {self.belief} at time {self.time}"

    def find_legal_moves(self, dialogue: Dialogue):
        return []

    def update_knowledge_base(self, other: Participant):
        other.other[self.time].event_stack[0].add(AddBelief(self.belief))


###############################################################################################################

class PerceptRemoveBelief(Move):
    def __init__(self, belief, time, player, responds_to):
        super().__init__(player, responds_to)
        self.belief = belief
        self.time = time

    def __str__(self):
        return f"{self.player} percieved the removal of {self.belief} at time {self.time}"

    def find_legal_moves(self, dialogue: Dialogue):
        return []

    def update_knowledge_base(self, other: Participant):
        other.other[self.time].event_stack[0].add(RemBelief(self.belief))
