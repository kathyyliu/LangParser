(sequence (declare b 123) (print (lookup b)) (assign (varloc b) (- 1 (lookup b))) (print (lookup b)))
