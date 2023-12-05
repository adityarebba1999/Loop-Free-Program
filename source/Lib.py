from z3 import *
from Component import *
import itertools
from itertools import *

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
    @staticmethod
    def arity(self):
        return sum(1 for inst in self.instructions if inst.operator == Operator.Var)
    
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


class Synthesizer:
    def __init__(self, context, library, spec):
        if not library.components:
            raise ValueError("No components in the library")

        self.context = context
        self.library = library
        self.spec = spec
        self.locations = LocationVars(context, library, Library.arity())
        invalid_connections = self.locations.invalid_connections(library)
        self.well_formed_program = self.locations.well_formed_program(context, library, invalid_connections)
        self.invalid_connections = invalid_connections
        self.not_invalid_assignments = Bool(context, True)
    

class LocationVars:
    def __init__(self, inputs, params, results, output, line_bit_width):
        self.inputs = inputs
        self.params = params
        self.results = results
        self.output = output
        self.line_bit_width = line_bit_width

    @classmethod
    def new(cls, context, library, num_inputs):
        max_line = num_inputs + len(library.components) + sum(c.operand_arity() for c in library.components)
        max_pow_2 = (max_line + 1).bit_length()
        line_bit_width = max_pow_2

        inputs = [cls.fresh_line(context, "input_location", line_bit_width) for _ in range(num_inputs)]
        params = [cls.fresh_line(context, "param_location", line_bit_width) for _ in range(sum(c.operand_arity() for c in library.components))]
        results = [cls.fresh_line(context, "result_location", line_bit_width) for _ in range(len(library.components))]
        output = cls.fresh_line(context, "output_line", line_bit_width)

        return cls(inputs, params, results, output, line_bit_width)
    
    def invalid_connections(self, library):
        invalid_connections = set()

        for a in self.inputs:
            for b in self.output:
                invalid_connections.add((a, b))

        for a, b in combinations(self.inputs, 2):
            invalid_connections.add((a, b))

        for p, q in combinations(self.params, 2):
            invalid_connections.add((p, q))

        params = iter(self.params)
        for r, c in zip(self.results, library.components):
            for p in itertools.islice(params, c.operand_arity()):
                invalid_connections.add((r, p))

        return invalid_connections
    

    @staticmethod
    def fresh_line(context, name, line_bit_width):
        return z3.BitVec(name, line_bit_width, context)
    
    def well_formed_program(self, context, library, invalid_connections):
        def line_le(lhs, rhs):
            return lhs.bvule(rhs)
        def line_lt(lhs, rhs):
            return lhs.bvult(rhs)
        
        wfp = []

        wfp.append(self.consistent(context, invalid_connections))
        wfp.append(self.acyclic(context, library))

        i_len = self.line_from_u32(context, len(self.inputs))
        m = self.line_from_u32(context, len(self.results) + len(self.inputs))
        zero = self.line_from_u32(context, 0)

        for i, l in enumerate(self.inputs):
            i_line = self.line_from_u32(context, i)
            wfp.append(l == i_line)

        for l in self.params:
            wfp.append(line_le(zero, l))
            wfp.append(line_lt(l, m))

        for l in self.results:
            wfp.append(line_le(i_len, l))
            wfp.append(line_lt(l, m))

        return And(*wfp)
