(sequence
    (declare Tree (class
        (declare leaves 200)))
    (declare leaves
        (call (lookup Tree) (arguments)))
    (print (member (lookup leaves) leaves)))