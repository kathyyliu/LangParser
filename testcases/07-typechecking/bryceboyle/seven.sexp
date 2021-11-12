(sequence
    (declare func thingy (function (signature int int) (parameters num)
        (sequence
            (return (lookup num)))))
    (declare int val 17)
    (if
        (> (lookup val) 2)
        (sequence
            (print (call (lookup thingy) (arguments (lookup val)))))))