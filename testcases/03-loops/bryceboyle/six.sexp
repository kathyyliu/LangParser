(sequence
    (ifelse
        (&& (&& 1 2) 3)
        (sequence
            (print 3))
        (sequence
            (print 0))
))
