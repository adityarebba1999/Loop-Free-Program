from z3 import *
import time
import sys 
from Lib import Library
from Builder import ProgramBuilder
sys.path.append('./source/component')

print(z3.get_version_string())


def p1(context, opts):
    library = Library.brahma_std()
    # print(library.components)

    builder = ProgramBuilder()
    
    a = builder.var()
    b = builder.const_(1)
    c = builder.sub(a, b)
    _ = builder.and_(a,c)
    spec = builder.finish()

    print(spec)

def p2(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(1)
    c = builder.add(a, b)
    _ = builder.and_(a, c)
    spec = builder.finish()
    print(spec)

def p3(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(0)
    c = builder.sub(b, a)
    _ = builder.and_(a, c)
    spec = builder.finish()
    print(spec)

def p4(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(1)
    c = builder.sub(a, b)
    _ = builder.xor(a, c)
    spec = builder.finish()
    print(spec)

def p5(context, opts):

    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(1)
    c = builder.sub(a, b)
    _ = builder.or_(a, c)
    spec = builder.finish()
    print(spec)

def p6(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    a = builder.var()
    b = builder.const_(1)
    c = builder.add(a, b)
    _ = builder.or_(a, c)
    spec = builder.finish()
    print(spec)

def p7(context, opts):
    library = Library.brahma_std()
    builder = ProgramBuilder()
    x = builder.var()
    # o1 = bvnot(x) = xor(x, MAX)
    a = builder.const_(2**64-1)
    o1 = builder.xor(x, a)
    b = builder.const_(1)
    o2 = builder.add(x, b)
    _ = builder.and_(o1, o2)
    spec = builder.finish()
    print(spec)

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

    
    for i in problems_list:
        name = i[0]
        func = i[1]
        print('Problems:',name)
        func('a','b')



    # context = z3.Context()
    # ... continue for all p1 to p25 functions


    # config = z3.Context().config
    # config.set("auto_config", False)
    # config.set("model_generation", True)

    # context = z3.Context(config)
    # for name, p in problems:
    #     if not opts.should_run_problem(name):
    #         continue

    #     print(f"==================== {name} ====================")
    #     then = time.time()
    #     program = p(context, opts)
    #     elapsed = time.time() - then

    #     print(f"\nElapsed: {elapsed:.3f}s\n")
    #     if isinstance(program, Program):
    #         print(f"Synthesized:\n\n{program}")
    #     else:
    #         print(f"Error: {program}\n")

if __name__ == "__main__":
    main()
