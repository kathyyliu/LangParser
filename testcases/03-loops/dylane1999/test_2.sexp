(sequence (declare x 1) (if (== (lookup x) 1) (sequence (if (== (lookup x) 1) (sequence (if (== (lookup x) 1) (sequence (if (== (lookup x) 1) (sequence (print (lookup x)))))))))) (print (lookup x)))
