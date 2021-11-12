(sequence
    (declare n 100)
    (print (lookup n))
    (declare printNum
        (function (parameters n)
            (sequence 
                (print (lookup n))
                (if
                    (> (lookup n) 9)
                        (sequence
                            (declare n 1)
                            (print (lookup n)))))))
    (call (lookup printNum) (arguments 10)))