(sequence (declare printer (function (parameters n) (sequence (print (lookup n) ) (return (+ (lookup n) 1))))) (declare a (call (lookup printer) (arguments 5))) (print (lookup a)))
