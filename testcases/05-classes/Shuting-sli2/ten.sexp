(sequence (declare C (class)) (declare c1 (call (lookup C) (arguments))) (declare c2 (call (lookup C) (arguments))) (print (+ (lookup c1) (lookup c2))))
