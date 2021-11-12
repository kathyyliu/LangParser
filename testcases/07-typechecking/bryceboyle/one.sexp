(sequence
    (declare func test (function (signature int) (parameters) 
        (sequence (return 1))))
    (assign (varloc test) 3)
    (print (lookup test)))