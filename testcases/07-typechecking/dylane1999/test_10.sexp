(sequence (declare func foo (function (signature func int) (parameters x) (sequence (declare int return_val (call (lookup x) (arguments))) (return (lookup return_val))))) (declare func bar (function (signature int) (parameters) (sequence (return 27)))) (print (call (lookup foo) (arguments (lookup bar)))))
