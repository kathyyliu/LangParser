(sequence
    (declare is_prime (function (parameters n) (sequence
        (declare i 2)
        (while (<= (* (lookup i) (lookup i)) (lookup n)) (sequence
            (declare factor (/ (lookup n) (lookup i)))
            (if (== (* (lookup i) (lookup factor)) (lookup n))
                (sequence (return 0)))
            (assign (varloc i) (+ (lookup i) 1))))
        (return 1))))
    (declare get_nth_prime (function (parameters n) (sequence
        (declare i 1)
        (declare count 0)
        (while (< (lookup count) (lookup n)) (sequence
            (assign (varloc i) (+ (lookup i) 1))
            (if (== (call (lookup is_prime) (arguments (lookup i))) 1)
                (sequence (assign (varloc count) (+ (lookup count) 1))))))
        (return (lookup i)))))
    (print (call (lookup get_nth_prime) (arguments 100))))
