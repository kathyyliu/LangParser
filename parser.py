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
        # elif term == "space":
            # return self.__parse_opt_space(string, index)
        elif term == "integer":
            return self.__parse_integer(string, index)
        elif term == "addition":
            return self.__parse_addition_expression(string, index)
        elif term == "operand":
            return self.__parse_operand(string, index)
        elif term == "parentheses":
            return self.__parse_parentheses(string, index)
        else:
            raise AssertionError("Unexpected term", term)

    def __parse_opt_space(self, string, index):
        skipped = index
        while skipped < len(string) and string[skipped] == " ":
            skipped += 1
        return skipped

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
        parse = self.parse(string, "addition", index + 1)
        if parse == Parser.FAIL:
            return Parser.FAIL
        if string[parse.index] != ")":
            return Parser.FAIL
        return Parse(parse.value, parse.index + 1)

    def __parse_addition_expression(self, string, index):
        index = self.__parse_opt_space(string, index)
        parse = self.parse(string, "operand", index)  # (paren before) int before + sign
        if parse == Parser.FAIL:
            return Parser.FAIL
        result = parse.value
        while index < len(string) and parse != Parser.FAIL:  # only parses + signs followed by an int
            parse = Parse(parse.value, self.__parse_opt_space(string, parse.index))
            index = parse.index
            if string[parse.index] != "+":
                break
            parse = Parse(parse.value, self.__parse_opt_space(string, index + 1))
            parse = self.parse(string, "operand", parse.index)  # find int or paren after + sign
            if parse != Parser.FAIL:
                result += parse.value
                index = parse.index
            parse = Parse(parse.value, self.__parse_opt_space(string, parse.index))
        return Parse(result, index)

    def __parse_integer(self, string, index):
        parsed = ""
        while index < len(string) and string[index].isdigit():
            parsed += string[index]
            if index < len(string):
                index += 1
        if not parsed:
            return Parser.FAIL
        return Parse(int(parsed), index)


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
    test_parse(parser, "b", "addition", Parser.FAIL)
    test_parse(parser, "", "addition", Parser.FAIL)
    test_parse(parser, "3-", "addition", Parse(3, 1))  # when only one int, still valid add
    test_parse(parser, "3++", "addition", Parse(3, 1))
    test_parse(parser, "3+4", "addition", Parse(7, 3))
    test_parse(parser, "2020+2021", "addition", Parse(4041, 9))
    test_parse(parser, "0+0", "addition", Parse(0, 3))
    test_parse(parser, "1+1-", "addition", Parse(2, 3))
    test_parse(parser, "1+1+-", "addition", Parse(2, 3))
    test_parse(parser, "0+0+0+0+0", "addition", Parse(0, 9))
    test_parse(parser, "42+0", "addition", Parse(42, 4))
    test_parse(parser, "0+42", "addition", Parse(42, 4))
    test_parse(parser, "123+234+345", "addition", Parse(702, 11))
    # parentheses tests
    test_parse(parser, "(0)", "parentheses", Parse(0, 3))
    test_parse(parser, "(0+0)", "parentheses", Parse(0, 5))
    test_parse(parser, "(1+2)", "parentheses", Parse(3, 5))
    test_parse(parser, "(1+2+3)", "parentheses", Parse(6, 7))
    test_parse(parser, "4+(1+2+3)", "addition", Parse(10, 9))
    test_parse(parser, "(1+2+3)+5", "addition", Parse(11, 9))
    test_parse(parser, "4+(1+2+3)+5", "addition", Parse(15, 11))
    test_parse(parser, "3+4+(5+6)+9", "addition", Parse(27, 11))
    # end-to-end test
    test_parse(parser, "(3+4)+((2+3)+0+(1+2+3))+9", "addition", Parse(27, 25))
    test_parse(parser, "1+1+b", "addition", Parse(2, 3))
    # spaces tests
    test_parse(parser, "3 + 1", "addition", Parse(4, 5))
    test_parse(parser, "( 3+1 )", "parentheses", Parse(4, 7))
    test_parse(parser, "( 3+1 ) ", "parentheses", Parse(4, 7))
    test_parse(parser, "( 1 + 2 + 3 )", "parentheses", Parse(6, 13))
    test_parse(parser, "4+(1 + 2 +3 )+ 5", "addition", Parse(15, 16))


def main():
    test()


if __name__ == '__main__':
    main()
