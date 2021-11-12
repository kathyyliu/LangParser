(sequence (declare x 5) (while (> (lookup x) 0) (sequence (if (== (lookup x) 3) (sequence (print 3))) (assign (varloc x) (- (lookup x) 1)))))
