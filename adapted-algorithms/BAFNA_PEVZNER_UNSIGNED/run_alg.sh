#!/bin/bash

number=$1
nperm=$2

rm -f output/t_$number.dist
rm -f output/t_$number.sort
rm -f output/t_20%_$number.dist
rm -f output/t_20%_$number.sort

file="../inputs/perm_$number.in"
for line in `head -n $nperm $file`; do
    sorting=`python2.7 real_bafna_pevzner.py $line output/t_$number.dist output/t_$number.sort`
done

file="../inputs/20%/t_$number.in"
for line in `head -n $nperm $file`; do
    sorting=`python2.7 real_bafna_pevzner.py $line output/t_20%_$number.dist output/t_20%_$number.sort`
done