class Dialogue:
  def __init__(self):
    self.moves=[]
    self.open_moves=set()
  
  def make_move(move):
    self.moves.append(move)
    to_remove=set()
    for m in self.open_moves():
      if m.check_closure(self):
        to_remove.add(m)
    self.open_moves.remove(to_remove)


