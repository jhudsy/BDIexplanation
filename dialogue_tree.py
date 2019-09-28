class DialogueTree:
    def __init__(self):
        self.children = []
        self.empty = True;
        
    def set_move(self, move):
        self.move = move;
        self.empty = False;
        
    def get_move(self):
        return self.move;
        
    def node_list(self):
        node_list = []
        node_list.append(self)
        for node in self.children:
            node_list = node_list + node.node_list()
        return node_list
                
    def size(self):
        return len(self.node_list())
        
    def add_child(self, move):
        child = DialogueTree()
        child.set_move(move)
        self.children.append(child)
        
    def __repr__(self):
        string = str(self.move)
        for node in self.children:
            string += str(node)
        return string
            
