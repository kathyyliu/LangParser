(sequence (declare a (function (parameters) (sequence (if 1 (sequence (if 1 (sequence (if 1 (sequence (return 7))) (return 6))) (return 5))) (return 4)))) (print (call (lookup a) (arguments))))