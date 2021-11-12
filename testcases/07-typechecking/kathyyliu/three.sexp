(sequence
    (declare myfunc (function
        (signature var var var) (parameters a b) (sequence 
            (print 1))))
    (declare x 1)
    (call (lookup myfunc) (arguments (lookup x) (lookup x)))
)