(sequence (declare a (function (parameters) (sequence (declare b (function (parameters) (sequence (print 1))))))) (call (lookup a) (arguments)))
