(sequence
    (declare a 0)
    (if
        1
        (sequence
            (print (lookup a))
            (declare a 1)
            (print (lookup a))
            (if
                1
                (sequence
                    (print (lookup a))
                    (declare a 2)
                    (print (lookup a))
                    (if
                        1
                        (sequence
                            (print (lookup a))
                            (declare a 3)
                            (print (lookup a)))))))))