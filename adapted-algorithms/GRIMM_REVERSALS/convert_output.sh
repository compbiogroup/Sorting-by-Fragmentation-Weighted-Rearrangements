#!/bin/bash

g++ convert_output.cpp -o convert_output

tam=10
max=500
nperm=1000
echo "n;mean;max;min" > output/grimm_signed_perm.result
while [ $tam -le $max ]
do
    for j in {1..6}
    do
      if [ "$tam" -le "$max" ]; then
        echo "n = $tam"
        mkdir -p output/$tam
        ./convert_output $nperm $tam output/perm_$tam/ ../output/sig_perm_sr_ >> output/grimm_signed_perm.result
        let "tam=$tam+5"
      fi
    done
    wait
done

tam=10
max=500
nperm=1000
echo "n;mean;max;min" > output/grimm_signed_20%.result
while [ $tam -le $max ]
do
    for j in {1..6}
    do
      if [ "$tam" -le "$max" ]; then
        echo "n = $tam"
        mkdir -p output/$tam
        ./convert_output $nperm $tam output/20%_$tam/ ../output/20%_sr_ >> output/grimm_signed_20%.result
        let "tam=$tam+5"
      fi
    done
    wait
done
