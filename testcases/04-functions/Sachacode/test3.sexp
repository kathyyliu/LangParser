(sequence
    (declare printNum
        (function (parameters n)
            (sequence (print (lookup n)))))
    (ifelse
        (> 1 0)
        (sequence
            (call (lookup printNum) (arguments 1)))
        (sequence
            (call (lookup printNum) (arguments 0)))))