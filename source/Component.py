from z3 import *
from abc import ABC, abstractmethod
from typing import List
import sys

class Operator:
    pass
class Id:
    pass

class Component(ABC):
    @abstractmethod
    def operand_arity(self) -> int:
        pass

    @abstractmethod
    def make_operator(self, immediates: List[int], operands: List[Operator]) -> Operator:
        pass

    @abstractmethod
    def make_expression(
        self, context: object, immediates: List[object], operands: List[object], bit_width: int
    ) -> object:
        pass

    def immediate_arity(self) -> int:
        return 0

class Add(Component):
    def operand_arity(self) -> int:
        return 2

    def make_operator(self, immediates: List[int], operands: List[Id]) -> Operator:
        return Operator.Add(operands[0], operands[1])

    def make_expression(
        self, context: object, immediates: List[BitVec], operands: List[BitVec], bit_width: int
    ) -> BitVec:
        return operands[0].bvadd(operands[1])
def add() -> Component:
    return Add()

class And(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, immediates, operands):
        return Operator("And", operands[0], operands[1])

    def make_expression(self, context, immediates, operands, bit_width):
        return operands[0].bvand(operands[1])

def and_op() -> Component:
    return And()

class Const(Component):
    def __init__(self, val):
        self.val = val

    def operand_arity(self):
        return 0

    def make_operator(self, immediates, operands):
        return Operator("Const", self.val if self.val is not None else immediates[0], None)

    def make_expression(self, context, immediates, operands, bit_width):
        return BitVec('const', bit_width) if self.val is None else BitVecVal(self.val, bit_width)

    def immediate_arity(self):
        return 0 if self.val is not None else 1

def const_(val=None) -> Component:
    return Const(val)
