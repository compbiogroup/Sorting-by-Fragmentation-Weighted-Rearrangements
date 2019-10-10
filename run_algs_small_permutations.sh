#!/bin/bash

# echo "Running algorithms - small permutations"
# echo "########################################"
# echo "Unsigned"
# echo "########################################"

DATE=`date +%Y-%m-%d`
echo "" > "$DATE"_small.result
nperm=1
for i in {2..10}
do
  let "nperm=$nperm*$i"
  #echo "n = $i"
  #echo "nperm = $nperm"
  ./prog -a r -n $i -q $nperm -s 0 -i inputs/perm_$i.in -v 2 >> "$DATE"_small.result
  ./prog -a r_g -n $i -q $nperm -s 0 -i inputs/perm_$i.in -v 2 >> "$DATE"_small.result
  ./prog -a t -n $i -q $nperm -s 0 -i inputs/perm_$i.in -v 2 >> "$DATE"_small.result
  ./prog -a t_g -n $i -q $nperm -s 0 -i inputs/perm_$i.in -v 2 >> "$DATE"_small.result
  ./prog -a rt -n $i -q $nperm -s 0 -i inputs/perm_$i.in -v 2 >> "$DATE"_small.result
  ./prog -a rt_g -n $i -q $nperm -s 0 -i inputs/perm_$i.in -v 2 >> "$DATE"_small.result
done

# echo "########################################"
# echo "Signed"
# echo "########################################"

nperm=2
for i in {2..9}
do
  let "nperm=$nperm*$i*2"
  #echo "n = $i"
  #echo "nperm = $nperm"
  ./prog -a sr -n $i -q $nperm -s 1 -i inputs/sig_perm_$i.in -v 2 >> "$DATE"_small.result
  ./prog -a sr_g -n $i -q $nperm -s 1 -i inputs/sig_perm_$i.in -v 2 >> "$DATE"_small.result
  ./prog -a srt -n $i -q $nperm -s 1 -i inputs/sig_perm_$i.in -v 2 >> "$DATE"_small.result
  ./prog -a srt_g -n $i -q $nperm -s 1 -i inputs/sig_perm_$i.in -v 2 >> "$DATE"_small.result
done
