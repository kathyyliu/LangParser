(sequence (declare x 5) (declare printer (function (parameters n) (sequence (print (+ (lookup n) 1)) (return 5)))) (assign (varloc x) (call (lookup printer) (arguments 42))) (print (lookup x)))
