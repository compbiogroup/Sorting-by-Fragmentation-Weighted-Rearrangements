#!/bin/bash

# echo "Running algorithms - permutations n = 10 ... 1000"
#
# echo "########################################"
# echo "Unsigned"
# echo "########################################"


DATE=`date +%Y-%m-%d`
echo "" > "$DATE"_unsigned.result

inc=10
nperm=1000 #number of permutations
n=20 #initial size
last_n=20 #initial size of first iteration
max=100 #max value for first iteration
global_max=500 #max value for all iterations

declare -a algs=("r" "r_g" "t" "t_g" "rt" "rt_g")

while [ $max -le $global_max ]
do
  for a in "${algs[@]}"
  do
    let "n=$last_n"
    #echo "$a"
    while [ $n -le $max ]
    do
      for j in {1..5}
      do
        echo "n = $n"
        if [ "$n" -le "$max" ]; then
    	     ./prog -a $a -n $n -q $nperm -s 0 -i inputs/perm_$n.in -v 2 >> "$DATE"_unsigned.result &
        fi
        let "n=$n+$inc"
      done
      wait
    done
  done
  let "last_n=$max+$inc"
  let "max=$max+100"
done
