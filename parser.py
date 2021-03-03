import parse as parse


class Parser:
    FAIL = parse.StatementParse("FAIL", -1)

    def __init__(self):
        pass

    def parse(self, string):
        parse = self.__parse(string, "program")
        if parse.index < len(string):
            return None
        return parse

    def __parse(self, string, term, index=0):
        if index > len(string):
            return Parser.FAIL
        methods = (self.__parse_program, self.__parse_statement, self.__parse_if_statement,
                   self.__parse_if_else_statement, self.__parse_while_statement, self.__parse_declaration_statement,
                   self.__parse_assignment_statement, self.__parse_location, self.__parse_print_statement,
                   self.__parse_expression_statement, self.__parse_expression, self.__parse_or_expression,
                   self.__parse_or_operator, self.__parse_and_expression, self.__parse_and_operator,
                   self.__parse_optional_not_expression, self.__parse_not_expression, self.__parse_comp_expression,
                   self.__parse_comp_operator, self.__parse_add_sub_expression, self.__parse_add_sub_operator,
                   self.__parse_mul_div_expression, self.__parse_mul_div_operator, self.__parse_operand,
                   self.__parse_parenthesized_expression, self.__parse_identifier, self.__parse_identifier_first_char,
                   self.__parse_identifier_char, self.__parse_integer, self.__parse_opt_space, self.__parse_req_space,
                   self.__parse_space, self.__parse_comment)
        for method in methods:
            if term == method.__name__[8:]:
                return method(string, index)
        raise ValueError("invalid term")

    # = opt_space ( statement opt_space )*
    def __parse_program(self, string, index):
        this_parse = self.__parse(string, "opt_space", index)
        parent = parse.StatementParse("sequence", this_parse.index)
        while this_parse != Parser.FAIL:
            this_parse = self.__parse(string, "statement", this_parse.index)
            if this_parse == Parser.FAIL:
                break
            this_parse.index = self.__parse(string, "opt_space", this_parse.index).index
            parent.add_child(this_parse)
            parent.index = this_parse.index
        return parent

    # = declaration | assignment | if_else | if | while | print | expression_statement
    def __parse_statement(self, string, index):
        for statement in ("declaration_statement", "assignment_statement", "if_else_statement", "if_statement",
                          "while_statement", "print_statement", "expression_statement"):
            parse = self.__parse(string, statement, index)
            if parse != Parser.FAIL:
                return parse
        return Parser.FAIL

    # = "if" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}"
    def __parse_if_statement(self, string, index):
        if index + 2 >= len(string):
            return Parser.FAIL
        if string[index : index + 2] != "if": # TODO: change others?
            return Parser.FAIL
        left = self.__parse(string, "opt_space", index + 2)
        if string[left.index] != '(':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        left = self.__parse(string, "expression", left.index)
        left.index = self.__parse(string, "opt_space", left.index).index
        if left == Parser.FAIL or string[left.index] != ')':
            return Parser.FAIL
        right = self.__parse(string, "opt_space", left.index + 1)
        if string[right.index] != '{':
            return Parser.FAIL
        right.index = self.__parse(string, "opt_space", right.index + 1).index
        right = self.__parse(string, "program", right.index)
        right.index = self.__parse(string, "opt_space", right.index).index
        if right == Parser.FAIL or string[right.index] != '}':
            return Parser.FAIL
        right.index += 1
        parent = parse.StatementParse("if", right.index)
        parent.add_child(left)
        parent.add_child(right)
        return parent

    # = "if" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}"
    # opt_space "else" opt_space "{" opt_space program opt_space "}"
    def __parse_if_else_statement(self, string, index):
        if index + 2 >= len(string):
            return Parser.FAIL
        if string[index : index + 2] != 'if':  # TODO: change others?
            return Parser.FAIL
        left = self.__parse(string, "opt_space", index + 2)
        if string[left.index] != '(':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        left = self.__parse(string, "expression", left.index)
        left.index = self.__parse(string, "opt_space", left.index).index
        if left == Parser.FAIL or string[left.index] != ')':
            return Parser.FAIL
        right1 = self.__parse(string, "opt_space", left.index + 1)
        if string[right1.index] != '{':
            return Parser.FAIL
        right1.index = self.__parse(string, "opt_space", right1.index + 1).index
        right1 = self.__parse(string, "program", right1.index)
        right1.index = self.__parse(string, "opt_space", right1.index).index
        if right1 == Parser.FAIL or string[right1.index] != '}':
            return Parser.FAIL
        right1.index = self.__parse(string, "opt_space", right1.index + 1).index
        if right1.index + 4 >= len(string):
            return Parser.FAIL
        if string[right1.index:right1.index + 4] != 'else':
            return Parser.FAIL
        right2 = self.__parse(string, "opt_space", right1.index + 4)
        if string[right2.index] != '{':
            return Parser.FAIL
        right2.index = self.__parse(string, "opt_space", right2.index + 1).index
        right2 = self.__parse(string, "program", right2.index)
        right2.index = self.__parse(string, "opt_space", right2.index).index
        if right2 == Parser.FAIL or string[right2.index] != '}':
            return Parser.FAIL
        right2.index += 1
        parent = parse.StatementParse("ifelse", right2.index)
        parent.add_child(left)
        parent.add_child(right1)
        parent.add_child(right2)
        return parent

    # = "while" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}"
    def __parse_while_statement(self, string, index):
        if index + 5 >= len(string):
            return Parser.FAIL
        if string[index : index + 5] != 'while':
            return Parser.FAIL
        left = self.__parse(string, "opt_space", index + 5)
        if string[left.index] != '(':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        left = self.__parse(string, "expression", left.index)
        left.index = self.__parse(string, "opt_space", left.index).index
        if left == Parser.FAIL or string[left.index] != ')':
            return Parser.FAIL
        right = self.__parse(string, "opt_space", left.index + 1)
        if string[right.index] != '{':
            return Parser.FAIL
        right.index = self.__parse(string, "opt_space", right.index + 1).index
        right = self.__parse(string, "program", right.index)
        right.index = self.__parse(string, "opt_space", right.index).index
        if right == Parser.FAIL or string[right.index] != '}':
            return Parser.FAIL
        right.index += 1
        parent = parse.StatementParse("while", right.index)
        parent.add_child(left)
        parent.add_child(right)
        return parent

    # = "var" req_space assignment_statement
    def __parse_declaration_statement(self, string, index):
        # index out of bounds protection; shortest possible len(var x=0;) = 8
        if len(string[index:]) < 8:
            return Parser.FAIL
        for i in range(3):
            if string[index + i] != "var"[i]:
                return Parser.FAIL
        parent = parse.StatementParse("declare", index + 3)
        this_parse = self.__parse(string, "req_space", parent.index)
        if this_parse == Parser.FAIL:
            return Parser.FAIL
        this_parse = self.__parse(string, "assignment_statement", this_parse.index)
        if this_parse == Parser.FAIL:
            return Parser.FAIL
        # turn appropriate children of assign to children of declare node
        parent.add_child(this_parse.children[0].children[0])    # child[0] is (varloc x), want x
        parent.add_child(this_parse.children[1])
        parent.index = parent.children[1].index
        return parent

    # = location opt_space "=" opt_space expression opt_space ";"
    def __parse_assignment_statement(self, string, index):
        left = self.__parse(string, "location", index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.name = "varloc"
        left.index = self.__parse(string, "opt_space", left.children[0].index).index
        if left.index <= len(string):
            if string[left.index] == '=':
                left.index += 1
                left.index = self.__parse(string, "opt_space", left.index).index
                right = self.__parse(string, "expression", left.index)
                if right == Parser.FAIL:
                    return Parser.FAIL
                right.index = self.__parse(string, "opt_space", right.index).index
                if right.index < len(string):
                    if string[right.index] == ";":
                        right.index += 1
                        parent = parse.StatementParse("assign", right.index)
                        parent.add_child(left)
                        parent.add_child(right)
                        return parent
        return Parser.FAIL

    # = identifier
    def __parse_location(self, string, index):
        this_parse = self.__parse(string, "identifier", index)
        return this_parse

    # = "print" req_space expression opt_space ";"
    def __parse_print_statement(self, string, index):
        if index + 5 >= len(string):
            return Parser.FAIL
        if string[index:index + 5] != 'print':
            return Parser.FAIL
        parent = parse.StatementParse("print", index + 5)
        this_parse = self.__parse(string, "req_space", parent.index)
        if this_parse == Parser.FAIL:
            return Parser.FAIL
        child = self.__parse(string, "expression", this_parse.index)
        if child == Parser.FAIL:
            return Parser.FAIL
        if child.index >= len(string):
            return Parser.FAIL
        if string[child.index] == ';':
            child.index += 1
            parent.add_child(child)
            return parent

    # = expression opt_space ";"
    def __parse_expression_statement(self, string, index):
        this_parse = self.__parse(string, "expression", index)
        if this_parse == Parser.FAIL:
            return Parser.FAIL
        this_parse.index = self.__parse(string, "opt_space", this_parse.index).index
        if this_parse.index < len(string):
            if string[this_parse.index] == ';':
                this_parse.index += 1
                return this_parse
        return Parser.FAIL

    # = or_expression
    def __parse_expression(self, string, index):
       return self.__parse(string, "or_expression", index)

    # = and_expression ( opt_space or_operator opt_space and_expression )*
    def __parse_or_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "and_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "or_operator", left.index)
            if parent != Parser.FAIL:
                parent.index = self.__parse(string, "opt_space", parent.index).index
                right = self.__parse(string, "and_expression", parent.index)
                if right != Parser.FAIL:
                    parent.add_child(left)
                    parent.add_child(right)
                    if right.index < len(string):
                        right.index = self.__parse(string, "opt_space", right.index).index
                    parent.index = right.index
                    left = parent
                else:
                    break
            else:
                break
        return left

    # = "||"
    def __parse_or_operator(self, string, index):
        if index + 2 <= len(string):
            if string[index] != '|' or string[index + 1] != '|':
                return Parser.FAIL
        return parse.StatementParse('||', index + 2)


    # = optional_not_expression (opt_space and_operator opt_space optional_not_expression ) *;
    def __parse_and_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "optional_not_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "and_operator", left.index)
            if parent != Parser.FAIL:
                parent.index = self.__parse(string, "opt_space", parent.index).index
                right = self.__parse(string, "optional_not_expression", parent.index)
                if right != Parser.FAIL:
                    parent.add_child(left)
                    parent.add_child(right)
                    if right.index < len(string):
                        right.index = self.__parse(string, "opt_space", right.index).index
                    parent.index = right.index
                    left = parent
                else:
                    break
            else:
                break
        return left

    # = "&&"
    def __parse_and_operator(self, string, index):
        if index + 1 <= len(string):
            if string[index] != '&' or string[index + 1] != '&':
                return Parser.FAIL
        return parse.StatementParse('&&', index + 2)

    # not_expression | comp_expression;
    def __parse_optional_not_expression(self, string, index):
        for expression in ("not_expression", "comp_expression"):
            parse = self.__parse(string, expression, index)
            if parse != Parser.FAIL:
                return parse
        return Parser.FAIL

    # = "!" opt_space comp_expression
    def __parse_not_expression(self, string, index):
        if index + 1 >= len(string) or string[index] != '!':
            return Parser.FAIL
        child = self.__parse(string, "opt_space", index + 1)
        child = self.__parse(string, "comp_expression", child.index)
        if child == Parser.FAIL:
            return Parser.FAIL
        parent = parse.StatementParse("!", child.index)
        parent.add_child(child)
        return parent

    # = add_sub_expression ( opt_space comp_operator opt_space add_sub_expression)*
    def __parse_comp_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "add_sub_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "comp_operator", left.index)
            if parent != Parser.FAIL:
                parent.index = self.__parse(string, "opt_space", parent.index).index
                right = self.__parse(string, "add_sub_expression", parent.index)
                if right != Parser.FAIL:
                    parent.add_child(left)
                    parent.add_child(right)
                    if right.index < len(string):
                        right.index = self.__parse(string, "opt_space", right.index).index
                    parent.index = right.index
                    left = parent
                else:
                    break
            else:
                break
        return left

    # = "==" | "!=" | "<=" | ">=" | "<" | ">"
    def __parse_comp_operator(self, string, index):
        if index + 1 < len(string):
            operator = string[index] + string[index + 1]
            if operator in ('==', '!=', '<=', '>='):
                return parse.StatementParse(operator, index + 2)
            elif string[index] in ('<', '>'):
                return parse.StatementParse(string[index], index + 1)
        return Parser.FAIL

    # = mul_div_expression (opt_space add_sub_operator opt_space mul_div_expression)*
    def __parse_add_sub_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "mul_div_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "add_sub_operator", left.index)
            if parent != Parser.FAIL:
                parent.index = self.__parse(string, "opt_space", parent.index).index
                right = self.__parse(string, "mul_div_expression", parent.index)
                if right != Parser.FAIL:
                    parent.add_child(left)
                    parent.add_child(right)
                    if right.index < len(string):
                        right.index = self.__parse(string, "opt_space", right.index).index
                    parent.index = right.index
                    left = parent
                else:
                    break
            else:
                break
        return left

    # = "+" | "-"
    def __parse_add_sub_operator(self, string, index):
        if index < len(string):
            if string[index] not in ("+", "-"):
                return Parser.FAIL
        return parse.StatementParse(string[index], index + 1)


    # = operand ( opt_space mul_div_operator opt_space operand )*
    def __parse_mul_div_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "operand", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "mul_div_operator", left.index)
            if parent != Parser.FAIL:
                parent.index = self.__parse(string, "opt_space", parent.index).index
                right = self.__parse(string, "operand", parent.index)
                if right != Parser.FAIL:
                    parent.add_child(left)
                    parent.add_child(right)
                    if right.index < len(string):
                        right.index = self.__parse(string, "opt_space", right.index).index
                    parent.index = right.index
                    left = parent
                else:
                    break
            else:
                break
        return left

    # = "*" | "\"
    def __parse_mul_div_operator(self, string, index):
        if index < len(string):
            if string[index] not in ("*", "/"):
                return Parser.FAIL
        return parse.StatementParse(string[index], index + 1)


    # = parenthesized_expression | identifier | integer
    def __parse_operand(self, string, index):
        for operand in ("parenthesized_expression", "identifier", "integer"):
            parse = self.__parse(string, operand, index)
            if parse != Parser.FAIL:
                return parse
        return Parser.FAIL

    # = "(" opt_space expression opt_space ")"
    def __parse_parenthesized_expression(self, string, index):
        if index == len(string):
            return Parser.FAIL
        if string[index] != "(":
            return Parser.FAIL
        parse = self.__parse(string, "add_sub_expression", index + 1)
        if parse == Parser.FAIL:
            return Parser.FAIL
        parse.index = self.__parse(string, "opt_space", parse.index).index
        if string[parse.index] != ")":
            return Parser.FAIL
        parse.index += 1
        return parse

    # = identifier_first_char ( identifier_char )*
    def __parse_identifier(self, string, index):
        this_parse = self.__parse(string, "identifier_first_char", index)
        if this_parse == Parser.FAIL:
            return Parser.FAIL
        this_index = this_parse.index
        while this_index < len(string):
            this_parse = self.__parse(string, "identifier_char", this_index)
            if this_parse == Parser.FAIL:
                break
            this_index = this_parse.index
        # check identifier is not keyword
        identifier = string[index:this_index]
        if identifier in ('print', 'var', 'if', 'else', 'while', 'func', 'ret', 'class', 'int', 'bool', 'string'):
            return Parser.FAIL
        parent = parse.StatementParse("lookup", this_index)
        parent.add_child(parse.StatementParse(identifier, this_index))
        return parent

    # = ALPHA | "_"
    def __parse_identifier_first_char(self, string, index):
        if index == len(string):
            return Parser.FAIL
        if not string[index].isalpha() and string[index] != '_':
            return Parser.FAIL
        return parse.IntegerParse(0, index + 1)

    # = ALNUM | "_"
    def __parse_identifier_char(self, string, index):
        if index == len(string):
            return Parser.FAIL
        if not string[index].isalnum() and string[index] != '_':
            return Parser.FAIL
        return parse.IntegerParse(0, index + 1)

    # = (DIGIT) +
    def __parse_integer(self, string, index):
        parsed = ""
        while index < len(string) and string[index].isdigit():
            parsed += string[index]
            if index < len(string):
                index += 1
        if not parsed:
            return Parser.FAIL
        return parse.IntegerParse(int(parsed), index)

    # = (space)*
    def __parse_opt_space(self, string, index):
        if index == len(string):
            return parse.IntegerParse(0, index)
        this_parse = self.__parse(string, "space", index)
        if this_parse == Parser.FAIL:
            return parse.IntegerParse(0, index)
        while this_parse.index < len(string):
            # prevent this_parse from actually becoming Parser.FAIL # FIXME
            if self.__parse(string, "space", this_parse.index) == Parser.FAIL:
                break
            this_parse = self.__parse(string, "space", this_parse.index)
        return parse.IntegerParse(0, this_parse.index)

    # = (space)+
    def __parse_req_space(self, string, index):
        this_parse = self.__parse(string, "space", index)
        if this_parse != Parser.FAIL:
            this_parse = self.__parse(string, "opt_space", this_parse.index)
            return parse.IntegerParse(0, this_parse.index)
        else:
            return Parser.FAIL

    # = comment | BLANK | NEWLINE
    def __parse_space(self, string, index):
        if -1 < index < len(string):
            this_parse = self.__parse(string, "comment", index)
            if this_parse != Parser.FAIL:
                return this_parse
            if string[index] in (" ", "\n"):
                return parse.IntegerParse(0, index + 1)
        return Parser.FAIL

    # = "#" (PRINT) * NEWLINE
    def __parse_comment(self, string, index):
        if index != len(string):
            if string[index] == "#":
                index += 1
                while index < len(string):
                    if string[index] == '\n':
                        return parse.IntegerParse(0, index + 1)
                    index += 1
        return Parser.FAIL
