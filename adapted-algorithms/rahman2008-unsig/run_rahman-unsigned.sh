#!/bin/bash

for ((number=10; number<=100; number=$number+10)); do
    file="/home/andre/perm-database/n$number.perm"
    for line in `cat $file`; do
        canonicals=`python rahman2008lin.py $line unsig/rahman.n$number.p2.dist unsig/rahman.n$number.p2.sort`
    done
done
