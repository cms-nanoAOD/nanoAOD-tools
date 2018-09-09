from ROOT import *
path = 'Tree_testNanoAOD.root'

def GetH():
  f = TFile.Open(path)
  t = f.Get('tree')
  t.Project("SumWeights", "0.5", "genWeight")
  o = gROOT.FindObject('SumWeights')
  print type(o)
  print 'SumOfWeights: ', o.Integral()
  #return h

GetH()
#print 'Number of entries: ', h.GetEntries(), ', sum of weights: ', h.GetBinContent(1)
