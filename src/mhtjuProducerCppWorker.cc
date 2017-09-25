#include "../interface/mhtjuProducerCppWorker.h"

std::pair<float,float> mhtjuProducerCppWorker::getHT(){

    math::XYZTLorentzVectorF ht(0,0,0,0);

    unsigned n = (*nJet).Get()[0];
    for (unsigned i=0; i<n; i++){
      ht += math::PtEtaPhiMLorentzVectorF((*Jet_pt)[i],0,(*Jet_phi)[i],0);
    }

    return std::pair<float,float>(ht.Pt(),ht.Phi());

};
