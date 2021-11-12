(sequence
    (declare func two (function (signature func int) (parameters k)
        (sequence (print (lookup k)) (return 2))))
    (declare int number 3)
    (print (call (lookup two) (arguments (lookup number)))))