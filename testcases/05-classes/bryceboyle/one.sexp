(sequence
    (declare fn 
        (function (parameters)
        (sequence
            (declare value 6))))
    (print 
        (member (lookup fn) value)))