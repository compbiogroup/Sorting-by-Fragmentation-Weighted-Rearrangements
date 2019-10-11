#include <bits/stdc++.h>
using namespace std; 

int main (int argc, char **argv){
  int n, m, val; 

  if (argc != 3)
    puts("Usage: -m -n < txt_input > txt_output, where m, n is the amount of permutations and size of permutations, respectively"); 
  else{
    m = atoi(argv[1]);
    n = atoi(argv[2]);
    puts("> identity");
    for (int i = 0; i < n-1; i++){
      printf ("%d ", i+1);
    }
    printf("%d\n", n);

    for (int j = 0; j < m; j++){
      printf ("> genome %d\n", (j+1)); 
      for (int i = 0 ; i < n-1; i++){
        scanf ("%d,", &val);
        printf ("%d ", val);
      }
      scanf ("%d", &val);
      printf ("%d\n", val);
    }
  }
}
