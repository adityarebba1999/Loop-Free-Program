from Lib import Instruction,Id
from Operator import *

class ProgramBuilder:
    def __init__(self):
        self.program = Program(instructions=[])
    
    def finish(self):
        return self.program.instructions
    
    def next_id(self):
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
    
    def eqz(self, a):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Eqz, a))))
        return result
    
    def clz(self, a):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Clz, a))))
        return result

    def ctz(self, a):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Ctz, a))))
        return result

    def popcnt(self, a):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Popcnt, a))))
        return result
    
    def eq(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Eq, a, b))))
        return result

    def ne(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Ne, a, b))))
        return result

    def lt_s(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.LtS, a, b))))
        return result

    def lt_u(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.LtU, a, b))))
        return result
    
    def gt_s(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.GtS, a, b))))
        return result

    def gt_u(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.GtU, a, b))))
        return result

    def le_s(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.LeS, a, b))))
        return result

    def le_u(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.LeU, a, b))))
        return result

    def ge_s(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.GeS, a, b))))
        return result

    def ge_u(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.GeU, a, b))))
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
    def mul(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Mul, a, b))))
        return result

    def div_s(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.DivS, a, b))))
        return result

    def div_u(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.DivU, a, b))))
        return result

    def rems(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.RemS, a, b))))
        return result

    def remu(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.RemU, a, b))))
        return result
    
    def shl(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Shl, a, b))))
        return result

    def shr_s(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.ShrS, a, b))))
        return result

    def shr_u(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.ShrU, a, b))))
        return result

    def rotl(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Rotl, a, b))))
        return result

    def rotr(self, a, b):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Rotr, a, b))))
        return result

    def select(self, a, b, c):
        result = self.next_id()
        self.program.instructions.append(str(Instruction(result, Operator(Operator.Select, a, b, c))))
        return result




class Program:
    def __init__(self, instructions):
        # print("called program")
        self.instructions = instructions

    def __repr__(self):
        return f"Program(instructions={self.instructions})"