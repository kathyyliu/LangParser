(sequence
    (declare Cat (class 
        (declare num_paws 4)))
    (declare Dog (class 
        (declare num_paws 4)))
    (print (== (lookup Cat) (lookup Dog)))
    (print (== (lookup Cat) (lookup Cat)))
    (print (== 
            (member (call (lookup Cat) (arguments)) num_paws) 
            (member (call (lookup Dog) (arguments)) num_paws)))
)