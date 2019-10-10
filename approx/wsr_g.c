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
#include "wr_g.h"

int sr_first_strip_end(permutation_t *p){
  int j = 1;

  while(p->pi[j+1] - p->pi[j] == 1 && j < p->size){
    j++;
  }

  return j;
}

int sr_find_strip_containing(permutation_t *p, int value, int pos){
  int i, j;

  for(i = 1; i <= p->size; i++){
    if(p->pi[i] == value){
      j = i;
    }
  }
  if(pos){
    while(p->pi[j] - p->pi[j-1] == 1){
      j--;
    }
  }else{
    while(p->pi[j] - p->pi[j-1] == 1){
      j--;
    }
  }

  return j;
}

void alg_2SR_g(permutation_t *p, int verbose, info_t* info) {/*{{{*/
    int i, j;
    int best_i, best_j;
    float best_cost, op_cost;

    int nof_b = nof_sig_R_breakpoints(p);
    while(nof_b > 0){
      best_cost = -1;

      for(i = 1; i <= p->size; i++){ // 1 <= i <= j <= n
        if(i > 1 && p->pi[i]-p->pi[i-1] == 1){
          continue;
        }
        for(j = i; j <= p->size; j++){
          op_cost = (nof_b - nofb_after_sig_r(p, i, j, nof_b))/ (fw_r(i, j, p->size) *1.0);
          if(op_cost > best_cost){
            best_i = i;
            best_j = j;
            best_cost = op_cost;
          }
        }
      }

      if(best_cost > 0){
        op_reversal(p, best_i, best_j);
        print_verbose(p, verbose, 'r', best_i, best_j, 0);
        info->nmoves++;
        info->weight += fw_r(best_i, best_j, p->size);
      }else{
        int j = sr_first_strip_end(p);

        if(p->pi[j] == -1){
          int next_j = sr_find_strip_containing(p, p->pi[1] - 1, 0);

          op_reversal(p, next_j, p->size);
          print_verbose(p, verbose, 'r', next_j, p->size, 0);
          info->nmoves++;
          info->weight += fw_r(next_j, p->size, p->size);

        }else if(p->pi[j] == p->size){
          int next_j = sr_find_strip_containing(p, p->pi[1] - 1, 1);

          op_reversal(p, next_j, p->size);
          print_verbose(p, verbose, 'r', next_j, p->size, 0);
          info->nmoves++;
          info->weight += fw_r(next_j, p->size, p->size);
        }else{
          op_reversal(p, 1, j);
          print_verbose(p, verbose, 'r', 1, j, 0);
          info->nmoves++;
          info->weight += fw_r(1, j, p->size);
        }
      }

      nof_b = nof_sig_R_breakpoints(p);
    }

    if(!is_identity(p)){
      op_reversal(p, 1, p->size);
      print_verbose(p, verbose, 'r', 1, p->size, 0);
      info->nmoves++;
      //weight remains the same
    }

}/*}}}*/
