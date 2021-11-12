(sequence (declare a 1) (declare b 2) (declare c 3) (declare d 4) (declare e 5) (print (* (+ (+ (+ (+ (lookup a) (lookup b)) (lookup c)) (lookup d)) (lookup e)) (lookup e))))
