(sequence (declare a (function (parameters) (sequence (declare b (function (parameters) (sequence (print 1)))) (return (lookup b))))) (call (call (lookup a) (arguments)) (arguments)))
