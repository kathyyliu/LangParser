(sequence
    (declare x 1)
    (declare y 1)
    (declare func add (function (signature int int int) (parameters a b) (sequence
        (return (+ (lookup a) (lookup b))))))
    (print (call (lookup add) (arguments (lookup x) (lookup y)))))