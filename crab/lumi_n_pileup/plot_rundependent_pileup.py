import ROOT as R

dataB = R.TFile.Open('MyDataPileupHistogram_RunB_UL2017.root','Read')
dataC = R.TFile.Open('MyDataPileupHistogram_RunC_UL2017.root','Read')
dataD = R.TFile.Open('MyDataPileupHistogram_RunD_UL2017.root','Read')
dataE = R.TFile.Open('MyDataPileupHistogram_RunE_UL2017.root','Read')
dataF = R.TFile.Open('MyDataPileupHistogram_RunF_UL2017.root','Read')

hisoPUB = dataB.Get('pileup')
hisoPUC = dataC.Get('pileup')
hisoPUD = dataD.Get('pileup')
hisoPUE = dataE.Get('pileup')
hisoPUF = dataF.Get('pileup')
#treeB.Print()
R.gROOT.cd()


can_purity = R.TCanvas('can_purity', '', 600, 600)
can_purity.cd()

hisoPUB.SetLineWidth(2)
hisoPUC.SetLineWidth(2)
hisoPUF.SetLineWidth(2)
hisoPUD.SetLineWidth(2)
hisoPUE.SetLineWidth(2)

hisoPUB.SetLineColor(R.kRed)
hisoPUC.SetLineColor(R.kBlue)
hisoPUD.SetLineColor(R.kGreen)
hisoPUE.SetLineColor(R.kYellow+2)
hisoPUF.SetLineColor(R.kPink+2)

hisoPUB.Scale(1/hisoPUB.Integral())
hisoPUC.Scale(1/hisoPUC.Integral())
hisoPUD.Scale(1/hisoPUD.Integral())
hisoPUE.Scale(1/hisoPUE.Integral())
hisoPUF.Scale(1/hisoPUF.Integral())

hisoPUB.Draw("hist")
hisoPUC.Draw("hist;same")
hisoPUD.Draw("hist;same")
hisoPUE.Draw("hist;same")
hisoPUF.Draw("hist;same")

leg = R.TLegend(0.6, 0.7, 0.85, 0.83)
leg.AddEntry(hisoPUB, 'RunB', 'l')
leg.AddEntry(hisoPUC, 'RunC', 'l')
leg.AddEntry(hisoPUD, 'RunD', 'l')
leg.AddEntry(hisoPUE, 'RunE', 'l')
leg.AddEntry(hisoPUF, 'RunF', 'l')
leg.SetTextSize(0.03)
leg.SetBorderSize(0)
leg.Draw()


raw_input()
