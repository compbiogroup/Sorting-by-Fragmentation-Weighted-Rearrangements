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
#include "../breakpoints.h"
#include "wt_g.h"

void alg_2T_g(permutation_t *p, int verbose, info_t* info) {/*{{{*/
    int i, j, k;
    int best_i, best_j, best_k;
    float best_cost, op_cost;

    int nof_b = nof_T_breakpoints(p);
    while(nof_b > 0){
      int begin= 1;
      int end = p->size;
      while(p->pi[begin] == begin && begin < p->size){
        begin++;
      }
      while(p->pi[end] == end && end >1){
        end--;
      }

      best_cost = -1;

      for(i = begin; i < end; i++){
        if(i > 1 && p->pi[i]-p->pi[i-1] == 1){
          continue;
        }
        for(j = i+1; j <= end; j++){
          if(p->pi[j]-p->pi[j-1] == 1){
            continue;
          }
          for(k = j+1; k <= end+1; k++){
            op_cost = (nof_b - nofb_after_t(p, i, j,k, nof_b))/ (fw_t(i, j, k, p->size) *1.0);
            if(op_cost > best_cost){
              best_i = i;
              best_j = j;
              best_k = k;
              best_cost = op_cost;
            }
          }
        }
      }

      op_transposition(p, best_i, best_j, best_k);
      print_verbose(p, verbose, 't', best_i, best_j, best_k);
      info->nmoves++;
      info->weight += fw_t(best_i, best_j, best_k, p->size);

      nof_b = nof_T_breakpoints(p);
    }

}/*}}}*/
