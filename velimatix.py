import ast
import ast, random, math
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System,Col
from getpass import getpass
__import__('sys').setrecursionlimit(999999999)

antipycdc = ""

for i in range(10000):
    antipycdc += "1/int(0),"

antipycdc = "try:ngocuyencoder=(" + antipycdc + ")\nexcept:pass"

ANTI_PYCDC = f"""
try:pass
except:pass
else:pass
finally:pass
{antipycdc}
finally:int(2008-2006)
"""
class Utils:
    def randomize_name(alphabet: str, length: int) -> str:
        name = ''.join([__import__('random').choice(alphabet) for _ in range(length)])
        while name[0].isdigit():name = ''.join([__import__('random').choice(alphabet) for _ in range(length)])
        return name
    def generate_next_num(current: int, max: int):
        next = current + __import__('random').randint(1, 1000)
        return next
    def find_parent(node, targets):
        parent = node.parent
        while True:
            for target in targets:
                if isinstance(parent, target):return parent
                elif isinstance(parent, ast.Module):return None
            parent = parent.parent
    def find_class(tree, node: ast.Call):
        for _node in ast.walk(tree):
            for child in ast.iter_child_nodes(_node):
                name = node.func.id
                if isinstance(child, ast.FunctionDef):
                    if child.name == name:return child.parent
                elif isinstance(child, ast.ClassDef):
                    if child.name == name:return child
        return None
    def get_chance():return random.randint(0, 100)
class BiOpaqueUtils:
    possible_args = []
    possible_functions = []
    alphabet = ""
    length = 16
    safe_mode = False
    def get_possible_functions(tree: ast.Module):
        if BiOpaqueUtils.possible_functions != []: return BiOpaqueUtils.possible_functions
        possible_functions = [ast.Name(id=func_id) for func_id in dir(__builtins__) if not func_id.startswith("_")]
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.FunctionDef):
                    if isinstance(child.parent, ast.ClassDef):possible_functions.append(ast.Attribute(value=ast.Name(id=child.parent.name), attr=child.name))
                    else:possible_functions.append(ast.Name(id=child.name))
        BiOpaqueUtils.possible_functions = possible_functions
        return BiOpaqueUtils.possible_functions
    def get_possible_args(tree: ast.Module):
        if BiOpaqueUtils.possible_args != []: return BiOpaqueUtils.possible_args
        possible_args = []
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Call):
                    for arg in child.args:possible_args.append(arg)
        BiOpaqueUtils.possible_args = possible_args
        return BiOpaqueUtils.possible_args
    def get_random_function(tree: ast.Module):
        possible_functions = BiOpaqueUtils.get_possible_functions(tree)
        return random.choice(possible_functions)
    def get_random_args(tree: ast.Module):
        possible_args = BiOpaqueUtils.get_possible_args(tree)
        return [random.choice(possible_args) for i in range(random.randint(0, 2))]
    def generate_bogus_body(tree, node):
        bogus = type(node).__new__(type(node))
        bogus.__dict__.update(node.__dict__)
        for name, field in ast.iter_fields(bogus):
            if isinstance(field, ast.Call):
                new_call = type(field).__new__(type(field))
                new_call.__dict__.update(field.__dict__)
                if isinstance(new_call.func, ast.Name) or isinstance(new_call.func, ast.Attribute):
                    new_call.func = BiOpaqueUtils.get_random_function(tree)
                    new_call.args = BiOpaqueUtils.get_random_args(tree)
                setattr(bogus, name, new_call)
            if isinstance(bogus, ast.Assign) and name == 'value':
                new_value = random.choice(BiOpaqueUtils.get_possible_args(tree))
                if isinstance(bogus.value, ast.List) or isinstance(bogus.value, ast.Dict):new_value = ast.List(elts=[random.choice(BiOpaqueUtils.get_possible_args(tree)) for ignored in range(random.randint(2, 6))])
                setattr(bogus, name, new_value)
            if isinstance(bogus, ast.AugAssign) and name == 'value':
                new_value = random.choice(BiOpaqueUtils.get_possible_args(tree))
                if isinstance(bogus.value, ast.List) or isinstance(bogus.value, ast.Dict):new_value = ast.List(elts=[random.choice(BiOpaqueUtils.get_possible_args(tree)) for ignored in range(random.randint(2, 6))])
                setattr(bogus, name, new_value)
                setattr(bogus, 'op', random.choice([ast.Add(), ast.Sub(), ast.Div(), ast.Mult(), ast.BitXor(), *([node.op] * 3)] ))
        return bogus
    def generate_roadline(goal: int):
        num = random.randint(1, 100)
        current_num = num
        roadline = []
        while current_num != goal:
            if current_num > goal:
                val = random.randint(1, num + 1)
                current_num -= val
                roadline.append([ast.Sub(), val])
            elif current_num < goal:
                val = random.randint(1, num + 1)
                current_num += val
                roadline.append([ast.Add(), val])
        return (num, roadline)
    def obscure_bool(value: bool, arg_name: str):
        roadline = BiOpaqueUtils.generate_roadline(value)
        while len(roadline[1]) > 6:roadline = BiOpaqueUtils.generate_roadline(value)
        original_number = roadline[0]
        roadline = roadline[1]
        binop_name = Utils.randomize_name(BiOpaqueUtils.alphabet, BiOpaqueUtils.length)
        binop = ast.Name(id=binop_name)
        for action in roadline:
            key = random.randint(1, 6996)
            xored_binop = ast.BinOp(left=ast.Constant(action[1] ^ key), op=ast.BitXor(), right=ast.Constant(value=key))
            binop = ast.BinOp(left=binop,op=action[0],right=ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),body=xored_binop),args=[],keywords=[]))
        if BiOpaqueUtils.safe_mode:
            return (ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=binop_name)],kwonlyargs=[],kw_defaults=[],defaults=[]),body=binop),args=[ast.Constant(value=original_number)],keywords=[]), None)
        return (ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=binop_name)],kwonlyargs=[],kw_defaults=[],defaults=[]),body=binop),args=[ast.Name(id=arg_name)],keywords=[]), original_number)
    def generate_opaquepredicate(tree, node, arg_name: str):
        test = BiOpaqueUtils.obscure_bool(True, arg_name)
        ret_node = ast.If(test=test[0],body=[node],orelse=[BiOpaqueUtils.generate_bogus_body(tree, node)])
        if Utils.get_chance() > 50:
            test = BiOpaqueUtils.obscure_bool(False, arg_name)
            ret_node.body, ret_node.orelse = ret_node.orelse, ret_node.body
            ret_node.test = test[0]
        return (ret_node, test[1])
    def fix_calls(tree, func_name: str, arg_name: str, value: int):
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Lambda):continue
                    elif isinstance(child.func, ast.Name):
                        if child.func.id == func_name:child.args.append(ast.Constant(value=value))
                    elif isinstance(child.func, ast.Attribute):
                        if child.func.attr == func_name:child.args.append(ast.Constant(value=value))
class BiOpaqueTransformer():
    def __init__(self, alphabet: str, length: int, safe_mode: bool):
        BiOpaqueUtils.alphabet = alphabet
        BiOpaqueUtils.length = length
        BiOpaqueUtils.safe_mode = safe_mode
    def proceed(self, tree: ast.Module):
        self.tree = tree
        for node in ast.walk(self.tree):
            for child in ast.iter_child_nodes(node):child.parent = node
        biopaque = BiOpaqueTransformer.BiOpaqueTransformer(self.tree)
        self.tree = biopaque.visit(self.tree)
        self.tree = ast.parse(ast.unparse(tree))
        return self.tree
    class BiOpaqueTransformer(ast.NodeTransformer):
        def __init__(self, tree: ast.Module):self.tree = tree
        def visit_FunctionDef(self, node: ast.FunctionDef):
            if isinstance(node, list): return node
            if node.args.vararg != None or node.args.kwarg != None: return node
            if node.name.startswith("__"): return node
            body = node.body
            body_length = len(body)
            bad_list = [ast.Global, ast.If, ast.For, ast.Return, ast.Pass, ast.Try, ast.ExceptHandler]
            chance = 75
            chance_step = int(50 / (body_length))
            if body_length == 1: return node
            for i in range(body_length):
                child = body[i]
                if isinstance(child, list): continue
                if chance <= 0 or chance >= 100: break
                if (Utils.get_chance() > chance and not type(child) in bad_list):
                    arg_name = Utils.randomize_name(BiOpaqueUtils.alphabet, BiOpaqueUtils.length)
                    predicate = BiOpaqueUtils.generate_opaquepredicate(self.tree, child, arg_name)
                    if not BiOpaqueUtils.safe_mode:
                        node.args.args.append(ast.arg(arg=arg_name))
                        BiOpaqueUtils.fix_calls(self.tree, node.name, arg_name, predicate[1])
                    body[i] = predicate[0]
                    chance += chance_step
            return node
class MutatorUtils:
    alphabet = ""
    length = 16
    safe_mode = False
    def generate_stack_elts(real: int):
        elts = [ast.Constant(value=random.randint(0xFF * len(str(str(real))) * 100, 0xFFFFFF * len(str(str(real))) * 10)) for i in range(random.randint(0, 15))]
        elts.append(ast.Constant(value=real))
        random.shuffle(elts)
        index = -1
        for elt in elts:
            if (elt.value == real):index = elts.index(elt)
        return [elts, index]
    def proceed_int_assign(node: ast.Assign, ladder: int):
        old_value = node.value.value
        name = Utils.randomize_name(MutatorUtils.alphabet, MutatorUtils.length)
        keys = [~(random.randint(0xFF, 0xFFFFFFF)) for i in range(ladder)]
        obscured = old_value
        for key in keys:obscured = obscured ^ ~(key)
        elts = MutatorUtils.generate_stack_elts(obscured)
        stack = ast.Assign(targets=[ast.Name(id=name)],value=ast.List(elts=elts[0]),lineno=None)
        key_index = random.randint(0xFF, 0xFFFFFFF)
        node.value.value = elts[1] ^ key_index
        name_obj = node.targets[0]
        body = []
        for key in keys:body.append(ast.Assign(targets=[ast.Subscript(value=ast.Name(id=name),slice=ast.BinOp(left=ast.Constant(value=key_index),op=ast.BitXor(),right=name_obj))],value=ast.BinOp(left=ast.Subscript(value=ast.Name(id=name),slice=ast.BinOp(left=ast.Constant(value=key_index),op=ast.BitXor(),right=name_obj)),op=ast.BitXor(),right=ast.UnaryOp(op=ast.Invert(),operand=ast.Constant(value=key))),lineno=None))
        body.append(ast.Assign(targets=node.targets,value=ast.Subscript(value=ast.Name(id=name),slice=ast.BinOp(left=ast.Constant(value=key_index),op=ast.BitXor(),right=name_obj)),lineno=None)
        )
        return [node, stack, body]
    def proceed_int_list_assign(node: ast.Assign, ladder: int):
        for elt in node.value.elts:
            if (isinstance(elt, ast.Constant)):
                if (not isinstance(elt.value, int)):return [node]
            else:return [node]
        old_elts = node.value.elts
        body = []
        name = node.targets[0].id
        for i in range(len(old_elts)):
            elt = old_elts[i]
            keys = [random.randint(-0xFFFFFFF, 0xFFFFFFF) for _ in range(ladder)]
            obscured_value = elt.value
            for key in keys:
                obscured_value ^= key
                body.append(ast.AugAssign(target=ast.Subscript(value=ast.Name(id=name),slice=ast.Constant(value=i)),op=ast.BitXor(),value=ast.Constant(value=key)))
            node.value.elts[i].value = obscured_value
        return [node, body]
    def proceed_float_list_assign(node: ast.Assign, ladder: int):
        for elt in node.value.elts:
            if (isinstance(elt, ast.Constant)):
                if (not isinstance(elt.value, float)):return node
            else:return node
        old_elts = node.value.elts
        body = []
        name = node.targets[0].id
        for i in range(len(old_elts)):
            elt = old_elts[i]
            elt_point_len = len(str(elt.value).split('.')[1])
            keys = [random.uniform(-0xFFFFFFF, 0xFFFFFFF) for _ in range(ladder)]
            obscured_value = elt.value
            for key in keys:
                obscured_value += key
                body.append(ast.AugAssign(target=ast.Subscript(value=ast.Name(id=name),slice=ast.Constant(value=i)),op=ast.Sub(),value=ast.Constant(value=key)))
            body.append(ast.Assign(targets=[ast.Subscript(value=ast.Name(id=name),slice=ast.Constant(value=i))],value=ast.Call(func=ast.Name(id='round'),args=[ast.Subscript(value=ast.Name(id=name),slice=ast.Constant(value=i)),ast.Constant(value=elt_point_len)],keywords=[]),lineno = None))
            node.value.elts[i].value = obscured_value
        return [node, body]
    def proceed_list_assign(node: ast.Assign, ladder: int):
        node = MutatorUtils.proceed_int_list_assign(node, ladder)
        if (len(node) > 1 or MutatorUtils.safe_mode == True):return node
        node = MutatorUtils.proceed_float_list_assign(node[0], ladder)
        return node
    def generate_binopt_int(value: int, keys):
        obscured_value = value
        for key in keys:obscured_value ^= key
        binopt = ast.BinOp(left = ast.Constant(value = obscured_value),op = ast.BitXor(),right = ast.Constant(value = keys[0]))
        for key in keys:
            if (keys[0] == key): continue
            binopt = ast.BinOp(left = binopt,op = ast.BitXor(),right = ast.Constant(value = key))
        return binopt
    def generate_binopt_float(value: float, keys):
        obscured_value = value
        point_len = len(str(value).split('.')[1])
        for key in keys:obscured_value += key
        binopt = ast.BinOp(left = ast.Constant(value = obscured_value),op = ast.Sub(),right = ast.Constant(value = keys[0]))
        for key in keys:
            if (keys[0] == key): continue
            binopt = ast.BinOp(left = binopt,op = ast.Sub(),right = ast.Constant(value = key))
        binopt = ast.Call(func=ast.Name(id='round'),args=[binopt,ast.Constant(value=point_len)],keywords=[])
        return binopt
    def proceed_int_constant(node: ast.Constant, ladder):
        keys = [random.randint(-0xFFFFFFFFF, 0xFFFFFFFFF) for _ in range(ladder)]
        name = Utils.randomize_name(MutatorUtils.alphabet, MutatorUtils.length)
        node = ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=name)],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(func=ast.Name(id=name),args=[],keywords=[])),args=[ast.Lambda(args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),body=MutatorUtils.generate_binopt_int(node.value, keys))],keywords=[])
        return node
    def proceed_float_constant(node: ast.Constant, ladder):
        keys = [random.uniform(0xFFFF, 0xFFFFFFFFF) for _ in range(ladder)]
        name = Utils.randomize_name(MutatorUtils.alphabet, MutatorUtils.length)
        node = ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=name)],kwonlyargs=[],kw_defaults=[],defaults=[]),body=ast.Call(func=ast.Name(id=name),args=[],keywords=[])),args=[ast.Lambda(args=ast.arguments(posonlyargs=[],args=[],kwonlyargs=[],kw_defaults=[],defaults=[]),body=MutatorUtils.generate_binopt_float(node.value, keys))],keywords=[])
        return node
class ExceptionJumpUtils:
    alphabet = ""
    length = 16
    def generate_junk(ex_name: str, max: int):
        cases = []
        line = max + 1
        for i in range (random.randint(0, 3)):
            case_name = Utils.randomize_name(ExceptionJumpUtils.alphabet, ExceptionJumpUtils.length)
            cases.append(ast.If(test=ast.Compare(left=ast.Subscript(value=ast.Attribute(value=ast.Name(id=ex_name),attr='args'),slice=ast.Constant(value=0)),ops=[ast.Eq()],comparators=[ast.Constant(value=line)]),body=[ast.Assign(targets=[ast.Name(id=case_name)],value=ast.Constant(value=random.randint(0xFFFFF, 0xFFFFFFFFFFFF)),lineno=None)],orelse=[]))
            line += 1
        return cases
    def generate_blockV(body):
        old_body = body
        body = []
        var_name = Utils.randomize_name(ExceptionJumpUtils.alphabet, ExceptionJumpUtils.length)
        ex_name = Utils.randomize_name(ExceptionJumpUtils.alphabet, ExceptionJumpUtils.length)
        body.append(ast.Assign(targets=[ast.Name(id=var_name)],value=ast.Constant(value=0),lineno=None))
        case = ast.While(test=ast.Compare(left=ast.Name(id=var_name),ops=[ast.NotEq()],comparators=[ast.Constant(value=len(old_body) + 1)]),body=[ast.AugAssign(target=ast.Name(id=var_name),op=ast.Add(),value=ast.Constant(value=1)),ast.Try(body=[ast.Raise(exc=ast.Call(func=ast.Name(id='VELIMATIX'),args=[ast.Name(id=var_name)],keywords=[]))],handlers=[ast.ExceptHandler(type=ast.Name(id='VELIMATIX'),name=ex_name,body=[])],orelse=[],finalbody=[])],orelse=[])
        line = 1
        for body_node in old_body:
            case.body[1].handlers[0].body.append(ast.If(test=ast.Compare(left=ast.Subscript(value=ast.Attribute(value=ast.Name(id=ex_name),attr='args'),slice=ast.Constant(value=0)),ops=[ast.Eq()],comparators=[ast.Constant(value=line)]),body=[body_node],orelse=[]))
            line += 1
        case.body[1].handlers[0].body.append(ExceptionJumpUtils.generate_junk(ex_name, len(old_body) + 1))
        random.shuffle(case.body[1].handlers[0].body)
        body.append(case)
        return body
    def generate_block(node):
        old_body = node.body
        node.body = []
        var_name = Utils.randomize_name(ExceptionJumpUtils.alphabet, ExceptionJumpUtils.length)
        ex_name = Utils.randomize_name(ExceptionJumpUtils.alphabet, ExceptionJumpUtils.length)
        node.body.append(ast.Assign(targets=[ast.Name(id=var_name)],value=ast.Constant(value=0),lineno=None))
        case = ast.While(test=ast.Compare(left=ast.Name(id=var_name),ops=[ast.NotEq()],comparators=[ast.Constant(value=len(old_body) + 1)]),body=[ast.AugAssign(target=ast.Name(id=var_name),op=ast.Add(),value=ast.Constant(value=1)),ast.Try(body=[ast.Raise(exc=ast.Call(func=ast.Name(id='VELIMATIX'),args=[ast.Name(id=var_name)],keywords=[]))],handlers=[ast.ExceptHandler(type=ast.Name(id='VELIMATIX'),name=ex_name,body=[])],orelse=[],finalbody=[])],orelse=[])
        globals_list = []
        line = 1
        for body_node in old_body:
            if isinstance(body_node, ast.Global):
                globals_list.append(body_node)
                continue
            case.body[1].handlers[0].body.append(ast.If(test=ast.Compare(left=ast.Subscript(value=ast.Attribute(value=ast.Name(id=ex_name),attr='args'),slice=ast.Constant(value=0)),ops=[ast.Eq()],comparators=[ast.Constant(value=line)]),body=[body_node],orelse=[]))
            line += 1
        case.body[1].handlers[0].body.append(ExceptionJumpUtils.generate_junk(ex_name, len(old_body) + 1))
        random.shuffle(case.body[1].handlers[0].body)
        node.body.append(case)
        for global_obj in globals_list:node.body.insert(0, global_obj)
        return node
class ExceptionJumpTransformer():
    def __init__(self, alphabet: str, length: int):
        ExceptionJumpUtils.alphabet = alphabet
        ExceptionJumpUtils.length = length
    def proceed(self, tree: ast.Module):
        self.tree = tree
        for node in ast.walk(self.tree):
            for child in ast.iter_child_nodes(node):child.parent = node
        renamer = ExceptionJumpTransformer.ExceptionJumpTransformer()
        self.tree = renamer.visit(self.tree)
        return self.tree
    class ExceptionJumpTransformer(ast.NodeTransformer):
        def visit_FunctionDef(self, node: ast.FunctionDef):
            node = ExceptionJumpUtils.generate_block(node)
            return node
        def visit_If(self, node: ast.If):
            node = ExceptionJumpUtils.generate_block(node)
            return node
        def visit_Assign(self, node: ast.Assign):
            node = ExceptionJumpUtils.generate_blockV([node])
            return node
class ControlFlowUtils:
  alphabet, length = "", 16
  def generate_junk_controlflow_block(maps, max, node: ast.FunctionDef):
    cases = []
    for i in range(__import__('random').randint(0, 3)):
      num = __import__('random').randint(1, max)
      while (num in maps):num = __import__('random').randint(1, max)
      case_name = Utils.randomize_name(ControlFlowUtils.alphabet,ControlFlowUtils.length)
      case = ast.match_case(pattern=ast.MatchValue(value=ast.Constant(value=num, parent=None)),body=[ast.Assign(targets=[ast.Name(id=case_name)],value=ast.Constant(value=__import__('random').randint(0xFFFFF, 0xFFFFFFFFFFFF),parent=None),lineno=None)])
      fixed_body = node.body
      if (len(fixed_body) > 1):
        choice = __import__('random').choice(fixed_body)
        if isinstance(choice, ast.Global):choice = ast.Pass
        elif isinstance(choice, list):choice = ast.Pass
        for body_child in ast.walk(choice):
          for body_child_child in ast.iter_child_nodes(body_child):
            if isinstance(body_child_child, ast.Global):body_child_child = ast.Pass;body_child = ast.Pass;choice = ast.Pass
        case.body.append(choice)
      cases.append(case)
    return cases
  def generate_controlflow_block(node):
    old_body = node.body;current = Utils.generate_next_num(0, 0xFFFF);next_num = Utils.generate_next_num(current, 0xFFFFFFFFFFFFFF);maps = [];global_list = []
    turn_name = Utils.randomize_name(ControlFlowUtils.alphabet,ControlFlowUtils.length)
    base = [ast.Assign(targets=[ast.Name(id=turn_name)],value=ast.Constant(value=current),lineno=None),ast.While(test=ast.Compare(left=ast.Name(id=turn_name),ops=[ast.Lt()],comparators=[ast.Constant(value=0xFFFFFFFFFFFFFF + 1)]),body=[],orelse=[])]
    new_base = ast.Match(subject=ast.Name(id=turn_name), cases=[])
    for body_node in old_body:
      if isinstance(body_node, ast.Global):
        global_list.append(body_node)
        continue
      new = ast.match_case(pattern=ast.MatchValue(value=ast.Constant(value=current)),body=[body_node])
      if (len(old_body) > 1):new.body.append(ast.Assign(targets=[ast.Name(id=turn_name)],value=ast.Constant(value=next_num),lineno=None))
      new_base.cases.append(new)
      maps.append(next_num)
      current = next_num
      next_num = Utils.generate_next_num(current, 0xFFFFFFFFFFFFFFFF)
    base[1].test.comparators[0].value = next_num
    new_base.cases[len(new_base.cases) - 1].body.append(ast.Break())
    new_base.cases.append(ControlFlowUtils.generate_junk_controlflow_block(maps, next_num, node))
    __import__('random').shuffle(new_base.cases)
    base[1].body.append(new_base)
    for global_def in global_list:base.insert(0, global_def)
    node.body = base
  def generate_methods_clone(tree, node: ast.FunctionDef):
    methods = []
    random_body = None
    for _ in range(__import__('random').randint(0, 5)):
      while random_body is None:
        for _node in ast.walk(tree):
          for _child in ast.iter_child_nodes(_node):
            if (isinstance(_child, ast.FunctionDef)):
              if (__import__('random').randint(0, 100) > 75):random_body = _child.body
      empty_node = ast.FunctionDef(name=node.name,args=node.args,body=random_body,decorator_list=[],lineno=None)
      methods.append(empty_node)
      random_body = None
    methods.append(node)
    return methods
class CallUtils:
  def get_object_for_letter(letter):
    objs = dir(__builtins__)
    __import__('random').shuffle(objs)
    for obj in objs:
      if letter in obj and hasattr(getattr(__builtins__, obj), '__name__') and getattr(__builtins__, obj).__name__ == obj and ('exception' in obj.lower() or 'error' in obj.lower() or '__' in obj.lower()):return [obj, obj.find(letter)]
    return None
  def generate_builtin_attr_block(node: ast.Call):
    name = node.func.id
    block = ast.Call(func=ast.Call(func=ast.Name(id="__import__('builtins').getattr"),args=[ast.Name(id='__builtins__'),ast.Call(func=ast.Attribute(value=ast.Constant(value=''),attr='join'),args=[ast.List(elts=[])],keywords=[])],keywords=[]),args=node.args,keywords=node.keywords)
    for letter in name:
      obj = CallUtils.get_object_for_letter(letter)
      block.func.args[1].args[0].elts.append(ast.Subscript(value=ast.Attribute(value=ast.Name(id=obj[0]),attr='__name__'),slice=ast.Constant(value=obj[1])))
    return block
  def generate_attribute_attr_block(node: ast.Call):
    name = node.func.attr
    value = node.func.value
    if not isinstance(value, ast.Name):return node
    block = ast.Call(func=ast.Call(func=ast.Name(id="__import__('builtins').getattr"),args=[ast.Name(id=value.id),ast.Call(func=ast.Attribute(value=ast.Constant(value=''),attr='join'),args=[ast.List(elts=[])],keywords=[])],keywords=[]),args=node.args,keywords=node.keywords)
    for letter in name:
      obj = CallUtils.get_object_for_letter(letter)
      block.func.args[1].args[0].elts.append(ast.Subscript(value=ast.Attribute(value=ast.Name(id=obj[0]),attr='__name__'),slice=ast.Constant(value=obj[1])))
    return block
class CallTransformer():
  def proceed(self, tree: ast.Module):
    self.tree = tree
    for node in ast.walk(self.tree):
      for child in ast.iter_child_nodes(node):child.parent = node
    call = CallTransformer.CallTransformer()
    self.tree = call.visit(self.tree)
    return self.tree
  class CallTransformer(ast.NodeTransformer):
    def visit_Call(self, node: ast.Call):
      if (isinstance(node.func, ast.Name)):
        is_builtin = str(node.func.id) in dir(__builtins__)
        if is_builtin:return CallUtils.generate_builtin_attr_block(node)
      return node
  class BiOpaqueTransformer(ast.NodeTransformer):
    def visit_Assign(self, node: ast.Assign):return node
class ObfuscatorSettings:
    def __init__(self):self.transformers = []
    def add_transformer(self, transformer):self.transformers.append(transformer)
    def exceptionjmp_transformer(self, alphabet: str, length: int):self.add_transformer(ExceptionJumpTransformer(alphabet, length))
    def call_transformer(self):self.add_transformer(CallTransformer())
    def biopaque_transformer(self, alphabet: str, length: int, safe_mode: bool):self.add_transformer(BiOpaqueTransformer(alphabet, length, safe_mode))
class OBF_STRING:
    def __init__(self, BAOMAT, STRING, content: str, clean = True, obfcontent = True) -> None:
        self.ABC = self._randvar()
        self.XYZ = self._randvar()
        self.ABCXYZ = self._randvar()
        self.XYZABC = self._randvar()
        self.CBAYXZ = self._randvar()
        self.ZYXCBA = self._randvar()
        self.A = self._randvar()
        self.B = self._randvar()
        self.C = self._randvar()
        self.D = self._randvar()
        self.E = self._randvar()
        self.F = self._randvar()
        self.G = self._randvar()
        self.H = self._randvar()
        self.J = self._randvar()
        #ADD IT IF U WANT ANTI HTTPTOOLKIT (change self.antihttptoolkit to self.content)
        self.antihttptoolkit = f"""
{self.ABC} = __import__('requests').get
{self.XYZ} = __import__('requests').head
{self.ZYXCBA} = "http://localhost:8001/"
class ProjectError(MemoryError):pass
def Object():return ProjectError("<< ANTI DEBUG - _ngocuyen_minhnguyen@Python.system.coder >>")
def {self.ABCXYZ}({self.XYZABC}):
    try:
        {self.XYZ}({self.ZYXCBA},timeout=0.01)
        raise Object() from None
    except __import__('requests').exceptions.RequestException:
        pass
    try:
        {self.XYZ}({self.ZYXCBA},timeout=0.01)
        raise Object() from None
    except __import__('requests').exceptions.RequestException:
        pass
    try:
        {self.XYZ}({self.ZYXCBA},timeout=0.01)
        raise Object() from None
    except __import__('requests').exceptions.RequestException:
        pass
    try:
        {self.ABC}("https://google.com",timeout=1)
        {self.CBAYXZ} = {self.ABC}({self.XYZABC})
    except:
        raise Object() from None
    return {self.CBAYXZ}
__import__('requests').get = {self.ABCXYZ}
def {self.A}():
    {self.B} = False
    {self.C} = None
    try:
        {self.D} = r'Software\Microsoft\Windows\CurrentVersion\Internet Settings'
        {self.E} = __import__('winreg').OpenKey(__import__('winreg').HKEY_CURRENT_USER, {self.D})
        {self.F}, {self.G}  = __import__('winreg').QueryValueEx({self.E}, 'ProxyEnable')
        {self.B} = bool({self.F})
        if {self.B}:
            {self.H}, {self.G} = __import__('winreg').QueryValueEx({self.E}, 'ProxyServer')
            {self.C} = {self.H}
        __import__('winreg').CloseKey({self.E})
    except:
        pass
    return {self.B}, {self.C}
{self.J} = __import__('platform').uname()
if isinstance({self.J}, tuple) and len({self.J}) >= 1:
    if __import__('platform').system().lower() == 'windows':
        {self.B}, {self.C} = {self.A}()
        if {self.B}:
            raise Object() from None
        else:
            pass
    else:
        pass
""" + content
        self.content = content
        self.BAOMAT = BAOMAT
        self.STRING = STRING
        self.add_imports = []
        self.CreateVars()
        self.strings = {}
        if obfcontent:self.ObfContent()
        if clean:self.CleanCode()
        self.Tochuc()
        self.AntiSkid()
    def AntiSkid(self):
        self.content = fr"""
{self.content}""".strip()
    def CreateVars(self):
        imports = self._to_import
        impcontent = ""[1:].splitlines()
        #builtins
        #xxx = """["b","u","i","l","t","i","n","s"][0][1][2][3][4][5]"""
        bucu = """__import__(''.join(['s', 'l', 'o', 'o', 't', 'c', 'n', 'u', 'f'][::-1])).reduce(lambda 點,符:點+符,['s', 'n', 'i', 't', 'l', 'i', 'u', 'b'][::-1])"""
        #nimpcontent = [f"__import__('builtins').__import__({bucu}).__import__({bucu}).__import__({bucu}).__import__({bucu}).__import__({bucu}).{imports[imp]}={imp}" for imp in imports]
        nimpcontent = [f"__import__('builtins').{imports[imp]}={imp}" for imp in imports]
        impcontent.extend(iter(nimpcontent))
        self.impcontent = impcontent
    def ObfContent(self):
        f = __import__('io').BytesIO(self.content.encode('utf-8'))
        self.tokens = list(__import__('tokenize').tokenize(f.readline))
        ntokens = []
        for token in self.tokens:
            string, type = token.string, token.type
            if type == 1:
                if string in ('True', 'False'):
                    string = self._obf_bool(string)
            elif type == 2:
                string = self._obf_int(string)
            elif type == 3:
                string = self._obf_str(string)
            ntokens.append(__import__('tokenize').TokenInfo(type, string, token.start, token.end, token.line))
        self.ostrings = self.strings
        strings = [f"{self.vars}()[{self._protect(var)}]={value}" for var, value in self.strings.items()]
        self.strings = strings
        self.content = __import__('tokenize').untokenize(ntokens).decode('utf-8')
    def RemoveComments(self):
        self.content = "".join(lin + '\n' for lin in self.content.splitlines() if lin.strip() and not lin.strip().startswith('#'))
    def CompressCode(self):
        content = self.content
        while True:
            for x in ('=','(',')','[',']','{','}','*','+','-','/',':','<','>',','):
                content = content.replace(f' {x}', x).replace(f'{x} ', x)
            if content == self.content:
                break
            self.content = content
    def CleanCode(self):
            self.RemoveComments()
            self.CompressCode()
    def Tochuc(self):
        Anti_hook = f"""
class VELIMATIX(MemoryError):0
try:
    if __Author__ != ("HuynhNgocUyen","MinhNguyen2412"):
        raise VELIMATIX('>> GOOD LUCK!! VELIMATIX') from None
    if __In4__ != ("https://www.facebook.com/datishnu1907","https://www.facebook.com/i.usr.bin.python.NguyenMinh"):
        raise VELIMATIX('>> GOOD LUCK!! VELIMATIX') from None
    if len(open(__file__).readlines()) != 33:
        raise VELIMATIX('>> GOOD LUCK!! VELIMATIX') from None
except:
    raise VELIMATIX('>> GOOD LUCK!! VELIMATIX') from None
import traceback, marshal
class _VELIMATIX_:
    CHECK_HOOKING = set()
    ALLOWED_MODULES = {{'builtins', '__main__'}}
    @staticmethod
    def velivantue():
        raise VELIMATIX('>> GOOD LUCK!! VELIMATIX') from None
    @staticmethod
    def CHECK_AND_BLOCK(FUNC):
        if callable(FUNC) and FUNC.__module__ not in _VELIMATIX_.ALLOWED_MODULES:
            _VELIMATIX_.CHECK_HOOKING.add(FUNC.__module__)
            _VELIMATIX_.velivantue()
    @staticmethod
    def BLOCK_AND_ANTI(FUNC):
        def HI(*args, **kwargs):
            if args and args[0] in _VELIMATIX_.CHECK_HOOKING:
                _VELIMATIX_.velivantue()
            return FUNC(*args, **kwargs)
        return HI
    @staticmethod
    def BYPASS_HOOKING():
        stack = traceback.extract_stack()
        for frame in stack[:-2]:
            if frame.filename != __file__:
                _VELIMATIX_.velivantue()
    @staticmethod
    def check(func, md):
        if callable(func) and func.__module__ != md:
            _VELIMATIX_.CHECK_HOOKING.add(md)
            raise ImportError(f'>> Detect [{{func.__name__}}] call [{{md}}] ! <<') from None
    @staticmethod
    def inpandcheck(md, namefunction):
        module = __import__(md)
        func_can_kiem_tra = namefunction if isinstance(namefunction, list) else [namefunction]
        [_VELIMATIX_.check(getattr(module, func, None), md) for func in func_can_kiem_tra]
    @staticmethod
    def lfn(valimtx, xyz):
        return callable(valimtx) and xyz and valimtx.__module__ != xyz.__name__
    @staticmethod
    def kiem_tra_func_ngoai(listfunctionandmodule):
        if any(_VELIMATIX_.lfn(valimtx, xyz) for valimtx, xyz in listfunctionandmodule):
           _VELIMATIX_.velivantue()
    @staticmethod
    def ctypes(md, namefunction):
        module = __import__(md)
        func = getattr(module, namefunction, None)
        if func is None:
            _VELIMATIX_.velivantue()
        type_goc = type(func)
        def ckfunc(func):
            if type(func) != type_goc:
                _VELIMATIX_.velivantue()
        ckfunc(func)
        return func
    @staticmethod
    def inpandcheck_type(md, namefunction):
        func = _VELIMATIX_.ctypes(md, namefunction)
        _VELIMATIX_.check(func, md)
    @staticmethod
    def ngan_chan_thuc_thi_marshal():
        __import__('sys').settrace(lambda *args, **keys: None)
        __import__('sys').modules['marshal'] = None
        __import__('sys').modules['marshal'] = type(__import__('sys'))('marshal')
        __import__('sys').modules['marshal'].loads = marshal.loads
def setcheck():
    nhap_can_kiem_tra = {{
        'marshal': 'loads'
    }}
    [_VELIMATIX_.inpandcheck_type(md, namefunction) for md, namefunction in nhap_can_kiem_tra.items()]

    listfunctionandmodule = [
        (__import__('marshal').loads, marshal)
    ]
    _VELIMATIX_.kiem_tra_func_ngoai(listfunctionandmodule)
    _VELIMATIX_.ngan_chan_thuc_thi_marshal()
setcheck()
_VELIMATIX_.BYPASS_HOOKING()





"""

        if self.BAOMAT.upper() == "Y":

            boc_marshal = OBF_Spam(self.OBF_Builtins('\n'.join(self.strings) + '\n' + self.content))
            
            #boc_marshal = OBF_Spam(self.OBF_Builtins(str(ANTI_PYCDC + '\n'.join(self.strings) + '\n' + self.content))) 
            #boc_marshal = f"{self.eval}({self.marshal}("+str(self.OBF_Marshal(OBF_Spam(self.OBF_Builtins(str(ANTI_PYCDC + '\n'.join(self.strings) + '\n' + self.content)))))+"))"
        else:
            boc_marshal = self.OBF_Builtins('\n'.join(self.strings) + '\n' + self.content)
            #boc_marshal = self.OBF_Builtins(str(ANTI_PYCDC + '\n'.join(self.strings) + '\n' + self.content)) 
            #boc_marshal = f"{self.eval}({self.marshal}("+str(self.OBF_Marshal(self.OBF_Builtins(str(ANTI_PYCDC + '\n'.join(self.strings) + '\n' + self.content)))) + "))"
        #Anti_hook = f"{self.eval}({self.marshal}("+str(self.OBF_Marshal(self.OBF_Builtins(str(ANTI_PYCDC + '\n'.join(self.strings) + '\n' + Anti_hook)))) + "))"
        VELI = """class VELIMATIX(MemoryError):0"""
        #IX = input(stage(f"Anti Hooking? (ONLY WORK IF U USE MARSHAL COMPILE) : [X] NO | [Y] YES: ", "velimatix", col2 = bpurple)).replace('"','').replace("'","")
        #if IX.upper()!="Y":Anti_hook=""    
        #Anti_hook = OBF_Spam(self.OBF_Builtins(Anti_hookx))
        
        self.content = VELI+"\n"+'\n'.join(self.impcontent) + '\n' + Anti_hook + '\n' + str(boc_marshal)
    def OBF_Builtins(self, code: str) -> str:
        builtins = dir(__builtins__)
        tree = __import__('ast').parse(code)
        for node in __import__('ast').walk(tree):
            if isinstance(node, __import__('ast').Name):
                if node.id in builtins:
                    if not node.id.startswith('__'):
                        if node.id == 'chr':node.id = self.chr
                        elif node.id == 'int':node.id = self.int
                        elif node.id == 'type':node.id = self.type
                        elif node.id == 'str':node.id = self.str
                        elif node.id == 'exec':node.id = self.exec
                        elif node.id == 'eval':node.id = self.eval
                        elif node.id == 'print':node.id = self.print
                        elif node.id == 'bool':node.id = self.bool
                        elif node.id == 'len':node.id = self.len
                        elif node.id == 'dir':node.id = self.dir
                        elif node.id == 'dict':node.id = self.dict
                        elif node.id == 'input':node.id = self.input
                        elif node.id == 'bytes':node.id = self.bytes
                        elif node.id == 'setattr':node.id = self.setattr
                        elif node.id == 'isinstance':node.id = self.isinstance
                        elif node.id == 'Exception':node.id = self.Exception
                        elif node.id == 'KeyboardInterrupt':node.id = self.KeyboardInterrupt
                        elif node.id == 'IndexError':node.id = self.IndexError
                        elif node.id == 'ValueError':node.id = self.ValueError
                        elif node.id == 'open':node.id = self.open
                        elif node.id == 'tuple':node.id = self.tuple
                        elif node.id == 'list':node.id = self.list
                        elif node.id == 'vars':node.id = self.vars
                        elif node.id == 'chr':node.id = self.chr
                        elif node.id == 'sum':node.id = self.sum
                        elif node.id == 'sorted':node.id = self.sorted

                        elif node.id == 'round':node.id = self.round
                        elif node.id == 'repr':node.id = self.repr
                        elif node.id == 'pow':node.id = self.pow
                        elif node.id == 'oct':node.id = self.oct
                        elif node.id == 'anext':node.id = self.anext
                        elif node.id == 'next':node.id = self.next
                        elif node.id == 'min':node.id = self.min
                        elif node.id == 'max':node.id = self.max
                        elif node.id == 'locals':node.id = self.locals
                        elif node.id == 'iter':node.id = self.iter
                        elif node.id == 'issubclass':node.id = self.issubclass
                        elif node.id == 'id':node.id = self.id
                        elif node.id == 'hash':node.id = self.hash
                        elif node.id == 'hasattr':node.id = self.hasattr
                        elif node.id == 'format':node.id = self.format
                        elif node.id == 'divmod':node.id = self.divmod
                        elif node.id == 'delattr':node.id = self.delattr
                        elif node.id == 'callable':node.id = self.callable
                        elif node.id == 'breakpoint':node.id = self.breakpoint
                        elif node.id == 'bin':node.id = self.bin
                        elif node.id == 'ascii':node.id = self.ascii
                        elif node.id == 'any':node.id = self.any
                        elif node.id == 'all':node.id = self.all
                        elif node.id == 'abs':node.id = self.abs
                        elif node.id == 'hex':node.id = self.hex
                        elif node.id == 'reversed':node.id = self.reversed
                        elif node.id == 'ord':node.id = self.ord
                        elif node.id == 'quit':node.id = self.quit
                        elif node.id == 'exit':node.id = self.exit
                        elif node.id == 'KeyError':node.id = self.KeyError
                        elif node.id == 'TypeError':node.id = self.TypeError
                        elif node.id == 'enumerate':node.id = self.enumerate
                        elif node.id == 'map':node.id = self.map
                        elif node.id == 'SyntaxError':node.id = self.SyntaxError
                        elif node.id == 'NameError':node.id = self.NameError
                        elif node.id == 'FileNotFoundError':node.id = self.FileNotFoundError
                        elif node.id == 'PermissionError':node.id = self.PermissionError
                        elif node.id == 'OSError':node.id = self.OSError
                        elif node.id == 'UnicodeDecodeError':node.id = self.UnicodeDecodeError
                        elif node.id == 'UnicodeEncodeError':node.id = self.UnicodeEncodeError
                        elif node.id == 'range':node.id = self.range
                        elif node.id == 'getattr':node.id = self.getattr
                        elif node.id == 'compile':node.id = self.compile
                        elif node.id == 'globals':node.id = self.globals
                        elif node.id == 'ImportError':node.id = self.ImportError
                        elif node.id == 'AttributeError':node.id = self.AttributeError
                        elif node.id == 'ModuleNotFoundError':node.id = self.ModuleNotFoundError
                        else:node.id = f"__builtins__.__dict__['{node.id}']"
        return __import__('ast').unparse(tree)
    def _randvar(self):
        while True:
            return "_Ox"+''.join(__import__('random').choices([str(i) for i in range(10)], k=6))

    def OBF_BYTE(self,string):
        keys = []
        magic =  __import__('random').randint(1000000, 9999999)
        for i in range(len(string)):
            logic = __import__('random').randint(1, 4)
            if logic == 1:logic = '+'
            elif logic == 2:logic = '*'
            elif logic == 3:logic = '<<'
            else:logic = '^'
            key = ord(string[i])
            key1 = logic
            key2 = magic
            if key1 == "^":
                key3 = eval(f"~{key} {key1} ~{magic}")
                keys.append(f"""(lambda : {self.chr}({self.int}({self.eval}("{self.str}(~{key2})")) ^ {self.int}({self.eval}("{self.str}(~{key3})"))))()""")
            else:
                if key1 == "<<":
                    magic = __import__('random').randint(1, 19)
                    key3 = eval(f"{key} {key1} {magic}")
                    PT = ">>"
                    keys.append(f"""(lambda : {self.chr}({self.int}({self.eval}("{self.str}('{key3}')")) {PT} {self.int}({self.eval}("{self.str}('{str(magic)[::-1]}')")[::-1])))()""")
                else:
                    key3 = eval(f"{key} {key1} {magic}")
                    if key1 == "+":PT = "-"
                    else:PT = "//"
                    keys.append(f"""(lambda : {self.chr}({self.int}({self.eval}("{self.str}('{key3}')")) {PT} {self.int}({self.eval}("{self.str}('{str(key2)[::-1]}')")[::-1])))()""")
        return f"(lambda : {self.join}(["+', '.join(keys)+"]))()"
        #     if key1 == "^":
        #         key3 = eval(f"~{key} {key1} ~{magic}")
        #         keys.append(f"""(lambda : chr(int(eval("str(~{key2})")) ^ int(eval("str(~{key3})"))))()""")
        #     else:
        #         if key1 == "<<":
        #             magic = __import__('random').randint(1, 19)
        #             key3 = eval(f"{key} {key1} {magic}")
        #             PT = ">>"
        #             keys.append(f"""(lambda : chr(int(eval("str('{key3}')")) {PT} int(eval("str('{str(magic)[::-1]}')")[::-1])))()""")
        #         else:
        #             key3 = eval(f"{key} {key1} {magic}")
        #             if key1 == "+":PT = "-"
        #             else:PT = "//"
        #             keys.append(f"""(lambda : chr(int(eval("str('{key3}')")) {PT} int(eval("str('{str(key2)[::-1]}')")[::-1])))()""")
        # return f"(lambda : ''.join(["+', '.join(keys)+"]))()"
    def _protect(self, var, basic=False, r=0, char=1):
        char = "'" if char == 1 else '"'
        if basic:
            return f"{char}{''.join(reversed(var))}{char}[::-1]"
        if type(var) == int:
            return self._adv_int(var)
        if r == 0:
            r = __import__('random').randint(1, 2)
        if r == 1:
            return f"{self.OBF_BYTE(var)}"
        else:
            return f"{char}{''.join(reversed(var))}{char}[::-1]"
    def _protect_built(self, var, lib='builtins'):
        protected = self._protect(lib, r=2, basic=True)
        return f"{self.getattr}({self.__import__}({protected}),{self.dir}({self.__import__}({protected}))[{self.dir}({self.__import__}({protected})).index({self._protect(var, r=2, basic=True)})])"
    def OBF_Marshal(self, code):
        return __import__('marshal').dumps(compile(code.encode(), '<_minhnguyen-ngocuyen>', 'exec'))
    def OBF_Zlib(self,code):
        return __import__('zlib').compress(code.encode('utf-8'))
    @property
    def _to_import(self):
        self.sum = self._randvar()
        self.sorted = self._randvar()
        self.round = self._randvar()
        self.repr = self._randvar()
        self.pow = self._randvar()
        self.oct = self._randvar()
        self.anext = self._randvar()
        self.next = self._randvar()
        self.min = self._randvar()
        self.max = self._randvar()
        self.locals = self._randvar()
        self.iter = self._randvar()
        self.issubclass = self._randvar()
        self.id = self._randvar()
        self.hash = self._randvar()
        self.hasattr = self._randvar()
        self.format = self._randvar()
        self.divmod = self._randvar()
        self.delattr = self._randvar()
        self.callable = self._randvar()
        self.breakpoint = self._randvar()
        self.bin = self._randvar()
        self.ascii = self._randvar()
        self.any = self._randvar()
        self.all = self._randvar()
        self.abs = self._randvar()
        self.hex = self._randvar()
        self.reversed = self._randvar()
        self.ord = self._randvar()
        self.quit = self._randvar()
        self.exit = self._randvar()
        self.KeyError = self._randvar()
        self.TypeError = self._randvar()
        self.enumerate = self._randvar()
        self.map = self._randvar()
        self.SyntaxError = self._randvar()
        self.NameError = self._randvar()
        self.FileNotFoundError = self._randvar()
        self.PermissionError = self._randvar()
        self.OSError = self._randvar()
        self.UnicodeDecodeError = self._randvar()
        self.UnicodeEncodeError = self._randvar()
        self.range = self._randvar()
        self.compile = self._randvar()
        self.globals = self._randvar()
        self.AttributeError = self._randvar()
        self.ModuleNotFoundError = self._randvar()
        self.getattr = self._randvar()
        self.dir = self._randvar()
        self.vars = self._randvar()
        self.__import__ = self._randvar()
        self.join = self._randvar()
        self.eval = self._randvar()
        self.true = self._randvar()
        self.false = self._randvar()
        self.bool = self._randvar()
        self.str = self._randvar()
        self.int = self._randvar()
        self.chr = self._randvar()
        self.float = self._randvar()
        self.bytes = self._randvar()
        self.zlib = self._randvar()
        self.marshal = self._randvar()
        self.sys = self._randvar()
        self.print = self._randvar()
        self.exec = self._randvar()
        self.input = self._randvar()
        self.len = self._randvar()
        self.list = self._randvar()
        self.UnboundLocalError = self._randvar()
        self.EOFError = self._randvar()
        self.isinstance = self._randvar()
        self.KeyboardInterrupt = self._randvar()
        self.Exception = self._randvar()
        self.IndexError = self._randvar()
        self.ValueError  = self._randvar()
        self.dict = self._randvar()
        self.open = self._randvar()
        self.type = self._randvar()
        self.tuple = self._randvar()
        self.setattr = self._randvar()
        self.requests_get = self._randvar()
        self.requests_post = self._randvar()
        self.ImportError = self._randvar()
        imports = {
            "getattr": self.getattr,
            "dir": self.dir,
            "__import__": self.__import__,
            self._protect_built('True'): self.true,
            self._protect_built('False'): self.false,
            self._protect_built('bool'): self.bool,
            self._protect_built('type'): self.type,
            self._protect_built('str'): self.str,
            self._protect_built('int'): self.int,
            self._protect_built('exec'): self.exec,
            self._protect_built('print'): self.print,
            self._protect_built('setattr'): self.setattr,
            self._protect_built('vars'): self.vars,
            self._protect_built('chr'): self.chr,
            self._protect_built('list'): self.list,
            self._protect_built('open'): self.open,
            self._protect_built('dir'): self.dir,
            self._protect_built('dict'): self.dict,
            self._protect_built('tuple'): self.tuple,
            self._protect_built('sum'): self.sum,
            self._protect_built('sorted'): self.sorted,
            self._protect_built('round'): self.round,
            self._protect_built('repr'): self.repr,
            self._protect_built('pow'): self.pow,
            self._protect_built('oct'): self.oct,
            self._protect_built('anext'): self.anext,
            self._protect_built('next'): self.next,
            self._protect_built('min'): self.min,
            self._protect_built('max'): self.max,
            self._protect_built('locals'): self.locals,
            self._protect_built('iter'): self.iter,
            self._protect_built('issubclass'): self.issubclass,
            self._protect_built('UnboundLocalError'): self.UnboundLocalError,
            self._protect_built('id'): self.id,
            self._protect_built('hash'): self.hash,
            self._protect_built('hasattr'): self.hasattr,
            self._protect_built('format'): self.format,
            self._protect_built('divmod'): self.divmod,
            self._protect_built('delattr'): self.delattr,
            self._protect_built('callable'): self.callable,
            self._protect_built('breakpoint'): self.breakpoint,
            self._protect_built('bin'): self.bin,
            self._protect_built('ascii'): self.ascii,
            self._protect_built('any'): self.any,
            self._protect_built('all'): self.all,
            self._protect_built('abs'): self.abs,
            self._protect_built('hex'): self.hex,
            self._protect_built('reversed'): self.reversed,
            self._protect_built('ord'): self.ord,
            self._protect_built('quit'): self.quit,
            self._protect_built('exit'): self.exit,
            self._protect_built('get', lib='requests'): self.requests_get,
            self._protect_built('post', lib='requests'): self.requests_post,
            self._protect_built('enumerate'): self.enumerate,
            self._protect_built('map'): self.map,
            self._protect_built('SyntaxError'): self.SyntaxError,
            self._protect_built('NameError'): self.NameError,
            self._protect_built('FileNotFoundError'): self.FileNotFoundError,
            self._protect_built('PermissionError'): self.PermissionError,
            self._protect_built('OSError'): self.OSError,
            self._protect_built('UnicodeEncodeError'): self.UnicodeEncodeError,
            self._protect_built('ImportError'): self.ImportError,
            self._protect_built('UnicodeDecodeError'): self.UnicodeDecodeError,
            self._protect_built('range'): self.range,
            self._protect_built('compile'): self.compile,
            self._protect_built('globals'): self.globals,
            self._protect_built('AttributeError'): self.AttributeError,
            self._protect_built('ModuleNotFoundError'): self.ModuleNotFoundError,
            self._protect_built('Exception'): self.Exception,
            self._protect_built('ValueError'): self.ValueError,
            self._protect_built('IndexError'): self.IndexError,
            self._protect_built('KeyboardInterrupt'): self.KeyboardInterrupt,
            self._protect_built('isinstance'): self.isinstance,
            self._protect_built('len'): self.len,
            self._protect_built('input'): self.input,
            self._protect_built('loads', lib='marshal'): self.marshal,
            f"{self.marshal}({__import__('marshal').dumps('')}).join": self.join,
            self._protect_built('float'): self.float,
            self._protect_built('EOFError'): self.EOFError,
            self._protect_built('bytes'): self.bytes,
            self._protect_built('exit', lib='sys'): self.sys,
            self._protect_built('eval'): self.eval,
            self._protect_built('decompress', lib='zlib'): self.zlib
        }
        return imports
    def _obf_bool(self, string):
        if string == 'False':
            obf = f'not({self.bool}({self.str}({self.false})))'
        elif string == 'True':
            obf = f'{self.bool}((~{self.false})or(({self.true})and({self.false})))'
        if self.STRING.upper() == "Y":
            string = self._randvar()
            while string in self.strings:
                string = self._randvar()
            self.strings[string] = obf
            return string
        else:
            return obf
    def _obf_int(self, string):
        if string.isdigit():
            obf = self._adv_int(int(string))
        elif string.replace('.', '').isdigit():
            obf = f"{self.float}({self._protect(string)})"
        else:
            return string
        if self.STRING.upper() == "Y":
            string = self._randvar()
            while string in self.strings:
                string = self._randvar()
            self.strings[string] = obf
            return string
        else:
            return obf
    def _obf_str(self, string):
        obf, do = self._adv_str(string)
        if self.STRING.upper() == "Y":
            if do:
                string = self._randvar()
                while string in self.strings:
                    string = self._randvar()
                self.strings[string] = obf
            else:
                string = obf
            return string
        else:
            return obf
    def _underscore_int(self, string):
        return '_'.join(str(string)).replace('-_','-').replace('+_','+')
    def _adv_int(self, string):
        n = __import__('random').choice((1, 2))
        if n == 1:
            rnum = __import__('random').randint(1000000,9999999999)
            x = rnum - string
            return f"{self.eval}({self._protect(f'{self._underscore_int(rnum)}+(-{self._underscore_int(x)})')})"
        elif n == 2:
            rnum = __import__('random').randint(0, string)
            x = string - rnum
            return f"{self.eval}({self._protect(f'{self._underscore_int(x)}-(-{self._underscore_int(rnum)})')})"
    def _adv_str(self, string):
        var = f"""{self.eval}({self._protect(string, r=1)})"""
        if (string.replace('b','').replace('u','').replace('r','').replace('f','')[0] == '"' and string.split('"')[0].count('f') != 0) or (string.replace('b','').replace('u','').replace('r','').replace('f','')[0] == "'" and string.split("'")[0].count('f') != 0):
            return var, False
        return var, True
class OBF_Formatter(ast.NodeTransformer):
    def visit_JoinedStr(self,node: ast.JoinedStr) -> ast.Call:return ast.Call(func=ast.Attribute(value=ast.Constant(value='{}'*len(node.values)), attr="format", ctx=ast.Load()),args=[value.value if isinstance(value, ast.FormattedValue) else value for value in node.values],keywords=[],)
def OBF_Import(code):
    imports_ = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:imports_.append(name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for name in node.names:
                if name.name == '*':imports_.append((module, '*'))
                else:imports_.append((module, name.name, name.asname))
    result_lines = code.splitlines()
    for i, line in enumerate(result_lines):
        if line.startswith('import') or line.startswith('from'):result_lines[i] = ''
    for imp in imports_:
        if isinstance(imp, tuple):
            if imp[1] == '*':result_lines.insert(0, f'from {imp[0]} import *')
            elif imp[2]:
                if '.' in imp[0]:result_lines.insert(0, f'from {imp[0]} import {imp[1]} as {imp[2]}')
                else:result_lines.insert(0, f"{imp[2]} = __import__('{imp[0]}').{imp[1]}")
            else:
                if '.' in imp[0]:result_lines.insert(0, f'from {imp[0]} import {imp[1]}')
                else:result_lines.insert(0, f"{imp[1]} = __import__('{imp[0]}').{imp[1]}")
        else:result_lines.insert(0, f"{imp.asname if imp.asname else imp.name} = __import__('{imp.name}')")
    return '\n'.join(result_lines)
def OBF_Spam(code):
    alphabet, length = "_Ox"+''.join(__import__('random').choices([str(i) for i in range(10)], k=6)),17
    settings = ObfuscatorSettings()
    # ==================
    setting = ast.parse(code)
    setting = ast.unparse(setting)
    settings.biopaque_transformer(alphabet, length, False)
    settings.call_transformer()
    settings.exceptionjmp_transformer(alphabet, length)
    tree = ast.parse(setting)
    for transformer in settings.transformers:
        tree = transformer.proceed(tree)
    return ast.unparse(tree)
def check_syntax(code):
    try:
        compile(code, '<MinhNguyen2412>', 'exec')
    except Exception as e:
        error_text = str(e)
        raise ChildProcessError(error_text)



text = """⠀⠀⠀⠀⠀


⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠶⠚⠉⢉⣩⠽⠟⠛⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠉⠀⢀⣠⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⣰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⡤⠤⠄⢤⣄⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠴⠒⠋⠉⠀⠀⠀⣀⣤⠴⠒⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡄⠀⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢳⡄⢀⡴⠚⠉⠀⠀⠀⠀⠀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⣰⠃⠀⠀⠹⡏⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⢬⣳⣄⣠⠤⠤⠶⠶⠒⠋⠀⠀⠀⠀⠹⡀⠀⠀⠀⠀⠈⠉⠛⠲⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠖⠋⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠉⢳⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⠋⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⢃⠈⠙⠲⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⠞⠁⠀⠀⠀⢀⢾⠃⠀⠀⠀⠀⠀⠀⠀⠀⢢⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⠮⣄⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⠋⠀⠀⢀⡤⡴⠃⠈⠦⣀⠀⠀⠀⠀⠀⠀⢀⣷⢸⠀⠀⠀⠀⢀⣀⠘⡄⠤⠤⢤⠔⠒⠂⠉⠁⠀⠀⠀⠑⢄⡀⠀⠀⠙⢦⡀⠀⠀⠀
⠀⠀⠀⠀⣼⠃⠀⠀⢠⣞⠟⠀⠀⠀⡄⠀⠉⠒⠢⣤⣤⠄⣼⢻⠸⠀⠀⠀⠀⠉⢤⠀⢿⡖⠒⠊⢦⠤⠤⣀⣀⡀⠀⠀⠀⠈⠻⡝⠲⢤⣀⠙⢦⠀⠀
⠀⠀⠀⢰⠃⠀⠀⣴⣿⠎⠀⠀⢀⣜⠤⠄⢲⠎⠉⠀⠀⡼⠸⠘⡄⡇⠀⠀⠀⠀⢸⠀⢸⠘⢆⠀⠘⡄⠀⠀⠀⢢⠉⠉⠀⠒⠒⠽⡄⠀⠈⠙⠮⣷⡀
⠀⠀⠀⡟⠀⠀⣼⢻⠧⠐⠂⠉⡜⠀⠀⡰⡟⠀⠀⠀⡰⠁⡇⠀⡇⡇⠀⠀⠀⠀⢺⠇⠀⣆⡨⢆⠀⢽⠀⠀⠀⠈⡷⡄⠀⠀⠀⠀⠹⡄⠀⠀⠀⠈⠁
⠀⠀⢸⠃⠀⠀⢃⠎⠀⠀⠀⣴⠃⠀⡜⠹⠁⠀⠀⡰⠁⢠⠁⠀⢸⢸⠀⠀⠀⢠⡸⢣⠔⡏⠀⠈⢆⠀⣗⠒⠀⠀⢸⠘⢆⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀
⠀⠀⢸⠀⠀⠀⡜⠀⠀⢀⡜⡞⠀⡜⠈⠏⠀⠈⡹⠑⠒⠼⡀⠀⠀⢿⠀⠀⠀⢀⡇⠀⢇⢁⠀⠀⠈⢆⢰⠀⠀⠀⠈⡄⠈⢢⠀⠀⠀⠈⣇⠀⠀⠀⠀
⠀⠀⢸⡀⠀⢰⠁⠀⢀⢮⠀⠇⡜⠀⠘⠀⠀⢰⠃⠀⠀⡇⠈⠁⠀⢘⡄⠀⠀⢸⠀⠀⣘⣼⠤⠤⠤⣈⡞⡀⠀⠀⠀⡇⠰⡄⢣⡀⠀⠀⢻⠀⠀⠀⠀
⠀⠀⠈⡇⠀⡜⠀⢀⠎⢸⢸⢰⠁⠀⠄⠀⢠⠃⠀⠀⢸⠀⠀⠀⠀⠀⡇⠀⠀⡆⠀⠀⣶⣿⡿⠿⡛⢻⡟⡇⠀⠀⠀⡇⠀⣿⣆⢡⠀⠀⢸⡇⠀⠀⠀
⠀⠀⢠⡏⠀⠉⢢⡎⠀⡇⣿⠊⠀⠀⠀⢠⡏⠀⠀⠀⠎⠀⠀⠀⠀⠀⡇⠀⡸⠀⠀⠀⡇⠀⢰⡆⡇⢸⢠⢹⠀⠀⠀⡇⠀⢹⠈⢧⣣⠀⠘⡇⠀⠀⠀
⠀⠀⢸⡇⠀⠀⠀⡇⠀⡇⢹⠀⠀⠀⢀⡾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢠⠃⠀⠀⠠⠟⡯⣻⣇⢃⠇⢠⠏⡇⠀⢸⡆⠀⢸⠀⠈⢳⡀⠀⡇⠀⠀⠀
⠀⠀⠀⣇⠀⡔⠋⡇⠀⢱⢼⠀⠀⡂⣼⡇⢹⣶⣶⣶⣤⣤⣀⠀⠀⠀⣇⠇⠀⠀⠀⠀⣶⡭⢃⣏⡘⠀⡎⠀⠇⠀⡾⣷⠀⣼⠀⠀⠀⢻⡄⡇⠀⠀⠀
⠀⠀⠀⣹⠜⠋⠉⠓⢄⡏⢸⠀⠀⢳⡏⢸⠹⢀⣉⢭⣻⡽⠿⠛⠓⠀⠋⠀⠀⠀⠀⠀⠘⠛⠛⠓⠀⡄⡇⠀⢸⢰⡇⢸⡄⡟⠀⠀⠀⠀⢳⡇⠀⠀⠀
⠀⣠⠞⠁⠀⠀⠀⠀⠀⢙⠌⡇⠀⣿⠁⠀⡇⡗⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠁⠁⠀⢸⣼⠀⠈⣇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⠁⠀⠀⢀⡠⠔⠚⠉⠉⢱⣇⢸⢧⠀⠀⠸⣱⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⠦⡔⠀⠀⠀⠀⠀⢀⡼⠀⠀⣼⡏⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⠀⠀⠀⠋⠀⠀⠀⢀⡠⠤⣿⣾⣇⣧⠀⠀⢫⡆⠀⠀⠀⠀⠀⠀⠀⢨⠀⠀⣠⠇⠀⠀⢀⡠⣶⠋⠀⠀⡸⣾⠁⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⡄⠀⠀⠀⠀⠠⠊⠁⠀⠀⢸⢃⠘⡜⡵⡀⠈⢿⡱⢲⡤⠤⢀⣀⣀⡀⠉⠉⣀⡠⡴⠚⠉⣸⢸⠀⠀⢠⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢧⠀⠀⠀⠀⠀⠀⠀⣀⠤⠚⠚⣤⣵⡰⡑⡄⠀⢣⡈⠳⡀⠀⠀⠀⢨⡋⠙⣆⢸⠀⠀⣰⢻⡎⠀⠀⡎⡇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⢷⡀⠀⠀⠀⠀⠀⠁⠀⠀⠀⡸⢌⣳⣵⡈⢦⡀⠳⡀⠈⢦⡀⠀⠘⠏⠲⣌⠙⢒⠴⡧⣸⡇⠀⡸⢸⠇⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣿⠢⡀⠀⠀⠀⠠⠄⡖⠋⠀⠀⠙⢿⣳⡀⠑⢄⠹⣄⡀⠙⢄⡠⠤⠒⠚⡖⡇⠀⠘⣽⡇⢠⠃⢸⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣾⠃⠀⠀⠀⠀⠀⢀⡼⣄⠀⠀⠀⠀⠀⠑⣽⣆⠀⠑⢝⡍⠒⠬⢧⣀⡠⠊⠀⠸⡀⠀⢹⡇⡎⠀⡿⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡼⠁⠀⠀⠀⠀⠀⠀⢀⠻⣺⣧⠀⠀⠀⠰⢢⠈⢪⡷⡀⠀⠙⡄⠀⠀⠱⡄⠀⠀⠀⢧⠀⢸⡻⠀⢠⡇⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⠇⠀⠀⠀⠀⠀⠀⠀⢸⠀⡏⣿⠀⠀⠀⠀⢣⢇⠀⠑⣄⠀⠀⠸⡄⠀⠀⠘⡄⠀⠀⠸⡀⢸⠁⠀⡾⢰⡏⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

banner = """
	 ▌ ▐·▄▄▄ .▄▄▌  ▪  • ▌ ▄ ·.  ▄▄▄· ▄▄▄▄▄▪  ▐▄• ▄ 
	▪█·█▌▀▄.▀·██•  ██ ·██ ▐███▪▐█ ▀█ •██  ██  █▌█▌▪
	▐█▐█•▐▀▀▪▄██▪  ▐█·▐█ ▌▐▌▐█·▄█▀▀█  ▐█.▪▐█· ·██· 
	 ███ ▐█▄▄▌▐█▌▐▌▐█▌██ ██▌▐█▌▐█ ▪▐▌ ▐█▌·▐█▌▪▐█·█▌
	. ▀   ▀▀▀ .▀▀▀ ▀▀▀▀▀  █▪▀▀▀ ▀  ▀  ▀▀▀ ▀▀▀•▀▀ ▀▀
"""
#CRE BIILYTHEGOAT
banner = Add.Add(text, banner, center=True)

dark = Col.dark_gray
light = Col.light_gray
purple = Colors.StaticMIX((Col.green, Col.white))
bpurple = Colors.StaticMIX((Col.green, Col.white))
def p(text):
    # sleep(0.05)
    return print(stage(text))

def stage(text: str, symbol: str = '...', col1 = light, col2 = None) -> str:
    if col2 is None:
        col2 = light if symbol == '...' else purple
    return f""" {Col.Symbol(symbol, col1, dark)} {col2}{text}{Col.reset}"""


def compl(v):
    #b = __import__("marshal").dumps(compile(__import__("zlib").compress(__import__("base64").b64encode(v))))
    b = __import__("marshal").dumps(compile(v,"velimatix","exec"))
    b = __import__("zlib").compress(b)
    b = __import__("base64").b64encode(b)
    return f"""
__Author__ = ("HuynhNgocUyen","MinhNguyen2412")
__In4__ = ("https://www.facebook.com/datishnu1907","https://www.facebook.com/i.usr.bin.python.NguyenMinh")
class VELIMATIX(MemoryError):0
__a__, _0xVELIxMATIX = ("HuynhNgocUyen","NguyenMinh2412"), [
    ["k","a","b"],["j","i","z"],["h","s","r"],["m","2","l"],
    ["o","d"],["1","3","4","6"],["p","e","c"],["y","u","n","g"],
    ["v","[","t","x"]
]
_0x0 = __import__(_0xVELIxMATIX[3][0]+_0xVELIxMATIX[0][1]+_0xVELIxMATIX[2][2]+_0xVELIxMATIX[2][1]+_0xVELIxMATIX[2][0]+_0xVELIxMATIX[0][1]+_0xVELIxMATIX[3][2])
_0x1 = __import__(_0xVELIxMATIX[1][2]+_0xVELIxMATIX[3][2]+_0xVELIxMATIX[1][1]+_0xVELIxMATIX[0][2])
_0x2 = __import__(_0xVELIxMATIX[0][2]+_0xVELIxMATIX[0][1]+_0xVELIxMATIX[2][1]+_0xVELIxMATIX[6][1]+_0xVELIxMATIX[5][3]+_0xVELIxMATIX[5][2])
_0x3 = __import__(_0xVELIxMATIX[0][2]+_0xVELIxMATIX[7][1]+_0xVELIxMATIX[1][1]+_0xVELIxMATIX[3][2]+_0xVELIxMATIX[8][2]+_0xVELIxMATIX[1][1]+_0xVELIxMATIX[7][2]+_0xVELIxMATIX[2][1])
_0x4 = vars().copy()
for VELI, MATIX in vars(_0x0).items():
    if callable(MATIX):
        if VELI == _0xVELIxMATIX[3][2]+_0xVELIxMATIX[4][0]+_0xVELIxMATIX[0][1]+_0xVELIxMATIX[4][1]+_0xVELIxMATIX[2][1]: _0x4["VE"] = MATIX
        else: _0x4[VELI] = MATIX
for VELI, MATIX in vars(_0x1).items():
    if callable(MATIX):
        if VELI == _0xVELIxMATIX[4][1]+_0xVELIxMATIX[6][1]+_0xVELIxMATIX[6][2]+_0xVELIxMATIX[4][0]+_0xVELIxMATIX[3][0]+_0xVELIxMATIX[6][0]+_0xVELIxMATIX[2][2]+_0xVELIxMATIX[6][1]+_0xVELIxMATIX[2][1]+_0xVELIxMATIX[2][1]: _0x4["LI"] = MATIX
        else: _0x4[VELI] = MATIX
for VELI, MATIX in vars(_0x2).items():
    if callable(MATIX):
        if VELI == _0xVELIxMATIX[0][2]+_0xVELIxMATIX[5][3]+_0xVELIxMATIX[5][2]+_0xVELIxMATIX[4][1]+_0xVELIxMATIX[6][1]+_0xVELIxMATIX[6][2]+_0xVELIxMATIX[4][0]+_0xVELIxMATIX[4][1]+_0xVELIxMATIX[6][1]: _0x4["MATIX"] = MATIX
        else: _0x4[VELI] = MATIX
for VELI, MATIX in vars(_0x3).items():
    if callable(MATIX):
        if VELI == _0xVELIxMATIX[6][1]+_0xVELIxMATIX[8][3]+_0xVELIxMATIX[6][1]+_0xVELIxMATIX[6][2]: _0x4["_VELIMATIX"] = MATIX
        else: _0x4[VELI] = MATIX
globals().update(_0x4)
try:_VELIMATIX(VE(LI(MATIX({b}))))
except Exception as e:print(e)
"""

def main():
    try:
        print(Colorate.Diagonal(Colors.DynamicMIX((purple, dark)), Center.XCenter(banner)))
        file = input(stage(f"File {dark}-> {Col.reset}", "velimatix", col2 = bpurple)).replace('"','').replace("'","")
        with open(file, mode='rb') as f:
            script = f.read().decode('utf-8')

        if "globals" in script:
                pass
        elif "global" in script:
            raise Exception("DONT SUPPORT global")
        #STRING = input("--> String <--\n[X] V1 | [Y] V2: ")
        STRING = input(stage(f"String : [X] V1 | [Y] V2: ", "velimatix", col2 = bpurple)).replace('"','').replace("'","")
        BAOMAT = input(stage(f"Exceptionjmp Protect? : [X] NO | [Y] YES: ", "velimatix", col2 = bpurple)).replace('"','').replace("'","")
        
        
        now = __import__('time').time()
        try:
            #LAYEY = ast.parse(OBF_Import(script))
            LAYER = ast.unparse(OBF_Formatter().visit(ast.parse(script)))
            LAYER = OBF_STRING(content=LAYER,STRING=STRING,BAOMAT=BAOMAT).content

            check_syntax(LAYER)
            MARSHAL = input(stage(f"Wall Compile (If U Dont Compile And Want Raw Code u just del Anti_hook ) : [X] NO | [Y] YES: ", "velimatix", col2 = bpurple)).replace('"','').replace("'","")
            if str(MARSHAL).upper() == "Y":
                LAYER = compl(antipycdc+"\n"+LAYER)
        except ChildProcessError as e:
            tb = __import__('traceback').format_exc().splitlines()
            custom_tb = tb[:1] + tb[3:4] + tb[-1:]
            print("\n".join(custom_tb))
        except Exception as e:__import__('logging').error(__import__('traceback').format_exc())
        
        now = round(__import__('time').time() - now, 2)
        #out = input("Nhập file lưu: ")
        #open(out, 'w', encoding='utf-8').write(str(pic[0]))
        outx = "veli-"+file
        open(outx, 'w', encoding='utf-8').write(str(LAYER))
        print(stage(f"File Save in {light}{outx}{bpurple}", "velimatix", col2 = bpurple))
        getpass(stage(f"Obfuscation completed succesfully in {light}{now}s{bpurple}.{Col.reset}", "velimatix", col2 = bpurple))
        
    except KeyboardInterrupt:pass
    except Exception as e:__import__('logging').error(__import__('traceback').format_exc())



if __name__ == '__main__':
    main()
