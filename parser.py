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
        method = getattr(self, 'parse_' + term)
        return method(string, index)

    # = opt_space ( statement opt_space )*
    def parse_program(self, string, index):
        this_parse = self.__parse(string, "opt_space", index)
        parent = parse.StatementParse("sequence", this_parse.index)
        while this_parse != Parser.FAIL:
            this_parse = self.__parse(string, "statement", this_parse.index)
            if this_parse == Parser.FAIL:
                break
            this_parse.index = self.__parse(string, "opt_space", this_parse.index).index
            parent.add_child(this_parse)
        return parent

    # = declaration | assignment | if_else | if | while | print | expression_statement
    def parse_statement(self, string, index):
        for statement in ("declaration_statement", "assignment_statement", "if_else_statement", "if_statement",
                          "while_statement", "return_statement", "print_statement", "expression_statement"):
            parse = self.__parse(string, statement, index)
            if parse != Parser.FAIL:
                return parse
        return Parser.FAIL

    # = "if" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}"
    def parse_if_statement(self, string, index):
        if index + 2 >= len(string) or string[index: index + 2] != 'if':
            return Parser.FAIL
        left = self.__parse(string, "opt_space", index + 2)
        if left.index >= len(string) or string[left.index] != '(':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        left = self.__parse(string, "expression", left.index)
        left.index = self.__parse(string, "opt_space", left.index).index
        if left.index >= len(string) or left == Parser.FAIL or string[left.index] != ')':
            return Parser.FAIL
        right = self.__parse(string, "opt_space", left.index + 1)
        if right.index >= len(string) or string[right.index] != '{' :
            return Parser.FAIL
        right.index = self.__parse(string, "opt_space", right.index + 1).index
        right = self.__parse(string, "program", right.index)
        right.index = self.__parse(string, "opt_space", right.index).index
        if right.index >= len(string) or right == Parser.FAIL or string[right.index] != '}':
            return Parser.FAIL
        right.index += 1
        parent = parse.StatementParse("if", right.index)
        parent.add_child(left)
        parent.add_child(right)
        return parent

    # = "if" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}"
    # opt_space "else" opt_space "{" opt_space program opt_space "}"
    def parse_if_else_statement(self, string, index):
        if index + 2 >= len(string) or string[index: index + 2] != 'if':
            return Parser.FAIL
        left = self.__parse(string, "opt_space", index + 2)
        if left.index >= len(string) or string[left.index] != '(':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        left = self.__parse(string, "expression", left.index)
        left.index = self.__parse(string, "opt_space", left.index).index
        if left.index >= len(string) or left == Parser.FAIL or string[left.index] != ')':
            return Parser.FAIL
        right1 = self.__parse(string, "opt_space", left.index + 1)
        if right1.index >= len(string) or string[right1.index] != '{':
            return Parser.FAIL
        right1.index = self.__parse(string, "opt_space", right1.index + 1).index
        right1 = self.__parse(string, "program", right1.index)
        right1.index = self.__parse(string, "opt_space", right1.index).index
        if right1.index >= len(string) or right1 == Parser.FAIL or string[right1.index] != '}':
            return Parser.FAIL
        right1.index = self.__parse(string, "opt_space", right1.index + 1).index
        if right1.index + 4 >= len(string) or string[right1.index:right1.index + 4] != 'else':
            return Parser.FAIL
        right2 = self.__parse(string, "opt_space", right1.index + 4)
        if right2.index >= len(string) or string[right2.index] != '{':
            return Parser.FAIL
        right2.index = self.__parse(string, "opt_space", right2.index + 1).index
        right2 = self.__parse(string, "program", right2.index)
        right2.index = self.__parse(string, "opt_space", right2.index).index
        if right2.index >= len(string) or right2 == Parser.FAIL or string[right2.index] != '}':
            return Parser.FAIL
        right2.index += 1
        parent = parse.StatementParse("ifelse", right2.index)
        parent.add_child(left)
        parent.add_child(right1)
        parent.add_child(right2)
        return parent

    # = "while" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}"
    def parse_while_statement(self, string, index):
        if index + 5 >= len(string) or string[index: index + 5] != 'while':
            return Parser.FAIL
        left = self.__parse(string, "opt_space", index + 5)
        if left.index >= len(string) or string[left.index] != '(':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        left = self.__parse(string, "expression", left.index)
        left.index = self.__parse(string, "opt_space", left.index).index
        if left.index >= len(string):
            return Parser.FAIL
        if left == Parser.FAIL or string[left.index] != ')':
            return Parser.FAIL
        right = self.__parse(string, "opt_space", left.index + 1)
        if right.index >= len(string) or string[right.index] != '{':
            return Parser.FAIL
        right.index = self.__parse(string, "opt_space", right.index + 1).index
        right = self.__parse(string, "program", right.index)
        right.index = self.__parse(string, "opt_space", right.index).index
        if right.index >= len(string) or right == Parser.FAIL or string[right.index] != '}':
            return Parser.FAIL
        right.index += 1
        parent = parse.StatementParse("while", right.index)
        parent.add_child(left)
        parent.add_child(right)
        return parent

    # = "ret" req_space expression opt_space ";"
    def parse_return_statement(self, string, index):
        if index + 3 >= len(string) or string[index : index + 3] != 'ret':
            return Parser.FAIL
        child = self.__parse(string, "req_space", index + 3)
        if child == Parser.FAIL:
            return Parser.FAIL
        child = self.__parse(string, "expression", child.index)
        if child == Parser.FAIL:
            return Parser.FAIL
        child.index = self.__parse(string, "opt_space", child.index).index
        if child.index >= len(string) or string[child.index] != ';':
            return Parser.FAIL
        child.index += 1
        parent = parse.StatementParse("return", child.index)
        parent.add_child(child)
        return parent

    # = "var" req_space identifier opt_space "=" opt_space expression opt_space ";"
    def parse_declaration_statement(self, string, index):
        if index + 3 >= len(string) or string[index:index + 3] != 'var':
            return Parser.FAIL
        parent = parse.StatementParse("declare", index + 3)
        left = self.__parse(string, "req_space", parent.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left = self.__parse(string, "identifier", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        if left.index >= len(string) or string[left.index] != '=':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        right = self.__parse(string, "expression", left.index)
        if right == Parser.FAIL:
            return Parser.FAIL
        right.index = self.__parse(string, "opt_space", right.index).index
        if right.index >= len(string) or string[right.index] != ";":
            return Parser.FAIL
        right.index += 1
        if isinstance(right, parse.StatementParse) and right.children:
            if right.children[0].name == "function" and right.name != "call":
                left = parse.ClosureParse(left.name, left.index)
        parent.add_child(left.children[0])
        parent.add_child(right)
        parent.index = right.index
        return parent

    # = location opt_space "=" opt_space expression opt_space ";"
    def parse_assignment_statement(self, string, index):
        left = self.__parse(string, "location", index)  # lookup x
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        if left.index >= len(string) or string[left.index] != '=':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        right = self.__parse(string, "expression", left.index)
        if right == Parser.FAIL:
            return Parser.FAIL
        right.index = self.__parse(string, "opt_space", right.index).index
        if right.index >= len(string) or string[right.index] != ';':
            return Parser.FAIL
        right.index += 1
        if isinstance(right, parse.StatementParse) and right.name == "function":
            if left.name == 'varloc':
                left.children[0] = parse.ClosureParse(left.children[0].name, left.index)
            else:
                left.children[1] = parse.ClosureParse(left.children[1].name, left.index)
        parent = parse.StatementParse("assign", right.index)
        parent.add_child(left)
        parent.add_child(right)
        return parent

    # = identifier ( "." identifier )*
    def parse_location(self, string, index):
        left = self.__parse(string, "identifier", index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.name = "varloc"
        while left.index < len(string) and left != Parser.FAIL:
            if string[left.index] != '.':
                break
            parent = self.__parse(string, "identifier", left.index + 1)
            if parent != Parser.FAIL:
                parent.name = "memloc"
                right = parent.children[0]
                parent.children[0] = left
                parent.add_child(right)
                parent.index = right.index
                left = parent
        return left

    # = "print" req_space expression opt_space ";"
    def parse_print_statement(self, string, index):
        if index + 5 >= len(string) or string[index:index + 5] != 'print':
            return Parser.FAIL
        this_parse = self.__parse(string, "req_space", index + 5)
        if this_parse == Parser.FAIL:
            return Parser.FAIL
        child = self.__parse(string, "expression", this_parse.index)
        if child == Parser.FAIL or child.index >= len(string) or string[child.index] != ';':
            return Parser.FAIL
        child.index += 1
        parent = parse.StatementParse("print", child.index)
        parent.add_child(child)
        return parent

    # = expression opt_space ";"
    def parse_expression_statement(self, string, index):
        this_parse = self.__parse(string, "expression", index)
        if this_parse == Parser.FAIL:
            return Parser.FAIL
        this_parse.index = self.__parse(string, "opt_space", this_parse.index).index
        if this_parse.index >= len(string) or string[this_parse.index] != ';':
            return Parser.FAIL
        this_parse.index += 1
        return this_parse

    # = or_expression
    def parse_expression(self, string, index):
        return self.__parse(string, "or_expression", index)

    # = and_expression ( opt_space or_operator opt_space and_expression )*
    def parse_or_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "and_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "or_operator", left.index)
            if parent == Parser.FAIL:
                break
            parent.index = self.__parse(string, "opt_space", parent.index).index
            right = self.__parse(string, "and_expression", parent.index)
            if right == Parser.FAIL:
                break
            parent.add_child(left)
            parent.add_child(right)
            if right.index < len(string):
                right.index = self.__parse(string, "opt_space", right.index).index
            parent.index = right.index
            left = parent
        return left

    # = "||"
    def parse_or_operator(self, string, index):
        if index + 2 >= len(string) or string[index:index + 2] != '||':
            return Parser.FAIL
        return parse.StatementParse('||', index + 2)

    # = optional_not_expression (opt_space and_operator opt_space optional_not_expression ) *;
    def parse_and_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "optional_not_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "and_operator", left.index)
            if parent == Parser.FAIL:
                break
            parent.index = self.__parse(string, "opt_space", parent.index).index
            right = self.__parse(string, "optional_not_expression", parent.index)
            if right == Parser.FAIL:
                break
            parent.add_child(left)
            parent.add_child(right)
            if right.index < len(string):
                right.index = self.__parse(string, "opt_space", right.index).index
            parent.index = right.index
            left = parent
        return left

    # = "&&"
    def parse_and_operator(self, string, index):
        if index + 2 >= len(string) or string[index:index + 2] != '&&':
            return Parser.FAIL
        return parse.StatementParse('&&', index + 2)

    # not_expression | comp_expression;
    def parse_optional_not_expression(self, string, index):
        for expression in ("not_expression", "comp_expression"):
            parse = self.__parse(string, expression, index)
            if parse != Parser.FAIL:
                return parse
        return Parser.FAIL

    # = "!" opt_space comp_expression
    def parse_not_expression(self, string, index):
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
    def parse_comp_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "add_sub_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        if left.index < len(string) and left != Parser.FAIL:
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
        return left

    # = "==" | "!=" | "<=" | ">=" | "<" | ">"
    def parse_comp_operator(self, string, index):
        if index + 1 >= len(string):
            return Parser.FAIL
        if index + 2 < len(string) and string[index:index + 2] in ('==', '!=', '<=', '>='):
            return parse.StatementParse(string[index:index + 2], index + 2)
        elif string[index] in ('<', '>'):
            return parse.StatementParse(string[index], index + 1)
        return Parser.FAIL

    # = mul_div_expression (opt_space add_sub_operator opt_space mul_div_expression)*
    def parse_add_sub_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "mul_div_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "add_sub_operator", left.index)
            if parent == Parser.FAIL:
                break
            parent.index = self.__parse(string, "opt_space", parent.index).index
            right = self.__parse(string, "mul_div_expression", parent.index)
            if right == Parser.FAIL:
                break
            parent.add_child(left)
            parent.add_child(right)
            if right.index < len(string):
                right.index = self.__parse(string, "opt_space", right.index).index
            parent.index = right.index
            left = parent
        return left

    # = "+" | "-"
    def parse_add_sub_operator(self, string, index):
        if index >= len(string) or string[index] not in ("+", "-"):
            return Parser.FAIL
        return parse.StatementParse(string[index], index + 1)

    # = call_member_expression ( opt_space mul_div_operator opt_space call_member_expression )*
    def parse_mul_div_expression(self, string, index):
        left = self.__parse(string, "opt_space", index)
        left = self.__parse(string, "call_member_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index).index
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "mul_div_operator", left.index)
            if parent == Parser.FAIL:
                break
            parent.index = self.__parse(string, "opt_space", parent.index).index
            right = self.__parse(string, "call_member_expression", parent.index)
            if right == Parser.FAIL:
                break
            parent.add_child(left)
            parent.add_child(right)
            if right.index < len(string):
                right.index = self.__parse(string, "opt_space", right.index).index
            parent.index = right.index
            left = parent
        return left

    # = "*" | "\"
    def parse_mul_div_operator(self, string, index):
        if index >= len(string) or string[index] not in ("*", "/"):
            return Parser.FAIL
        return parse.StatementParse(string[index], index + 1)

    # = operand ( opt_space call_member )*
    def parse_call_member_expression(self, string, index):
        left = self.__parse(string, "operand", index)
        if left == Parser.FAIL:
            return Parser.FAIL
        while left.index < len(string) and left != Parser.FAIL:
            left.index = self.__parse(string, "opt_space", left.index).index
            parent = self.__parse(string, "call_member", left.index)
            if parent != Parser.FAIL:
                right = parent.children[0]
                parent.children[0] = left
                parent.add_child(right)
                parent.index = right.index
                left = parent
            else:
                break
        return left

    # = function_call | member
    def parse_call_member(self, string, index):
        for call in ("function_call", "member"):
            parse = self.__parse(string, call, index)
            if parse != Parser.FAIL:
                return parse
        return Parser.FAIL

    #  = "." opt_space identifier;
    def parse_member(self, string, index):
        if index == len(string) or string[index] != '.':
            return Parser.FAIL
        child = self.__parse(string, "opt_space", index + 1)
        child = self.__parse(string, "identifier", child.index).children[0]
        if child == Parser.FAIL or child.index >= len(string):
            return Parser.FAIL
        parent = parse.StatementParse("member", child.index)
        parent.add_child(child)
        parent.index = child.index
        return parent

    # = "(" opt_space arguments opt_space ")"
    def parse_function_call(self, string, index):
        if index == len(string) or string[index] != '(':
            return Parser.FAIL
        child = self.__parse(string, "opt_space", index + 1)
        child = self.__parse(string, "arguments", child.index)
        child.index = self.__parse(string, "opt_space", child.index).index
        if child == Parser.FAIL or child.index >= len(string) or string[child.index] != ')':
            return Parser.FAIL
        child.index += 1
        parent = parse.StatementParse("call", child.index)
        parent.add_child(child)
        return parent

    # = ( expression opt_space ( "," opt_space expression opt_space )* )?
    def parse_arguments(self, string, index):
        parent = parse.StatementParse("arguments", index)
        if index >= len(string):
            return Parser.FAIL
        elif string[index] == ')':
            return parent
        child = self.__parse(string, "expression", index)
        if child == Parser.FAIL:
            return Parser.FAIL
        child.index = self.__parse(string, "opt_space", child.index).index
        parent.add_child(child)
        while child.index < len(string):
            if string[child.index] != ',':
                break
            child = self.__parse(string, "expression", child.index + 1)
            if child == Parser.FAIL:
                break
            child.index = self.__parse(string, "opt_space", child.index).index
            parent.add_child(child)
        return parent

    # = parenthesized_expression | function | identifier | integer
    def parse_operand(self, string, index):
        for operand in ("class", "parenthesized_expression", "function", "identifier", "integer"):
            parse = self.__parse(string, operand, index)
            if parse != Parser.FAIL:
                return parse
        return Parser.FAIL

    # = "class" opt_space "{" ( opt_space declaration_statement )* opt_space "}"
    def parse_class(self, string, index):
        if index + 5 >= len(string) or string[index: index + 5] != 'class':
            return Parser.FAIL
        child = self.__parse(string, "opt_space", index + 5)
        if child.index >= len(string) or string[child.index] != '{':
            return Parser.FAIL
        child.index += 1
        parent = parse.StatementParse("class", child.index)
        while child.index < len(string) and child != Parser.FAIL:
            child.index = self.__parse(string, "opt_space", child.index).index
            child = self.__parse(string, "declaration_statement", child.index)
            if child != Parser.FAIL:
                parent.add_child(child)
                parent.index = child.index
        parent.index = self.__parse(string, "opt_space", parent.index).index
        if string[parent.index] != '}':
            return Parser.FAIL
        parent.index += 1
        return parent

    # = "(" opt_space expression opt_space ")"
    def parse_parenthesized_expression(self, string, index):
        if index >= len(string)or string[index] != "(":
            return Parser.FAIL
        parse = self.__parse(string, "opt_space", index + 1)
        parse = self.__parse(string, "expression", parse.index)
        if parse == Parser.FAIL:
            return Parser.FAIL
        parse.index = self.__parse(string, "opt_space", parse.index).index
        if parse.index >= len(string) or string[parse.index] != ")":
            return Parser.FAIL
        parse.index += 1
        return parse

    # = "func" opt_space "(" opt_space parameters opt_space ")" opt_space "{" opt_space program opt_space "}"
    def parse_function(self, string, index):
        if index + 4 >= len(string) or string[index: index + 4] != 'func':
            return Parser.FAIL
        left = self.__parse(string, "opt_space", index + 4)
        if left.index >= len(string) or string[left.index] != '(':
            return Parser.FAIL
        left.index = self.__parse(string, "opt_space", left.index + 1).index
        left = self.__parse(string, "parameters", left.index)
        left.index = self.__parse(string, "opt_space", left.index).index
        if left.index >= len(string) or left == Parser.FAIL or string[left.index] != ')':
            return Parser.FAIL
        right = self.__parse(string, "opt_space", left.index + 1)
        if right.index >= len(string) or string[right.index] != '{':
            return Parser.FAIL
        right.index = self.__parse(string, "opt_space", right.index + 1).index
        right = self.__parse(string, "program", right.index)
        right.index = self.__parse(string, "opt_space", right.index).index
        if right.index >= len(string) or right == Parser.FAIL or string[right.index] != '}':
            return Parser.FAIL
        right.index += 1
        parent = parse.StatementParse("function", right.index)
        parent.add_child(left)  # lookup
        parent.add_child(right) # arguments
        return parent   # call

    # = ( identifier opt_space ( "," opt_space identifier opt_space )* )?
    def parse_parameters(self, string, index):
        parent = parse.StatementParse("parameters", index)
        if index >= len(string):
            return Parser.FAIL
        elif string[index] == ')':
            return parent
        child = self.__parse(string, "identifier", index)
        if child == Parser.FAIL:
            return Parser.FAIL
        child.index = self.__parse(string, "opt_space", child.index).index
        parent.add_child(child.children[0])
        parent.index = child.index
        while child.index < len(string):
            if string[child.index] != ',':
                break
            child.index = self.__parse(string, "opt_space", child.index + 1).index
            child = self.__parse(string, "identifier", child.index)
            if child == Parser.FAIL:
                break
            child.index = self.__parse(string, "opt_space", child.index).index
            parent.add_child(child.children[0])
            parent.index = child.index
        return parent

    # = identifier_first_char ( identifier_char )*
    def parse_identifier(self, string, index):
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
    def parse_identifier_first_char(self, string, index):
        if index >= len(string) or (not string[index].isalpha() and string[index] != '_'):
            return Parser.FAIL
        return parse.IntegerParse(0, index + 1)

    # = ALNUM | "_"
    def parse_identifier_char(self, string, index):
        if index >= len(string) or (not string[index].isalnum() and string[index] != '_'):
            return Parser.FAIL
        return parse.IntegerParse(0, index + 1)

    # = (DIGIT) +
    def parse_integer(self, string, index):
        parsed = ""
        while index < len(string) and string[index].isdigit():
            parsed += string[index]
            if index < len(string):
                index += 1
        if not parsed:
            return Parser.FAIL
        return parse.IntegerParse(int(parsed), index)

    # = (space)*
    def parse_opt_space(self, string, index):
        if index >= len(string):
            return parse.IntegerParse(0, index)
        this_parse = self.__parse(string, "space", index)
        if this_parse == Parser.FAIL:
            return parse.IntegerParse(0, index)
        while this_parse.index < len(string):
            if self.__parse(string, "space", this_parse.index) == Parser.FAIL:
                break
            this_parse = self.__parse(string, "space", this_parse.index)
        return parse.IntegerParse(0, this_parse.index)

    # = (space)+
    def parse_req_space(self, string, index):
        this_parse = self.__parse(string, "space", index)
        if this_parse != Parser.FAIL:
            this_parse = self.__parse(string, "opt_space", this_parse.index)
            return parse.IntegerParse(0, this_parse.index)
        else:
            return Parser.FAIL

    # = comment | BLANK | NEWLINE
    def parse_space(self, string, index):
        if -1 < index < len(string):
            this_parse = self.__parse(string, "comment", index)
            if this_parse != Parser.FAIL:
                return this_parse
            if string[index] in (" ", "\n", "\t"):
                return parse.IntegerParse(0, index + 1)
        return Parser.FAIL

    # = "#" (PRINT) * NEWLINE
    def parse_comment(self, string, index):
        if index >= len(string) or string[index] != "#":
            return Parser.FAIL
        index += 1
        while index < len(string):
            if string[index] == '\n':
                return parse.IntegerParse(0, index + 1)
            index += 1

