#ifndef PhysicsTools_NanoAODTools_PyJetParametersWrapper_h
#define PhysicsTools_NanoAODTools_PyJetParametersWrapper_h

#include "CondFormats/JetMETObjects/interface/JetResolutionObject.h"

#include <string>

class PyJetParametersWrapper : public JME::JetParameters
{
 public:
  PyJetParametersWrapper();
  //PyJetParametersWrapper(const PyJetParametersWrapper& rhs);
  PyJetParametersWrapper(std::initializer_list<typename value_type::value_type> init);
};

#endif
