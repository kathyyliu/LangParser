(sequence
    (declare b 
        (function (parameters)
            (sequence (print 20))))
    (declare A (class
        (declare b 
        (function (parameters this)
            (sequence (print 10))))))
    (declare c (call (lookup A) (arguments)))
    (call (member (lookup c) b) (arguments))
    (call (lookup b) (arguments)))