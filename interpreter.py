import parse as parse

class Interpreter:

    operations = {
        '||': lambda left, right: 1 if left or right else 0,
        '&&': lambda left, right: 1 if left and right else 0,
        '==': lambda left, right: 1 if left == right else 0,
        '!=': lambda left, right: 1 if left != right else 0,
        '<=': lambda left, right: 1 if left <= right else 0,
        '>=': lambda left, right: 1 if left >= right else 0,
        '<': lambda left, right: 1 if left < right else 0,
        '>': lambda left, right: 1 if left > right else 0
    }

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
        elif node.children[0].name == "class":
            self.return_value = Class(node.children[0], self.curr_environment)
        else:
            self.return_value = self.eval(node.children[0])

    def __exec_declare(self, node):
        if len(node.children) > 2:
            type = node.children[0]
            identifier = node.children[1]
            value = node.children[2]
        else:
            type = parse.StatementParse("var", 0)
            identifier = node.children[0]
            value = node.children[1]
        if value.name == "function":
            value = Closure(value, self.curr_environment)
        elif value.name == "class":
            value = Class(value, self.curr_environment)
        else:
            value = self.eval(value)
        if identifier.name in self.curr_environment.map:
            self.output += "runtime error: variable already defined"
            raise RuntimeError
        if not self.check_type(type, value):
            self.output += "runtime error: type mismatch"
            raise RuntimeError
        self.curr_environment.add_var(identifier.name, type, value)

    def check_type(self, type, value):
        if (type.name == 'int' and not isinstance(value, int)) \
                    or (type.name == 'func' and not isinstance(value, Closure)):
            return False
        return True

    def __exec_assign(self, node):
        if node.children[1].name == "function":
            value = Closure(node.children[1], self.curr_environment)
        elif node.children[1].name == "class":
            value = Class(node.children[1], self.curr_environment)
        else:
            value = self.eval(node.children[1])
        location = self.eval(node.children[0])
        if not self.check_type(location.environment.map[location.name][0], value):
            self.output += "runtime error: type mismatch"
            raise RuntimeError
        location.environment.map[location.name][1] = value

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
            return self.__eval_call(node)
        elif node.name in ("member", "memloc"):
            return self.__eval_member(node)
        elif node.name == "lookup":
            return self.__eval_lookup(node)
        elif node.name == "varloc":
            return self.__eval_varloc(node)
        if node.name in ("||", "&&", "!", "==", "!=", "<=", ">=", "<", ">"):
            return self.__eval_comp(node)
        elif node.name in ("+", "-", "*", "/"):
            return self.__eval_math(node)
        elif node.name.isdigit():
            return self.__eval_int(node)

    def __eval_call(self, node):
        if node.children[0].name == "function":
            callable = Closure(node.children[0], self.curr_environment)
        elif node.children[0].name == "class":
            callable = Class(node.children[0], self.curr_environment)
        else:
            callable = self.eval(node.children[0])
            if not isinstance(callable, Callable):
                self.output += "runtime error: calling a non-function"
                raise RuntimeError
        if isinstance(callable, Class):
            if node.children[1].children:
                self.output += "runtime error: argument mismatch"
                raise RuntimeError
        else:
            if len(callable.parse.children) > 2:
                params = callable.parse.children[1]
                body = callable.parse.children[2]
                typed = True
            else:
                params = callable.parse.children[0]
                body = callable.parse.children[1]
                typed = False
            num_args = len(node.children[1].children)
            if callable.environment.is_object:
                num_args += 1
            if num_args != len(params.children):
                self.output += "runtime error: argument mismatch"
                raise RuntimeError
            arguments = []
            if callable.environment.is_object:  # if func is member append obj as 1st arg
                instance = callable.environment
                arguments.append(instance)
                num_args -= 1
            for i in range(num_args):  # eval each arg in order in curr env
                arg = node.children[1].children[i]
                if arg.name == "function":
                    arguments.append(Closure(arg, self.curr_environment))
                elif arg.name == "class":
                    arguments.append(Class(arg, self.curr_environment))
                else:
                    arguments.append(self.eval(arg))
        temp = self.curr_environment  # save curr env to a var
        new_environment = Environment()  # push new env
        new_environment.parent = callable.environment
        self.curr_environment = new_environment
        if isinstance(callable, Closure):
            for i in range(len(arguments)):  # add all args to new env
                var_name = params.children[i].name
                if var_name in self.curr_environment.map:
                    self.output += "runtime error: duplicate parameter"
                    raise RuntimeError
                if typed:
                    if not self.check_type(callable.parse.children[0].children[i], arguments[i]):
                        self.output += "runtime error: type mismatch"
                        raise RuntimeError
                    self.curr_environment.add_var(var_name, callable.parse.children[0].children[i], arguments[i])
                else:
                    self.curr_environment.add_var(var_name, parse.StatementParse("var", 0), arguments[i])
        self.num_func_calls += 1
        if isinstance(callable, Closure):  # execute body of func
            self.exec(body)
            if self.return_value:
                if typed and not self.check_type(callable.parse.children[0].children[-1], self.return_value):
                    self.output += "runtime error: type mismatch"
                    raise RuntimeError
                result = self.return_value
            else:
                result = 0
                if typed and not self.check_type(callable.parse.children[0].children[-1], result):
                    self.output += "runtime error: type mismatch"
                    raise RuntimeError
        else:  # create object
            for child in callable.parse.children:
                self.exec(child)
            result = self.curr_environment
            self.curr_environment.is_object = True
        self.num_func_calls -= 1
        self.return_value = None
        self.curr_environment = temp  # set curr env back
        return result

    def __eval_member(self, node):
        identifier = node.children[1].name
        instance = self.eval(node.children[0])
        if node.name == "memloc":
            instance = instance.environment.map[instance.name][1]
        if not isinstance(instance, Environment) or not instance.is_object:
            self.output += "runtime error: member of non-object"
            raise RuntimeError
        if identifier not in instance.map:
            self.output += "runtime error: undefined member"
            raise RuntimeError
        if node.name == "memloc":
            return Location(instance, identifier)
        else:
            return instance.map[identifier][1]

    def __eval_varloc(self, node):
        identifier = node.children[0].name
        environment = self.curr_environment
        while not identifier in environment.map:
            if not environment.parent:
                self.output += "runtime error: undefined variable"
                raise RuntimeError
            environment = environment.parent
        return Location(environment, identifier)

    def __eval_lookup(self, node):
        identifier = node.children[0].name
        environment = self.curr_environment
        while not identifier in environment.map:  # find correct environment
            if not environment.parent:
                self.output += "runtime error: undefined variable"
                raise RuntimeError
            environment = environment.parent
        return environment.map[identifier][1]

    def __eval_comp(self, node):
        left = self.eval(node.children[0])
        if node.name == '!':
            return 1 if not left else 0
        elif node.name == '||' and left:
            return 1
        right = self.eval(node.children[1])
        if node.name in ('<=', '>=', '<', '>'):
            for type in (Closure, Environment, Class):
                if isinstance(left, type) or isinstance(right, type):
                    self.output += "runtime error: math operation on functions"
                    raise RuntimeError
        return self.operations[node.name](left, right)

    def __eval_math(self, node):
        left = self.eval(node.children[0])
        right = self.eval(node.children[1])
        for type in (Closure, Environment, Class):
            if isinstance(left, type) or isinstance(right, type):
                self.output += "runtime error: math operation on functions"
                raise RuntimeError
        if node.name == '/':
            if right == 0:
                self.output += "runtime error: divide by zero"
                raise RuntimeError
            return left // right
        return eval(str(left) + node.name + str(right))

    def __eval_int(self, node):
        return node.value


class Callable:

    def __init__(self, parse, environment):
        self.parse = parse
        self.environment = environment


class Closure(Callable):

    def __init__(self, parse, environment):
        super().__init__(parse, environment)

    def __str__(self):
        return "closure"


class Class(Callable):

    def __init__(self, parse, environment):
        super().__init__(parse, environment)

    def __str__(self):
        return "class"


class Environment:

    def __init__(self):
        self.map = {}
        self.parent = None
        self.is_object = False

    def add_var(self, identifier, type, value):
        self.map[identifier] = [type, value]

    def __eq__(self, other):
        return self is other

    def __str__(self):
        return "obj"


class Location:

    def __init__(self, environment, name):
        self.environment = environment
        self.name = name
