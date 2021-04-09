import parse as parse

class Interpreter:

    def __init__(self):
        self.output = ""
        self.curr_environment = Environment()
        self.return_value = None
        self.num_func_calls = 0

    def execute(self, node):
        try:
            self.exec(node)
        except RuntimeError:
            pass
        finally:
            return self.output

    def exec(self, node):
        if node.name == "print":
            self.__exec_print(node)
        elif node.name == "sequence":
            self.__exec_sequence(node)
        elif node.name == "return":
            self.__exec_return(node)
        elif node.name == "declare":
            self.__exec_declare(node)
        elif node.name == "assign":
            self.__exec_assign(node)
        elif node.name == "if":
            self.__exec_if(node)
        elif node.name == "ifelse":
            self.__exec_ifelse(node)
        elif node.name == "while":
            self.__exec_while(node)
        else:
            self.eval(node)

    def __exec_print(self, node):
        x = str(self.eval(node.children[0])) + '\n'
        self.output += x

    def __exec_sequence(self, node):
        for child in node.children:
            if self.return_value is not None:
                break
            self.exec(child)

    def __exec_return(self, node):
        if self.num_func_calls == 0:
            self.output += "runtime error: returning outside function"
            raise RuntimeError
        if node.children[0].name == "function":
            self.return_value = Closure(node.children[0], self.curr_environment)
        else:
            self.return_value = self.eval(node.children[0])

    def __exec_declare(self, node):
        if node.children[1].name == "function":
            value = Closure(node.children[1], self.curr_environment)
        else:
            value = self.eval(node.children[1])
        if node.children[0].name in self.curr_environment.map:
            self.output += "runtime error: variable already defined"
            raise RuntimeError
        self.curr_environment.add_var(node.children[0].name, value)

    def __exec_assign(self, node):
        value = self.eval(node.children[1])
        identifier = node.children[0].children[0].name
        environment = self.curr_environment
        while not identifier in environment.map:
            if not environment.parent:
                self.output += "runtime error: undefined variable"
                raise RuntimeError
            environment = environment.parent
        environment.map[identifier] = value

    def __exec_if(self, node):
        new_env = Environment()
        new_env.parent = self.curr_environment
        self.curr_environment = new_env
        if self.eval(node.children[0]):
            self.exec(node.children[1])
        self.curr_environment = self.curr_environment.parent

    def __exec_ifelse(self, node):
        new_env = Environment()
        new_env.parent = self.curr_environment
        self.curr_environment = new_env
        if self.eval(node.children[0]):
            self.exec(node.children[1])
        else:
            self.exec(node.children[2])
        self.curr_environment = self.curr_environment.parent

    def __exec_while(self, node):
        while self.eval(node.children[0]):
            new_env = Environment()
            new_env.parent = self.curr_environment
            self.curr_environment = new_env
            self.exec(node.children[1])
            self.curr_environment = self.curr_environment.parent
            if self.return_value is not None:
                break

    def eval(self, node):
        if node.name == "call":
            return self.__eval_function_call(node)
        elif node.name == "lookup":
            return self.__eval_lookup(node)
        if node.name in ("||", "&&", "!", "==", "!=", "<=", ">=", "<", ">"):
            return self.__eval_comp(node)
        elif node.name in ("+", "-", "*", "/"):
            return self.__eval_math(node)
        elif node.name.isdigit():
            return self.__eval_int(node)

    # (call (lookup func) (arguments 1 2))
    def __eval_function_call(self, node):
        if node.children[0].name == "function":
            closure = Closure(node.children[0], self.curr_environment)
        else:
            closure = self.eval(node.children[0])
            if not isinstance(closure, Closure):
                self.output += "runtime error: calling a non-function"
                raise RuntimeError
        num_args = len(node.children[1].children)
        if num_args != len(closure.parse.children[0].children):
            self.output += "runtime error: argument mismatch"
            raise RuntimeError
        arguments = []
        for i in range(num_args):                           # eval each arg in order in the curr env
            arg = node.children[1].children[i]
            if arg.name == "function":
                arguments.append(Closure(arg, self.curr_environment))
            else:
                arguments.append(self.eval(arg))
        temp = self.curr_environment                        # save curr env to a var
        new_environment = Environment()                     # push new env
        new_environment.parent = closure.environment
        self.curr_environment = new_environment
        for i in range(len(arguments)):                     # add all args to new env
            var_name = closure.parse.children[0].children[i].name
            if var_name in self.curr_environment.map:
                self.output += "runtime error: duplicate parameter"
                raise RuntimeError
            self.curr_environment.add_var(var_name, arguments[i])
        self.num_func_calls += 1
        self.exec(closure.parse.children[1])                # execute body of func
        if self.return_value:
            result = self.return_value
        else:
            result = 0
        self.num_func_calls -= 1
        self.return_value = None
        self.curr_environment = temp                        # set curr env back
        return result

    def __eval_lookup(self, node):
        identifier = node.children[0].name
        environment = self.curr_environment
        while not identifier in environment.map:  # find correct environment
            if not environment.parent:
                self.output += "runtime error: undefined variable"
                raise RuntimeError
            environment = environment.parent
        return environment.map[identifier]

    def __eval_comp(self, node):
        left = self.eval(node.children[0])
        if node.name == '!':
            return 1 if not left else 0
        right = self.eval(node.children[1])
        if (isinstance(left, Closure) or isinstance(right, Closure)) and node.name in ('<=', '>=', '<', '>'):
            self.output += "runtime error: math operation on functions"
            raise RuntimeError
        operations = {
            '||': lambda left, right : 1 if left or right else 0,
            '&&': lambda left, right : 1 if left and right else 0,
            '==': lambda left, right : 1 if left == right else 0,
            '!=': lambda left, right : 1 if left != right else 0,
            '<=': lambda left, right : 1 if left <= right else 0,
            '>=': lambda left, right : 1 if left >= right else 0,
            '<': lambda left, right : 1 if left < right else 0,
            '>': lambda left, right : 1 if left > right else 0
        }
        return operations[node.name](left, right)

    def __eval_math(self, node):
        left = self.eval(node.children[0])
        right = self.eval(node.children[1])
        if isinstance(left, Closure) or isinstance(right, Closure):
            self.output += "runtime error: math operation on functions"
            raise RuntimeError
        if node.name == '/':
            if right == 0:
                self.output += "runtime error: divide by zero"
                raise RuntimeError
            return left // right
        return eval(str(left)+node.name+str(right))

    def __eval_int(self, node):
        return node.value


class Closure:

    def __init__(self, parse, environment):
        self.parse = parse              # (function (param 1 2) (sequence))
        self.environment = environment  # environment in which func is defined

    def __str__(self):
        return "closure"


class Environment:

    def __init__(self):
        self.map = {}
        self.parent = None

    def add_var(self, identifier, value):
        self.map[identifier] = value

