(sequence (declare x 5) (declare printer (function (parameters n) (sequence (print 10) (function (parameters) (sequence (print 5)))))) (call (lookup printer) (arguments 42)))
