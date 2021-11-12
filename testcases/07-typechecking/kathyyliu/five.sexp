(sequence
    (declare myfunc (function
        (signature int) (parameters) (sequence 
            (return (function (parameters) (sequence))))))
    (call (lookup myfunc) (arguments))
)