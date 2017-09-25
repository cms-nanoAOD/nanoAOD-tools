#include "../interface/jecUncertProducerCppWorker.h"

jecUncertProducerCppWorker::jecUncertProducerCppWorker(std::string unc_factorized_path, std::vector<std::string> vec_uncerts){

  for (auto x : vec_uncerts) {
    _pars.push_back(std::make_unique<JetCorrectorParameters>(unc_factorized_path, x));;
    _unc.push_back(std::make_unique<JetCorrectionUncertainty>(*(_pars.back().get())));
  }

  _nUnc = _unc.size();
  _uncerts = vec_uncerts;

}

void jecUncertProducerCppWorker::doCppOutput(TTree *outputTree, unsigned maxEntries){

  if (_doCppOutput) throw cms::Exception("LogicError","doCppOutput cannot be called twice");
  _doCppOutput = true;
  _maxEntries = maxEntries;
  _buff_nJet.reset(new unsigned);
  if (!(outputTree->GetBranch("nJet"))) outputTree->Branch("nJet",_buff_nJet.get(),"nJet/i");
  for (unsigned i=0; i<_nUnc; i++){
    _buffers.emplace_back(std::unique_ptr<float[]>(new float[_maxEntries]));
    outputTree->Branch(Form("Jet_jecUncert%s",_uncerts[i].c_str()),_buffers[i].get(),Form("Jet_jecUncert%s[nJet]/F",_uncerts[i].c_str()));
  }

}

std::vector<float> jecUncertProducerCppWorker::getUnc(unsigned j){

  if (j>=_nUnc) throw cms::Exception("LogicError","Trying to access uncertainty index beyond boundary");
  auto unc = _unc[j].get();

  std::vector<float> output;

  unsigned n = (*nJet).Get()[0];
  for (unsigned i=0; i<n; i++){
    unc->setJetEta((*Jet_eta)[i]);
    unc->setJetPt((*Jet_pt)[i]);
    output.push_back(unc->getUncertainty(true));
  }

  return output;

}

void jecUncertProducerCppWorker::fillAllUnc(){

  if (!_doCppOutput) throw cms::Exception("LogicError","fillAllUnc only works if output is handled by the worker class");

  unsigned n = (*nJet).Get()[0];
  if (n>_maxEntries) throw cms::Exception("LogicError","Too many jets found in the event, please use a larger maxEntries value");
  *(_buff_nJet.get())=n;

  for (unsigned j=0; j<_nUnc; j++){
    auto unc = _unc[j].get();
    auto buff = _buffers[j].get();
    for (unsigned i=0; i<n; i++){
      unc->setJetEta((*Jet_eta)[i]);
      unc->setJetPt((*Jet_pt)[i]);
      buff[i] = unc->getUncertainty(true);
    }
  }

}
