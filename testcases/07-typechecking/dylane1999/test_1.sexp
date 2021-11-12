(sequence (declare func foo (function (signature func) (parameters) (sequence (return 12)))) (call (lookup foo) (arguments)))
