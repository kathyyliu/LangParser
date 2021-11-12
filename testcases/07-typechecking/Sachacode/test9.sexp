(sequence
    (declare func a (function (signature int int) (parameters x) (sequence 
        (return (lookup x)))))
    (declare func b (function (signature int int) (parameters x) (sequence 
        (return (* (- 0 1) (lookup x))))))
    (declare func c (function (signature int func func int) (parameters i x y) (sequence
        (return (+ (call (lookup x) (arguments (lookup i))) (call (lookup y) (arguments (lookup i))))))))
    (declare int n 5)
    (print (call (lookup c) (arguments (lookup n) (lookup a) (lookup b)))))