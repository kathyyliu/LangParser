(sequence (declare A (class (declare b 1))) (declare x (call (lookup A) (arguments))) (declare y (call (lookup A) (arguments))) (print (== (member (lookup x) b) (member (lookup y) b))))
