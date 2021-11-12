(sequence
    (declare Thing (class
        (declare count 0)
        (declare increase 
            (function (parameters this n)
            (sequence
                (assign (varloc n) (+ (lookup n) 1)))))))
    (declare thing1
        (call (lookup Thing) (arguments)))
    (call (member (lookup thing1) increase) (arguments (member (lookup thing1) count)))
    (declare thing2
        (call (lookup Thing) (arguments)))
    (print (member (lookup thing2) count)))