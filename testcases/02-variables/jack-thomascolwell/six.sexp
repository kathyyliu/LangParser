(sequence (declare a 12) (print (lookup a)) (assign (varloc a) 10) (print (lookup a)) (declare b 2) (assign (varloc b) 10) (print (lookup b)) (assign (varloc b) 9) (print (lookup b)))
