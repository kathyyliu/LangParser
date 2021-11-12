(sequence
(declare Test (class (declare b 10) (declare a (function (parameters this) (sequence (print (member (lookup this) b)))))))
(declare x (call (lookup Test) (arguments)))
(declare y (member (lookup x) a))
(call (lookup y) (arguments))
)
