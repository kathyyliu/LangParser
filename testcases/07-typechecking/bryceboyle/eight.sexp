(sequence
    (declare func outer (function (signature int func) (parameters value)
        (sequence
            (declare func inner (function (signature int) (parameters)
                (sequence (print 4))))
            (print (lookup value))
            (return (lookup inner)))
        ))
    (call (call (lookup outer) (arguments 2)) (arguments)))