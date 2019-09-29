import random
from dialogue_tree import *
from rules import ExecuteAction

# For ease of debugging
action_start = 4
action_end = 5

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
                
    def __repr__(self):
        return str(self.player.name()) + ": Why " + str(self.action) + " at " + str(self.trace_point)

class IDid(Move):
    def __init__(self, turn, action, i, parent):
        Move.__init__(self, parent, turn)
        self.action = action
        self.trace_point = i
        self.closed = True
        
    def __repr__(self):
        return str(self.player.name()) + ": I Did " + str(self.action) + " at " + str(self.trace_point)
        
class IDidnt(Move):
    def __init__(self, turn, action, i, parent):
        Move.__init__(self, parent, turn)
        self.action = action
        self.trace_point = i
        self.closed = True
        
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
                            if (move_parent == self):
                                self.closed = True
                                break
                        if (isinstance(move, WhyPi)):
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
                        if (move_parent == self):
                            self.closed = True
                            break
                        
                        
    def __repr__(self):
        return str(self.player.name()) + ": Selected " + str(self.pi) + " at " + str(self.trace_point)
        
class NotInLibrary(Move):
    def __init__(self, turn, pi, parent):
        Move.__init__(self, parent, turn)
        self.pi = pi
        self.closed = True
        
    def __repr__(self):
        return str(self.player.name()) + ": " + str(self.pi) + " is not in my plan library"
        
class Precedence(Move):
    def __init__(self, turn, pi, parent):
        Move.__init__(self, parent, turn)
        self.pi = pi
        self.closed = True
        
    def __repr__(self):
        return str(self.player.name()) + ": " + str(self.pi) + " has precedence in my plan library"
        
class WhyBelief(Move):
    def __init__(self, turn, belief, i, parent):
        Move.__init__(self, parent, turn)
        self.belief = belief
        self.trace_point = i
        self.closed = False
        
class WhyPi(Move):
    def __init__(self, turn, pi, i, parent):
        Move.__init__(self, turn, parent)
        self.pi = pi
        self.trace_point = i
        self.closed = False

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
                        if (move.belief in rule.effects):
                            move_list.append(AssertPi(turn, rule, move.trace_point - 1,node))
                    if (isinstance(move, AssertPi)):
                        player_internal_trace_point = turn.trace[move.trace_point]
                        rule = player_internal_trace_point[5]
                        if (rule.effects == set()):
                            break;
                        if (rule != move.pi):
                            potential_new_move = AssertPi(turn, rule, move.trace_point,node)
                            legal_move = True
                            for node1 in store.node_list():
                                if (node1.empty):
                                    continue
                                move1 = node.get_move();
                                if (move1 == potential_new_move):
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
        
# Actual dialogue class

class Dialogue:
    def __init__(self, human, robot, actions):
       self.store=DialogueTree()
       self.turn = human;
       self.initiator = human;
       self.responder = robot;
       self.move_list = [];
       self.can_continue = True;
       self.actions = actions;
       
       self.move_list.append(WhyNotActionType())
       self.move_list.append(IDidActionType())
       self.move_list.append(WhyActionType())
       self.move_list.append(IDidntType())
       self.move_list.append(AssertPiType())
       self.move_list.append(NotInLibraryType())
       self.move_list.append(PrecedenceType())
    
    def move(self):
        legal_moves = self.calculate_legal_moves();
        if (len(legal_moves) != 0):
            next_move = self.choose_next_move(legal_moves);
            next_move.perform()
            self.propagate_closure()
            if (self.turn == self.initiator):
                self.turn = self.responder
            else:
                self.turn = self.initiator
            print(next_move)

    def calculate_legal_moves(self):
        legal_move_list = []
        for move_type in self.move_list:
            for move in move_type.legal(self.store, self.turn, self.actions):
                legal_move_list.append(move)
        if len(legal_move_list) == 0:
            self.can_continue = False
        return legal_move_list
    
    def choose_next_move(self, move_list):
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
        
