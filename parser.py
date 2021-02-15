import parse as parse


class Parser:
    FAIL = parse.StatementParse("FAIL", -1)

    def __init__(self):
        pass

    def parse(self, string, term, index=0):
        if index > len(string):
            return Parser.FAIL
        elif term == "program":
            return self.__parse_program(string, index)
        elif term == "statement":
            return self.__parse_statement(string, index)
        elif term == "print_statement":
            return self.__parse_print_statement(string, index)
        elif term == "expression":
            return self.__parse_expression(string, index)
        elif term == "add_sub_expression":
            return self.__parse_add_sub_expression(string, index)
        elif term == "add_sub_operator":
            return self.__parse_add_sub_operator(string, index)
        elif term == "mul_div_expression":
            return self.__parse_mul_div_expression(string, index)
        elif term == "mul_div_operator":
            return self.__parse_mul_div_operator(string, index)
        elif term == "operand":
            return self.__parse_operand(string, index)
        elif term == "parentheses":
            return self.__parse_parentheses(string, index)
        elif term == "integer":
            return self.__parse_integer(string, index)
        elif term == "opt_space":
            return self.__parse_opt_space(string, index)
        elif term == "req_space":
            return self.__parse_req_space(string, index)
        elif term == "space":
            return self.__parse_space(string, index)
        elif term == "comment":
            return self.__parse_comment(string, index)
        else:
            raise ValueError("invalid term")

    # = opt_space ( statement opt_space )*
    def __parse_program(self, string, index):
        this_parse = self.parse(string, "opt_space", index)
        curr_index = this_parse.index
        while curr_index < len(string) and this_parse != Parser.FAIL:
            this_parse = self.parse(string, "statement", curr_index)
            curr_index = self.__get_last_descendant(this_parse).index
            if curr_index < len(string) and this_parse != Parser.FAIL:
                curr_index = self.parse(string, "opt_space", curr_index).index
                self.__get_last_descendant(this_parse).index = curr_index
        # did not parse whole program
        if curr_index < len(string):
            return None
        return this_parse

    # = print_statement | expression
    def __parse_statement(self, string, index):
        parse = self.parse(string, "print_statement", index)
        if parse != Parser.FAIL:
            return parse
        parse = self.parse(string, "expression", index)
        if parse != Parser.FAIL:
            return parse
        else:
            return Parser.FAIL

    # = "print" req_space expression opt_space ";"
    def __parse_print_statement(self, string, index):
        for i in range(5):
            if string[index + i] != "print"[i]:
                return Parser.FAIL
        parent = parse.StatementParse("print", index + 5)
        parent.index = self.parse(string, "req_space", parent.index).index
        child = self.parse(string, "expression", parent.index)
        if child == Parser.FAIL:
            return Parser.FAIL
        if string[self.__get_last_descendant(child).index] != ";":
            raise SyntaxError
        self.__get_last_descendant(child).index += 1
        parent.add_child(child)
        return parent

    # = add_sub_expression
    def __parse_expression(self, string, index):
       return self.parse(string, "add_sub_expression", index)

    # = mul_div_expression (opt_space add_sub_operator opt_space mul_div_expression)*
    def __parse_add_sub_expression(self, string, index):
        left = self.parse(string, "opt_space", index)
        left = self.parse(string, "mul_div_expression", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        # sets index to right-most child if available
        left.index = self.parse(string, "opt_space", self.__get_last_descendant(left).index).index
        curr_index = left.index
        while curr_index < len(string) and left != Parser.FAIL:
            curr_index = self.parse(string, "opt_space", curr_index).index
            parent = self.parse(string, "add_sub_operator", curr_index)
            if parent != Parser.FAIL:
                parent.index = self.parse(string, "opt_space", parent.index).index
                right = self.parse(string, "mul_div_expression", parent.index)
                if right != Parser.FAIL:
                    parent.add_child(left)
                    parent.add_child(right)
                    left = parent
                    if right.index < len(string):
                        right.index = self.parse(string, "opt_space", self.__get_last_descendant(right).index).index
                    curr_index = right.index
            else:
                break
        return left

    # = "+" | "-"
    def __parse_add_sub_operator(self, string, index):
        if index < len(string):
            if string[index] in ("+", "-"):
                return parse.StatementParse(string[index], index + 1)
        return Parser.FAIL

    # = operand ( opt_space mul_div_operator opt_space operand )*
    def __parse_mul_div_expression(self, string, index):
        left = self.parse(string, "opt_space", index)
        left = self.parse(string, "operand", left.index)
        if left == Parser.FAIL:
            return Parser.FAIL
        # sets index to right-most child if available
        left.index = self.parse(string, "opt_space", self.__get_last_descendant(left).index).index
        curr_index = left.index
        while curr_index < len(string) and left != Parser.FAIL:
            curr_index = self.parse(string, "opt_space", curr_index).index
            parent = self.parse(string, "mul_div_operator", curr_index)
            if parent != Parser.FAIL:
                curr_index = self.parse(string, "opt_space", parent.index).index
                right = self.parse(string, "operand", curr_index)
                if right != Parser.FAIL:
                    parent.add_child(left)
                    parent.add_child(right)
                    left = parent
                    if right.index < len(string):
                        right.index = self.parse(string, "opt_space", self.__get_last_descendant(right).index).index
                    curr_index = right.index
            else:
                break
        return left

    def __parse_mul_div_operator(self, string, index):
        if index < len(string):
            if string[index] in ("*", "/"):
                return parse.StatementParse(string[index], index + 1)
        return Parser.FAIL

    def __parse_operand(self, string, index):
        parse = self.parse(string, "integer", index)
        if parse != Parser.FAIL:
            return parse
        parse = self.parse(string, "parentheses", index)
        if parse != Parser.FAIL:
            return parse
        return Parser.FAIL

    def __parse_parentheses(self, string, index):
        if string[index] != "(":
            return Parser.FAIL
        parse = self.parse(string, "add_sub_expression", index + 1)
        if parse == Parser.FAIL:
            return Parser.FAIL
        last = self.__get_last_descendant(parse)
        last.index = self.parse(string, "opt_space", last.index).index
        if string[last.index] != ")":
            return Parser.FAIL
        last.index += 1
        parse.index = last.index
        return parse

    def __parse_integer(self, string, index):
        parsed = ""
        while index < len(string) and string[index].isdigit():
            parsed += string[index]
            if index < len(string):
                index += 1
        if not parsed:
            return Parser.FAIL
        return parse.IntegerParse(int(parsed), index)

    def __parse_opt_space(self, string, index):
        this_parse = self.parse(string, "space", index)
        if this_parse != Parser.FAIL:
            while this_parse.index < len(string):
                # prevent this_parse from actually becoming Parser.FAIL
                if self.parse(string, "space", this_parse.index) == Parser.FAIL:
                    break
                this_parse = self.parse(string, "space", this_parse.index)
            return parse.IntegerParse(0, this_parse.index)
        else:
            return parse.IntegerParse(0, index)

    def __parse_req_space(self, string, index):
        this_parse = self.parse(string, "space", index)
        if this_parse != Parser.FAIL:
            while this_parse.index < len(string):
                # prevent this_parse from actually becoming Parser.FAIL
                if self.parse(string, "space", this_parse.index) == Parser.FAIL:
                    break
                this_parse = self.parse(string, "space", this_parse.index)
            return parse.IntegerParse(0, this_parse.index)
        else:
            raise SyntaxError

    def __parse_space(self, string, index):
        if index < len(string):
            this_parse = self.parse(string, "comment", index)
            if this_parse != Parser.FAIL:
                return this_parse
            if string[index] in (" ", "\n"):
                return parse.IntegerParse(0, index + 1)
        return Parser.FAIL

    # = "#" (PRINT) * NEWLINE;
    def __parse_comment(self, string, index):
        if string[index] == "#":
            index += 1
            while index < len(string):
                if string[index] == '\n':
                    return parse.StatementParse("comment", index + 1)
                index += 1
        return Parser.FAIL

    # returns right-most descendant of node, returns itself if no children
    def __get_last_descendant(self, node):
            last = node
            while isinstance(last, parse.StatementParse):
                if last.children:
                    last = last.children[-1]
                else:
                    break
            return last

