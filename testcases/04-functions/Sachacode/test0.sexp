(sequence
    (declare printNum
        (function (parameters n)
            (sequence (print (lookup n)))))
    (call (lookup printNum) (arguments 10)))