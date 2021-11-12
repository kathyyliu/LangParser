(sequence
    (assign (varloc w) 10)
    (while
        (> (lookup w) 0)
        (sequence
            (assign (varloc w)
                (- (lookup w) 1))
            (print (lookup w))
)))
