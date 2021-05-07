class Parse:

    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __eq__(self, other):
        return (
                isinstance(other, Parse)
                and self.name == other.name
                and self.index == other.index
        )

    def __str__(self):
        return self._s_expression(self)

    # str helper
    def _s_expression(self, node, expression=''):
        if isinstance(node, StatementParse):
            if node.children:
                expression += '('+ node.name
                for child in node.children:
                    expression += ' '
                    expression = self._s_expression(child, expression)
                expression += ')'
            else:
                if node.name in ("sequence", "parameters", "arguments", "class"):
                    expression += '(' + node.name + ')'
                # identifier
                else:
                    expression += node.name
        # lone IntegerParse
        elif not expression:
            return '(' + node.name + ')'
        # IntegerParse
        else:
            expression += node.name
        return expression


class IntegerParse(Parse):

    def __init__(self, value, index):
        super().__init__(str(value), index)
        self.value = value

    def __eq__(self, other):
        return (
                isinstance(other, IntegerParse)
                and self.value == other.value
                and self.index == other.index
        )


class ClosureParse(Parse):

    def __init__(self, name, index):
        super().__init__(name, index)

    def __eq__(self, other):
        return self is other


class StatementParse(Parse):

    def __init__(self, name, index):
        super().__init__(name, index)
        self.children = []

    def __eq__(self, other):
        return (
                isinstance(other, StatementParse)
                and self.name == other.name
                and self.index == other.index
        )

    def add_child(self, parse):
        self.children.append(parse)
        self.index = parse.index
