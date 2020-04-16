import ROOT
import ROOT.TMath as TMath
import math
import os
import optparse
import sys
import copy as copy
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import PhysicsTools.NanoAODTools.postprocessing.samples.samples as losamples
import multiprocessing as mp

ROOT.gROOT.SetBatch()

colors = [ROOT.kRed,
          ROOT.kGreen+1,
          ROOT.kMagenta+2,
          ROOT.kAzure+8,
          ROOT.kBlack,          
          ROOT.kSpring-7,
          ROOT.kOrange+2,
          ROOT.kTeal-5,
          ROOT.kGray+1,
          ROOT.kYellow-6,
]


class variabile(object):
    def __init__(self, name, title, taglio, nbins, xmin, xmax):
        self._name = name
        self._title = title
        self._cut = taglio
        self._nbins = nbins
        self._xmin = xmin
        self._xmax = xmax

    def __str__(self):
        return  '\"'+str(self._name)+'\",\"'+str(self._title)+'\",'+str(self._nbins)+','+str(self._xmin)+','+str(self._xmax)

def cutToTag(cut):
    newstring = cut.replace("(Electron_effSF)*", "").replace("(Muon_effSF)*", "").replace(">=","_GE_").replace(">","_G_").replace(" ","").replace("&&","_AND_").replace("||","_OR_").replace("<=","_LE_").replace("<","_L_").replace(".","p").replace("((", "_").replace("))", "_").replace("(","").replace(")","").replace("==","_EQ_").replace("=","_EQ_").replace("*","_AND_").replace("+","_OR_").replace("-", "neg")
    return newstring

def collect_result(result):
    global results
    results.append(result)

def getsampleslist(nfile):
    findsamples = open(str(nfile), "r")
    samples = []
    for line in findsamples:
        samples.append(line.split())
    findsamples.close()
    return samples

def createhlist(plot):
    var = None
    hlist = None
    name = "h_" + plot[0]
    title = plot[0]
    cut = None
    if plot[1] == 'nocut':
        cut = ""
    else:
        cut = plot[1]
        name = name + "_" + cutToTag(cut)
    nbins = int(float(plot[2]))
    nmin = float(plot[3])
    nmax = float(plot[4])
    var = variabile(name, title, cut, nbins, nmin, nmax)
    #hlist = []
    hlist = copy.deepcopy(var)
    #hlist.append(ROOT.TH1F(name, title, nbins, nmin, nmax))
    return hlist

def createh(hvar):
    hf = ROOT.TH1F(hvar._name, hvar._title, hvar._nbins, hvar._xmin, hvar._xmax)
    return hf

def getfilelist(sampledir, toRemove=''):
    files = [fil for fil in os.listdir(sampledir) if (os.path.isfile(os.path.join(sampledir, fil)) and toRemove not in fil)]
    return files

def getplotslist(nfile):
    findplots = open(str(nfile), "r")
    plots = []
    for line in findplots:
        plots.append(line.split())
    findplots.close()
    return plots

def producestack(plotfile):
    plotlist = getplotslist(plotfile)
    hlist = []
    for plot in plotlist:
        hlist.append(createhlist(plot))
    files = getfilelist("./", ".py")

    rootfiles = {
        "mu": [copy.deepcopy(fil) for fil in files if 'mu' in fil],
        "ele": [copy.deepcopy(fil) for fil in files if 'ele' in fil],
    }

    #print rootfiles
    mcstacks = {
        "mu": [],
        "ele": [],
    }
    dataplots = {
        "mu": [],
        "ele": [],
    }

    for k, h in enumerate(hlist):
        for key in mcstacks.keys():
            mcstacks[key].append(ROOT.THStack())
            mcstacks[key][k].SetTitle(h._title+" MCStacked")
            mcstacks[key][k].SetName(h._title+"_"+key+"_MCStacked")
        for key in dataplots.keys():
            dataplots[key].append(createh(h))
            dataplots[key][k].SetTitle(h._title+" Data "+key)
            dataplots[key][k].SetName(h._title+"_"+key+"_Data")
            dataplots[key][k].SetLineColor(ROOT.kBlue)
            #print dataplots[key][k].GetTitle(), dataplots[key][k].GetName()

    for key in mcstacks.keys():
        for i, fil in enumerate(rootfiles[key]):
            if 'Data' in fil:
                continue
            rf = None
            rf = ROOT.TFile.Open(fil, "READ")

            for c, h in enumerate(hlist):
                temph = None
                temph = rf.Get(str(h._name))
                temph.SetLineColor(colors[i])
                temph.SetFillColor(colors[i])
                temph.SetTitle(str(fil.replace("_", " ").replace(".root", "")))
                temph.SetName(h._title+"_"+str(fil.replace(".root", "")))
                mcstacks[key][c].Add(copy.deepcopy(temph))
            rf.Close()

    for key in dataplots.keys():
        for i, fil in enumerate(rootfiles[key]):
            if 'Data' in fil:
                rf = None
                rf = ROOT.TFile.Open(fil, "READ")
                for c, h in enumerate(hlist):
                    temph = None
                    temph = rf.Get(str(h._name))
                    try:
                        temph.GetEntries()
                    except:
                        continue
                    print temph, h._name
                    dataplots[key][c].Add(temph)
                rf.Close()
                break
            
 
    for key in mcstacks.keys():
        for t, mcstack in enumerate(mcstacks[key]):
            c1 = None
            c1 = ROOT.TCanvas(str(mcstack.GetName()).replace("_MCStacked", ""), str(mcstack.GetTitle()).replace(" MCStacked", ""))
            dataplots[key][t].Draw("HIST SAME")
            mcstack.Draw("HIST SAME")
            c1.SetLogy(1)
            c1.Pad().Modified()
            c1.Pad().Update()
            c1.BuildLegend()
            c1.Print("./plots/" + mcstack.GetName() + '.root')




    
    '''
    for key in dataplots.keys():
        print dataplots[key][0].Print()



        
   
    for key, value in rootfiles.items():
        mg = None
        mg = ROOT.THStack()
        for i, h in enumerate(value):
            

        if stack:
            h.SetFillColor(colors[i])
            mg.Add(h)
        i += 1
        mg.Draw(option)
        mg.GetXaxis().SetTitle(hist[0].GetXaxis().GetTitle())
        mg.GetYaxis().SetTitle(hist[0].GetYaxis().GetTitle())

'''
producestack(sys.argv[1])
