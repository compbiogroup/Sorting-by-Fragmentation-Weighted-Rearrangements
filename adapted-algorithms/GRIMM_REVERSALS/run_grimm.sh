#!/bin/bash

tam=10
max=500
while [ $tam -le $max ]
do
    for j in {1..3}
    do
      if [ "$tam" -le "$max" ]; then
        echo "n = $tam"
        mkdir -p output/perm_$tam
	      mkdir -p output/20%_$tam
        python2.7 checkgrimm.py $tam ../inputs/sig_perm_$tam.in perm
	      python2.7 checkgrimm.py $tam ../inputs/20%/sr_$tam.in 20% 
        let "tam=$tam+5"
      fi
    done
    wait
done