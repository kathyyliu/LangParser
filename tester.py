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
        actual = str(my_parser.parse(case[0]))
        expected = case[1]
        assert actual == expected, 'S-expression for "{}"; expected {} but got {}'.format(
            case[0], expected, actual
            )


def test_interpreter(test_cases):
    my_parser = parser.Parser()
    for case in test_cases:
        my_interpreter = interpreter.Interpreter()
        node = my_parser.parse(case[0])
        actual = my_interpreter.execute(node)
        expected = case[1]
        assert actual == expected, 'Interpretation for "{}"; expected {} but got {}'.format(
            case[0], expected, actual
        )


def test():
    tests = []

    ########## parser tests #########

    # math tests
    # tests.append(("3;", "(sequence 3)"))
    # tests.append(("1+2;", "(sequence (+ 1 2))"))
    # tests.append(("1*2;", "(sequence (* 1 2))"))
    # tests.append((" 1 * 2 ;", "(sequence (* 1 2))"))
    # tests.append((" 1 * 2 + 1;", "(sequence (+ (* 1 2) 1))"))
    # tests.append(("2 - 3 * 4;", "(sequence (- 2 (* 3 4)))"))
    # tests.append(("2 - 3 * 4 - 5;", "(sequence (- (- 2 (* 3 4)) 5))"))
    # tests.append(("1 + 2 - 3 * 4 - 5;", "(sequence (- (- (+ 1 2) (* 3 4)) 5))"))
    # tests.append(("( 1 + 2 ) * 4;", "(sequence (* (+ 1 2) 4))"))
    # tests.append(("(( 1 + 2 ) - 3 )* (4 - 5);", "(sequence (* (- (+ 1 2) 3) (- 4 5)))"))
    # print tests
    # tests.append(("print 1;", "(sequence (print 1))"))
    # tests.append(("print 1 + 2;", "(sequence (print (+ 1 2)))"))
    # tests.append(("print 1 * (( 1 + 2 ) - 3 )* (4 - 5);", "(sequence (print (* (* 1 (- (+ 1 2) 3)) (- 4 5))))"))
    # tests.append(("print 1+2+();", "None"))
    # tests.append(("print ( 3 ( 4 ( 5 ) ) );", "None"))
    # variable tests
    # tests.append(("x = 1;", "(sequence (assign (varloc x) 1))"))
    # tests.append(("num1 = 144;", "(sequence (assign (varloc num1) 144))"))
    # tests.append(("var num1 = 144;", "(sequence (declare num1 144))"))
    # tests.append(("x+1;", "(sequence (+ (lookup x) 1))"))
    # tests.append(("x+1; 2;", "(sequence (+ (lookup x) 1) 2)"))
    # tests.append(("var x = 0; x = 1;", "(sequence (declare x 0) (assign (varloc x) 1))"))
    # tests.append(("var x = 0; # comment  \n x = 1;", "(sequence (declare x 0) (assign (varloc x) 1))"))
    # tests.append(("var x = 3*1;\nx = x + 1;", "(sequence (declare x (* 3 1)) (assign (varloc x) (+ (lookup x) 1)))"))
    # tests.append(("var _wh33= 90; print _wh33;", "(sequence (declare _wh33 90) (print (lookup _wh33)))"))
    # tests.append(("print 1+ ();", "None"))
    # tests.append(("var x = 5+5*2;", "(sequence (declare x (+ 5 (* 5 2))))"))
    # branches tests
    # tests.append(("if (1) {print 1;}", "(sequence (if 1 (sequence (print 1))))"))
    # tests.append(("var x = 10; if (2* (1 + 0)) {print x;}", "(sequence (declare x 10) (if (* 2 (+ 1 0)) (sequence (print (lookup x)))))"))
    # tests.append(("if (3-2) {print 10;} else {var num = 1;}\n", "(sequence (ifelse (- 3 2) (sequence (print 10)) (sequence (declare num 1))))"))
    # comparison tests
    # tests.append(("1 == 1;", "(sequence (== 1 1))"))
    # tests.append(("print 1 == 1;", "(sequence (print (== 1 1)))"))
    # tests.append(("var x = 0; if (x != 1) { x = x + 1;} print x;", "(sequence (declare x 0) (if (!= (lookup x) 1) (sequence (assign (varloc x) (+ (lookup x) 1)))) (print (lookup x)))"))
    # tests.append(("print 1 >= 2;", "(sequence (print (>= 1 2)))"))
    # loop tests
    # tests.append(("var x = 1; while (x) {print x; x = 0;}", "(sequence (declare x 1) (while (lookup x) (sequence (print (lookup x)) (assign (varloc x) 0))))"))
    # function tests
    # tests.append(("var myfunc = func() {};", "(sequence (declare myfunc (function (parameters) (sequence))))"))


    # test_parse_tree(tests)

    ############ interpreter tests #############

    # tests.clear()
    # tests.append(("print 1;", "1"))
    # tests.append(("print 1 + 2;", "3"))
    # tests.append(("print 1 * (( 1 + 2 ) - 3 )* (4 - 5);", "0"))
    # variable tests
    # tests.append(("var num1 = 144;", ""))
    # tests.append(("var num1 = 144; print num1;", "144"))
    # tests.append(("var num1 = 144; num1 = 12; print num1;", "12"))
    # tests.append(("print 4/2/0/2;", "runtime error: divide by zero"))
    # tests.append(("b = (3*8) + 14;", "runtime error: undefined variable"))
    # tests.append(("var b = 0 + 0;", ""))
    # tests.append(("# fibonacci\nvar a = 1;                      #1\n"
    #             "var b = a;              #1\n"
    #             "var c = b + a;          #2\n"
    #             "var d = c + b;          #3\n"
    #             "var e = d + c;          #5\n"
    #             "var f = e + d;          #8\n"
    #             "var g = f + e;          #13\n"
    #             "print g;\n", "13\n"))
    # branches tests
    # tests.append(("if (1) {print 1;}", "1\n"))
    # tests.append(("var x = 10; if (2* (1 + 0)) {print x;}", "10\n"))
    # tests.append(("if (2-2) {print 10;} else {var num = 1; print num;} \n", "1\n"))
    # tests.append(("var a = 1; var b = 1; var c = 1 ; var d = 1 ; var e = 1 ; var f = 1 ;  \nif (a ==1 && b == 1 && c ==1 && d ==1  && e ==1 && f ==1){ print 1; }", "1\n"))
    # tests.append(("   if ((10 > 2) == 1){ print 1; }", "1\n"))
    tests.append(("var outer = func() {ret func() {};};\n"
                  "var fn1 = outer();\nvar fn2 = outer();\n"
                  "print fn1 == fn1;\n", "1\n"))

    test_interpreter(tests)
#
                  #
    #"print fn1 == fn2;\n"
#                   "print fn2 == fn2;\n"
#                   "print fn1 != fn2;\n"
#                   "print fn1;\n"
#                   "print !fn1;"

def main():
    test()

if __name__ == '__main__':
    main()
