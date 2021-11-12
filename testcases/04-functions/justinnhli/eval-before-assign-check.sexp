(sequence (declare run_first (function (parameters) (sequence (print 42)))) (assign (varloc nonexistant) (call (lookup run_first) (arguments))))
