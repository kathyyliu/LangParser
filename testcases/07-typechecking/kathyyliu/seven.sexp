(sequence
    (declare is_two (function
        (signature int int) (parameters a) (sequence 
            (ifelse (== (lookup a) 2) 
                (sequence (return 1))
                (sequence (return 0))))))
    (print (call (lookup is_two) (arguments 2)))
)