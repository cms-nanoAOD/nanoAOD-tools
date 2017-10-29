#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionScaleFactorWrapper.h"

PyJetResolutionScaleFactorWrapper::PyJetResolutionScaleFactorWrapper(const std::string& filename)
   : JME::JetResolutionScaleFactor(filename)
{}
 
PyJetResolutionScaleFactorWrapper::PyJetResolutionScaleFactorWrapper(const JME::JetResolutionObject& object)
  : JME::JetResolutionScaleFactor(object)
{}

PyJetResolutionScaleFactorWrapper::PyJetResolutionScaleFactorWrapper()
  : JME::JetResolutionScaleFactor()
{}
