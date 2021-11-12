(sequence (declare a (function (signature int var var) (parameters x x) (sequence (return 1)))) (print (call (lookup a) (arguments 1 1))))
