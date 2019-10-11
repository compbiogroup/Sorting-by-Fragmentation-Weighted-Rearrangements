#!/bin/bash

number=$1
nperm=$2

mkdir -p output
rm -f output/rt_$number.dist
rm -f output/rt_$number.sort

rm -f output/rt_20%_$number.dist
rm -f output/rt_20%_$number.sort

file="../inputs/perm_$number.in"
for line in `head -n $nperm $file`; do
    sorting=`python2.7 unsigned_walter1998.py $line output/rt_$number.dist output/rt_$number.sort`
done
file2="../inputs/20%/rt_$number.in"
for line in `head -n $nperm $file2`; do
    sorting=`python2.7 unsigned_walter1998.py $line output/rt_20%_$number.dist output/rt_20%_$number.sort`
done