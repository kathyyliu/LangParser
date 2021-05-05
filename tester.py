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
    tests.append(("var func1 = func(){var func2 = func(){"
                  "var func3 = func(){print 4;};ret func3;};ret func2;};"
                  "func1()()();", "(sequence (declare myfunc (function (parameters) (sequence))))"))


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
    # tests.append(("print 1-2-3 + 10/5/2;", "-3\n"))
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
    # tests.append(("var x = func() {}; x+1;", "runtime error: math operation on functions"))
    # functions tests
    # tests.append(("var myfunc = func() {print 1;}; myfunc();", "1\n"))
    # tests.append(("var run_first = func() { print 42;};"
    #               "nonexistant = run_first();", "42\nruntime error: undefined variable"))
    # tests.append(("var outer = func() {ret func() {};};\n"
    #               "var fn1 = outer();\nvar fn2 = outer();\n"
    #               "print fn1 == fn1;\n", "1\n"))
    # tests.append(("var pair = func(first, second) {ret func(f) {ret f(first, second);};}; "
    #               "var NULL = pair(0, 0);"
    #               "var first = func(pair) {ret pair(func(first, second) {ret first;});}; "
    #               "var second = func(pair) {ret pair(func(first, second) {ret second;});}; "
    #               "var range = func(start, end) {var _range = func(start, end, partial) {"
    #               "if (start == end) {ret partial;} "
    #               "else {ret _range(start, end - 1, pair(end - 1, partial));}}; "
    #               "ret _range(start, end, NULL);};"
    #               "var filter = func(list, fn) {var _filter = func(list, fn, result) {"
    #               "if (list == NULL) {ret result;} else {"
    #               "if (fn(first(list)) == 1) {ret _filter(second(list), fn, pair(first(list), result));} "
    #               "else {ret _filter(second(list), fn, result);}}}; "
    #               "ret _filter(list, fn, NULL);};"
    #               "var reduce = func(list, fn, result) {"
    #               "if (list == NULL) {ret result;} else {ret reduce(second(list), fn, fn(result, first(list)));}}; "
    #               "var mod = func(a, b) {ret a - (b * (a / b));};"
    #               "var euler1 = func(n) {ret reduce(filter(range(0, n),"
    #               "func(n) {if (mod(n, 3) == 0 || mod(n, 5) == 0) {ret 1;} else {ret 0;}}),"
    #               "func(a, b) {ret a + b;},0);}; "
    #               "print euler1(20);", "78\n"))
    # tests.append(("var pair = func(first, second) {ret func(f) {ret f(first, second);};}; "
    #               "var NULL = pair(0, 0);"
    #               "var first = func(pair) {ret pair(func(first, second) {ret first;});}; "
    #               "var second = func(pair) {ret pair(func(first, second) {ret second;});}; "
    #               "var euler1 = func(n) { var x = pair(1, n); ret second(x);}; "
    #               "print euler1(20);", "20\n"))
    # tests.append(("var mod = func(a, b) {ret a - (b * (a / b));};"
    #                     "var euler1 = func(n) {"
    #                     "ret mod(20, n); }; "
    #                     "print euler1(2);", "0\n"))
    # tests.append(("var pair = func(first, second) {"
    #               "ret func(f) {"
    #               "ret f(first, second);};};"
    #               "var NULL = func(first, second) {"
    #               "ret 1;};"
    #               "var range = func(start, end) {"
    #               "var _range = func(start, end, partial) {"
    #               "if (start == end) {"
    #               "ret partial;"
    #               "} else {"
    #               "ret _range(start, end - 1, pair(end - 1, partial)); }};"
    #               "ret _range(start, end, NULL);};"
    #               "print range(1, 2)(NULL);", "1\n"))
    # tests.append(("var myfunc = func() {ret 1;}; print myfunc();", "1\n"))
    # tests.append(("var myfunc = func() { var inner = func(num) {ret num + 1;}; ret inner;};"
    #               "var x = myfunc(); print x(1);", "2\n"))
    # tests.append(("var is_prime = func(n) { var i = 2; "
    #               "while (i * i <= n) {"
    #               "var factor = n / i; if (i * factor == n) { ret 0;} i = i + 1;} ret 1;}; "
    #               "var get_nth_prime = func(n) { var i = 1; var count = 0; "
    #               "while (count < n) { i = i + 1; "
    #               "if (is_prime(i) == 1) { count = count + 1;}} ret i;}; "
    #               "print get_nth_prime(100);", "541\n"))
    # tests.append(("var is_prime = func(n) { var i = 2; "
    #               "while (i * i <= n) {"
    #               "var factor = n / i; if (i * factor == n) { ret 0;} i = i + 1;} ret 1;}; "
    #               "var get_nth_prime = func(n) { var i = 1; var count = 0; "
    #               "while (count < n) { i = i + 1; "
    #               "if (is_prime(i) == 1) { count = count + 1;}} ret i;}; "
    #               "print get_nth_prime(3);", "5\n"))
    # tests.append(("var printer = func(n) { print n;};"
    #               "print printer(1);", "1\n0\n"))
    # tests.append(("var Rational = func(numerator, denominator) { "
    #               "var get_numerator = func() {ret numerator;};"
    #               "var get_denominator = func() {ret denominator;};"
    #               "var set_numerator = func(val) {numerator = val;};"
    #               "var set_denominator = func(val) {denominator = val;};"
    #               "var multiply = func(other) {"
    #               "ret Rational(numerator * other(1)(),denominator * other(2)());};"
    #               "ret func(index) {"
    #               "if (index == 1) {ret get_numerator;}"
    #               "if (index == 2) {ret get_denominator;}"
    #               "if (index == 3) {ret set_numerator;}"
    #               "if (index == 4) {ret set_denominator;}"
    #               "if (index == 5) {ret multiply;}};};"
    #               "var a = Rational(0, 0);"
    #               "a(3)(1); a(4)(2);"
    #               "var b = Rational(2, 1);"
    #               "var c = a(5)(b)(5)(b)(5)(b);"
    #               "print c(1)() / c(2)();", "4\n"))


    test_interpreter(tests)


def main():
    test()

if __name__ == '__main__':
    main()
