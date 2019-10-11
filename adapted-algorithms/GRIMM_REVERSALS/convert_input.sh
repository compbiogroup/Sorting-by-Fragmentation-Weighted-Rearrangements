#!/bin/bash

echo "Converting Inputs ..."

g++ convert_input.cpp -o convert_input

for ((tam=15; tam<=50; tam=$tam+5));
do
  echo "Size $tam..."
  ./convert_input 1000 $tam < ../inputs/perm_$tam.in > ../inputs/grim_perm_$tam.in
done
