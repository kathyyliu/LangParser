(sequence (declare a (function (parameters b c) (sequence (print (lookup b)) (print (lookup c))))) (call (lookup a) (arguments 1 2)))
