class Interpreter:

    def __init__(self):
        self.output = ""
        self.curr_environment = Environment()

    def execute(self, node):
        try:
            self.exec(node)
            return self.output
        except RuntimeError:
            pass

    def exec(self, node):
        if node.name == "print":
            self.__exec_print(node)
        elif node.name == "sequence":
            self.__exec_sequence(node)
        elif node.name == "declare":
            self.__exec_declare(node)
        elif node.name == "assign":
            self.__exec_assign(node)
        elif node.name == "if":
            self.__exec_if(node)
        elif node.name == "while":
            self.__exec_while(node)
        else:
            self.eval(node)

    def __exec_print(self, node):
        self.output += str(self.eval(node.children[0]))

    def __exec_sequence(self, node):
        self.curr_environment = self.curr_environment.add_node_after(Environment())
        for child in node.children:
            self.exec(child)
        self.curr_environment = self.curr_environment.parent

    def __exec_declare(self, node):
        if node.children[0].name in self.curr_environment.map:
            raise RuntimeError("variable already defined")
        self.curr_environment.add_var(node.children[0].name, self.eval(node.children[1]))

    def __exec_assign(self, node):
        self.__eval_lookup(node.children[0])    # will raise error if not in curr_environment
        identifier = node.children[0].children[0].name
        self.curr_environment.map[identifier] = self.eval(node.children[1])

    def __exec_if(self, node):
        pass

    def __exec_while(self, node):
        pass

    def eval(self, node):
        if node.name == "lookup":
            return self.__eval_lookup(node)
        elif node.name == "+":
            return self.__eval_plus(node)
        elif node.name == "-":
            return self.__eval_minus(node)
        elif node.name == "*":
            return self.__eval_mult(node)
        elif node.name == "/":
            return self.__eval_div(node)
        elif node.name.isdigit():
            return self.__eval_int(node)
        else:
            raise AssertionError("Unexpected term", node.name)

    def __eval_lookup(self, node):
        identifier = node.children[0].name
        environment = self.curr_environment
        while not identifier in environment.map:    # find correct environment
            if not environment.parent:
                raise RuntimeError("undefined variable")
            environment = environment.parent
        return environment.map[identifier]

    def __eval_plus(self, node):
        return self.eval(node.children[0]) + self.eval(node.children[1])

    def __eval_minus(self, node):
        return self.eval(node.children[0]) - self.eval(node.children[1])

    def __eval_mult(self, node):
        return self.eval(node.children[0]) * self.eval(node.children[1])

    def __eval_div(self, node):
        divisor = self.eval(node.children[1])
        if divisor == 0:
            raise RuntimeError("divide by zero")
        return self.eval(node.children[0]) / divisor

    def __eval_int(self, node):
        return node.value


class Environment:

    def __init__(self):
        self.map = {}
        self.parent = None

    def add_node_after(self, new_node):
        new_node.parent = self
        return new_node

    def add_var(self, identifier, value):
        if (identifier in self.map):
            self.map[identifier] = value
            return False
        else:
            self.map[identifier] = value
            return True
