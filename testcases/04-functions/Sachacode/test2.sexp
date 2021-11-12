(sequence
    (declare printNum
        (function (parameters n)
            (sequence (print (lookup n)))))
    (declare i 0)
    (while
        (< (lookup i) 6)
            (sequence
                (call (lookup printNum) (arguments (lookup i)))
                (assign (varloc i) (+ (lookup i) 1)))))