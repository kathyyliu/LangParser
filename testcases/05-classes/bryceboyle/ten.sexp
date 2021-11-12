(sequence
    (declare Yay (class
        (declare value 2)))
    (declare fun_times
        (call (lookup Yay) (arguments)))
    (print (* (lookup fun_times) 2)))