(sequence (declare run_first (function (parameters) (sequence (print 42)))) (declare existant 0) (declare existant (call (lookup run_first) (arguments))))
