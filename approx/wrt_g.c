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

void alg_2RT_g(permutation_t *p, int verbose, info_t* info) {/*{{{*/
    int i, j, k;
    int best_i, best_j, best_k, best_rearr;
    float best_cost, op_cost;

    int nof_b = nof_RT_breakpoints(p);
    while(nof_b > 0){
      best_cost = -1;

      for(i = 1; i < p->size; i++){
        for(j = i+1; j <= p->size; j++){
          op_cost = (nof_b - nofb_after_rt(p, 'r', i, j, 0, nof_b))/ (fw_r(i, j, p->size) *1.0);
          if(op_cost > best_cost || (op_cost == best_cost && best_rearr == 't')){
            best_i = i;
            best_j = j;
            best_rearr = 'r';
            best_cost = op_cost;
          }
        }
      }

      for(i = 1; i < p->size; i++){
        if(i > 1 && abs(p->pi[i]-p->pi[i-1]) == 1 && abs(p->pi[i+1]-p->pi[i]) == 1){
          continue;
        }
        for(j = i+1; j <= p->size; j++){
          if(abs(p->pi[j]-p->pi[j-1]) == 1 && abs(p->pi[i-1]-p->pi[j]) != 1){
            continue;
          }
          for(k = j+1; k <= p->size+1; k++){
            op_cost = (nof_b - nofb_after_rt(p, 't', i, j, k, nof_b))/ (fw_t(i, j, k, p->size) *1.0);
            if(op_cost > best_cost){
              best_i = i;
              best_j = j;
              best_k = k;
              best_rearr = 't';
              best_cost = op_cost;
            }
          }
        }
      }

      if(best_rearr == 't'){
        op_transposition(p, best_i, best_j, best_k);
        print_verbose(p, verbose, 't', best_i, best_j, best_k);
        info->nmoves++;
        info->weight += fw_t(best_i, best_j, best_k, p->size);
      }else{
        op_reversal(p, best_i, best_j);
        print_verbose(p, verbose, 'r', best_i, best_j, 0);
        info->nmoves++;
        info->weight += fw_r(best_i, best_j, p->size);
      }

      nof_b = nof_RT_breakpoints(p);
    }

    if(!is_identity(p)){
      op_reversal(p, 1, p->size);
      info->nmoves++;
      //weight remains the same
    }

}/*}}}*/
