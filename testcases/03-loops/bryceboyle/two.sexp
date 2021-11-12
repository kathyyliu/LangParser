(sequence
    (declare j 1)
    (if
        (< (+ (lookup j) 3) 10)
        (sequence
            (print (+ (lookup j) 3))
)))