(sequence 
    (declare makePerson (function (parameters n) (sequence 
        (return (call (class 
            (declare age (lookup n))) (arguments))))))
    (declare kathy (call (lookup makePerson) (arguments 19)))
    (print (member (lookup kathy) age))
)