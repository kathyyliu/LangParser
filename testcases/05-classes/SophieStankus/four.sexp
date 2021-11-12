(sequence (declare x (class (declare y 5))) (declare z (call (lookup x) (arguments))) (assign (memloc (varloc z) y) 4) (print (member (lookup z) y)))
