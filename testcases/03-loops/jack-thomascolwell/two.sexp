(sequence (while 0 (sequence (print 1))) (declare x 0) (while (< (lookup x) 3) (sequence (print (lookup x)) (assign (varloc x) (+ (lookup x) 1)))))
 
