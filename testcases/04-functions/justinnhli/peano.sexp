(sequence
    (declare ZERO (function (parameters) (sequence)))
    (declare succ (function (parameters n) (sequence
        (return (function (parameters) (sequence 
            (return (lookup n))))))))
    (declare add (function (parameters a b) (sequence
        (ifelse
            (== (lookup a) (lookup ZERO))
            (sequence (return (lookup b)))
            (sequence
                (return (call (lookup add) (arguments
                    (call (lookup a) (arguments))
                    (call (lookup succ) (arguments (lookup b)))))))))))
    (declare equals (function (parameters a b) (sequence
        (if
            (&& (== (lookup a) (lookup ZERO)) (== (lookup b) (lookup ZERO)))
            (sequence (return 1)))
        (if
            (|| (== (lookup a) (lookup ZERO)) (== (lookup b) (lookup ZERO)))
            (sequence (return 0)))
        (return (call (lookup equals) (arguments (call (lookup a) (arguments)) (call (lookup b) (arguments))))))))
    (declare ONE (call (lookup succ) (arguments (lookup ZERO))))
    (declare TWO (call (lookup succ) (arguments (lookup ONE))))
    (declare THREE (call (lookup succ) (arguments (lookup TWO))))
    (print (call (lookup equals) (arguments (call (lookup add) (arguments (lookup ONE) (lookup TWO))) (lookup THREE)))))
