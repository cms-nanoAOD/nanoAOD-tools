import ROOT as R

file = R.TFile.Open("/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/Lepton_Trig_Effi/v10/egammaEffi.txt_EGM2D.root")
SF_hist = file.Get("EGamma_SF2D")

can1 = R.TCanvas("can1","can1",600,600)
#R.gStyle.SetPaintTextFormat("0.11f");
can1.cd()

pad1 = R.TPad("pad1","pad1",0.0,0.0,0.96555,0.990683)
pad1.Draw()
pad1.cd()
pad1.SetLogy()



SF_hist.Print()
SF_hist.Draw("colz;text")


SF_hist_error = SF_hist.Clone()
SF_hist_error.Print()

for i in range(1,11):
    print(i," : ",SF_hist_error.GetBinError(i,0))

raw_input()

