(sequence (declare x 1) (if 1 (sequence (declare x 2) (print (lookup x)))) (print (lookup x)))
