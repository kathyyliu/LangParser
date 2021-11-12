(sequence (declare Test (class (declare a 1)))  (declare Inst (call (lookup Test) (arguments))) (assign (varloc Test) (class (declare a 10))) (print (member (lookup Inst) a)))
