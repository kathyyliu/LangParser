(sequence
    (declare a 0)
    (if
        1
        (sequence
            (print (lookup a))
            (declare a (+ (lookup a) 1))
            (print (lookup a)))))