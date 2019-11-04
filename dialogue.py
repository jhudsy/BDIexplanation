import random
from dialogue_tree import *
from rules import ExecuteAction, AddBelief, RemoveBelief, Perception

# For ease of debugging
action_start = 1
action_end = 30

# Specific moves
class Move:
    def __init__(self, parent, player):
        self.closed = False
        self.parent = parent
        self.player = player
        
    def is_closed(self):
        return self.closed
        
    def get_player(self):
        return self.player
        
    def check_closure(self, position, store):
        pass
        
    def perform(self):
        if (self.parent.empty):
            self.parent.set_move(self)
        else:
            self.parent.add_child(self)
            
    def move_equals(self, move):
        print(self.player.name())
        print(move.player.name())
        if (self.player.name() == move.player.name()):
            return True
        return False
        
class WhyNotAction(Move):
    def __init__(self, turn, action, i, parent):
        Move.__init__(self, parent, turn)
        self.action = action
        self.trace_point = i
        
    def check_closure(self, position, store):
        for node in store.node_list():
            move = node.get_move()
            if (isinstance(move, WhyAction)):
                if move.action == self.action:
                    if (move.trace_point == self.trace_point):
                        self.closed = True
                        break
            if (isinstance(move, IDid)):
                if move.action == self.action:
                    if (move.trace_point == self.trace_point):
                        self.closed = True
                        break
    
    def __repr__(self):
        return str(self.player.name()) + ": Why Not " + str(self.action) + " at " + str(self.trace_point)
        
    def move_equals(self, move):
        if (isinstance(move, WhyNotAction)):
            if super.move_equals(move):
                if self.action == move.action:
                    if self.trace_point == move.trace_point:
                        return True
        return False
                
class WhyAction(Move):
    def __init__(self, turn, action, i, parent):
        Move.__init__(self, parent, turn)
        self.action = action
        self.trace_point = i
        
    def check_closure(self, position, store):
        for node in store.node_list():
            move = node.get_move()
            if (move.trace_point == self.trace_point - 1):
                if (isinstance(move, AssertPi)):
                    for effect in move.pi.effects:
                        if (isinstance(effect, ExecuteAction)):
                        # print (effect.action)
                        # print (move.action)
                            if effect.action == self.action:
                                self.closed = True
                                break
                    if (self.closed):
                        break
            if (isinstance(move, IDidnt)):
                 if move.action == self.action:
                    if (move.trace_point == self.trace_point):
                        self.closed = True
                        break
    
    def move_equals(self, move):
        if (isinstance(move, WhyAction)):
            if super().move_equals(move):
                if self.action == move.action:
                    if self.trace_point == move.trace_point:
                        return True
        return False
                
    def __repr__(self):
        return str(self.player.name()) + ": Why " + str(self.action) + " at " + str(self.trace_point)

class IDid(Move):
    def __init__(self, turn, action, i, parent):
        Move.__init__(self, parent, turn)
        self.action = action
        self.trace_point = i
        self.closed = True
        
    def move_equals(self, move):
        if (isinstane(move, IDid)):
            if super().move_equals(move):
                if self.action == move.action:
                    if self.trace_point == move.trace_point:
                        return True
        return False
        
    def __repr__(self):
        return str(self.player.name()) + ": I Did " + str(self.action) + " at " + str(self.trace_point)
        
class IDidnt(Move):
    def __init__(self, turn, action, i, parent):
        Move.__init__(self, parent, turn)
        self.action = action
        self.trace_point = i
        self.closed = True
        
    def move_equals(self, move):
        if (isinstane(move, IDidnt)):
            if super().move_equals(move):
                if self.action == move.action:
                    if self.trace_point == move.trace_point:
                        return True
        return False
        
    def __repr__(self):
        if (self.player.name() == "robot"):
            return str(self.player.name()) + ": I Didn't " + str(self.action) + " at " + str(self.trace_point)
        else:
            return str(self.player.name()) + ": I Didn't expect " + str(self.action) + " at " + str(self.trace_point)
        
class AssertPi(Move):
    def __init__(self, turn, pi, i, parent):
        Move.__init__(self, parent, turn)
        self.pi = pi
        self.trace_point = i
        self.closed = False
        
    def check_closure(self, position, store):
        for node in store.node_list():
            move = node.get_move()
            if (hasattr(move, 'trace_point')):
                if (move.trace_point == self.trace_point):
                    if (move.get_player() != self.get_player()):
                        if (isinstance(move, AssertPi)):
                            node_parent = move.parent
                            move_parent = node_parent.get_move()
                            if (move_parent.move_equals(self)):
                                self.closed = True
                                break
                        if (isinstance(move, WhyPi)):
                            self.closed = True
                            break
                        if (isinstance(move, AcceptPi)):
                            node_parent = move.parent
                            move_parent = node_parent.get_move()
                            if (move_parent.move_equals(self)):
                                self.closed = True
                                break
            else:
                if (move.get_player() != self.get_player()):
                    if (isinstance(move, NotInLibrary)):
                        if move.pi == self.pi:
                            self.closed = True
                            break
                    if (isinstance(move, Precedence)):
                        node_parent = move.parent
                        move_parent = node_parent.get_move()
                        if (move_parent.move_equals(self)):
                            self.closed = True
                            break
                            
    def move_equals(self, move):
        if (isinstance(move, AssertPi)):
            if (super().move_equals(move)):
                 if self.pi == move.pi:
                    if self.trace_point == move.trace_point:
                        return True
        return False
                        
    def __repr__(self):
        return str(self.player.name()) + ": Selected " + str(self.pi) + " at " + str(self.trace_point)
        
class NotInLibrary(Move):
    def __init__(self, turn, pi, parent):
        Move.__init__(self, parent, turn)
        self.pi = pi
        self.closed = True
        
    def move_equals(self, move):
        if (isinstance(move, NotInLibrary)):
            if (super().move_equals(move)):
                if self.pi == move.pi:
                    return True
        return False
        
    def __repr__(self):
        return str(self.player.name()) + ": " + str(self.pi) + " is not in my plan library"
        
class Precedence(Move):
    def __init__(self, turn, pi, parent):
        Move.__init__(self, parent, turn)
        self.pi = pi
        self.closed = True
        
        
    def move_equals(self, move):
        if (isinstance(move, Precedence)):
            if (super.move_equals(move)):
                if self.pi == move.pi:
                    return True
        return False

    def __repr__(self):
        return str(self.player.name()) + ": " + str(self.pi) + " has precedence in my plan library"
        
class AcceptPi(Move):
    def __init__(self, turn, pi, i, parent):
        Move.__init__(self, parent, turn)
        self.pi = pi
        self.trace_point = i
        self.closed = True
        
        
    def move_equals(self, move):
        if (isinstance(move, AcceptPi)):
            if (super().move_equals(move)):
                if self.pi == move.pi:
                    if self.trace_point == move.trace_point:
                        return True
        return False
        
    def __repr__(self):
        return str(self.player.name()) + ": I agree that " + str(self.pi) + " was selected at " + str(self.trace_point)
                
class WhyPi(Move):
    def __init__(self, turn, pi, i, parent):
        Move.__init__(self, parent, turn)
        self.pi = pi
        self.trace_point = i
        self.closed = False
        
    def check_closure(self, position, store):
        for bel in self.pi.beliefs:
            bel_literal = AddBelief(bel) # At the moment plans only contain positive beliefs
            bl_closed = False
            for node in store.node_list():
                move = node.get_move()
                if (isinstance(move, AssertBelief)):
                    if (move.belief.effect_equals(bel_literal)):
                        if (move.trace_point == self.trace_point):
                            bl_closed = True
                            break;
            if (not bl_closed):
                return
        self.closed = True
            
    def move_equals(self, move):
        if (isinstance(move, WhyPi)):
            if (super().move_equals(move)):
                if self.pi == move.pi:
                    if self.trace_point == move.trace_point:
                        return True

    def __repr__(self):
        return str(self.player.name()) + ": Why select " + str(self.pi) + " at " + str(self.trace_point)
        
class AssertBelief(Move):
    def __init__(self, turn, belief, i1, i2, parent):
        Move.__init__(self, parent, turn)
        self.belief = belief
        self.lowerbound = i1
        self.trace_point = i2
        
    def check_closure(self, position, store):
        for node in store.node_list():
            move = node.get_move()
            if (isinstance(move, WhyBelief)):
                if (move.belief == self.belief and move.trace_point == self.lowerbound):
                    self.closed = True
                    break
            if (isinstance(move, AssertBelief)):
                notbelief = move.belief
                if (isinstance(self.belief, AddBelief)):
                    if (isinstance(notbelief, RemoveBelief)):
                        if (self.belief.belief == notbelief.belief):
                            if (self.trace_point == move.trace_point):
                                if (self.lowerbound < move.lowerbound):
                                    self.closed = True
                                    break
                if (isinstance(self.belief, RemoveBelief)):
                    if (isinstance(notbelief, AddBelief)):
                        if (self.belief.belief == notbelief.belief):
                            if (self.trace_point == move.trace_point):
                                if (self.lowerbound < move.lowerbound):
                                    self.closed = True
                                    break
            if (isinstance(move, AcceptBelief)):
                if (move.belief == self.belief and move.trace_point == self.trace_point and move.lowerbound == self.lowerbound):
                    self.closed = True
                    break
                    
    def move_equals(self, move):
        if (isinstance(move, AssertBelief)):
             if super().move_equals(move):
                 if self.belief.effect_equals(move.belief):
                    if self.lowerbound == move.lowerbound:
                        if self.trace_point == move.trace_point:
                             return True
        return False
            

    def __repr__(self):
        return str(self.player.name()) + ": " + str(self.belief) + " at time " + str(self.lowerbound) + " and it remained so until at least " + str(self.trace_point)
        
class AcceptBelief(Move):
    def __init__(self, turn, belief, i1, i2, parent):
        Move.__init__(self, parent, turn)
        self.belief = belief
        self.lowerbound = i1
        self.trace_point = i2
        self.closed = True
        
    def move_equals(self, move):
        if (isinstance(move, AcceptBelief)):
             if super().move_equals(move):
                if self.belief.effect_equals(move.belief):
                    if self.lowerbound == move.lowerbound:
                        if self.trace_point == move.trace_point:
                            return True
        return False

    def __repr__(self):
        return str(self.player.name()) + ": I agree " + str(self.belief) + " between " + str(self.lowerbound) + " and " + str(self.trace_point)

class WhyBelief(Move):
    def __init__(self, turn, belief, i, parent):
        Move.__init__(self, parent, turn)
        self.belief = belief
        self.trace_point = i
        self.closed = False
        
    def check_closure(self, position, store):
        for node in store.node_list():
            move = node.get_move()
            if (isinstance(move, AssertPi)):
                if (move.trace_point == self.trace_point - 1):
                    self.closed = True
            if (isinstance(move, Percept)):
                if (move.trace_point == self.trace_point):
                    if (move.belief.effect_equals(self.belief)):
                        self.closed = True
    
    def move_equals(self, move):
        if (isinstance(move, WhyBelief)):
             if super().move_equals(move):
                if self.belief.effect_equals(move.belief):
                    if self.trace_point == move.trace_point:
                        return True

    def __repr__(self):
        return str(self.player.name()) + ": Why " + str(self.belief) + " at " + str(self.trace_point)
        
class Percept(Move):
    def __init__(self, turn, belief, i, parent):
        Move.__init__(self, parent, turn)
        self.belief = belief
        self.trace_point = i;
        self.closed = True
        
    def move_equals(self, move):
         if (isinstance(move, Percept)):
              if super().move_equals(move):
                 if self.belief.effect_equals(move.belief):
                     if self.trace_point == move.trace_point:
                         return True

    def __repr__(self):
        return str(self.player.name()) + ": I perceived " + str(self.belief) + " at " + str(self.trace_point)
        

# Types of move - there may be several of each sort that are legal at any one point
class MoveType:
    
    def legal(self, store, turn, actions):
        return []
        
class WhyNotActionType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        if (store.empty):
            for action in actions:
                for i in range(action_start, action_end):
                    move_list.append(WhyNotAction(turn, action, i, store))
        return move_list
        
class IDidActionType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move();
            if (not move.is_closed()):
                if (isinstance(move, WhyNotAction)):
                    if (move.get_player() != turn):
                        player_internal_trace_point = turn.trace[move.trace_point]
                        actions = player_internal_trace_point[4]
                        if (move.action in actions):
                            move_list.append(IDid(turn, move.action, move.trace_point, node))
        return move_list
        
class WhyActionType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                for action in actions:
                    for i in range(action_start, action_end):
                        move_list.append(WhyAction(turn, action, i, store))
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (isinstance(move, WhyNotAction)):
                    if (move.get_player() != turn):
                        move_list.append(WhyAction(turn, move.action, move.trace_point, node))
        return move_list
        
class IDidntType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move();
            if (not move.is_closed()):
                if (isinstance(move, WhyAction)):
                    if (move.get_player() != turn):
                        player_internal_trace_point = turn.trace[move.trace_point]
                        actions = player_internal_trace_point[4]
                        #print(player_internal_trace_point)
                        #print(actions)
                        #print(move.action)
                        if (not (move.action in actions)):
                            move_list.append(IDidnt(turn, move.action, move.trace_point, node))
        return move_list

class AssertPiType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (move.get_player() != turn):
                    if (isinstance(move, WhyAction)):
                        # print(move)
                        player_internal_trace_point = turn.trace[move.trace_point - 1]
                        rule = player_internal_trace_point[5]
                        if (rule.effects == set()):
                            break;
                        for effect in rule.effects:
                            # print(effect)
                            if (isinstance(effect, ExecuteAction)):
                                # print (effect.action)
                                # print (move.action)
                                if effect.action == move.action:
                                    move_list.append(AssertPi(turn, rule, move.trace_point - 1,node))
                                    break;
                    if (isinstance(move, WhyBelief)):
                        player_internal_trace_point = turn.trace[move.trace_point - 1]
                        rule = player_internal_trace_point[5]
                        if (rule.effects == set()):
                            break;
                        for effect in rule.effects:
                            if (move.belief.effect_equals(effect)):
                                move_list.append(AssertPi(turn, rule, move.trace_point - 1,node))
                                break
                    if (isinstance(move, AssertPi)):
                        player_internal_trace_point = turn.trace[move.trace_point]
                        rule = player_internal_trace_point[5]
                        if (rule.effects == set()):
                            break;
                        if (not rule.rule_equals(move.pi)):
                            potential_new_move = AssertPi(turn, rule, move.trace_point,node)
                            legal_move = True
                            for node1 in store.node_list():
                                if (node1.empty):
                                    continue
                                move1 = node.get_move();
                                if (move1.move_equals(potential_new_move)):
                                    legal_move = False
                                    break
                                if (move1.parent.get_move().move_equals(potential_new_move)):
                                    legal_move = False
                                    break
                            if (legal_move):
                                 move_list.append(potential_new_move)
        return move_list
        
class NotInLibraryType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (move.get_player() != turn):
                    if (isinstance(move, AssertPi)):
                        if (not move.pi.in_rule_list(turn.rules)):
                            move_list.append(NotInLibrary(turn, move.pi, node))
        return move_list
        
class PrecedenceType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (move.get_player() != turn):
                    if (isinstance(move, AssertPi)):
                        # print("found assert pi")
                        # print(move.pi)
                        # print(turn.rules)
                        if (move.pi.in_rule_list(turn.rules)):
                            # print("move pi in rules")
                            node_parent = move.parent
                            move_parent = node_parent.get_move()
                            if (isinstance(move_parent, AssertPi)):
                                # print("move parent is assert pi")
                                if (move_parent.get_player() == turn):
                                    # print("move parent is me")
                                    move_list.append(Precedence(turn, move_parent.pi, node))
        return move_list
        
class AcceptPiType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (move.get_player() != turn):
                    if (isinstance(move, AssertPi)):
                        trace_point_num = move.trace_point
                        trace_point = turn.trace[trace_point_num]
                        rule = trace_point[5]
                        if (rule.effects == set()):
                            break;
                        if (rule.rule_equals(move.pi)):
                            move_list.append(AcceptPi(turn, rule, trace_point_num, node))
        return move_list
        
class WhyPiType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (move.get_player() != turn):
                    if (isinstance(move, AssertPi)):
                        move_list.append(WhyPi(turn, move.pi, move.trace_point, node))
        return move_list
        
class AssertBeliefType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (move.get_player() != turn):
                    if (isinstance(move, WhyPi)):
                        pi = move.pi
                        trace_point = move.trace_point
                        for belief in pi.beliefs:
                            # print(belief)
                            # if (isinstance(belief, AddBelief)):
                            #     print("b")
                            #     bel = belief.belief
                            for x in range(trace_point, 0, -1):
                                if (belief in turn.trace[x][2]):
                                    new_move = AssertBelief(turn, AddBelief(belief), x, move.trace_point, node)
                                    # print(new_move)
                                    not_repeat = self.not_repeat(store, new_move)
                                    if not_repeat:
                                        # print("not repeated")
                                        move_list.append(new_move)
                                    break
                            # if (isinstance(belief, RemoveBelief)):
                            #     print("c")
                            #     bel = belief.belief
                            #     for x in range(trace_point, 0, -1):
                            #         if (bel in turn.trace[x][3]):
                            #             move_list.append(AssertBelief(turn, belief, x, move.trace_point, node))
                            #             break
                            #         if (x == 1):
                            #             move_list.append(AssertBelief(turn, belief, x, move.trace_point, node))
                    if (isinstance(move, AssertBelief)):
                        notbelief = move.belief
                        upperbound = move.trace_point
                        lowerbound = move.lowerbound
                        for x in range(upperbound, lowerbound, -1):
                            if (isinstance(notbelief, AddBelief)):
                                bel = notbelief.belief
                                if (bel in turn.trace[x][3]):
                                    new_move = AssertBelief(turn, RemoveBelief(bel), x, move.trace_point, node)
                                    not_repeat = self.not_repeat(store, new_move)
                                    if not_repeat:
                                        move_list.append(new_move)
                                    break
                            if (isinstance(notbelief, RemoveBelief)):
                                bel = notbelief.belief
                                if (bel in turn.trace[x][2]):
                                    new_move = AssertBelief(turn, AddBelief(bel), x, move.upperbound, node)
                                    not_repeat = self.not_repeat(store, new_move)
                                    if not_repeat:
                                        move_list.append(new_move)
                                    break
        return move_list
        
    def not_repeat(self, store, new_move):
        not_repeat = True
        for node in store.node_list():
            move1 = node.get_move()
            if (move1.move_equals(new_move)):
                if (move1.parent.get_move().move_equals(new_move.parent.get_move())):
                    not_repeat = False
                break
        return not_repeat
        
class AcceptBeliefType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (move.get_player() != turn):
                    if (isinstance(move, AssertBelief)):
                        bel_literal = move.belief
                        if (isinstance(bel_literal, AddBelief)):
                            belief = bel_literal.belief
                            lowerbound = move.lowerbound
                            upperbound = move.trace_point
                            for x in range(lowerbound, upperbound + 1):
                                holds = True
                                if (belief not in turn.trace[x][0]):
                                    holds = False
                                    break
                            if (holds):
                                move_list.append(AcceptBelief(turn, bel_literal, lowerbound, upperbound, node))
                        if (isinstance(bel_literal, RemoveBelief)):
                            belief = bel_literal.belief
                            lowerbound = move.lowerbound
                            upperbound = move.trace_point
                            for x in range(lowerbound, upperbound + 1):
                                holds = True
                                if (belief in turn.trace[x][0]):
                                    holds = False
                                    break
                            if (holds):
                                move_list.append(AcceptBelief(turn, bel_literal, lowerbound, upperbound, node))
        return move_list
        
class WhyBeliefType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            # print("why belief" + move.__repr__())
            if (not move.is_closed()):
                # print("a")
                if (move.get_player() != turn):
                    # print("b")
                    if (isinstance(move, AssertBelief)):
                        bel_literal = move.belief
                        move_list.append(WhyBelief(turn, bel_literal, move.lowerbound, node))
        return move_list

class PerceptType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (move.get_player() != turn):
                    if (isinstance(move, WhyBelief)):
                        bel_literal = move.belief
                        trace_point = move.trace_point
                        # print(turn.trace[trace_point])
                        if (isinstance(turn.trace[trace_point][5], Perception)):
                            if (isinstance(bel_literal, AddBelief)):
                                for belief in turn.trace[trace_point][2]:
                                    if (belief == bel_literal.belief):
                                        move_list.append(Percept(turn, bel_literal, trace_point, node))
                            if (isinstance(bel_literal, RemoveBelief)):
                                for belief in turn.trace[trace_point][3]:
                                    if (belief == bel_literal.belief):
                                        move_list.append(Percept(turn, bel_literal, trace_point, node))
        return move_list
                        
            
        
# Actual dialogue class

class Dialogue:
    def __init__(self, human, robot, actions, public_trace):
       # Basic strategy mechanism -- needs to be configurable somehow
       # self.strategy = "random"
       self.strategy = "public_action_diff"
    
       self.store=DialogueTree()
       self.turn = human;
       self.initiator = human;
       self.responder = robot;
       self.move_list = [];
       self.can_continue = True;
       self.actions = actions;
       self.public_trace = public_trace
       
       self.move_list.append(WhyNotActionType())
       self.move_list.append(IDidActionType())
       self.move_list.append(WhyActionType())
       self.move_list.append(IDidntType())
       self.move_list.append(AssertPiType())
       self.move_list.append(NotInLibraryType())
       self.move_list.append(PrecedenceType())
       self.move_list.append(AcceptPiType())
       self.move_list.append(WhyPiType())
       self.move_list.append(AssertBeliefType())
       self.move_list.append(AcceptBeliefType())
       self.move_list.append(WhyBeliefType())
       self.move_list.append(PerceptType())
    
    def move(self):
        legal_moves = self.calculate_legal_moves();
        if (len(legal_moves) == 0):
            # print("no legal moves for " + self.turn.name())
            if (self.turn == self.responder):
                self.turn = self.initiator
            else:
                self.turn = self.responder
                
            legal_moves = self.calculate_legal_moves()
            
            
        if (len(legal_moves) != 0):
            next_move = self.choose_next_move(legal_moves);
            next_move.perform()
            self.propagate_closure()
            
            next_turn = random.randint(0,1);
            if (next_turn == 0):
                self.turn = self.responder
            else:
                self.turn = self.initiator
            print(next_move)
        else:
            self.can_continue = False
            print("No Legal Moves")

    def calculate_legal_moves(self):
        legal_move_list = []
        for move_type in self.move_list:
            for move in move_type.legal(self.store, self.turn, self.actions):
                legal_move_list.append(move)
        # if len(legal_move_list) == 0:
        #     self.can_continue = False
        return legal_move_list
    
    def choose_next_move(self, move_list):
        if (self.strategy == "random"):
            return random.choice(move_list)
        if (self.strategy == "public_action_diff"):
            new_move_list = []
            if (self.store.empty):
                for move in move_list:
                    trace_point = move.trace_point
                    if (trace_point % 3 == 2): # This is a point where an action might have taken place
                        # print(move)
                        public_trace_point = (trace_point // 3) # This should be the relevant point in the public trace
                        # print(public_trace_point)
                        if (len(self.public_trace[public_trace_point]) > 1): # Someone was expecting an action here.
                            if (len(self.public_trace[public_trace_point]) > 2): # Everyone was expecting an action here.
                                robot_action_string = self.public_trace[public_trace_point][1].split(":")[1]
                                human_action_string = self.public_trace[public_trace_point][2].split(":")[1]
                                if (not robot_action_string == human_action_string):
                                    if (isinstance(move, WhyAction)):
                                        if (move.action == robot_action_string):
                                            new_move_list.append(move)
                                    if (isinstance(move, WhyNotAction)):
                                        if (move.action == human_action_string):
                                            new_move_list.append(move)
                            else:
                                action_array = self.public_trace[public_trace_point][1].split(":")
                                actor = action_array[0]
                                action = action_array[1]
                                if (actor == "robot"):
                                    if (isinstance(move, WhyAction)):
                                        # print(move)
                                        # print(action)
                                        # print(move.action)
                                        if (move.action == action):
                                            new_move_list.append(move)
                                else:
                                    if (isinstance(move, WhyNotAction)):
                                        if (move.action == action):
                                            new_move_list.append(move)
                        # print(self.public_trace[public_trace_point])
                        # print(self.turn.trace[trace_point])
                        # public_trace_point == public_trace[trace_point]
                return random.choice(new_move_list)
            else:
                return random.choice(move_list)
        
    def propagate_closure(self):
        i = 0
        for node in self.store.node_list():
            move = node.get_move()
            if (not move.is_closed()):
                move.check_closure(i, self.store)
            i = i + 1
        return
            
    def is_closed(self):
        if (len(self.store.node_list()) == 0):
            return False
        for node in self.store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            if (not move.is_closed()):
                return False;
        return True
    
    def can_proceed(self):
        return self.can_continue
        
    def __repr__(self):
        string = "Dialogue:\n"
        for node in self.store.node_list():
            if (node.empty):
                continue
            move = node.get_move()
            string += str(move) + "\n"
        return string
        
