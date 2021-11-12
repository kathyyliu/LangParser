(sequence
    (declare A (function (parameters n)
        (sequence
            (declare b (lookup n))
            (print (lookup b)))))
    (print (member (lookup A) b)))