# "Lang" Parser & Interpreter

### Overview
This project is my work from the course COMP 337: Programming Languages at Occidental College.
Given the grammar rules and expected behavior of the made-up language "Lang,"
I built a fully-functional parser and interpreter for Lang in Python.

Lang supports:
- arithmetic
- printing
- variables
- control flow
- functions
- classes
- typing

Each of the features above were implemented using **test-driven development** using ~200 testcases per feature
in the form of a `.lang` file containing the program, an accompanying `.sexp` file representing the expected output from parser,
and a `.out` file with the expected program output. The testcases were pooled from all students in the course and includes consideration for edge cases.

### How to run
run:

`python3 main.py`

This program will iterate through all the testcases, passing the `.lang` testcases through the parser and interpreter,
and comparing the outputs to the corresponding `.sexp` and `.out` files. If the output does not match expected, the program will throw an error.

note: `main.py` was written by the professor instructing the course.

### Lang grammar rules
**program**                         = opt_space ( statement opt_space )*;

**statement**                       = declaration_statement
                                    | assignment_statement
                                    | if_else_statement
                                    | if_statement
                                    | while_statement
                                    | return_statement
                                    | print_statement
                                    | expression_statement;

**if_statement**                    = "if" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}";  
**if_else_statement**               = "if" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}" opt_space "else" opt_space "{" opt_space program opt_space "}";

**while_statement**                 = "while" opt_space "(" opt_space expression opt_space ")" opt_space "{" opt_space program opt_space "}";

**return_statement**                = "ret" req_space expression opt_space ";";

**declaration_statement**           = type req_space identifier opt_space "=" opt_space expression opt_space ";";  
**assignment_statement**            = location opt_space "=" opt_space expression opt_space ";";  
**location**                        = identifier ( "." identifier )*;  
**print_statement**                 = "print" req_space expression opt_space ";";

**type**                            = "func"
                                    | "int"
                                    | "var";

**expression_statement**            = expression opt_space ";";

**expression**                      = or_expression;

**or_expression**                   = and_expression ( opt_space or_operator opt_space and_expression )*;  
**or_operator**                     = "||";  
**and_expression**                  = optional_not_expression ( opt_space and_operator opt_space optional_not_expression )*;  
**and_operator**                    = "&&";

**optional_not_expression**         = comp_expression
                                    | not_expression;

**not_expression**                  = "!" opt_space comp_expression;

**comp_expression**                 = add_sub_expression ( opt_space comp_operator opt_space add_sub_expression )?;  
**comp_operator**                   = "=="
                                    | "!="
                                    | "<="
                                    | ">="
                                    | "<"
                                    | ">";

**add_sub_expression**              = mul_div_expression ( opt_space add_sub_operator opt_space mul_div_expression )*;  
**add_sub_operator**                = "+"
                                    | "-";  
**mul_div_expression**              = call_member_expression ( opt_space mul_div_operator opt_space call_member_expression )*;  
**mul_div_operator**                = "*"
                                    | "/";

**call_member_expression**          = operand ( opt_space call_member )*;  
**call_member**                     = function_call
                                    | member;

**member**                          = "." opt_space identifier;  
**function_call**                   = "(" opt_space arguments opt_space ")";  
**arguments**                       = ( expression opt_space ( "," opt_space expression opt_space )* )?;

**operand**                         = class
                                    | parenthesized_expression
                                    | function
                                    | identifier
                                    | integer;

**class**                           = "class" opt_space "{" ( opt_space declaration_statement )* opt_space "}";

**parenthesized_expression**        = "(" opt_space expression opt_space ")";

**function**                        = "func" opt_space "(" opt_space parameters opt_space ")" ( opt_space return_type )? opt_space "{" opt_space statements opt_space "}";  
**parameters**                      = ( parameter opt_space ( "," opt_space parameter opt_space )* )?;  
**parameter**                       = ( type req_space )? identifier;  
**return_type**                     = "->" opt_space type;

note: identifier cannot be a keyword: print, var, if, else, while, func, ret, class, int, bool, string  
**identifier**                      = identifier_first_char ( identifier_char )*;  
**identifier_first_char**           = ALPHA
                                    | "_";  
**identifier_char**                 = ALNUM
                                    | "_";

**integer**                         = ( DIGIT )+;

**opt_space**                       = ( space )*;  
**req_space**                       = ( space )+;  
**space**                           = comment
                                    | BLANK
                                    | NEWLINE;  
**comment**                         = "#" ( PRINT )* NEWLINE;