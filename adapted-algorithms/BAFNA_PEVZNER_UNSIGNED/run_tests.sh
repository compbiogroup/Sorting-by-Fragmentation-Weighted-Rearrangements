tam=10
max=500
while [ $tam -le $max ]
do
    for j in {1..6}
    do
      if [ "$tam" -le "$max" ]; then
        echo "n = $tam"
        bash run_alg.sh $tam 1000 &
        let "tam=$tam+5"
      fi
    done
    wait
done