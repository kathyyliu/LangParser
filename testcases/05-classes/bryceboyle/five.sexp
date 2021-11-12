(sequence
    (declare Book (class
        (declare get_num_pages 
            (function (parameters)
            (sequence
                (return 360))))))
    (declare chaos
        (call (lookup Book) (arguments)))
    (print (call (lookup chaos) (arguments))))