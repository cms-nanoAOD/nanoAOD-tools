#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionScaleFactorWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/PyJetParametersWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/WeightCalculatorFromHistogram.h"
#include "PhysicsTools/NanoAODTools/interface/ReduceMantissa.h"
#include "PhysicsTools/NanoAODTools/interface/LeptonEfficiencyCorrectorCppWorker.h"

PyJetResolutionWrapper jetRes;
PyJetResolutionScaleFactorWrapper jetResScaleFactor;
PyJetParametersWrapper jetParams;
WeightCalculatorFromHistogram wcalc;
ReduceMantissaToNbitsRounding red(12);
LeptonEfficiencyCorrectorCppWorker lepSF;
