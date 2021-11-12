(sequence (declare x 1) (if (! (! (|| (> (lookup x) 0) (== (lookup x) 2)))) (sequence (print (lookup x)))))
