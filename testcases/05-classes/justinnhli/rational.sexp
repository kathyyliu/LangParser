(sequence 
    (declare Rational (class
        (declare numerator 0)
        (declare denominator 1)
        (declare constructor (function (parameters this numer denom) (sequence
            (assign (varloc numerator) (lookup numer))
            (assign (varloc denominator) (lookup denom))
            (return (lookup this)))))
        (declare multiply (function (parameters this other) (sequence
            (return (call (member (call (lookup Rational) (arguments)) constructor) (arguments
                (* (member (lookup this) numerator) (member (lookup other) numerator))
                (* (member (lookup this) denominator) (member (lookup other) denominator))))))))))
    (declare main (function (parameters) (sequence 
        (declare a (call (lookup Rational) (arguments)))
        (assign (memloc (varloc a) numerator) 1)
        (assign (memloc (varloc a) denominator) 2)
        (declare b (call (member (call (lookup Rational) (arguments)) constructor) (arguments 2 1)))
        (declare c (call (member (call (member (call (member (lookup a) multiply) (arguments (lookup b))) multiply) (arguments (lookup b))) multiply) (arguments (lookup b))))
        (print (/ (member (lookup c) numerator) (member (lookup c) denominator))) (return 0))))
    (call (lookup main) (arguments)))
