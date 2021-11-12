(sequence
    (declare BinarySearchTree (class
        (declare Node (class
            (declare value 0)
            (declare left 0)
            (declare right 0)
            (declare constructor (function (parameters this value) (sequence
                (assign (memloc (varloc this) value) (lookup value))
                (return (lookup this)))))))
        (declare root 0)
        (declare constructor (function (parameters this) (sequence
            (return (lookup this)))))
        (declare add (function (parameters this value) (sequence
            (assign (varloc root) (call (lookup recur_add) (arguments (lookup root) (lookup value))))))) 
        (declare recur_add (function (parameters this node value) (sequence
            (if (== (lookup node) 0)
                (sequence (return (call (member (call (lookup Node) (arguments)) constructor) (arguments (lookup value))))))
            (if (<= (lookup value) (member (lookup node) value)) (sequence
                (assign (memloc (varloc node) left)
                    (call (member (lookup this) recur_add) (arguments (member (lookup node) left) (lookup value))))
                (return (lookup node))))
            (if (> (lookup value) (member (lookup node) value)) (sequence
                (assign (memloc (varloc node) right)
                    (call (lookup recur_add) (arguments (member (lookup node) right) (lookup value))))
                (return (lookup node)))))))
        (declare in_order_print (function (parameters this) (sequence
            (call (lookup recur_in_order_print) (arguments (lookup root))))))
        (declare recur_in_order_print (function (parameters this node) (sequence
            (if (!= (lookup node) 0) (sequence
                (call (lookup recur_in_order_print) (arguments (member (lookup node) left)))
                (print (member (lookup node) value))
                (call (lookup recur_in_order_print) (arguments (member (lookup node) right))))))))))
    (declare tree (call (member (call (lookup BinarySearchTree) (arguments)) constructor) (arguments)))
    (call (member (lookup tree) add) (arguments 9))
    (call (member (lookup tree) add) (arguments 7))
    (call (member (lookup tree) add) (arguments 0))
    (call (member (lookup tree) add) (arguments 1))
    (call (member (lookup tree) add) (arguments 3))
    (call (member (lookup tree) add) (arguments 2))
    (call (member (lookup tree) add) (arguments 6))
    (call (member (lookup tree) add) (arguments 8))
    (call (member (lookup tree) add) (arguments 4))
    (call (member (lookup tree) add) (arguments 5))
    (call (member (lookup tree) in_order_print) (arguments)))
