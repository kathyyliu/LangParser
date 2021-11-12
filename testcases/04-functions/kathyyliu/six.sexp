(sequence 
    (declare x 1) 
    (declare outer (function (parameters) (sequence 
        (declare x 2) 
        (declare inner (function (parameters) (sequence 
            (print (lookup x)) 
            (assign (varloc x) 3)))) 
        (return (lookup inner))))) 
    (call (call (lookup outer) (arguments)) (arguments)) 
    (print (lookup x)))