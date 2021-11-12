(sequence
    (declare printNum
        (function (parameters n)
            (sequence (print (/ (lookup n) 0)))))
    (call (lookup printNum) (arguments 1)))