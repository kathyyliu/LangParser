(sequence
    (declare outer (function (parameters) (sequence
        (return (function (parameters) (sequence))))))
    (declare fn1 (call (lookup outer) (arguments)))
    (declare fn2 (call (lookup outer) (arguments)))
    (print (== (lookup fn1) (lookup fn1)))
    (print (== (lookup fn1) (lookup fn2)))
    (print (== (lookup fn2) (lookup fn2)))
    (print (!= (lookup fn1) (lookup fn2)))
    (print (lookup fn1))
    (print (! (lookup fn1)))
    (ifelse (lookup fn1) (sequence (print 1)) (sequence (print 0)))
    (ifelse (! (lookup fn1)) (sequence (print 1)) (sequence (print 0))))
