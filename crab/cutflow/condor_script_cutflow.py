#!/usr/bin/env python

from cutflowModule_new import *

#inputFiles=["root://se01.indiacms.res.in//store/user/psuryade/RUN2_UL/Tree_crab/SIXTEEN_v2/MC_postVFP/Tchannel/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/Tree_07_Aug22_MCUL2016postVFP_Tchannel/220807_064033/0000/tree_34.root"]
#inputFiles=["root://cms-xrd-global.cern.ch//store/user/mikumar/RUN2_UL/Tree_crab/SIXTEEN/MC_preVFP_v2/Tchannel/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/Tree_06_Aug22_MCUL2016preVFP_Tchannel/220806_113029/0000/tree_1.root"]
inputFiles=["../tree_6.root"]

for i in inputFiles:
        MCIso = ROOT.TFile.Open(i,'Read')
        ROOT.gROOT.cd()
        myTree = MCIso.Get('Events')
        #myTree.Print()

        modules=cutflowModuleConstr_2J1T1_mu_data_UL2018()
        modules.analyze(myTree)

        print "DONE"

