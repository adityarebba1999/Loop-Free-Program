from z3 import *
from abc import ABC, abstractmethod
from Operator import *
from typing import List
import sys
from z3 import BitVec

def bit_vec_from_u64(context, val, bit_width):
    return BitVec('bv{}'.format(val), bit_width).as_long(val)

def zero(context, bit_width):
    return bit_vec_from_u64(context, 0, bit_width)

def one(context, bit_width):
    return bit_vec_from_u64(context, 1, bit_width)


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

    def make_operator(self, immediates: List[int], operands ) -> Operator:
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

class Eqz(Component):
    def operand_arity(self):
        return 1

    def make_operator(self, _immediates, operands):
        return Operator("Eqz", operands[0])

    def make_expression(self, context, _immediates, operands, bit_width):
        return If(operands[0] == BitVecVal(0, bit_width), BitVecVal(1, bit_width), BitVecVal(0, bit_width))

def eqz() -> Component:
    return Eqz()

class LeS(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("LeS", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].bvsle(operands[1]).ite(one(context, bit_width), zero(context, bit_width))

def le_s() -> Component:
    return LeS()

class LeU(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("LeU", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].bvule(operands[1]).ite(one(context, bit_width), zero(context, bit_width))

def le_u() -> Component:
    return LeU()

class GeS(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("GeS", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].bvsge(operands[1]).ite(one(context, bit_width), zero(context, bit_width))

def ge_s() -> Component:
    return GeS()

class GeU(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("GeU", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].bvuge(operands[1]).ite(one(context, bit_width), zero(context, bit_width))

def ge_u() -> Component:
    return GeU()


class Clz(Component):
    def operand_arity(self):
        return 1

    def make_operator(self, _immediates, operands):
        return Operator("Clz", operands[0])

    def make_expression(self, context, _immediates, operands, bit_width):
        def clz(context, input, one_bit, bit_width, i):
            if i == bit_width:
                return BitVecVal(i, bit_width)
            else:
                condition = input.extract(bit_width - 1 - i, bit_width - 1 - i) == one_bit
                true_branch = BitVecVal(i, bit_width)
                false_branch = clz(context, input, one_bit, bit_width, i + 1)
                return If(condition, true_branch, false_branch)

        one_bit = BitVecVal(1, 1)
        return clz(context, operands[0], one_bit, bit_width, 0)

def clz() -> Component:
    return Clz()

class Ctz(Component):
    def operand_arity(self):
        return 1

    def make_operator(self, _immediates, operands):
        return Operator("Ctz", operands[0])

    def make_expression(self, context, _immediates, operands, bit_width):
        def ctz(context, input, one_bit, bit_width, i):
            if i == bit_width:
                return BitVecVal(i, bit_width)
            else:
                condition = input.extract(i, i) == one_bit
                true_branch = BitVecVal(i, bit_width)
                false_branch = ctz(context, input, one_bit, bit_width, i + 1)
                return If(condition, true_branch, false_branch)

        one_bit = BitVecVal(1, 1)
        return ctz(context, operands[0], one_bit, bit_width, 0)

def ctz() -> Component:
    return Ctz()

class Popcnt(Component):
    def operand_arity(self):
        return 1

    def make_operator(self, _immediates, operands):
        return Operator("Popcnt", operands[0])

    def make_expression(self, _context, _immediates, operands, bit_width):
        bits = [(operands[0].extract(i, i)).zero_ext(bit_width - 1) for i in range(bit_width)]
        initial = bits.pop()
        return sum(bits, initial)

def popcnt() -> Component:
    return Popcnt()

class Eq(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Eq", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0]._eq(operands[1]).ite(one(context, bit_width), zero(context, bit_width))

def eq() -> Component:
    return Eq()

class Ne(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Ne", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0]._eq(operands[1]).ite(zero(context, bit_width), one(context, bit_width))

def ne() -> Component:
    return Ne()

class LtS(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("LtS", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].bvslt(operands[1])

def lt_s() -> Component:
    return LtS()

class LtU(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("LtU", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].bvult(operands[1])

def lt_u() -> Component:
    return LtU()

class GtS(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("GtS", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].bvsgt(operands[1])

def gt_s() -> Component:
    return GtS()

class GtU(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("GtU", operands[0], operands[1])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].bvugt(operands[1])

def gt_u() -> Component:
    return GtU()



class Sub(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Sub", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvsub(operands[1])

def sub() -> Component:
    return Sub()

class Mul(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Mul", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvmul(operands[1])

def mul() -> Component:
    return Mul()

class DivS(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("DivS", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvsdiv(operands[1])

def div_s() -> Component:
    return DivS()

class DivU(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("DivU", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvudiv(operands[1])

def div_u() -> Component:
    return DivU()

class RemS(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("RemS", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvsrem(operands[1])

def rem_s() -> Component:
    return RemS()

class RemU(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("RemU", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvurem(operands[1])

def rem_u() -> Component:
    return RemU()

class Or(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Or", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvor(operands[1])

def or_() -> Component:
    return Or()

class Xor(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Xor", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvxor(operands[1])

def xor() -> Component:
    return Xor()

class Shl(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Shl", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvshl(operands[1])

def shl() -> Component:
    return Shl()

class ShrS(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("ShrS", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvashr(operands[1])

def shr_s() -> Component:
    return ShrS()

class ShrU(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("ShrU", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvlshr(operands[1])

def shr_u() -> Component:
    return ShrU()

class Rotl(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Rotl", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvrotl(operands[1])

def rotl() -> Component:
    return Rotl()

class Rotr(Component):
    def operand_arity(self):
        return 2

    def make_operator(self, _immediates, operands):
        return Operator("Rotr", operands[0], operands[1])

    def make_expression(self, _context, _immediates, operands, _bit_width):
        return operands[0].bvrotr(operands[1])

def rotr() -> Component:
    return Rotr()

class Select(Component):
    def operand_arity(self):
        return 3

    def make_operator(self, _immediates, operands):
        return Operator("Select", operands[0], operands[1], operands[2])

    def make_expression(self, context, _immediates, operands, bit_width):
        return operands[0].eq(zero(context, bit_width)).ite(operands[2], operands[1])

def select() -> Component:
    return Select()
