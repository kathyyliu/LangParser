(sequence
    (declare my_class1 (class
        (declare num 1)))
    (declare my_class2 (class
        (declare num 1)))
    (ifelse
        (== (lookup my_class1) (lookup my_class2))
        (sequence
            (print 1))
        (sequence
            (print 0))
    ))