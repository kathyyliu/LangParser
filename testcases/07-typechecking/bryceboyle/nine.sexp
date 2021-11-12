(sequence
    (declare int number1 1)
    (declare number2 2)
    (declare func number3 (function (signature int) (parameters)
            (sequence (return 3))))
    (print (+ (+ (lookup number1) (lookup number2)) (call (lookup number3) (arguments)))))

    