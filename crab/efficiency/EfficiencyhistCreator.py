import ROOT
import  sys , os
from dataset_2016 import *
from dataset_2017 import *
#https://indico.cern.ch/event/704163/contributions/2936719/attachments/1693833/2726445/Tutorial-PyROOT.pdf
if len(sys.argv) != 2:
	print "USAGE: %s  < year dataset>"%(sys.argv [0])
	sys.exit (1)
year   = sys.argv [1]

if(year == '2016'):
    RequestName = RequestName_MC_2016
if(year == '2017'):
    RequestName = RequestName_MC_2017

for i in range(0,len(RequestName)):
    inFileName   = "Efficiency_2017_RAW/"+RequestName[i]+"_Tagging_Efficiency.root"
    outfile_flag = RequestName[i]
    print "Reading  from", inFileName 

    #read histogram and store
    inFile = ROOT.TFile.Open(inFileName,"READ")
    hist_cri=[]
    hist_full=[]
    for flav in ["B","C","L"] :
        for wkp in ["No","L","M","T"]:
	    if(wkp!="No"):
	          hist_cri.append(inFile.Get("Efficiency/Flavour"+flav+"_Wp_pass_B"+wkp))
	    else:
	          hist_full.append(inFile.Get("Efficiency/Flavour"+flav+"_Wp_pass_"+wkp)) 
		
		
    #calculate Efficiency
    name = ["L","M","T"]
    for num in range(0,len(hist_cri)):
	if(num<3):
		Effi=ROOT.TEfficiency(hist_cri[num],hist_full[0])
		Effi.SetStatisticOption(ROOT.TEfficiency.kFCP)
		Effi = Effi.CreateHistogram()
		Effi.SetName("FlavourB_TagEffi_As_B"+name[num])
		hist_cri[num]=Effi
	elif(num<6):
		Effi=ROOT.TEfficiency(hist_cri[num],hist_full[1])
                Effi.SetStatisticOption(ROOT.TEfficiency.kFCP)
                Effi = Effi.CreateHistogram()
                Effi.SetName("FlavourC_TagEffi_As_B"+name[num-3])                    
                hist_cri[num]=Effi
	elif(num<9):
                Effi=ROOT.TEfficiency(hist_cri[num],hist_full[2])
                Effi.SetStatisticOption(ROOT.TEfficiency.kFCP)
                Effi = Effi.CreateHistogram()
                Effi.SetName("FlavourL_TagEffi_As_B"+name[num-6])
                hist_cri[num]=Effi			

        #Btag_effi_L = ROOT.TEfficiency(FlavourB_Wp_pass_BL,FlavourB_Wp_pass_No)
	#Btag_effi_L.SetStatisticOption(ROOT.TEfficiency.kFCP)
	#Btag_effi_L = Btag_effi_L.CreateHistogram()


	#print Btag_effi_L.GetBinContent(Btag_effi_L.FindBin(55.0,0.45))
	#print Btag_effi_L.GetBinError(Btag_effi_L.FindBin(55.0,0.45))

	#print hist_cri[0].GetBinContent(hist_cri[0].FindBin(55.0,0.45))
	#print hist_cri[0].GetBinError(hist_cri[0].FindBin(55.0,0.45))

	#canvas = ROOT . TCanvas ( " canvas " )
	#canvas . cd ()
	#Btag_effi_L3.Draw("colz")
	#canvas.Print("plots.pdf")

    outfile="/afs/cern.ch/user/m/mikumar/work/private/NanoAOD/CMSSW_10_6_0/src/PhysicsTools/NanoAODTools/crab/Efficiency_2017/"+outfile_flag+"_Tagging_Efficiency.root"
    cmd_rm= "rm -rf "+outfile
    os.system(cmd_rm)

    outRootFile = ROOT.TFile.Open(outfile ,"RECREATE")
    print 'output file = ',outfile
    outRootFile.cd()
    for num in range(0,len(hist_cri)):
        hist_cri[num].Write()
    outRootFile.Close()

    for num in range(0,len(hist_cri)):
        hist_cri[num].Delete()
    for num in range(0,len(hist_full)):
        hist_full[num].Delete()
