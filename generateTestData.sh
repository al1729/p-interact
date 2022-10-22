 #!/bin/bash

# script for iteratively generating stories to be used as test data 

# genre is currently hardcoded as 'na', however, if we want to do it with different genres, we can replace 'na' with a random selection from a list of genres or iterate over a list of genres doing a different one each time etc

# temperature, top_p, frequency_penalty parameters (used in the generate function) can be passed in as command line args (they're currently hardcoded) 

for n in {1..5};
do
    echo n = $n
    python3 game.py --testData "yes" --temp 0.4 --top_p 0.2 --freq_pen 0.69 <<EOF 
na
$(( $RANDOM % 4 + 1 ))
$(( $RANDOM % 4 + 1 ))
$(( $RANDOM % 4 + 1 ))
EOF
done
