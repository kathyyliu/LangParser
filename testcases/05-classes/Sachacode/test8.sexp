(sequence
    (declare A (class (declare b (/ 0 0))))
    (declare c (call (lookup A) (arguments)))
    (print (member (lookup c) b)))