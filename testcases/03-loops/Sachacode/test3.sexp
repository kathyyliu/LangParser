(sequence
    (declare i 0)
    (while
        (< (lookup i) 6)
        (sequence
            (print (lookup i))
            (assign (varloc i) (+ (lookup i) 1)))))