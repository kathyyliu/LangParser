(sequence
    (declare a 1)
    (ifelse
        (== (lookup a) 1)
        (sequence
            (print 1))
        (sequence
            (print 0))))