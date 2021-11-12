(sequence 
    (declare Element (call 
        (function (parameters) (sequence
            (declare counter 1)
            (return (class
                (declare atomic_number 0)
                (declare constructor (function (parameters this) (sequence
                    (assign (memloc (varloc this) atomic_number) (lookup counter))
                    (assign (varloc counter) (+ (lookup counter) 1))
                    (return (lookup this)))))))))
        (arguments)))
    (declare hydrogen (call
        (member (call (lookup Element) (arguments)) constructor) (arguments)))
    (declare helium (call
        (member (call (lookup Element) (arguments)) constructor) (arguments)))
    (declare lithium (call
        (member (call (lookup Element) (arguments)) constructor) (arguments)))
    (declare beryllium (call
        (member (call (lookup Element) (arguments)) constructor) (arguments)))
    (declare boron (call (member
        (call (lookup Element) (arguments)) constructor) (arguments)))
    (declare carbon (call
        (member (call (lookup Element) (arguments)) constructor) (arguments)))
    (print (member (lookup hydrogen) atomic_number))
    (print (member (lookup helium) atomic_number))
    (print (member (lookup lithium) atomic_number))
    (print (member (lookup beryllium) atomic_number))
    (print (member (lookup boron) atomic_number))
    (print (member (lookup carbon) atomic_number)))
