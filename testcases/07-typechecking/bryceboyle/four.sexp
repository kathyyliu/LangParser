(sequence
    (declare func add_one (function (signature var int) (parameters a)
        (sequence
            (assign (varloc a) (+ (lookup a) 1)))))
    (declare int bit 0)
    (call (lookup add_one) (arguments (lookup bit)))
    (print (lookup bit)))