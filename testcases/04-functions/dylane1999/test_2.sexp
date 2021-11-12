(sequence (declare x 5) (declare printer (function (parameters n) (sequence))) (assign (varloc x) (call (lookup printer) (arguments 42))) (print (lookup x)))
