#ifndef PhysicsTools_NanoAODTools_mhtjuProducerCppWorker_h
#define PhysicsTools_NanoAODTools_mhtjuProducerCppWorker_h

#include <vector>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "DataFormats/Math/interface/LorentzVector.h"

class mhtjuProducerCppWorker {

public:

  mhtjuProducerCppWorker(){};

  void setJets(TTreeReaderValue<unsigned> *nJet_, TTreeReaderArray<float> *Jet_pt_, TTreeReaderArray<float> *Jet_phi_){
    nJet = nJet_; Jet_pt = Jet_pt_; Jet_phi = Jet_phi_;
  }

  std::vector<float> getHT();

private:
  TTreeReaderValue<unsigned> *nJet;
  TTreeReaderArray<float> *Jet_pt;
  TTreeReaderArray<float> *Jet_phi;

};

#endif
