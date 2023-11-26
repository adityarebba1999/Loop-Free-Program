from z3 import *
import time
import sys 
from Lib import Library
from Builder import ProgramBuilder
sys.path.append('./source/component')

print(z3.get_version_string())

def print_spec(components, name):
    print(f"Problem: {name}")
    for component in components:
        print(component)

def p1(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    
    a = builder.var()
    b = builder.const_(1)
    c = builder.sub(a, b)
    _ = builder.and_(a, c)
    spec = builder.finish()

    print_spec(spec, "p1")

def p2(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(1)
    c = builder.add(a, b)
    _ = builder.and_(a, c)
    spec = builder.finish()
    
    print_spec(spec, "p2")

def p3(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(0)
    c = builder.sub(b, a)
    _ = builder.and_(a, c)
    spec = builder.finish()
    
    print_spec(spec, "p3")

def p4(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(1)
    c = builder.sub(a, b)
    _ = builder.xor(a, c)
    spec = builder.finish()
    
    print_spec(spec, "p4")

def p5(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(1)
    c = builder.sub(a, b)
    _ = builder.or_(a, c)
    spec = builder.finish()
    
    print_spec(spec, "p5")

def p6(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(1)
    c = builder.add(a, b)
    _ = builder.or_(a, c)
    spec = builder.finish()
    
    print_spec(spec, "p6")

def p7(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    x = builder.var()
    a = builder.const_(2**64-1)
    o1 = builder.xor(x, a)
    b = builder.const_(1)
    o2 = builder.add(x, b)
    _ = builder.and_(o1, o2)
    spec = builder.finish()
    
    print_spec(spec, "p7")

def main():
    problems = {
        'p1': p1,
        'p2': p2,
        'p3': p3,
        'p4' : p4,
        'p5' : p5,
        'p6' : p6,
        'p7' : p7
    }

    solver = Solver()
    set_param('auto_config', False)
    set_param('model', True)
    context = Context()
    solver = Solver(ctx=context)
    problems_list = list(problems.items())

    config = {}
    config['auto_config'] = False
    config['model'] = True

    context = Context(**config)

    for name, func in problems_list:
        func('a', 'b')
        print()

if __name__ == "__main__":
    main()


