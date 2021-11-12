(sequence
    (declare Cat (class))
    (if (lookup Cat) (sequence
        (print 1)))
    (if (call (lookup Cat) (arguments)) (sequence
        (print 1)))
)