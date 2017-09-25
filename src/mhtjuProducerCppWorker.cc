#include "../interface/mhtjuProducerCppWorker.h"

std::vector<float> mhtjuProducerCppWorker::getHT(){

    math::XYZTLorentzVectorF ht(0,0,0,0);

    unsigned n = (*nJet).Get()[0];
    for (unsigned i=0; i<n; i++){
      ht += math::PtEtaPhiMLorentzVectorF((*Jet_pt)[i],0,(*Jet_phi)[i],0);
    }

    std::vector<float> result = {ht.Pt(),ht.Phi()};
    return result;

};
