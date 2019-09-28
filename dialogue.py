import random
from dialogue_tree import *

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
                    if (self.action in move.get_rule().effects):
                        self.closed=True
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
        
class AssertPi(Move):
    def __init__(self, turn, pi, i, parent):
        Move.__init__(self, parent, turn)
        self.pi = pi
        self.trace_point = i
        self.closed = False

class MoveType:
    
    def legal(self, store, turn, actions):
        return []
        
class WhyNotActionType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        if (store.empty):
            for action in actions:
                for i in range(3, 5):
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
                        actions = player_internal_trace_point[2]
                        if (move.action in actions):
                            move_list.append(IDid(turn, move.action, move.trace_point, node))
        return move_list
        
class WhyActionType(MoveType):
    def legal(self, store, turn, actions):
        move_list = []
        for node in store.node_list():
            if (node.empty):
                for action in actions:
                    for i in range(3, 5):
                        move_list.append(WhyAction(turn, action, i, store))
                continue
            move = node.get_move()
            if (not move.is_closed()):
                if (isinstance(move, WhyNotAction)):
                    if (move.get_player() != turn):
                        move_list.append(WhyAction(turn, move.action, move.trace_point, node))
        return move_list

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
            move = node.get_move()
            if (not move.is_closed()):
                return False;
        return True
    
    def can_proceed(self):
        return self.can_continue
        
    def __repr__(self):
        string = "Dialogue:\n"
        for node in self.store.node_list():
            move = node.get_move()
            string += str(move) + "\n"
        return string
        
