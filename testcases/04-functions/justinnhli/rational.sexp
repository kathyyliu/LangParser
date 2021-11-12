(sequence
    (declare Rational (function (parameters numerator denominator) (sequence
        (declare get_numerator (function (parameters) (sequence
            (return (lookup numerator)))))
        (declare get_denominator (function (parameters) (sequence
            (return (lookup denominator)))))
        (declare set_numerator (function (parameters val) (sequence
            (assign (varloc numerator) (lookup val)))))
        (declare set_denominator (function (parameters val) (sequence
            (assign (varloc denominator) (lookup val)))))
        (declare multiply (function (parameters other) (sequence
            (return (call (lookup Rational) (arguments (* (lookup numerator) (call (call (lookup other) (arguments 1)) (arguments))) (* (lookup denominator) (call (call (lookup other) (arguments 2)) (arguments)))))))))
        (return (function (parameters index) (sequence
            (if (== (lookup index) 1) (sequence
                (return (lookup get_numerator))))
            (if (== (lookup index) 2) (sequence
                (return (lookup get_denominator))))
            (if (== (lookup index) 3) (sequence
                (return (lookup set_numerator))))
            (if (== (lookup index) 4) (sequence
                (return (lookup set_denominator))))
            (if (== (lookup index) 5) (sequence
                (return (lookup multiply))))))))))
    (declare a (call (lookup Rational) (arguments 0 0)))
    (call (call (lookup a) (arguments 3)) (arguments 1))
    (call (call (lookup a) (arguments 4)) (arguments 2))
    (declare b (call (lookup Rational) (arguments 2 1)))
    (declare c
        (call
            (call
                (call
                    (call
                        (call
                            (call (lookup a)
                                (arguments 5))
                            (arguments (lookup b)))
                        (arguments 5))
                    (arguments (lookup b)))
                (arguments 5))
            (arguments (lookup b))))
    (print (/
        (call (call (lookup c) (arguments 1)) (arguments))
        (call (call (lookup c) (arguments 2)) (arguments)))))
