(sequence (declare adder (function (parameters x) (sequence (return (lookup x))))) (print (+ (call (lookup adder) (arguments 1)) (call (lookup adder) (arguments 2)))))
