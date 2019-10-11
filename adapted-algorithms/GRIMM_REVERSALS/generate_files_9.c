#define _LARGEFILE64_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define _GNU_SOURCE
#include <getopt.h>
#include <float.h>
#include <math.h>
#include <limits.h>

void translate(char* str)
{
    if (str[0] == '\0')
        return;

    // Start traversing from second chracter
    for (int i=1; str[i] != '\0'; i++)
    {
        if (str[i]==',')
        {
            str[i] = ' ';
        }
    }
    return;
}

int main(){
  FILE *fout, *fin;
  char strout[500], strprm[6500];
  char command[10000];
  fin = fopen("../inputs/sig_perm_9.in", "r");
  int nperms = 10;
  for(int i = 0; i < nperms; i++){
    printf("%d\n", i);

    fscanf(fin, "%s", strprm);
    sprintf(strout, "tmp.in");
    fout = fopen(strout, "w");

    fprintf(fout,">1\n");
    fprintf(fout,"1 2 3 4 5 6 7 8 9\n");
    fprintf(fout,">2\n");
    translate(strprm);
    fprintf(fout,"%s\n", strprm);

    fclose(fout);
    sprintf(command, "./grimm -f tmp.in -L -d -g 1,2 -S 2 > tmp_%d.out", i);

    system(command);

  }

}
