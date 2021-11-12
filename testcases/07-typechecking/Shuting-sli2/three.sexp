(sequence (declare outter (function (signature func) (parameters) (sequence (return (function (parameters) (sequence)))))) (declare func num (call (lookup outter) (arguments))))
