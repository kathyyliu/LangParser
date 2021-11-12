(sequence (declare a 2) (assign (varloc a) (- (lookup a) (/ (- (* (lookup a) (lookup a)) (lookup a)) (lookup a)))) (print (lookup a)))
