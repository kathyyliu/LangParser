(sequence
    (declare x 1)
    (declare y 1)
    (declare int add (function (signature var var var) (parameters a b) (sequence
        (return (+ (lookup a) (lookup b))))))
    (print (call (lookup add) (arguments (lookup x) (lookup y)))))