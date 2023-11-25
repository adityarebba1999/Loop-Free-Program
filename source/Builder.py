from Lib import Instruction,Id
from Operator import *

class ProgramBuilder:
    def __init__(self):
        # print("called")
        self.program = Program(instructions=[])
    
    def finish(self):
        return self.program.instructions
    
    def next_id(self):
        # print(len(self.program.instructions))
        return Id(len(self.program.instructions))
    
    def var(self):
        assert all(inst.operator == Operator.Var for inst in self.program.instructions), \
            "All `var`s must be at the start of the program"

        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator.Var)))
        return result
    
    def const_(self, c):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Const,c))))
        return result
    
    def sub(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Sub, a, b))))
        return result
    
    def and_(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.And,a, b))))
        return result
    
    def add(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Add, a, b))))
        return result
    
    def xor(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Xor, a, b))))
        return result
    
    def or_(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Or, a, b))))
        return result




class Program:
    def __init__(self, instructions):
        # print("called program")
        self.instructions = instructions

    def __repr__(self):
        return f"Program(instructions={self.instructions})"