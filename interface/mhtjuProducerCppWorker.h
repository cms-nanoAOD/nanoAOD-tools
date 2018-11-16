#ifndef PhysicsTools_NanoAODTools_mhtjuProducerCppWorker_h
#define PhysicsTools_NanoAODTools_mhtjuProducerCppWorker_h

#include <utility>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
//#include "DataFormats/Math/interface/LorentzVector.h"
#include <TLorentzVector.h>

class mhtjuProducerCppWorker {

public:

  mhtjuProducerCppWorker(){}

  void setJets(TTreeReaderValue<unsigned> *nJet_, TTreeReaderArray<float> *Jet_pt_, TTreeReaderArray<float> *Jet_eta_, TTreeReaderArray<float> *Jet_phi_, TTreeReaderArray<int> *Jet_puId_, 
	       TTreeReaderArray<float> *Jet_chHEF_, TTreeReaderArray<float> *Jet_neHEF_,  TTreeReaderArray<int> *Jet_electronIdx1_, TTreeReaderArray<int> *Jet_electronIdx2_, TTreeReaderArray<int> *Jet_muonIdx1_,
	       TTreeReaderArray<int> *Jet_muonIdx2_, TTreeReaderArray<int> *Jet_nElectrons_, TTreeReaderArray<int> *Jet_nMuons_){
    nJet = nJet_; Jet_pt = Jet_pt_; Jet_eta = Jet_eta_; Jet_phi = Jet_phi_; Jet_puId = Jet_puId_; Jet_chHEF = Jet_chHEF_; Jet_neHEF = Jet_neHEF_; Jet_electronIdx1 = Jet_electronIdx1_; Jet_electronIdx2 = Jet_electronIdx2_;
    Jet_muonIdx1 = Jet_muonIdx1_; Jet_muonIdx2 = Jet_muonIdx2_; Jet_nElectrons = Jet_nElectrons_; Jet_nMuons = Jet_nMuons_;
  }
  void setElectron(TTreeReaderValue<unsigned> *nElectron_, TTreeReaderArray<float> *Electron_pt_, TTreeReaderArray<float> *Electron_phi_, TTreeReaderArray<float> *Electron_eta_, TTreeReaderArray<int> *Electron_cutBased_, TTreeReaderArray<int> *Electron_jetIdx_){
    nElectron = nElectron_; Electron_pt = Electron_pt_; Electron_phi = Electron_phi_; Electron_eta = Electron_eta_; Electron_cutBased = Electron_cutBased_; Electron_jetIdx = Electron_jetIdx_;
  }
  void setMuon(TTreeReaderValue<unsigned> *nMuon_, TTreeReaderArray<float> *Muon_pt_, TTreeReaderArray<float> *Muon_phi_, TTreeReaderArray<float> *Muon_eta_, TTreeReaderArray<bool> *Muon_softId_, TTreeReaderArray<bool> *Muon_mediumId_, TTreeReaderArray<bool> *Muon_tightId_, TTreeReaderArray<int> *Muon_jetIdx_){
    nMuon = nMuon_; Muon_pt = Muon_pt_; Muon_phi = Muon_phi_; Muon_eta = Muon_eta_; Muon_softId = Muon_softId_; Muon_mediumId = Muon_mediumId_; Muon_tightId = Muon_tightId_; Muon_jetIdx = Muon_jetIdx_;
  }
  void setGen(TTreeReaderValue<unsigned> *nGenPart_, TTreeReaderArray<float> *GenPart_pt_, TTreeReaderArray<int> *GenPart_pdgId_){
    nGenPart = nGenPart_; GenPart_pt = GenPart_pt_; GenPart_pdgId = GenPart_pdgId_;
  }


  std::pair<float,float> getHT();
  float ptZCorr(bool);
  void reportHT();

private:
  TTreeReaderValue<unsigned> *nJet = nullptr;
  TTreeReaderArray<float> *Jet_pt = nullptr;
  TTreeReaderArray<float> *Jet_eta = nullptr;
  TTreeReaderArray<float> *Jet_phi = nullptr;
  TTreeReaderArray<int> *Jet_puId = nullptr;
  TTreeReaderArray<float> *Jet_chHEF = nullptr;
  TTreeReaderArray<float> *Jet_neHEF = nullptr;
  TTreeReaderArray<int> *Jet_electronIdx1 = nullptr;
  TTreeReaderArray<int> *Jet_electronIdx2 = nullptr;
  TTreeReaderArray<int> *Jet_muonIdx1 = nullptr;
  TTreeReaderArray<int> *Jet_muonIdx2 = nullptr;
  TTreeReaderArray<int> *Jet_nElectrons = nullptr;
  TTreeReaderArray<int> *Jet_nMuons = nullptr;
  
  TTreeReaderValue<unsigned> *nElectron = nullptr;
  TTreeReaderArray<float> *Electron_pt = nullptr;
  TTreeReaderArray<float> *Electron_phi = nullptr;
  TTreeReaderArray<float> *Electron_eta = nullptr;
  TTreeReaderArray<int> *Electron_cutBased = nullptr;
  TTreeReaderArray<int> *Electron_jetIdx = nullptr;

  TTreeReaderValue<unsigned> *nMuon = nullptr;
  TTreeReaderArray<float> *Muon_pt = nullptr;
  TTreeReaderArray<float> *Muon_phi = nullptr;
  TTreeReaderArray<float> *Muon_eta = nullptr;
  TTreeReaderArray<bool> *Muon_softId = nullptr;
  TTreeReaderArray<bool> *Muon_mediumId = nullptr;
  TTreeReaderArray<bool> *Muon_tightId = nullptr;
  TTreeReaderArray<int> *Muon_jetIdx = nullptr;

  TTreeReaderValue<unsigned> *nGenPart = nullptr;
  TTreeReaderArray<float> *GenPart_pt = nullptr;
  TTreeReaderArray<int> *GenPart_pdgId = nullptr;

};

#endif
