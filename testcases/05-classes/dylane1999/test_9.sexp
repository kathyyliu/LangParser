(sequence (declare foo (class (declare bar 5))) (declare x (call (lookup foo) (arguments))) (print (== (member (lookup x) bar) (lookup foo))))
