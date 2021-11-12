(sequence (declare x 10) (if (== (lookup x) 10) (sequence (assign (varloc x) (+ (lookup x) 1)))) (print (lookup x)))
