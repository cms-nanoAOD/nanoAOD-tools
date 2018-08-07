#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/PyJetResolutionScaleFactorWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/PyJetParametersWrapper.h"
#include "PhysicsTools/NanoAODTools/interface/WeightCalculatorFromHistogram.h"
#include "PhysicsTools/NanoAODTools/interface/ReduceMantissa.h"
#include "PhysicsTools/NanoAODTools/interface/EventShapes.h"
#include "PhysicsTools/NanoAODTools/interface/TFEval.h"

namespace {
    PyJetResolutionWrapper jetRes;
    PyJetResolutionScaleFactorWrapper jetResScaleFactor;
    PyJetParametersWrapper jetParams;
    WeightCalculatorFromHistogram wcalc;
    ReduceMantissaToNbitsRounding red(12);
    EventShapes evShapes;
    TFEval tfEval;
    TFEval::BranchAccessor branchAccessor(nullptr);
    TFEval::ArrayFeatureGroup arrayFeatureGroup("blub",10,10,&branchAccessor);
    TFEval::ValueFeatureGroup valueFeatureGroup("blub",10);
    TFEval::Result result;
    TFEval::PyAccessor pyAccessor(nullptr,nullptr);
}
