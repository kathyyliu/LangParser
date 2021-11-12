(sequence
    (declare Constants (class (declare pi 314159)))
    (declare consts (call (lookup Constants) (arguments)))
    (print (member (lookup consts) pi))
    (assign (memloc (varloc consts) e) 271828)
    (print (member (lookup consts) e)))
