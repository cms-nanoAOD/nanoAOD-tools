#include "PhysicsTools/NanoAODTools/interface/PyJetParametersWrapper.h"

#include <algorithm>

PyJetParametersWrapper::PyJetParametersWrapper()
  : JME::JetParameters()
{}

//PyJetParametersWrapper::PyJetParametersWrapper(const PyJetParametersWrapper& rhs)
//  : JME::JetParameters(rhs)
//{}

PyJetParametersWrapper::PyJetParametersWrapper(std::initializer_list<typename value_type::value_type> init)
  : JME::JetParameters(init)
{}
