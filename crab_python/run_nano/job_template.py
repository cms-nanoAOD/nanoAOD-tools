job_data_template = '''
#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.trigger.triggerFilter import triggerFilter
from PhysicsTools.NanoAODTools.postprocessing.bff.bffPreselModule import bffPreselProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleRes{era} 
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

isMC = False
dataYear = "{era}"
#runPeriod = ""

triggers= {triggers}

keep_and_drop = 'keep_and_drop_bff.txt'

modules=[
    countHistogramsProducer(),
    triggerFilter(triggers),
    muonScaleRes{era}(),
    bffPreselProducer(int(dataYear), triggers, isMC=isMC, btag_type="{btag_type}")
    ]

p = PostProcessor(".",
                  inputFiles(),
                  modules=modules,
                  provenance=True,
                  fwkJobReport=True,
                  outputbranchsel=keep_and_drop,
                  jsonInput=runsAndLumis()
                  )
p.run()

print("DONE")
#note: lepSF has to go before puWeight due to the lepton weight constructor redefining the weight constructor
#-I PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer btagSF$era \
'''

job_mc_template = '''
#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.trigger.triggerFilter import triggerFilter
from PhysicsTools.NanoAODTools.postprocessing.bff.bffPreselModule import bffPreselProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSF 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import lepSF{era}
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeight_{era} 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleRes{era} 
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

isMC = True
dataYear = "{era}"
runPeriod = ""

triggers= {triggers}

jmeCorrections = createJMECorrector(
    isMC=isMC, 
    dataYear=dataYear, 
    runPeriod=runPeriod,
    jesUncert="Total", 
    applySmearing=True,
    jetType="AK4PFchs",
    noGroom=False)

keep_and_drop = 'keep_and_drop_bff.txt'

modules=[
    countHistogramsProducer(),
    triggerFilter(triggers),
    btagSF(dataYear),
    jmeCorrections(),
    puWeight_{era}(),
    muonScaleRes{era}(),
    lepSF{era}(),
    bffPreselProducer(int(dataYear), triggers, isMC=isMC, btag_type="{btag_type}")
    ]

p = PostProcessor(".",
                  inputFiles(),
                  modules=modules,
                  provenance=True,
                  fwkJobReport=True,
                  outputbranchsel=keep_and_drop,
                  )
p.run()

print("DONE")
#note: lepSF has to go before puWeight due to the lepton weight constructor redefining the weight constructor
#-I PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer btagSF$era \
'''


job_mc_local_template='''
#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.trigger.triggerFilter import triggerFilter
from PhysicsTools.NanoAODTools.postprocessing.bff.bffPreselModule import bffPreselProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector
from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import countHistogramsProducer 
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSF 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import lepSF{era}
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import puWeight_{era}
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import muonScaleRes{era}
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles, runsAndLumis

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("outdir")
parser.add_argument( '-g','--glob', default=False, action='store_true')
parser.add_argument( '-x','--xrdcp', default=False, action='store_true')
args = parser.parse_args()

infile = args.infile
outdir = args.outdir
glob = args.glob
xrdcp = args.xrdcp

print(infile, outdir, glob)
if glob:
    import glob
    ifilename = glob.glob(infile)
else:
    ifilename = [infile]

if xrdcp:
    sourceprefix="root://cms-xrd-global.cern.ch/"
else:
    sourceprefix="./"
ifname = ["{{}}{{}}".format(sourceprefix, fname) for fname in ifilename]
isMC = True
dataYear = "{era}"
runPeriod = ""

triggers= {triggers}

jmeCorrections = createJMECorrector(
    isMC=isMC, 
    dataYear=dataYear, 
    runPeriod=runPeriod,
    jesUncert="Total", 
    applySmearing=True,
    jetType="AK4PFchs",
    noGroom=False)
    
keep_and_drop = 'keep_and_drop_bff.txt'

modules=[
    countHistogramsProducer(),
    triggerFilter(triggers),
    btagSF(dataYear),
    jmeCorrections(),
    puWeight_{era}(),
    muonScaleRes{era}(),
    lepSF{era}(),
    bffPreselProducer(int(dataYear), triggers, isMC=isMC, btag_type="{btag_type}")
    ]

p = PostProcessor(outdir,
                  ifilename,
                  modules=modules,
                  provenance=True,
                  fwkJobReport=True,
                  outputbranchsel=keep_and_drop,
                  #maxEntries=1000,
                  )
p.run()

print("DONE")
#note: lepSF has to go before puWeight due to the lepton weight constructor redefining the weight constructor
#-I PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer btagSF$era \
'''