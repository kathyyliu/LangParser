(sequence
    (declare x 0)
    (declare y 1)
    (if
        (|| (lookup x) (lookup y))
        (sequence
            (print (lookup x))
            (print (lookup y)))
))
