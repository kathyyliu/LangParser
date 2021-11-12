(sequence (declare a 12) (declare x (function (parameters) (sequence (print (lookup a))))) (if 1 (sequence (declare a 2) (call (lookup x) (arguments)) (print (lookup a)))))
