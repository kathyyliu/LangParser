class Parse:

    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __eq__(self, other):
        return (
                isinstance(other, Parse)
                and self.value == other.value
                and self.index == other.index
        )

    def __str__(self):
        return 'Parse(value={}, index{})'.format(self.value, self.index)


class Parser:
    FAIL = Parse(0, -1)

    def __init__(self):
        pass

    def parse(self, string, term, index=0):
        if index >= len(string):
            return Parser.FAIL
        elif term == "add_sub_expression":
            return self.__parse_add_sub_expression(string, index)
        elif term == "mul_div_expression":
            return self.__parse_mul_div_expression(string, index)
        elif term == "operand":
            return self.__parse_operand(string, index)
        elif term == "parentheses":
            return self.__parse_parentheses(string, index)
        elif term == "integer":
            return self.__parse_integer(string, index)
        elif term == "opt_space":
            return self.__parse_opt_space(string, index)
        else:
            raise AssertionError("Unexpected term", term)

    def __parse_add_sub_expression(self, string, index):
        parse = self.parse(string, "opt_space", index)
        parse = self.parse(string, "mul_div_expression", parse.index)
        if parse == Parser.FAIL:
            return Parser.FAIL
        result = parse.value
        index = parse.index
        while parse.index < len(string) and parse != Parser.FAIL:
            parse = self.parse(string, "opt_space", parse.index)
            if string[parse.index] == "+":
                add = True
            elif string[parse.index] == "-":
                add = False
            else:
                break
            parse = self.parse(string, "opt_space", parse.index + 1)
            parse = self.parse(string, "mul_div_expression", parse.index)
            if parse != Parser.FAIL:
                if add:
                    result += parse.value
                elif not add:
                    result -= parse.value
                if parse.index < len(string):
                    parse = self.parse(string, "opt_space", parse.index)
                index = parse.index
        return Parse(result, index)

    def __parse_mul_div_expression(self, string, index):
        parse = self.parse(string, "opt_space", index)
        parse = self.parse(string, "operand", parse.index)
        if parse == Parser.FAIL:
            return Parser.FAIL
        result = parse.value
        index = parse.index
        while parse.index < len(string) and parse != Parser.FAIL:
            parse = self.parse(string, "opt_space", parse.index)
            if string[parse.index] == "*":
                mul = True
            elif string[parse.index] == "/":
                mul = False
            else:
                break
            parse = self.parse(string, "opt_space", parse.index + 1)
            parse = self.parse(string, "operand", parse.index)
            if parse != Parser.FAIL:
                if mul:
                    result *= parse.value
                else:
                    result //= parse.value
                if parse.index < len(string):
                    parse = self.parse(string, "opt_space", parse.index)
                index = parse.index
        return Parse(result, index)

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
        if string[parse.index] != ")":
            return Parser.FAIL
        return Parse(parse.value, parse.index + 1)

    def __parse_integer(self, string, index):
        parsed = ""
        while index < len(string) and string[index].isdigit():
            parsed += string[index]
            if index < len(string):
                index += 1
        if not parsed:
            return Parser.FAIL
        return Parse(int(parsed), index)

    def __parse_opt_space(self, string, index):
        while index < len(string) and string[index] == " ":
            index += 1
        return Parse(0, index)


def test_parse(parser, string, term, expected):
    actual = parser.parse(string, term)
    assert actual is not None, 'Got None when parsing "{}"'.format(string)
    assert actual == expected, 'Parsing "{}"; expected {} but got {}'.format(
        string, expected, actual
    )


def test():
    parser = Parser()
    # integer tests
    test_parse(parser, "3", "integer", Parse(3, 1))
    test_parse(parser, "0", "integer", Parse(0, 1))  # at index 1, value is 0
    test_parse(parser, "100", "integer", Parse(100, 3))  # 3 dif characters, value is 100
    test_parse(parser, "2021", "integer", Parse(2021, 4))
    test_parse(parser, "b", "integer", Parser.FAIL)
    test_parse(parser, "", "integer", Parser.FAIL)
    # addition tests
    test_parse(parser, "b", "add_sub_expression", Parser.FAIL)
    test_parse(parser, "", "add_sub_expression", Parser.FAIL)
    test_parse(parser, "3-", "add_sub_expression", Parse(3, 1))  # when only one int, still valid add
    test_parse(parser, "3++", "add_sub_expression", Parse(3, 1))
    test_parse(parser, "3+4", "add_sub_expression", Parse(7, 3))
    test_parse(parser, "2020+2021", "add_sub_expression", Parse(4041, 9))
    test_parse(parser, "0+0", "add_sub_expression", Parse(0, 3))
    test_parse(parser, "1+1-", "add_sub_expression", Parse(2, 3))
    test_parse(parser, "1+1+-", "add_sub_expression", Parse(2, 3))
    test_parse(parser, "0+0+0+0+0", "add_sub_expression", Parse(0, 9))
    test_parse(parser, "42+0", "add_sub_expression", Parse(42, 4))
    test_parse(parser, "0+42", "add_sub_expression", Parse(42, 4))
    test_parse(parser, "123+234+345", "add_sub_expression", Parse(702, 11))
    # parentheses tests
    test_parse(parser, "(0)", "parentheses", Parse(0, 3))
    test_parse(parser, "(0+0)", "parentheses", Parse(0, 5))
    test_parse(parser, "(1+2)", "parentheses", Parse(3, 5))
    test_parse(parser, "(1+2+3)", "parentheses", Parse(6, 7))
    test_parse(parser, "4+(1+2+3)", "add_sub_expression", Parse(10, 9))
    test_parse(parser, "(1+2+3)+5", "add_sub_expression", Parse(11, 9))
    test_parse(parser, "4+(1+2+3)+5", "add_sub_expression", Parse(15, 11))
    test_parse(parser, "3+4+(5+6)+9", "add_sub_expression", Parse(27, 11))
    # end-to-end test
    test_parse(parser, "(3+4)+((2+3)+0+(1+2+3))+9", "add_sub_expression", Parse(27, 25))
    test_parse(parser, "1+1+b", "add_sub_expression", Parse(2, 3))
    # spaces tests
    test_parse(parser, "3 + 1", "add_sub_expression", Parse(4, 5))
    test_parse(parser, "( 3+1 )", "parentheses", Parse(4, 7))
    test_parse(parser, "( 3+1 ) ", "parentheses", Parse(4, 7))  # should actually be 8
    test_parse(parser, "( 1 + 2 + 3 )", "parentheses", Parse(6, 13))
    test_parse(parser, "4+(1 + 2 +3 )+ 5", "add_sub_expression", Parse(15, 16))
    # subtraction tests
    test_parse(parser, "", "add_sub_expression", Parser.FAIL)
    test_parse(parser, "3-", "add_sub_expression", Parse(3, 1))
    test_parse(parser, "4-3", "add_sub_expression", Parse(1, 3))
    test_parse(parser, "3-3", "add_sub_expression", Parse(0, 3))
    test_parse(parser, "3-0", "add_sub_expression", Parse(3, 3))
    test_parse(parser, "0-3", "add_sub_expression", Parse(-3, 3))
    test_parse(parser, "0-0-0-0", "add_sub_expression", Parse(0, 7))
    test_parse(parser, "100-56-4", "add_sub_expression", Parse(40, 8))
    # end-to-end tests
    test_parse(parser, "(3+4)-((2+3)+0-(1-2+3))+9", "add_sub_expression", Parse(13, 25))
    test_parse(parser, "( 3+ 4) - ( (2+3)+0 -(1 - 2+3))+ 9", "add_sub_expression", Parse(13, 34))
    # multiplication tests
    test_parse(parser, "", "mul_div_expression", Parser.FAIL)
    test_parse(parser, "3*", "mul_div_expression", Parse(3, 1))
    test_parse(parser, "3*4", "mul_div_expression", Parse(12, 3))
    test_parse(parser, "3*4 * 5*0", "mul_div_expression", Parse(0, 9))
    test_parse(parser, "12 * 25 * 1", "mul_div_expression", Parse(300, 11))
    # division tests
    test_parse(parser, "", "mul_div_expression", Parser.FAIL)
    test_parse(parser, "3/", "mul_div_expression", Parse(3, 1))
    test_parse(parser, "22/5", "mul_div_expression", Parse(4, 4))
    test_parse(parser, "2/2", "mul_div_expression", Parse(1, 3))
    test_parse(parser, "3 / 5", "mul_div_expression", Parse(0, 5))
    test_parse(parser, "3/1/5/1", "mul_div_expression", Parse(0, 7))
    test_parse(parser, "12 / 3/2", "mul_div_expression", Parse(2, 8))
    # mixed expression tests
    test_parse(parser, "3+4*2", "add_sub_expression", Parse(11, 5))
    test_parse(parser, "(3+4 ) * 2", "add_sub_expression", Parse(14, 10))
    test_parse(parser, "1-5/2", "add_sub_expression", Parse(-1, 5))
    test_parse(parser, "(1 -5)/ 2", "add_sub_expression", Parse(-2, 9))
    test_parse(parser, "3+4*2+1-5/2", "add_sub_expression", Parse(10, 11))
    test_parse(parser, "( (3+4 )* 2+ 1-5 )/ 2 +1", "add_sub_expression", Parse(6, 24))
    test_parse(parser, "(19- (5+ 2 *0) / 9+ (3/1))", "parentheses", Parse(22, 26))
    test_parse(parser, "11 / (8/ 4*(7-5))", "mul_div_expression", Parse(2, 17))


def main():
    test()


if __name__ == '__main__':
    main()
