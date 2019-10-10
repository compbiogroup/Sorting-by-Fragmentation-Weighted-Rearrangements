#!/bin/bash

echo "Generating input ..."

echo "Unsigned ..."

size=10
nperms=1000
for i in {1..99}
do
  echo "n = $size..."
  ./generate-unsigned --size $size --nperms $nperms > inputs/perm_$size.in
  let "size=10+($i*5)"
done

size=10

for i in {1..99}
do
  echo "n = $size..."
  ./generate-signed --size $size --nperms $nperms > inputs/sig_perm_$size.in
  let "size=10+($i*5)"
done
