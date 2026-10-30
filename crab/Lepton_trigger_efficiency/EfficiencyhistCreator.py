import ROOT
import  sys , os
#https://indico.cern.ch/event/704163/contributions/2936719/attachments/1693833/2726445/Tutorial-PyROOT.pdf


FileName_Mc   = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/Lepton_Trig_Effi/v10/Ele_trigger_ttbar_FullyLeptonic_mu.root"
FileName_data = "/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/Lepton_Trig_Effi/v10/Ele_trigger_Data_mu_mu.root"
print "Reading  Mc from Events ", FileName_Mc
print "Reading  Data from Events ", FileName_data

#read histogram and store
inFile_Mc = ROOT.TFile.Open(FileName_Mc,"READ")
inFile_data = ROOT.TFile.Open(FileName_data,"READ")

hist_Mc_elNmu = inFile_Mc.Get("Events_2D_hist/Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27_HLT_Ele30_eta2p1_crossJet")
hist_Mc_mu = inFile_Mc.Get("Events_2D_hist/Event_HLT_IsoMu27")

hist_data_elNmu = inFile_data.Get("Events_2D_hist/Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27_HLT_Ele30_eta2p1_crossJet")
hist_data_mu = inFile_data.Get("Events_2D_hist/Event_HLT_IsoMu27")
		
		
#calculate Efficiency
Effi_Mc = ROOT.TEfficiency(hist_Mc_elNmu,hist_Mc_mu)
Effi_Mc.SetStatisticOption(ROOT.TEfficiency.kFCP)
Effi_Mc_hist = Effi_Mc.CreateHistogram()
Effi_data = ROOT.TEfficiency(hist_data_elNmu,hist_data_mu)
Effi_data.SetStatisticOption(ROOT.TEfficiency.kFCP)
Effi_data_hist = Effi_data.CreateHistogram()

hist_Mc_Z_elNmu = ROOT.TH1D("hist_Mc_Z_elNmu","hist_Mc_Z_elNmu",82,1,83)
hist_Mc_Z_mu = ROOT.TH1D("hist_Mc_Z_mu","hist_Mc_Z_mu",82,1,83)

hist_data_Z_elNmu = ROOT.TH1D("hist_data_Z_elNmu","hist_data_Z_elNmu",82,1,83)
hist_data_Z_mu = ROOT.TH1D("hist_data_Z_mu","hist_data_Z_mu",82,1,83)

for Y in range(1,7):
    for X in range(1,11):
        Bin=hist_Mc_elNmu.GetBin(X,Y)
        hist_Mc_Z_elNmu.SetBinContent(Bin,hist_Mc_elNmu.GetBinContent(Bin))
        hist_Mc_Z_elNmu.SetBinError(Bin,hist_Mc_elNmu.GetBinError(Bin)) 
        hist_Mc_Z_mu.SetBinContent(Bin,hist_Mc_mu.GetBinContent(Bin))
        hist_Mc_Z_mu.SetBinError(Bin,hist_Mc_mu.GetBinError(Bin))       

        hist_data_Z_elNmu.SetBinContent(Bin,hist_data_elNmu.GetBinContent(Bin))
        hist_data_Z_elNmu.SetBinError(Bin,hist_data_elNmu.GetBinError(Bin))
        hist_data_Z_mu.SetBinContent(Bin,hist_data_mu.GetBinContent(Bin))
        hist_data_Z_mu.SetBinError(Bin,hist_data_mu.GetBinError(Bin))
        #print(hist_Mc_Z_elNmu.GetBinError(Bin))

for Bin in range(1,83):
        if(hist_Mc_Z_elNmu.GetBinContent(Bin)==0 and hist_Mc_Z_elNmu.GetBinError(Bin)==0):
                hist_Mc_Z_elNmu.SetBinContent(Bin,1.0)
                hist_Mc_Z_elNmu.SetBinError(Bin,1.0)
                hist_Mc_Z_mu.SetBinContent(Bin,1.0)
                hist_Mc_Z_mu.SetBinError(Bin,1.0)

                hist_data_Z_elNmu.SetBinContent(Bin,1.0)
                hist_data_Z_elNmu.SetBinError(Bin,1.0)
                hist_data_Z_mu.SetBinContent(Bin,1.0)
                hist_data_Z_mu.SetBinError(Bin,1.0)    
        #print(Bin," ",hist_Mc_Z_elNmu.GetBinContent(Bin)," ",hist_Mc_Z_elNmu.GetBinError(Bin))    
"""can1 = ROOT.TCanvas("can1","can1",600,600)
can1.cd()
hist_Mc_Z_elNmu.Draw("hist;text")

can2 = ROOT.TCanvas("can2","can2",600,600)
can2.cd()
hist_Mc_elNmu.Draw("colz;text")"""

Assi_Effi_Mc = ROOT.TGraphAsymmErrors(hist_Mc_Z_elNmu,hist_Mc_Z_mu, "pois")
#Assi_Effi_Mc.Print()
Assi_Effi_data = ROOT.TGraphAsymmErrors(hist_data_Z_elNmu,hist_data_Z_mu, "pois")

#for Bin in range(1,83):
#        print(Bin,Assi_Effi_Mc.GetErrorYhigh(Bin))

for Y in range(1,7):
    for X in range(1,11):
        Bin=Effi_Mc_hist.GetBin(X,Y)
        Effi_Mc_hist.SetBinError(Bin,Assi_Effi_Mc.GetErrorYhigh(Bin-1)) #Assimaetric erros start from 0
        Effi_data_hist.SetBinError(Bin,Assi_Effi_data.GetErrorYhigh(Bin-1))
        #print(Bin,Assi_Effi_Mc.GetErrorYhigh(Bin-1))
        #print(Bin,Effi_Mc_hist.GetBinError(Bin))
        

Effi_Mc_hist.GetYaxis().SetTitle("p_{T} [GeV]")
Effi_Mc_hist.GetXaxis().SetTitle("SuperCluster #eta") #SuperCluster

Effi_data_hist.GetYaxis().SetTitle("p_{T} [GeV]")
Effi_data_hist.GetXaxis().SetTitle("SuperCluster #eta") #SuperCluster

SF = Effi_data_hist.Clone()
SF.Divide(Effi_Mc_hist)

for Y in range(1,7):
    for X in range(1,11):
        Bin=SF.GetBin(X,Y)
        
        print(Bin,Effi_Mc_hist.GetBinError(Bin))       
        #print(Bin,Effi_Mc_hist.GetBinContent(Bin)+Effi_Mc_hist.GetBinError(Bin),Effi_data_hist.GetBinContent(Bin)+Effi_data_hist.GetBinError(Bin))
        # print(Bin,Effi_Mc_hist.GetBinContent(Bin),Effi_data_hist.GetBinContent(Bin))

raw_input()

outfile="/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/Lepton_Trig_Effi/v10/egammaEffi.txt_EGM2D.root"

outRootFile = ROOT.TFile.Open(outfile ,"RECREATE")
print 'output file = ',outfile
outRootFile.cd()

Effi_Mc_hist.Write("EGamma_EffMC2D")
Effi_data_hist.Write("EGamma_EffData2D")
SF.Write("EGamma_SF2D")
