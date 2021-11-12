(sequence
    (declare pair (function (parameters first second) (sequence
        (return (function (parameters f) (sequence
            (return (call (lookup f) (arguments (lookup first) (lookup second))))))))))
    (declare NULL (call (lookup pair) (arguments (lookup pair) (lookup pair))))
    (declare first (function (parameters pair) (sequence
        (return (call (lookup pair) (arguments
            (function (parameters first second) (sequence
                (return (lookup first))))))))))
    (declare second (function (parameters pair) (sequence
        (return (call (lookup pair) (arguments
            (function (parameters first second) (sequence
                (return (lookup second))))))))))
    (declare range (function (parameters end) (sequence
        (declare _range (function (parameters end partial) (sequence
            (ifelse
                (== (lookup end) 0)
                (sequence (return (lookup partial)))
                (sequence (return (call (lookup _range) (arguments
                    (- (lookup end) 1)
                    (call (lookup pair) (arguments (- (lookup end) 1) (lookup partial)))))))))))
        (return (call (lookup _range) (arguments (lookup end) (lookup NULL)))))))
    (declare reverse (function (parameters list) (sequence
        (declare _reverse (function (parameters list result) (sequence
            (ifelse
                (== (lookup list) (lookup NULL))
                (sequence (return (lookup result)))
                (sequence (return (call (lookup _reverse) (arguments
                    (call (lookup second) (arguments (lookup list)))
                    (call (lookup pair) (arguments
                        (call (lookup first) (arguments (lookup list)))
                        (lookup result)))))))))))
        (return (call (lookup _reverse) (arguments (lookup list) (lookup NULL)))))))
    (declare map (function (parameters list fn) (sequence
        (declare _map (function (parameters list fn result) (sequence
            (ifelse
                (== (lookup list) (lookup NULL))
                (sequence (return (lookup result))) 
                (sequence (return (call (lookup _map) (arguments
                    (call (lookup second) (arguments (lookup list)))
                    (lookup fn)
                    (call (lookup pair) (arguments
                        (call (lookup fn) (arguments (call (lookup first) (arguments (lookup list)))))
                        (lookup result)))))))))))
        (return (call (lookup reverse) (arguments (call (lookup _map) (arguments (lookup list) (lookup fn) (lookup NULL)))))))))
    (declare filter (function (parameters list fn) (sequence
        (declare _filter (function (parameters list fn result) (sequence
            (if 
                (== (lookup list) (lookup NULL))
                (sequence (return (lookup result))))
            (ifelse
                (== (call (lookup fn) (arguments (call (lookup first) (arguments (lookup list))))) 1)
                (sequence (return (call (lookup _filter) (arguments
                    (call (lookup second) (arguments (lookup list)))
                    (lookup fn)
                    (call (lookup pair) (arguments
                        (call (lookup first) (arguments (lookup list)))
                        (lookup result)))))))
                (sequence (return (call (lookup _filter) (arguments
                    (call (lookup second) (arguments (lookup list)))
                    (lookup fn)
                    (lookup result)))))))))
        (return (call (lookup reverse) (arguments (call (lookup _filter) (arguments
            (lookup list) (lookup fn) (lookup NULL)))))))))
    (declare reduce (function (parameters list fn result) (sequence
        (ifelse
            (== (lookup list) (lookup NULL))
            (sequence
                (return (lookup result)))
            (sequence
                (return (call (lookup reduce) (arguments
                    (call (lookup second) (arguments (lookup list)))
                    (lookup fn)
                    (call (lookup fn) (arguments
                        (lookup result)
                        (call (lookup first) (arguments (lookup list)))))))))))))
    (declare mod (function (parameters a b) (sequence
        (return (- (lookup a) (* (lookup b) (/ (lookup a) (lookup b))))))))
    (declare euler_1 (function (parameters n) (sequence
        (return (call (lookup reduce) (arguments
            (call (lookup filter) (arguments
                (call (lookup map) (arguments
                    (call (lookup range) (arguments (- (lookup n) 1)))
                    (function (parameters n) (sequence
                        (return (+ (lookup n) 1))))))
                (function (parameters n) (sequence
                    (return (||
                        (== (call (lookup mod) (arguments (lookup n) 3)) 0)
                        (== (call (lookup mod) (arguments (lookup n) 5)) 0)))))))
            (function (parameters a b) (sequence (return (+ (lookup a) (lookup b)))))
            0))))))
    (print (call (lookup euler_1) (arguments 10))))
