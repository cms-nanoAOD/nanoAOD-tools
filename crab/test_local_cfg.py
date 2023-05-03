import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this would take care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.examples.exampleModule import *

from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from  PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.tauCorrProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muSFProducer2 import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.ggTemporaryScale import *

import sys
print sys.argv
suffix=sys.argv[2].split("=")[1]
analysis=sys.argv[3].split("=")[1]


selection='''Sum$(Photon_pt > 18 && (Photon_isScEtaEB || Photon_isScEtaEE) && Photon_electronVeto > 0.5 && Photon_hoe < 0.08) > 1'''


#files=[ '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8033.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8034.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8035.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8036.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8037.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8038.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8039.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8040.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8041.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_804.root' ]

#files=[ '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8042.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8043.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8044.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8045.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8046.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8047.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8048.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8049.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8050.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_805.root' ]

#files=[ '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8051.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8052.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8053.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8054.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8055.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8056.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8057.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8058.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_8059.root',
#        '/ceph/cms/store/user/evourlio/XtoYH_customNanoAOD/EGamma_Run2018D-UL2018_MiniAODv2-v2_MINIAOD_v0/nanoaod_806.root' ]


#2016 modules MC
PrefireCorr2016 = lambda : PrefCorr("L1prefiring_jetpt_2016BtoH.root", "L1prefiring_jetpt_2016BtoH", "L1prefiring_photonpt_2016BtoH.root", "L1prefiring_photonpt_2016BtoH")
bTagShapeSFAndUnc2016preVFP = lambda : btagSFProducer("UL2016preVFP", "deepjet", [ "shape_corr" ])
bTagShapeSFAndUnc2016postVFP = lambda : btagSFProducer("UL2016postVFP", "deepjet", [ "shape_corr" ])

#2017 modules MC
PrefireCorr2017 = lambda : PrefCorr('L1prefiring_jetpt_2017BtoF.root', 'L1prefiring_jetpt_2017BtoF', 'L1prefiring_photonpt_2017BtoF.root', 'L1prefiring_photonpt_2017BtoF')
bTagShapeSFAndUnc2017 = lambda : btagSFProducer("UL2017", "deepjet", [ "shape_corr" ])

#2018 modules MC
bTagShapeSFAndUnc2018 = lambda : btagSFProducer("UL2018", "deepjet", [ "shape_corr"])


if suffix=='16a':
  p=PostProcessor(".", 
                  files,
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=([puAutoWeight_UL2016(), jetmetUncertaintiesAPV2016UL(), jetmetUncertaintiesAPV2016ULAll(), muonScaleRes2016v5ULAPV(), PrefireCorr2016(), tauCorrs2016ULpreVFP(), lepSFID2016_B(), lepSFISO2016_B(), gammaSF_UL16PreVFP()] if analysis=="ggtautau" \
                      else [puAutoWeight_UL2016(), jetmetUncertaintiesAPV2016UL(), jetmetUncertaintiesAPV2016ULAll(), bTagShapeSFAndUnc2016preVFP(), gammaSF_UL16PreVFP()] if analysis=="ggbb" \
                      else []),
                  provenance=True
                  )

elif suffix=='16b' :
  p=PostProcessor(".", 
                  files,
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=([puAutoWeight_UL2016(), jetmetUncertainties2016UL(), jetmetUncertainties2016ULAll(), muonScaleRes2016v5UL(), PrefireCorr2016(), tauCorrs2016ULpostVFB(), lepSFID2016_H(), lepSFISO2016_H(), gammaSF_UL16PostVFP()] if analysis=="ggtautau" \
                      else [puAutoWeight_UL2016(), jetmetUncertainties2016UL(), jetmetUncertainties2016ULAll(), bTagShapeSFAndUnc2016postVFP(), gammaSF_UL16PostVFP()] if analysis=="ggbb" \
                      else []),
                  provenance=True
                  )

elif suffix=='17':
  p=PostProcessor(".", 
                  files,
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=([puAutoWeight_UL2017(), jetmetUncertainties2017UL(), jetmetUncertainties2017ULAll(), muonScaleRes2017v5UL(), PrefireCorr2017(), tauCorrs2017UL(), lepSFID2017(), lepSFISO2017(), gammaSF_UL17()] if analysis=="ggtautau" \
                      else [puAutoWeight_UL2017(), jetmetUncertainties2017UL(), jetmetUncertainties2017ULAll(), bTagShapeSFAndUnc2017(), gammaSF_UL17()] if analysis=="ggbb" \
                      else []),
                  provenance=True
                  )

elif suffix=='18':
  p=PostProcessor(".", 
                  files,
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=([puAutoWeight_UL2018(), jetmetUncertainties2018UL(), jetmetUncertainties2018ULAll(), muonScaleRes2018v5UL(), tauCorrs2018UL(), lepSFID2018(), lepSFISO2018(), gammaSF_UL18()] if analysis=="ggtautau" \
                      else [puAutoWeight_UL2018(), jetmetUncertainties2018UL(), jetmetUncertainties2018ULAll(), bTagShapeSFAndUnc2018(), gammaSF_UL18()] if analysis=="ggbb" \
                      else []),
                  provenance=True
                  )

elif suffix=='16aD':
  p=PostProcessor(".",
                  files,
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=([muonScaleRes2016v5ULAPV()] if analysis=="ggtautau" \
                      else [] if analysis=="ggbb" \
                      else []),
                  provenance=True
                  )

elif suffix=='16bD' :
  p=PostProcessor(".",
                  files,
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=([muonScaleRes2016v5UL()] if analysis=="ggtautau" \
                      else [] if analysis=="ggbb" \
                      else []),
                  provenance=True
                  )

elif suffix=='17D':
  p=PostProcessor(".",
                  files,
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=([muonScaleRes2017v5UL()] if analysis=="ggtautau"\
                      else [] if analysis=="ggbb" \
                      else []),
                  provenance=True
                  )

elif suffix=='18D':
  p=PostProcessor(".",
                  files,
                  selection.replace('\n',''),
                  branchsel="keep_and_drop.txt",
                  outputbranchsel="keep_and_drop.txt",
                  modules=([muonScaleRes2018v5UL()] if analysis=="ggtautau" \
                      else [] if analysis=="ggbb" \
                      else []),
                  provenance=True
                  )

else:
  print "bo"


# keep and drop printout
print p.branchsel._ops
print p.outputbranchsel._ops

p.run()

print("DONE")
