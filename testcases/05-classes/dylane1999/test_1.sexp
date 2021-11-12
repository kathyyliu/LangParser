(sequence (declare foo (class (declare bar (function (parameters) (sequence (print 27)))))) (declare x (call (lookup foo) (arguments))) (call (member (lookup x) bar) (arguments)))
