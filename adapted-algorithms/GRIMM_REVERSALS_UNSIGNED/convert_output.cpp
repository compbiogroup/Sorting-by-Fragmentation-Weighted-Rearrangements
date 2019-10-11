//Author: Guilherme Henrique Santos Miranda
//sorry by grammar mistakes :D
#include <bits/stdc++.h>
#include <limits.h>
using namespace std;

int fw_r(int i, int j, int size);

int fw_r(int i, int j, int size){
  if(i == 1 && j == size){
    return 0;
  }else if(i == 1 || j == size){
    return 1;
  }else{
    return 2;
  }
}

int main (int argc, char **argv){


  long double total_approx = 0;
  double approx = 0;
  double max_approx = 0;
  double min_approx = LONG_MAX;
  int lower_bound;


  if (argc != 5){
    printf ("Usage: ./%s m n dir", argv[0]);
    puts("where:\n n is the size of permutation;"
        "\nm is the amount of permutations at inputfiles;"
        "\nand dir is a string in the form local/of/input/.");
    return 0;
  }

  FILE *file, *filelb;
  char filename[30], filenamelb[30], str[100], dir[100], dir_lb[100], path[130];
  int gen1, gen2, i, j, n, m;


  //Initializing variables ...
  strcpy(dir, argv[3]);
  strcpy(dir_lb, argv[4]);
  n = atoi(argv[2]);
  m = atoi(argv[1]);

  sprintf (filenamelb, "%s%d.out", dir_lb, n);
  // -----------------------
  filelb = fopen(filenamelb, "r");
  
  for (int k = 1; k <= m; k++) {
      //TODO change to include approx mean

      approx = 0;//approx of current sorting

      sprintf (filename, "%d.out", k);

      strcpy(path, dir);
      strcat(path, filename);
      file = fopen(path, "r");
      bool flag = false;

      //printf ("reading %s...\n", filename);
      while (fscanf (file, "%s", str) != EOF){
        if (str[0] == '=' and str[2] == '=')//this is not a cool strategy, but it works.
          break;
      }
      while (fscanf(file, "%s", str) != EOF){
        if (strcmp(str, "gene") == 0){
          if (!flag)
            fscanf (file, "%d", &gen1);
          else{
            fscanf (file, "%d", &gen2);
            int i,j;
            i = gen1 + 1;
            j = gen2 + 1;

            approx += fw_r(i,j,n);

            //printf("%d %d %d\n", i, j, approx);

          }
          flag = !flag;
        }

      }
      //printf("%ld\n", approx);
      fscanf (filelb, "%d", &lower_bound);
      // printf("%d\n", lower_bound);
      if(lower_bound == 0){
        approx = 1;
      }else{
        approx = approx / (1.0*lower_bound);
      }
      total_approx += approx;
      if(approx > max_approx){
        max_approx = approx;
      }

      if(approx < min_approx){
        min_approx = approx;
      }
      fclose(file);

  }

  total_approx = total_approx / (m*1.0);
  
  printf("%d;%Lf;%lf;%lf\n", n, total_approx, max_approx, min_approx);

}
