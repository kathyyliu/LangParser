(sequence
    (declare A (class
        (declare b 0)
        (declare constructor
            (function (parameters this num)
                (sequence
                    (assign (varloc b) (lookup num)))))))
    (declare c (call (lookup A) (arguments)))
    (call (member (lookup c) constructor) (arguments 5))
    (print (member (lookup c) b)))