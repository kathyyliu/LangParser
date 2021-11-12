(sequence
    (declare printer (function (parameters n) (sequence
        (print (lookup n)))))
    (print (call (lookup printer) (arguments 1))))
