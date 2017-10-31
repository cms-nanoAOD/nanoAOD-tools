#ifndef PhysicsTools_NanoAODTools_jecUncertProducerCppWorker_h
#define PhysicsTools_NanoAODTools_jecUncertProducerCppWorker_h

#include <memory>
#include <string>
#include <vector>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

class jecUncertProducerCppWorker {

public:

  jecUncertProducerCppWorker(std::string, std::vector<std::string>);

  void setJets(TTreeReaderValue<unsigned> *nJet_, TTreeReaderArray<float> *Jet_pt_, TTreeReaderArray<float> *Jet_eta_){
    nJet = nJet_; Jet_pt = Jet_pt_; Jet_eta = Jet_eta_;
  }

  void doCppOutput(TTree *outputTree, unsigned maxEntries=50);

  std::vector<float> getUnc(unsigned);
  void fillAllUnc();

private:
  TTreeReaderValue<unsigned> *nJet = nullptr;
  TTreeReaderArray<float> *Jet_pt = nullptr;
  TTreeReaderArray<float> *Jet_eta = nullptr;

  unsigned _nUnc = 0;
  std::vector<std::string> _uncerts;
  std::vector<std::unique_ptr<JetCorrectorParameters>> _pars;
  std::vector<std::unique_ptr<JetCorrectionUncertainty>> _unc;

  bool _doCppOutput = false;
  unsigned _maxEntries = 0;
  std::unique_ptr<unsigned> _buff_nJet;
  std::vector<std::unique_ptr<float[]>> _buffers;

};

#endif
