(sequence (declare a 2) (print (lookup a)) (declare b 3) (print (lookup b)) (declare temp (lookup b)) (print (lookup temp)) (assign (varloc b) (lookup a)) (print (lookup b)) (assign (varloc a) (lookup temp)) (print (lookup a)) (print (lookup temp)))