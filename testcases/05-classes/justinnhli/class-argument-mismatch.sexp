(sequence 
    (declare Rational (class
        (declare numerator 0)
        (declare denominator 1)))
    (print (call (lookup Rational) (arguments 42))))
