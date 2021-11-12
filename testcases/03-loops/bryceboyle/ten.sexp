(sequence
    (if
        (== 1 1)
        (sequence
            (declare z 2)
            (if
                (== (lookup z) 2)
                (sequence
                    (assign (varloc z) (+ (lookup z) 2))))
            (declare z 0)
            (print (lookup z))
)))
