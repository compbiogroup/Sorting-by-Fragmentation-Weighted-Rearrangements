#!/bin/bash

number=$1
nperm=$2

mkdir -p output
rm -f output/rt_$number.dist
rm -f output/rt_$number.sort
rm -f output/rt_20%_$number.dist
rm -f output/rt_20%_$number.sort

file="../inputs/sig_perm_$number.in"
sorting=`python2.7 signed_walter1998.py $file output/rt_$number.dist output/rt_$number.sort $nperm`
file2="../inputs/20%/srt_$number.in"
sorting=`python2.7 signed_walter1998.py $file2 output/rt_20%_$number.dist output/rt_20%_$number.sort $nperm`