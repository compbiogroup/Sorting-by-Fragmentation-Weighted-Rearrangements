#!/bin/bash

tam=10
max=0
while [ $tam -le $max ]
do
    for j in {1..3}
    do
      if [ "$tam" -le "$max" ]; then
        echo "n = $tam"
        file="../inputs/perm_$tam.in"
	file2="../inputs/20%/r_$tam.in"
        mkdir -p output/perm_$tam
	mkdir -p output/20%_$tam
	rm -f lin_perm_$tam.in
	rm -f lin_20%_r_$tam.in
        python2.7 checksiglin.py $file 1000 ../inputs/lin_perm_$tam.in
	python2.7 checksiglin.py $file2 1000 ../inputs/lin_20%_r_$tam.in
        let "tam=$tam+5"
      fi
    done
    wait
done


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
        python2.7 checkgrimm.py $tam ../inputs/lin_perm_$tam.in perm 
        python2.7 checkgrimm.py $tam ../inputs/lin_20%_r_$tam.in 20% 
	let "tam=$tam+5"
      fi
    done
    wait
done