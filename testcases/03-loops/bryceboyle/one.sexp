(sequence
    (declare a 2)
    (while
        (< (lookup a) 10)
        (sequence
            (while 
                (< (lookup a) 7)
                (sequence
                    (assign (varloc a)
                        (+ (lookup a) 1))))
            (assign (varloc a)
                (+ (lookup a) 1))
            (print (lookup a))
)))
