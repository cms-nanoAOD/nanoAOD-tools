#ifndef PhysicsTools_NanoAODTools_PyJetResolutionScaleFactorWrapper_h
#define PhysicsTools_NanoAODTools_PyJetResolutionScaleFactorWrapper_h

#include "JetMETCorrections/Modules/interface/JetResolution.h"

#include "CondFormats/JetMETObjects/interface/JetResolutionObject.h"

#include <string>

class PyJetResolutionScaleFactorWrapper : public JME::JetResolutionScaleFactor
{
 public:
  PyJetResolutionScaleFactorWrapper(const std::string& filename);
  PyJetResolutionScaleFactorWrapper(const JME::JetResolutionObject& object);
  PyJetResolutionScaleFactorWrapper();
};

#endif
