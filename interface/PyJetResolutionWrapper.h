#ifndef PhysicsTools_NanoAODTools_PyJetResolutionWrapper_h
#define PhysicsTools_NanoAODTools_PyJetResolutionWrapper_h

#include "JetMETCorrections/Modules/interface/JetResolution.h"

#include "CondFormats/JetMETObjects/interface/JetResolutionObject.h"

#include <string>

class PyJetResolutionWrapper : public JME::JetResolution
{
 public:
  PyJetResolutionWrapper(const std::string& filename);
  PyJetResolutionWrapper(const JME::JetResolutionObject& object);
  PyJetResolutionWrapper();
};

#endif
