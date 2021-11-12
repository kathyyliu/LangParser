(sequence
    (declare Llama (class
        (declare height 0)
        (declare weight 0)))
    (declare bob
        (call (lookup Llama) (arguments)))
    (print (member (lookup bob) age)))