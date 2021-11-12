(sequence (declare outter (function (signature int) (parameters) (sequence (return (function (parameters) (sequence)))))) (call (call (lookup outter) (arguments)) (arguments)))
