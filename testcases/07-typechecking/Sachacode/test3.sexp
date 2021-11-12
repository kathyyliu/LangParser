(sequence
    (declare int x 1)
    (declare int y 1)
    (declare func sub (function (signature int int int) (parameters a b) (sequence
        (return (- (lookup a) (lookup b))))))
    (print (call (lookup sub) (arguments (lookup x) (lookup y)))))