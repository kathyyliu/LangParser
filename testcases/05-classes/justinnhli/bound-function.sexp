(sequence
    (declare Thing (class
        (declare n 42)
        (declare print_n (function (parameters this) (sequence
            (print (member (lookup this) n)))))))
    (declare thing (call (lookup Thing) (arguments)))
    (declare bound (member (lookup thing) print_n))
    (call (lookup bound) (arguments)))
