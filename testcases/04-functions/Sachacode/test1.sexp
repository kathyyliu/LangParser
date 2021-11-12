(sequence
    (declare printTen
        (function (parameters)
            (sequence (print 10))))
    (call (lookup printTen) (arguments)))