/***********************************************************
 * Created: Wed 02 Aug 2017 02:00:22 PM BRST
 *
 * Author: Alexsandro Alexandrino, a.o.alexsandro@gmail.com
 *
 ***********************************************************/

#define _LARGEFILE64_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define _GNU_SOURCE
#include <getopt.h>
#include <float.h>
#include <math.h>
#include <limits.h>

#include "util.h"
#include "permutations.h"
#include "breakpoints.h"
#include "approx/wr.h"
#include "approx/wr_g.h"
#include "approx/wt.h"
#include "approx/wt_g.h"
#include "approx/wrt_g.h"
#include "approx/wsr.h"
#include "approx/wsr_g.h"
#include "approx/wsrt_g.h"

void print_help(char progname[]);
void print_algs();

int main(int argc, char *argv[]){

  extern char *optarg;
  char op, *alg_name = NULL, *output_filename = NULL, strprm[6500], signal = 0;
  int verbose = 1, size = 0, nperms = 0, n;
  FILE *fin = NULL, *fout = NULL;
  permutation_t p;
  info_t info;

//   long double total_weight = 0;
//   long max_weight = 0;
//   long min_weight = LONG_MAX;
//   long double mean_break = 0;

  struct option longopts[] = {
      {"algorithm", 1, NULL, 'a'},
      {"size", 1, NULL, 'n'},
      {"signal", 1, NULL, 's'},
      {"nperms", 1, NULL, 'q'},
      {"input", 1, NULL, 'i'},
      {"output", 1, NULL, 'o'},
      {"verbose", 1, NULL, 'v'},
      {"help", 0, NULL, 'h'},
  };

  while ((op = getopt_long(argc, argv, "a:n:s:q:i:o:x:v:h", longopts, NULL)) != -1) {
      switch (op) {
          case 'a':
              alg_name = optarg;
              break;
          case 'n':
              size = atoi(optarg);
              break;
          case 's':
              signal = atoi(optarg);
              break;
          case 'q':
              nperms = atoi(optarg);
              break;
          case 'i':
              fin = fopen(optarg, "r");
              break;
          case 'o':
              output_filename = optarg;
              break;
          case 'v':
              verbose = atoi(optarg);
              break;
          case 'h':
              print_help(argv[0]);
              exit(0);
      }
  }

  create_permutation(&p, size, signal);
  p.alpha = 1;

  fout = fopen(output_filename, "w");

  for (n = 1; n <= nperms; n++) {
    fscanf(fin, "%s", strprm);

    //fprintf(fout, "%s;", strprm);

    init_info(&info);
    prmfill_fromstr(strprm, &p);

    int nof_b = 0;

    if (!strcmp(alg_name, "r")){
      nof_b = nof_R_breakpoints(&p);
    } else if (!strcmp(alg_name, "r_g")){
      nof_b = nof_R_breakpoints(&p);
    } else if (!strcmp(alg_name, "t")){
      nof_b = nof_T_breakpoints(&p);
    }else if (!strcmp(alg_name, "t_g")){
      nof_b = nof_T_breakpoints(&p);
    }else if (!strcmp(alg_name, "rt")){
      nof_b = nof_RT_breakpoints(&p);
    }else if (!strcmp(alg_name, "rt_g")){
      nof_b = nof_RT_breakpoints(&p);
    }else if (!strcmp(alg_name, "sr")){
      nof_b = nof_sig_R_breakpoints(&p);
    }else if (!strcmp(alg_name, "sr_g")){
      nof_b = nof_sig_R_breakpoints(&p);
    }else if (!strcmp(alg_name, "srt")){
      nof_b = nof_sig_RT_breakpoints(&p);
    }else if (!strcmp(alg_name, "srt_g")){
      nof_b = nof_sig_RT_breakpoints(&p);
    }

    fprintf(fout, "%d\n", nof_b);
    fflush(fout);
  }

  fclose(fout);
  fclose(fin);
  destroy_permutation(&p);
  return 0;
}

void print_help(char progname[]) {/*{{{*/
    printf("usage: %s [options] \n", progname);
    printf("options: \n");
    printf("\t--algorithm <name> or -a <name>: name of the algorithm to be tested. They can be:\n");
    print_algs();
    printf("\t--size <size> or -n <size>: size of the permutations to be tested\n");
    printf("\t--nperms <n> or -q <n>: number of permutations to be tested\n");
    printf("\t--signal <s> or -s <s>: signal (0=unsigned, 1=signed)\n");
    printf("\t--input <file> or -i <file>: gets the input from <file>\n");
    printf("\t It must contain <nperms> of size <size>, in which the elements are separated by comma\n");
    printf("\t--verbose <n> or -v <n>: define the level of information to be printed\n");
    printf("\t\tuse 2 for distance\n");
    printf("\t\tuse 3 for sorting sequence\n");
    printf("\t\tuse 4 for both\n");
    printf("\t\tuse 5 for rearrangement events sequence\n");
    printf("\n");
}/*}}}*/

void print_algs(){
  printf("\t\t r -> sorting permutations by fragmentation-weighted reversals\n");
  printf("\t\t r_g -> greedy alg for sorting permutations by fragmentation-weighted reversals\n");
  printf("\t\t t -> sorting permutations by fragmentation-weighted transpositions\n");
  printf("\t\t t -> greedy alg for sorting permutations by fragmentation-weighted transpositions\n");
  printf("\t\t rt -> sorting permutations by fragmentation-weighted reversals and transpositions\n");
  printf("\t\t sr -> sorting permutations by fragmentation-weighted signed reversals\n");
  printf("\t\t sr_g -> greedy alg for sorting signed permutations by fragmentation-weighted reversals\n");
  printf("\t\t srt -> sorting permutations by fragmentation-weighted signed reversals and transpositions\n");
}
