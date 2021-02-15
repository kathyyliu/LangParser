class Interpreter:
    output = ""

    def __init__(self):
        pass

    def execute(self, node):
        try:
            exec(node)
        except RuntimeError:
            pass

    def exec(self, node):
        if node.name == "print":
            self.__exec_print(node)
        elif node.name == "sequence":
            self.__exec_sequence(node)
        elif node.name == "if":
            self.__exec_if(node)
        elif node.name == "while":
            self.__exec_while(node)
        else:
            self.eval(node)

    def __exec_print(self, node):
        self.output = eval(node.children[0])

    def __exec_sequence(self, node):
        pass

    def __exec_if(self, node):
        pass

    def __exec_while(self, node):
        pass

    def eval(self, node):
        if node.name == "+":
            return self.__eval_plus(node)
        elif node.name == "-":
            return self.__eval_minus(node)
        elif node.name == "*":
            return self.__eval_mult(node)
        elif node.name == "/":
            return self.__eval_div(node)
        elif node.name == "int":
            return self.__eval_int(node)
        else:
            raise AssertionError("Unexpected term", node.name)

    def __eval_plus(self, node):
        return eval(node.children[0]) + eval(node.children[1])

    def __eval_minus(self, node):
        return eval(node.children[0]) - eval(node.children[1])

    def __eval_mult(self, node):
        return eval(node.children[0]) * eval(node.children[1])

    def __eval_div(self, node):
        divisor = eval(node.children[1])
        if divisor != 0:
            return eval(node.children[0]) / divisor
        else:
            raise RuntimeError("divide by zero")

    def __eval_int(self, node):
        return node.value

