(sequence
    (declare Cat (class
        (declare age 0)))
    (declare rocky
        (call (lookup Cat) (arguments)))
    (print (member (lookup rocky) age))
    (assign (memloc (varloc rocky) age) 10)
    (print (member (lookup rocky) age)))