import ROOT as R

#hisopv = R.TH1F('hisopv', 'PV', 99,0.,99.)
hisoGpvB = R.TH1F('hisoGpvB', 'GPV', 99,0.,99.)
hisoGpvC = R.TH1F('hisoGpvC', 'GPV', 99,0.,99.)
hisoGpvD = R.TH1F('hisoGpvD', 'GPV', 99,0.,99.)
hisoGpvE = R.TH1F('hisoGpvE', 'GPV', 99,0.,99.)
hisoGpvF = R.TH1F('hisoGpvF', 'GPV', 99,0.,99.)


dataB = R.TFile.Open('Run2017B.root','Read')
dataC = R.TFile.Open('Run2017C.root','Read')
dataD = R.TFile.Open('Run2017D.root','Read')
dataE = R.TFile.Open('Run2017E.root','Read')
dataF = R.TFile.Open('Run2017F.root','Read')

treeB = dataB.Get('Events')
treeC = dataC.Get('Events')
treeD = dataD.Get('Events')
treeE = dataE.Get('Events')
treeF = dataF.Get('Events')
#treeB.Print()
R.gROOT.cd()

#treeB.Project('hisopv', 'PV_npvs')
treeB.Project('hisoGpvB', 'PV_npvsGood',"")
treeC.Project('hisoGpvC', 'PV_npvsGood',"")
treeD.Project('hisoGpvD', 'PV_npvsGood',"")
treeE.Project('hisoGpvE', 'PV_npvsGood',"")
treeF.Project('hisoGpvF', 'PV_npvsGood',"")

can_purity = R.TCanvas('can_purity', '', 600, 600)
can_purity.cd()

hisoGpvB.SetLineWidth(2)
hisoGpvC.SetLineWidth(2)
hisoGpvF.SetLineWidth(2)
hisoGpvD.SetLineWidth(2)
hisoGpvE.SetLineWidth(2)

hisoGpvB.SetLineColor(R.kRed)
hisoGpvC.SetLineColor(R.kBlue)
hisoGpvD.SetLineColor(R.kGreen)
hisoGpvE.SetLineColor(R.kYellow+2)
hisoGpvF.SetLineColor(R.kPink+2)

hisoGpvB.Scale(1/hisoGpvB.Integral())
hisoGpvC.Scale(1/hisoGpvC.Integral())
hisoGpvD.Scale(1/hisoGpvD.Integral())
hisoGpvE.Scale(1/hisoGpvE.Integral())
hisoGpvF.Scale(1/hisoGpvF.Integral())

hisoGpvB.Draw("hist")
hisoGpvC.Draw("hist;same")
hisoGpvD.Draw("hist;same")
hisoGpvE.Draw("hist;same")
hisoGpvF.Draw("hist;same")

leg = R.TLegend(0.6, 0.7, 0.85, 0.83)
leg.AddEntry(hisoGpvB, 'RunB', 'l')
leg.AddEntry(hisoGpvC, 'RunC', 'l')
leg.AddEntry(hisoGpvD, 'RunD', 'l')
leg.AddEntry(hisoGpvE, 'RunE', 'l')
leg.AddEntry(hisoGpvF, 'RunF', 'l')
leg.SetTextSize(0.03)
leg.SetBorderSize(0)
leg.Draw()


raw_input()
