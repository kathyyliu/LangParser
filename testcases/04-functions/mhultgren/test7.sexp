(sequence (declare a 1) (declare outer (function (parameters) (sequence (declare a 2) (declare inner (function (parameters) (sequence (print (lookup a))))) (return (lookup inner))))) (call (call (lookup outer) (arguments)) (arguments)))