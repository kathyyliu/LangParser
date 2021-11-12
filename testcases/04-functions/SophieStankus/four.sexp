(sequence (declare a (function (parameters) (sequence (print 1)))) (declare b (function (parameters) (sequence (call (lookup a) (arguments))))) (call (lookup b) (arguments)))
