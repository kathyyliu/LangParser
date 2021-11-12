(sequence (declare foo (class (declare bar 5))) (assign (memloc (varloc foo) bar) 6) (print (member (lookup foo) bar)))
