import re
import sys
from pathlib import Path

from parser import Parser
from interpreter import Interpreter
# from transforms import ConstantFoldingTransform # FIXME change this line to use your code if necessary


def normalize_sexp(string):

    def fail(index):
        return None, index

    def skip_whitespace(string, index):
        while index < len(string) and string[index] in ' \n':
            index += 1
        return index

    def _normalize_sexp(string, index):
        if index > len(string):
            return fail(index)
        index = skip_whitespace(string, index)
        sexp = ''
        if index < len(string) and string[index] == '(':
            index = skip_whitespace(string, index + 1)
            sexp += '('
        match = re.match('[^() \n]+', string[index:])
        if not match:
            return fail(index)
        if sexp == '':
            return match.group(), index + len(match.group())
        sexp = '(' + match.group()
        index += len(match.group())
        # match all children
        while True:
            index = skip_whitespace(string, index)
            # match a child
            child, index = _normalize_sexp(string, index)
            if child is None:
                break
            sexp += ' ' + child
        index = skip_whitespace(string, index)
        if not string[index] == ')':
            raise SyntaxError('malformed S-expression')
        sexp += ')'
        index = skip_whitespace(string, index + 1)
        return sexp, index

    sexp, index = _normalize_sexp(string, 0)
    if index == len(string):
        return sexp
    else:
        raise SyntaxError('malformed S-expression')



def fix_newlines(string):
    return '\n'.join(line for line in string.splitlines() if line.strip()) + '\n'


def test_sexp(sexp_path, parse, message):
    """Test a parse's S-expression, if one is specified.

    Parameters:
        sexp_path (Path): The path of the expected S-expression.
        parse (Parse): The Parse object to serialize.
        message (str): The message to output if the test fails.

    Raises:
        AssertError: If the test does not pass.
    """
    if not sexp_path.exists():
        return
    with sexp_path.open() as fd:
        expected_sexp = normalize_sexp(fd.read())
    # process the expected and actual output to deal with whtiespace
    actual_sexp = normalize_sexp(str(parse))
    error = [message,]
    error.append('EXPECTED S-EXPRESSION (multiple whitespaces are ignored)')
    error.append(expected_sexp)
    error.append('ACTUAL S-EXPRESSION (multiple whitespaces are ignored)')
    error.append(actual_sexp)
    assert actual_sexp == expected_sexp, '\n' + '\n'.join(error)


def test_with_file(lang_path):
    """Test using the lang program at the file path.

    Parameters:
        lang_path (Path): The path of the input program.

    Raises:
        AssertError: If the test does not pass.
    """
    # read the program to run
    with lang_path.open() as fd:
        program = fix_newlines(fd.read())
    print()
    print(f'RUNNING {lang_path}')
    print(program)
    # parse the code
    parser = Parser()
    parse = parser.parse(program)
    if parse is None:
        # if there's a syntax error, that's our only output
        actual_output = 'syntax error'
    else:
        # otherwise, check against the intermediate representation
        sexp_path = lang_path.parent.joinpath(lang_path.stem + '.sexp')
        test_sexp(sexp_path, parse, 'intermediate representation does not match')
        # check against the transformed intermediate representation
        # sexp2_path = lang_path.parent.joinpath(lang_path.stem + '.sexp2')
        # parse = ConstantFoldingTransform().visit(parse)
        # test_sexp(sexp2_path, parse, 'transformed intermediate representation does not match')
        # run the program to get the output
        actual_output = Interpreter().execute(parse)
    # read the expected output
    out_path = lang_path.parent.joinpath(lang_path.stem + '.out')
    with out_path.open() as fd:
        expected_output = fd.read()
    # process the expected and actual output to deal with newlines
    expected_output = fix_newlines(expected_output)
    actual_output = fix_newlines(actual_output)
    # check against the output
    if actual_output != expected_output:
        lines = ['\n\n']
        lines.append('EXPECTED OUTPUT:')
        lines.append(expected_output)
        lines.append('')
        lines.append('ACTUAL OUTPUT:')
        lines.append(actual_output)
        assert actual_output == expected_output, '\n'.join(lines)


def test_with_directory(dir_path):
    """Test using the lang programs in the directory.

    Arguments:
        dir_path (Path): A directory containing input programs.
    """
    for lang_path in sorted(dir_path.glob('**/*.lang'), key=(lambda path: str(path).lower())):
        test_with_file(lang_path)


def main():
    """Run command line tests."""
    # set recursion limit to be really high
    sys.setrecursionlimit(10**6)
    for arg in sys.argv[1:]:
        path = Path(arg).expanduser().resolve()
        if path.is_dir():
            test_with_directory(path)
        else:
            test_with_file(path)


if __name__ == '__main__':
    main()
