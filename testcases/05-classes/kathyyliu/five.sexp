(sequence
    (declare Cat (class))
    (declare kitty (call (lookup Cat) (arguments)))
    (print (< (member (lookup kitty) meow) 3))
)