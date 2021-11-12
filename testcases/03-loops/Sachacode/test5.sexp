(sequence
    (declare i 1)
    (while
        (< (lookup i) 6)
        (sequence
            (print (lookup i))
            (assign (varloc i) (+ (lookup i) 1))
            (declare i 10)
            (print (lookup i)))))