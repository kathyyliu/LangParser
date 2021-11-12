(sequence
    (declare computer (function (parameters beep boop)
        (sequence
            (print (lookup beep))
            (return (lookup boop)))))
    (declare i 1)
    (declare j 0)
    (print (call (lookup computer) (arguments (lookup i) (lookup j)))))