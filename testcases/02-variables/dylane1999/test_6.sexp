(sequence (declare foo (+ 5 (* 5 2))) (print (lookup foo)) (declare bar (lookup foo)) (print (lookup bar)))
