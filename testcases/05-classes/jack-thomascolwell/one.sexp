(sequence (declare Test (class (declare a 1))) (declare Inst (call (lookup Test) (arguments))) (print (member (lookup Inst) a)))
