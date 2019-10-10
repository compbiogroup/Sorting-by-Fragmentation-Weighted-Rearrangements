#!/bin/bash

echo "Generating input ..."

echo "Unsigned ..."

for i in {2..10}
do
  echo "n = $i..."
  ./generate-small-unsigned $i > inputs/perm_$i.in
done

echo "Signed ..."

for i in {2..9}
do
  echo "n = $i..."
  ./generate-small-signed $i > inputs/sig_perm_$i.in
done
