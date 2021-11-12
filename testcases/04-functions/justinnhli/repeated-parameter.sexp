(sequence
    (declare foo (function (parameters a b a) (sequence
        (print (lookup a))
        (print (lookup b)))))
    (call (lookup foo) (arguments 1 2 3)))
