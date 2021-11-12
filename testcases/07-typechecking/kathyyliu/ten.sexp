(sequence
    (declare func myfunc (function 
        (signature int var) (parameters a) (sequence 
            (return (lookup a)))))
    (call (lookup myfunc) (arguments 1))
)