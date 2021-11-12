(sequence
    (declare Thing (class))
    (declare x (call (lookup Thing) (arguments)))
    (declare y (call (lookup Thing) (arguments)))
    (declare z (lookup x))
    (print (== (lookup x) (lookup y)))
    (print (== (lookup x) (lookup x)))
    (print (== (lookup z) (lookup x)))
)