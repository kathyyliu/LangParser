(sequence
    (declare A (class (declare b 0)))
    (declare c (call (lookup A) (arguments)))
    (assign (memloc (varloc c) b) 10)
    (print (member (lookup c) b)))