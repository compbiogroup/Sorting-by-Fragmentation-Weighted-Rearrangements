/***********************************************************
 * Created: Wed 02 Aug 2017 02:00:22 PM BRST
 *
 * Author: Alexsandro Alexandrino, a.o.alexsandro@gmail.com
 *
 ***********************************************************/

#include <stdio.h>
#include <stdlib.h>
#include "../util.h"
#include "../permutations.h"
#include "../rearrangements.h"
#include "wt.h"

void alg_2T(permutation_t *p, int verbose, info_t* info) {/*{{{*/
    int i, j, next_strip;

    next_strip = p->size;

    while (!is_identity(p)) {
        j = p->inv_pi[next_strip];
        i = j;
        while(i > 1 && p->pi[i] == p->pi[i-1] + 1){
          i--;
        }

        if(j == next_strip){
          //updates value of the next (out of place) strip
          next_strip = i-1; //\pi_i is in the right position, so \pi_i = i
        }else{
          //if the largest strip is in the wrong position, the first transposition will be t(1,j+1,n+1)
          op_prefix_transposition(p, j+1, next_strip +1 );
          print_verbose(p, verbose, 't', 1, j+1, next_strip+1);

          info->weight += fw_t(1, j+1, next_strip+1, p->size);
          info->nmoves++;
        }

    }
}/*}}}*/
