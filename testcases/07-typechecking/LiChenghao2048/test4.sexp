(sequence (declare x (function (signature int var) (parameters y) (sequence (return ( + (lookup y) (lookup y)))))) (print (call (lookup x)(arguments (+ 1 1)))))
