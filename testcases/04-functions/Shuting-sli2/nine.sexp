(sequence (declare a (function (parameters x) (sequence (ifelse (< (lookup x) 5) (sequence (ifelse (< (lookup x) 3) (sequence (return (* 2 (lookup x)))) (sequence (return (+ (lookup x) 1))))) (sequence (ifelse (> (lookup x) 8) (sequence (return (/ (lookup x) 5))) (sequence (return (- (lookup x) 2))))))))) (print (call (lookup a) (arguments 10))))