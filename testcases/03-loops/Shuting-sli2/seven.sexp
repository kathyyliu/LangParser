(sequence (declare a 1) (declare b 2) (declare c 5) (while (< (* (lookup a) (lookup b)) (lookup c)) (sequence (assign (varloc c) (- (lookup c) 1)))) (print (* (* (lookup a) (lookup b)) (lookup c))))
