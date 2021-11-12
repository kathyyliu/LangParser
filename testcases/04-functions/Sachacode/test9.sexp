(sequence
    (declare addNums
        (function (parameters a b c d e f g h i j)
            (sequence 
                (print (+ (+ (+ (+ (+ (+ (+ (+ (+ (lookup a) (lookup b)) (lookup c)) (lookup d)) (lookup e)) (lookup f)) (lookup g)) (lookup h)) (lookup i)) (lookup j))))))
    (call (lookup addNums) (arguments 0 1 2 3 4 5 6 7 8 9)))