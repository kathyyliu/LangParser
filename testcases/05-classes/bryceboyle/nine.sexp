 (sequence
    (declare Abc (class
        (declare num 0)))
    (declare swap 
            (function (parameters a b)
            (sequence
                (declare temp 0)
                (assign (varloc temp) (member (lookup a) num))
                (assign (memloc (varloc a) num) (member (lookup b) num))
                (assign (memloc (varloc b) num) (lookup temp)))))
    (declare one
        (call (lookup Abc) (arguments)))
    (assign (memloc (varloc one) num) 1)
    (declare two
        (call (lookup Abc) (arguments)))
    (assign (memloc (varloc two) num) 2)
    (call (lookup swap) (arguments (lookup one) (lookup two)))
    (print (member (lookup one) num))
    (print (member (lookup two) num)))