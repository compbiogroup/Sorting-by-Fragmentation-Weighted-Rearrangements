/***********************************************************
* Created: Wed 06 Aug 2017 02:00:22 PM BRST
*
* Author: Alexsandro Alexandrino, a.o.alexsandro@gmail.com
*
***********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define _GNU_SOURCE
#include <getopt.h>
#include <math.h>

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

void print_algs();
void print_help(char progname[]);
void test_inputs(int size, char *strprm, char *alg_name);

int main(int argc, char *argv[]) {

    extern char *optarg;
    char op, *alg_name = NULL, *strprm = NULL, signal = 0;
    int verbose = 1, size = 0;
    permutation_t p;
    info_t info;

    struct option longopts[] = {
        {"algorithm", 1, NULL, 'a'},
        {"size", 1, NULL, 'n'},
        {"signal", 1, NULL, 's'},
        {"perm", 1, NULL, 'p'},
        {"verbose", 1, NULL, 'v'},
        {"help", 0, NULL, 'h'},
    };

    while ((op = getopt_long(argc, argv, "a:n:s:p:v:h", longopts, NULL)) != -1) {
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
            case 'p':
                strprm = optarg;
                break;
            case 'v':
                verbose = atoi(optarg);
                break;
            case 'h':
                print_help(argv[0]);
                exit(0);
        }
    }

    test_inputs(size, strprm, alg_name);

    create_permutation(&p, size, signal);

    p.alpha = 1;

    prmfill_fromstr(strprm, &p);
    init_info(&info);

    print_permutation(&p);

    int nof_b;

    if (!strcmp(alg_name, "r")){
      nof_b = nof_R_breakpoints(&p);
      alg_2R(&p, verbose, &info);
    } else if (!strcmp(alg_name, "r_g")){
      nof_b = nof_R_breakpoints(&p);
      alg_2R_g(&p, verbose, &info);
    } else if (!strcmp(alg_name, "t")){
      nof_b = nof_T_breakpoints(&p);
      alg_2T(&p, verbose, &info);
    }else if (!strcmp(alg_name, "t_g")){
      nof_b = nof_T_breakpoints(&p);
      alg_2T_g(&p, verbose, &info);
    }else if (!strcmp(alg_name, "rt")){
      nof_b = nof_RT_breakpoints(&p);
      alg_2R(&p, verbose, &info);
    }else if (!strcmp(alg_name, "rt_g")){
      nof_b = nof_RT_breakpoints(&p);
      alg_2RT_g(&p, verbose, &info);
    }else if (!strcmp(alg_name, "sr")){
      nof_b = nof_sig_R_breakpoints(&p);
      alg_2SR(&p, verbose, &info);
    }else if (!strcmp(alg_name, "sr_g")){
      nof_b = nof_sig_R_breakpoints(&p);
      alg_2SR_g(&p, verbose, &info);
    }else if (!strcmp(alg_name, "srt")){
      nof_b = nof_sig_RT_breakpoints(&p);
      alg_2SR(&p, verbose, &info);
    }else if (!strcmp(alg_name, "srt_g")){
      nof_b = nof_sig_RT_breakpoints(&p);
      alg_2SRT_g(&p, verbose, &info);
    }

    printf("%d %Lf\n", info.nmoves, info.weight);

    destroy_permutation(&p);

    return 0;
}


void test_inputs(int size, char *strprm, char *alg_name) {/*{{{*/
    if (size == 0) {
        printf("A size of permutation must be specified.\n");
        exit(0);
    }

    if (!strprm) {
        printf("A permutation must be provided.\n");
        exit(0);
    }

    if (!alg_name) {
        printf("A name of algorithm must be provided.\n");
        exit(0);
    }
}/*}}}*/

void print_algs(){
  printf("\t\t r -> sorting permutations by fragmentation-weighted reversals\n");
  printf("\t\t r_g -> greedy alg for sorting permutations by fragmentation-weighted reversals\n");
  printf("\t\t t -> sorting permutations by fragmentation-weighted transpositions\n");
  printf("\t\t rt -> sorting permutations by fragmentation-weighted reversals and transpositions\n");
  printf("\t\t sr -> sorting permutations by fragmentation-weighted signed reversals\n");
  printf("\t\t sr_g -> greedy alg for sorting signed permutations by fragmentation-weighted reversals\n");
  printf("\t\t srt -> sorting permutations by fragmentation-weighted signed reversals and transpositions\n");
}

void print_help(char progname[]) {/*{{{*/
   printf("usage: %s [options] \n", progname);
   printf("options: \n");
   printf("\t--algorithm <name> or -a <name>: name of the algorithm to be tested. They can be:\n");
   print_algs();
   printf("\t--size <size> or -n <size>: size of the permutation\n");
   printf("\t--perm <p> or -p <p>: permutation to be tested. Example: 1,2,3,4,5,6\n");
   printf("\t--signal <size> or -s <size>: sign of the permutations\n");
   printf("\t--verbose <n> or -v <n>: define the level of information to be printed\n");
   printf("\t\tuse 2 for distance\n");
   printf("\t\tuse 3 for sorting sequence\n");
   printf("\t\tuse 4 for both\n");
   printf("\t\tuse 5 for rearrangement events sequence\n");
   printf("\n");
}/*}}}*/
