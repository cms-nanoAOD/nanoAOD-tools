#check from where following run number belondws to pre or Post VFP
 "278769": [[75, 111]] 
RunF_UL2016_GoldenJSON.txt (seems like it does not belongs this file but previously it was coped here now removed)
RunF_HIPM_UL2016_GoldenJSON.txt (seems belongs to this file but previousli it was not here now it coped in this file)
lumi in the below table mite very because of this run number this is beloges to preVFP but i have consider in post VFP

#Run Dependent Pileup distribition can we created 
pileupCalc.py -i RunC_UL2017.txt --inputLumiJSON pileup_latest.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 99 --numPileupBins 99 MyDataPileupHistogram_RunC_UL2017.root

#To Make new files for paticular runs look at the following twiki
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile

#To set the brill cal inviroment vist the following page
https://twiki.cern.ch/twiki/bin/view/CMS/BrilcalcQuickStart

	export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
	pip install --user --upgrade brilws
	
	
#Golden jeson file
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile
/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/

#To get the latest tag for the calculation visit the following page
https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec

	brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt
	brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt
	brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt 

|UL2016			|Lumi (1/ub)	|Lumi (1/pb)|
|:---------------------:|:-------------:|:----------|
|2016 RUN B_ver1	|0		|0	    |
|2016 RUN B_ver2	|5829427727	|5.829427727|
|2016 RUN C		|2621304822	|2.621304822|
|2016 RUN D		|4286031797	|4.286031797|
|2016 RUN E		|4065974751	|4.065974751|
|2016 RUN F_HIPM	|2718489255	|2.718489255|
|Total BCDEF		|19521228352	|19.52122835|
|2016 RUN F		|418771191	|0.418771191|
|2016 RUN G		|7653261227	|7.653261227|
|2016 RUN H		|8740119304	|8.740119304|
|total FGH		|16812151722	|16.81215172|
|All era		|36333380074	|36.33338007|


UL2017 data (5 (+2) eras: B, C, D, E, F, (+G (5 TeV) and H (lowPU)))

https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis


|UL2017		|Lumi (1/ub)		|Lumi ( 1/fb)|
|:-------------:|:---------------------:|:----------|
|2017 RUN A	|0			|0
|2017 RUN B	|4803371586		|4.803371586|
|2017 RUN C	|9574029838		|9.574029838|
|2017 RUN D	|4247792714		|4.247792714|
|2017 RUN E	|9314581016		|9.314581016|
|2017 RUN F	|13539905374		|13.53990537|
|All era	|41479680528		|41.47968053|


|UL2018		|Lumi (1/ub)		|Lumi ( 1/fb| 
|:-------------:|:---------------------:|:----------|
|2017 RUN A	|14027614284		|14.02761428|
|2017 RUN B	|7066552169		|7.066552169|
|2017 RUN C	|6898816878		|6.898816878|
|2017 RUN D	|31229758296		|31.2297583 |
|All era	|59222741627		|59.22274163|
