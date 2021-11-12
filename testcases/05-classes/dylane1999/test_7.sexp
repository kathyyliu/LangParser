(sequence (declare foo (class (declare bar 5))) (declare x (call (lookup foo) (arguments))) (declare y (call (lookup foo) (arguments))) (print (== (lookup x) (lookup y))))
