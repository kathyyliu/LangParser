(sequence (declare i (function (parameters) (sequence (return 1) (print 2)))) (declare o (function (parameters) (sequence (call (lookup i) (arguments)) (print 3)))) (call (lookup o) (arguments)))
