#include "../interface/jecUncertProducerCppWorker.h"

jecUncertProducerCppWorker::jecUncertProducerCppWorker(std::string unc_factorized_path, std::vector<std::string> vec_uncerts){

  for (auto x : vec_uncerts) {
    _pars.push_back(std::make_unique<JetCorrectorParameters>(unc_factorized_path, x));;
    _unc.push_back(std::make_unique<JetCorrectionUncertainty>(*(_pars.back().get())));
  }

  _nUnc = _unc.size();

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
