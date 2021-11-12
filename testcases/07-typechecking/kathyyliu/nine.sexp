(sequence
    (declare func myfunc (function 
        (signature func) (parameters) (sequence 
            (print 123))))
    (call (lookup myfunc) (arguments))
)