(sequence (declare x 100) (while (> (lookup x) 10) (sequence (assign (varloc x) (- (lookup x) 1)))) (print (lookup x)))
