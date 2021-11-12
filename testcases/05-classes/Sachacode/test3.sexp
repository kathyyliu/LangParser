(sequence
    (declare A (class (declare b 0)))
    (declare c (call (lookup A) (arguments)))
    (while
        (< (member (lookup c) b) 6)
        (sequence
            (print (member (lookup c) b))
            (assign (memloc (varloc c) b) (+ (member (lookup c) b) 1)))))