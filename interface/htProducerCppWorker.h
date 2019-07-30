#ifndef PhysicsTools_NanoAODTools_htProducerCppWorker_h
#define PhysicsTools_NanoAODTools_htProducerCppWorker_h

#include <utility>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "DataFormats/Math/interface/LorentzVector.h"

class htProducerCppWorker {

public:

  htProducerCppWorker(){}

  void setJets(TTreeReaderValue<unsigned> *nJet_, TTreeReaderArray<float> *Jet_pt_){
    nJet = nJet_; Jet_pt = Jet_pt_; 
  }

  float getHT();

private:
  TTreeReaderValue<unsigned> *nJet = nullptr;
  TTreeReaderArray<float> *Jet_pt = nullptr;

};

#endif
