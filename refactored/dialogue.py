from participant import Participant
from move import Move


class Dialogue:
    p1: Participant
    p2: Participant
    moves: list[Move]

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
