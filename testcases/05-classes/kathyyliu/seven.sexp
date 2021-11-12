(sequence 
    (declare eatsFish (function (parameters pet) (sequence 
        (ifelse (member (lookup pet) meow) 
            (sequence (return 1))
            (sequence (return 0))))))
    (declare Cat (class
        (declare meow 1)))
    (declare Dog (class
        (declare meow 0)))
    (print (call (lookup eatsFish) (arguments 
        (call (lookup Cat) (arguments)))))
    (print (call (lookup eatsFish) (arguments 
        (call (lookup Dog) (arguments)))))
)