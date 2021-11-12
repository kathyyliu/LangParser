(sequence
    (declare Fruit (class
        (declare Fruit (function (parameters this) (sequence 
            (return 1))))))
    (declare myfunc (function (parameters) (sequence 
        (declare Fruit (call (lookup Fruit) (arguments)))
        (print (lookup Fruit)))))
    (print (lookup Fruit))
    (call (lookup myfunc) (arguments))
    (print (member (call (lookup Fruit) (arguments)) Fruit))
    (print (call (member (call (lookup Fruit) (arguments)) Fruit) (arguments)))
)