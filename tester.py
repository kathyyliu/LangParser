import parser as parser
import interpreter as interpreter

def test_parse(parser, string, term, expected):
    actual = parser.parse(string, term)
    assert actual is not None, 'Got None when parsing "{}"'.format(string)
    assert actual == expected, 'Parsing "{}"; expected {} but got {}'.format(
        string, expected, actual
    )


def test_parse_tree(test_cases):
    my_parser = parser.Parser()
    for case in test_cases:
        actual = str(my_parser.parse(case[0], "program"))
        expected = case[1]
        assert actual == expected, 'S-expression for "{}"; expected {} but got {}'.format(
            case[0], expected, actual
            )


def test_interpreter(test_cases):
    my_parser = parser.Parser()
    my_interpreter = interpreter.Interpreter()
    for case in test_cases:
        my_interpreter.output = ''
        node = my_parser.parse(case[0], "program")
        actual = my_interpreter.execute(node)
        expected = case[1]
        assert actual is not None, 'Got None when interpreting "{}"'.format(case[0])
        assert actual == expected, 'Interpretation for "{}"; expected {} but got {}'.format(
            case[0], expected, actual
        )


def test():
    tests = []

    ########## parser tests #########

    # math tests
    tests.append(("3;", "(sequence 3)"))
    tests.append(("1+2;", "(sequence (+ 1 2))"))
    tests.append(("1*2;", "(sequence (* 1 2))"))
    tests.append((" 1 * 2 ;", "(sequence (* 1 2))"))
    tests.append((" 1 * 2 + 1;", "(sequence (+ (* 1 2) 1))"))
    tests.append(("2 - 3 * 4;", "(sequence (- 2 (* 3 4)))"))
    tests.append(("2 - 3 * 4 - 5;", "(sequence (- (- 2 (* 3 4)) 5))"))
    tests.append(("1 + 2 - 3 * 4 - 5;", "(sequence (- (- (+ 1 2) (* 3 4)) 5))"))
    tests.append(("( 1 + 2 ) * 4;", "(sequence (* (+ 1 2) 4))"))
    tests.append(("(( 1 + 2 ) - 3 )* (4 - 5);", "(sequence (* (- (+ 1 2) 3) (- 4 5)))"))
    # print tests
    tests.append(("print 1;", "(sequence (print 1))"))
    tests.append(("print 1 + 2;", "(sequence (print (+ 1 2)))"))
    tests.append(("print 1 * (( 1 + 2 ) - 3 )* (4 - 5);", "(sequence (print (* (* 1 (- (+ 1 2) 3)) (- 4 5))))"))
    # variable tests
    tests.append(("x = 1;", "(sequence (assign (varloc x) 1))"))
    tests.append(("num1 = 144;", "(sequence (assign (varloc num1) 144))"))
    tests.append(("var num1 = 144;", "(sequence (declare num1 144))"))
    tests.append(("x+1;", "(sequence (+ (lookup x) 1))"))
    tests.append(("x+1; 2;", "(sequence (+ (lookup x) 1) 2)"))
    tests.append(("var x = 0; x = 1;", "(sequence (declare x 0) (assign (varloc x) 1))"))
    tests.append(("var x = 0; # comment  \n x = 1;", "(sequence (declare x 0) (assign (varloc x) 1))"))
    tests.append(("var x = 3*1;\nx = x + 1;", "(sequence (declare x (* 3 1)) (assign (varloc x) (+ (lookup x) 1)))"))
    tests.append(("var _wh33= 90; print _wh33;", "(sequence (declare _wh33 90) (print (lookup _wh33)))"))


    test_parse_tree(tests)

    ############ interpreter tests #############

    # tests.append(("print 1;", "1"))
    # tests.append(("print 1 + 2;", "3"))
    # tests.append(("print 1 * (( 1 + 2 ) - 3 )* (4 - 5);", "0"))

    # test_interpreter(tests)



#     parser = Parser()
#     # integer tests
#     test_parse(parser, "3", "integer", Parse(3, 1))
#     test_parse(parser, "0", "integer", Parse(0, 1))  # at index 1, value is 0
#     test_parse(parser, "100", "integer", Parse(100, 3))  # 3 dif characters, value is 100
#     test_parse(parser, "2021", "integer", Parse(2021, 4))
#     test_parse(parser, "b", "integer", Parser.FAIL)
#     test_parse(parser, "", "integer", Parser.FAIL)
#     # addition tests
#     test_parse(parser, "b", "add_sub_expression", Parser.FAIL)
#     test_parse(parser, "", "add_sub_expression", Parser.FAIL)
#     test_parse(parser, "3-", "add_sub_expression", Parse(3, 1))  # when only one int, still valid add
#     test_parse(parser, "3++", "add_sub_expression", Parse(3, 1))
#     test_parse(parser, "3+4", "add_sub_expression", Parse(7, 3))
#     test_parse(parser, "2020+2021", "add_sub_expression", Parse(4041, 9))
#     test_parse(parser, "0+0", "add_sub_expression", Parse(0, 3))
#     test_parse(parser, "1+1-", "add_sub_expression", Parse(2, 3))
#     test_parse(parser, "1+1+-", "add_sub_expression", Parse(2, 3))
#     test_parse(parser, "0+0+0+0+0", "add_sub_expression", Parse(0, 9))
#     test_parse(parser, "42+0", "add_sub_expression", Parse(42, 4))
#     test_parse(parser, "0+42", "add_sub_expression", Parse(42, 4))
#     test_parse(parser, "123+234+345", "add_sub_expression", Parse(702, 11))
#     # parentheses tests
#     test_parse(parser, "(0)", "parentheses", Parse(0, 3))
#     test_parse(parser, "(0+0)", "parentheses", Parse(0, 5))
#     test_parse(parser, "(1+2)", "parentheses", Parse(3, 5))
#     test_parse(parser, "(1+2+3)", "parentheses", Parse(6, 7))
#     test_parse(parser, "4+(1+2+3)", "add_sub_expression", Parse(10, 9))
#     test_parse(parser, "(1+2+3)+5", "add_sub_expression", Parse(11, 9))
#     test_parse(parser, "4+(1+2+3)+5", "add_sub_expression", Parse(15, 11))
#     test_parse(parser, "3+4+(5+6)+9", "add_sub_expression", Parse(27, 11))
#     # end-to-end test
#     test_parse(parser, "(3+4)+((2+3)+0+(1+2+3))+9", "add_sub_expression", Parse(27, 25))
#     test_parse(parser, "1+1+b", "add_sub_expression", Parse(2, 3))
#     # spaces tests
#     test_parse(parser, "3 + 1", "add_sub_expression", Parse(4, 5))
#     test_parse(parser, "( 3+1 )", "parentheses", Parse(4, 7))
#     test_parse(parser, "( 3+1 ) ", "parentheses", Parse(4, 7))  # should actually be 8
#     test_parse(parser, "( 1 + 2 + 3 )", "parentheses", Parse(6, 13))
#     test_parse(parser, "4+(1 + 2 +3 )+ 5", "add_sub_expression", Parse(15, 16))
#     # subtraction tests
#     test_parse(parser, "", "add_sub_expression", Parser.FAIL)
#     test_parse(parser, "3-", "add_sub_expression", Parse(3, 1))
#     test_parse(parser, "4-3", "add_sub_expression", Parse(1, 3))
#     test_parse(parser, "3-3", "add_sub_expression", Parse(0, 3))
#     test_parse(parser, "3-0", "add_sub_expression", Parse(3, 3))
#     test_parse(parser, "0-3", "add_sub_expression", Parse(-3, 3))
#     test_parse(parser, "0-0-0-0", "add_sub_expression", Parse(0, 7))
#     test_parse(parser, "100-56-4", "add_sub_expression", Parse(40, 8))
#     # end-to-end tests
#     test_parse(parser, "(3+4)-((2+3)+0-(1-2+3))+9", "add_sub_expression", Parse(13, 25))
#     test_parse(parser, "( 3+ 4) - ( (2+3)+0 -(1 - 2+3))+ 9", "add_sub_expression", Parse(13, 34))
#     # multiplication tests
#     test_parse(parser, "", "mul_div_expression", Parser.FAIL)
#     test_parse(parser, "3*", "mul_div_expression", Parse(3, 1))
#     test_parse(parser, "3*4", "mul_div_expression", Parse(12, 3))
#     test_parse(parser, "3*4 * 5*0", "mul_div_expression", Parse(0, 9))
#     test_parse(parser, "12 * 25 * 1", "mul_div_expression", Parse(300, 11))
#     # division tests
#     test_parse(parser, "", "mul_div_expression", Parser.FAIL)
#     test_parse(parser, "3/", "mul_div_expression", Parse(3, 1))
#     test_parse(parser, "22/5", "mul_div_expression", Parse(4, 4))
#     test_parse(parser, "2/2", "mul_div_expression", Parse(1, 3))
#     test_parse(parser, "3 / 5", "mul_div_expression", Parse(0, 5))
#     test_parse(parser, "3/1/5/1", "mul_div_expression", Parse(0, 7))
#     test_parse(parser, "12 / 3/2", "mul_div_expression", Parse(2, 8))
#     # mixed expression tests
#     test_parse(parser, "3+4*2", "add_sub_expression", Parse(11, 5))
#     test_parse(parser, "(3+4 ) * 2", "add_sub_expression", Parse(14, 10))
#     test_parse(parser, "1-5/2", "add_sub_expression", Parse(-1, 5))
#     test_parse(parser, "(1 -5)/ 2", "add_sub_expression", Parse(-2, 9))
#     test_parse(parser, "3+4*2+1-5/2", "add_sub_expression", Parse(10, 11))
#     test_parse(parser, "( (3+4 )* 2+ 1-5 )/ 2 +1", "add_sub_expression", Parse(6, 24))
#     test_parse(parser, "(19- (5+ 2 *0) / 9+ (3/1))", "parentheses", Parse(22, 26))
#     test_parse(parser, "11 / (8/ 4*(7-5))", "mul_div_expression", Parse(2, 17))
#
#     test_parse(parser, "print 1;", "print_statement", parse.StatementParse("print", 6))
#     test_parse(parser, "print 1;", "statement", parse.StatementParse("print", 6))
#     test_parse(parser, "# comment", "comment", parse.StatementParse("comment", 9))
#


def main():
    test()

if __name__ == '__main__':
    main()
