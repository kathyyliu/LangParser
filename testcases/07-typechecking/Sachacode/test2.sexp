(sequence
    (declare x 1)
    (declare y 1)
    (declare func addTyped (function (signature var var int) (parameters a b) (sequence
        (return (+ (lookup a) (lookup b))))))
    (declare add (function (parameters a b) (sequence
        (return (+ (lookup a) (lookup b))))))
    (print (call (lookup addTyped) (arguments (lookup x) (lookup y))))
    (print (call (lookup add) (arguments (lookup x) (lookup y)))))