class Operator:
    Var = 'Var'
    Const = 'Const'
    Eqz = 'Eqz'
    Clz = 'Clz'
    Ctz = 'Ctz'
    Popcnt = 'Popcnt'
    Eq = 'Eq'
    Ne = 'Ne'
    LtS = 'LtS'
    LtU = 'LtU'
    GtS = 'GtS'
    GtU = 'GtU'
    LeS = 'LeS'
    LeU = 'LeU'
    GeS = 'GeS'
    GeU = 'GeU'
    Add = 'Add'
    Sub = 'Sub'
    Mul = 'Mul'
    DivS = 'DivS'
    DivU = 'DivU'
    RemS = 'RemS'
    RemU = 'RemU'
    And = 'And'
    Or = 'Or'
    Xor = 'Xor'
    Shl = 'Shl'
    ShrS = 'ShrS'
    ShrU = 'ShrU'
    Rotl = 'Rotl'
    Rotr = 'Rotr'
    Select = 'Select'

    def __init__(self, variant: str, *args):
        self.variant = variant
        self.args = args

    def __str__(self):
        if self.variant == Operator.Var:
            return "var"
        elif self.variant == Operator.Const:
            return f"const {self.args[0]:#X}"
        elif self.variant == Operator.Eqz:
            return f"eqz {self.args[0]}"
        elif self.variant == Operator.Clz:
            return f"clz {self.args[0]}"
        elif self.variant == Operator.Ctz:
            return f"ctz {self.args[0]}"
        elif self.variant == Operator.Popcnt:
            return f"popcnt {self.args[0]}"
        elif self.variant == Operator.Eq:
            return f"eq {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Ne:
            return f"ne {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.LtS:
            return f"lt_s {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.LtU:
            return f"lt_u {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.GtS:
            return f"gt_s {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.GtU:
            return f"gt_u {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.LeS:
            return f"le_s {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.LeU:
            return f"le_u {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.GeS:
            return f"ge_s {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.GeU:
            return f"ge_u {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Add:
            return f"add {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Sub:
            return f"sub {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Mul:
            return f"mul {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.DivS:
            return f"div_s {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.DivU:
            return f"div_u {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.RemS:
            return f"rem_s {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.RemU:
            return f"rem_u {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.And:
            return f"and {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Or:
            return f"or {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Xor:
            return f"xor {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Shl:
            return f"shl {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.ShrS:
            return f"shr_s {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.ShrU:
            return f"shr_u {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Rotl:
            return f"rotl {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Rotr:
            return f"rotr {self.args[0]}, {self.args[1]}"
        elif self.variant == Operator.Select:
            return f"select {self.args[0]}, {self.args[1]}, {self.args[2]}"
        else:
            raise ValueError(f"Invalid operator: {self}")

    def arity(self) -> int:
        if self.variant in (Operator.Var, Operator.Const):
            return 0
        elif self.variant in (
            Operator.Eqz,
            Operator.Clz,
            Operator.Ctz,
            Operator.Popcnt,
        ):
            return 1
        elif self.variant in (
            Operator.Eq,
            Operator.Ne,
            Operator.LtS,
            Operator.LtU,
            Operator.GtS,
            Operator.GtU,
            Operator.LeS,
            Operator.LeU,
            Operator.GeS,
            Operator.GeU,
            Operator.Add,
            Operator.Sub,
            Operator.Mul,
            Operator.DivS,
            Operator.DivU,
            Operator.RemS,
            Operator.RemU,
            Operator.And,
            Operator.Or,
            Operator.Xor,
            Operator.Shl,
            Operator.ShrS,
            Operator.ShrU,
            Operator.Rotl,
            Operator.Rotr,
        ):
            return 2
        elif self.variant == Operator.Select:
            return 3

    def immediates(self, f):
        if self.variant == Operator.Const:
            f(self.args[0])

    def operands(self, f):
        if self.variant in [Operator.Var, Operator.Const]:
            pass
        elif self.variant in (
            Operator.Eqz,
            Operator.Clz,
            Operator.Ctz,
            Operator.Popcnt,
        ):
            f(self.args[0])
        elif self.variant in (
            Operator.Eq,
            Operator.Ne,
            Operator.LtS,
            Operator.LtU,
            Operator.GtS,
            Operator.GtU,
            Operator.LeS,
            Operator.LeU,
            Operator.GeS,
            Operator.GeU,
            Operator.Add,
            Operator.Sub,
            Operator.Mul,
            Operator.DivS,
            Operator.DivU,
            Operator.RemS,
            Operator.RemU,
            Operator.And,
            Operator.Or,
            Operator.Xor,
            Operator.Shl,
            Operator.ShrS,
            Operator.ShrU,
            Operator.Rotl,
            Operator.Rotr,
        ):
            f(self.args[0])
            f(self.args[1])
        elif self.variant == Operator.Select:
            f(self.args[0])
            f(self.args[1])
            f(self.args[2])

    def operands_mut(self, f):
        if self.variant in [Operator.Var, Operator.Const]:
            pass
        elif self.variant in (
            Operator.Eqz,
            Operator.Clz,
            Operator.Ctz,
            Operator.Popcnt,
        ):
            f(self.args[0])
        elif self.variant in (
            Operator.Eq,
            Operator.Ne,
            Operator.LtS,
            Operator.LtU,
            Operator.GtS,
            Operator.GtU,
            Operator.LeS,
            Operator.LeU,
            Operator.GeS,
            Operator.GeU,
            Operator.Add,
            Operator.Sub,
            Operator.Mul,
            Operator.DivS,
            Operator.DivU,
            Operator.RemS,
            Operator.RemU,
            Operator.And,
            Operator.Or,
            Operator.Xor,
            Operator.Shl,
            Operator.ShrS,
            Operator.ShrU,
            Operator.Rotl,
            Operator.Rotr,
        ):
            f(self.args[0])
            f(self.args[1])
        elif self.variant == Operator.Select:
            f(self.args[0])
            f(self.args[1])
            f(self.args[2])

