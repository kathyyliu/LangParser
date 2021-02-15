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
                expression += '('
        elif not expression:  # lone IntegerParse
            return '(' + node.name + ')'
        expression += node.name
        if isinstance(node, StatementParse) and node.children:
            for child in node.children:
                expression += ' '
                expression = self._s_expression(child, expression)
            expression += ')'
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

    # def __str__(self):
    #     return 'Parse(value={}, index{})'.format(self.value, self.index)

    def get_value(self):
        return self.value


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

    # def __str__(self):
    #      return 'Parse(value={}, index{})'.format(self.name, self.index)

    def add_child(self, parse):
        self.children.append(parse)

    # returns right-most descendant of node, returns itself if no children
    def get_last_descendant(self, node):
        last = node
        while last.chilren:
            last = last.children[-1]
        return last

