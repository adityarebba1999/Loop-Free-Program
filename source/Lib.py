from z3 import *
from Component import *

class Library:
    def __init__(self, components):
        # print("called Library")
        self.components = components

    @classmethod
    def brahma_std(cls):
        context = Context()
        # print("called brahma")
        # print(cls)
        return cls([
            add(),
            and_op(),
            const_(0),
            const_(sys.maxsize),

        ])
    
class Instruction:
    def __init__(self, result, operator):
        self.result = result
        self.operator = operator

    def __str__(self):
        return f"{self.result} ← {self.operator}"

    def __repr__(self):
        return f"Instruction(result={self.result}, operator={self.operator})"
    
class Id:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        s = ""
        x = self.value

        if x==0:
            s = 'a'+s
        while x > 0:
            y = (x) % 26
            s = chr(ord('a') + y) + s
            x = (x - 1) // 26
        return s

