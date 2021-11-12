(sequence
    (declare age 0)
    (declare Person (class
        (declare age 1)))
    (declare kathy (call (lookup Person) (arguments)))
    (print (lookup age))
    (print (member (lookup kathy) age))
)