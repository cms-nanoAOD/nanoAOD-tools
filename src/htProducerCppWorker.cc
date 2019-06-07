#include "../interface/htProducerCppWorker.h"

float htProducerCppWorker::getHT(){

    float ht(0.0);

    unsigned n = (*nJet).Get()[0];
    for (unsigned i=0; i<n; i++){
      ht += (*Jet_pt)[i];
    }

    return ht; 

};
