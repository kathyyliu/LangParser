(sequence (declare outer (function (parameters) (sequence (declare inner (function (parameters) (sequence (print 0)))) (return (lookup inner))))) (declare foo (call (lookup outer) (arguments))))
