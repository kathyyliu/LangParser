(sequence
    (declare a 0)
    (if
        (== (lookup a) 2)
        (sequence
            (declare b (lookup a))))
    (print (lookup b))
)
