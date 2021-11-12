(sequence (declare a (function (parameters) (sequence (return 1)))) (declare b (call (lookup a) (arguments))) (print (lookup b)))
