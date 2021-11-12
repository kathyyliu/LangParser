(sequence
    (declare addOne
        (function (parameters n)
            (sequence 
                (return (+ (lookup n) 1) ))))
    (declare b (call (lookup addOne) (arguments 0)))
    (print (lookup b)))