#!/bin/bash

# echo "Running algorithms - permutations n = 10 ... 1000"
#
# echo "########################################"
# echo "Signed"
# echo "########################################"


DATE=`date +%Y-%m-%d`
echo "" > "$DATE"_signed.result

inc=10
n=10 #number of permutations
nperm=1000 #initial size
last_n=10 #initial size of first iteration
max=100 #max value for first iteration
global_max=500 #max value for all iterations

declare -a algs_signed=("sr" "sr_g" "srt" "srt_g")

while [ $max -le $global_max ]
do
  for a in "${algs_signed[@]}"
  do
    let "n=$last_n"
    #echo "$a"
    while [ $n -le $max ]
    do
      for j in {1..5}
      do
        echo "n = $n"
        if [ "$n" -le "$max" ]; then
          ./prog -a $a -n $n -q $nperm -s 1 -i inputs/sig_perm_$n.in -v 2 >> "$DATE"_signed.result &
        fi
        let "n=$n+$inc"
      done
      wait
    done
  done
  let "last_n=$max+$inc"
  let "max=$max+100"
done
