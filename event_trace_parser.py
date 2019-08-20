from lark import Lark
from env import *

parser= Lark(r"""
    
    STRING: /[a-zA-Z_]\w*/
    NUMBER: /[0-9_]\w*/
    COMMENT: /#[^\n]*/
    
    timestep: timestamp add_beliefs del_beliefs
    timestamp: NUMBER
    add_beliefs: [addbelief ("," addbelief)*]
    del_beliefs: [rembelief ("," rembelief)*]
    belief: STRING
    addbelief:  "+"belief
    rembelief: "-"belief

    %import common.WS
    %ignore WS
    %ignore COMMENT
    
    """,start='ruleset')
