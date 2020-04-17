import ROOT
import ROOT.TMath as TMath
import math
import copy as copy
from os import path
from array import array
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim
print "PhysicsTools implemented"

class systWeights(object):

    def __init__(self):
        self.onlyNominal = True
        self.addPDF = False
        self.addQ2 = False
        self.addTopPt = False
        self.addVHF = False
        self.addTTSplit = False
        self.maxSysts = 0
        self.maxSystsNonPDF = 0
        self.shortPDFFiles = False
        self.isData = False
        self.nPDF = 0
        self.nCategories = 0
        self.nSelections = 0
        self.nEventBasedSysts = 0
        self.weightedSysts = array('f', [0.])
        self.eventBasedScenario = ""
        self.wCats = array('d', [0.])
        self.eventBasedNames = []
        self.baseSelections = array('i', [0])
        self.weightedNames = []
        self.selectionsNames = []
        self.categoriesNames = []

    def initTreesSysts(self, trees, tfile):
        tfile.cd()
        for s in range(self.nSelections):
            temptree = ROOT.TTree(str("events_"+self.selectionsNames[s]), "")
            isEventBasedSelection = self.isEventBasedSelection(s)
            self.__initTreesSysts2S(temptree, isEventBasedSelection)

    def __initTreesSysts2S(tree, isEventBasedSyst=False):
        Max = self.maxSysts
        if self.shortPDFFiles:
            Max = self.maxSystsNonPDF
        for sy in range(Max):
            if isEventBasedSyst and sy > 0:
                continue
            ns = str(self.weightedNames[sy])
            if sy == 0:
                ns = "w_nominal"
            tree.Branch(str(ns), (self.weightedSysts[int(sy)]))
        for c in range(self.nCategories):
            cname = str(self.categoriesNames[c])
            tree.Branch(cname, self.wCats[c])

    def addSelection(self, selection):
        self.selectionsNames.append(str(selection))
        initSelection = self.nSelections
        self.nSelections += 1
        for sc in range(self.nEventsBasedSysts):
            self.selectionsNames.append(str(selection) + "_" + str(self.eventBasedNames[sc]))
            self.baseSelections.append(initSelection)
            self.nSelections += 1

    def setSelectionsNames(self, selections):
        for s in range(self.nSelections):
            if s < (len(self.selectionNames) - 1):
                self.selectionsNames[s] = copy.deepcopy(selections[s])
            else:
                self.selectionsNames[s].append(copy.deepcopy(selections[s]))

    def branchTreesSysts(self, trees, selection, name, tfile, f):
        tfile.cd()
        tname = ROOT.TString(name)
        for s in range(self.nSelections):
            print " selection # ", str(s), " name ", str(self.selectionsNames[s]), " name ", str(tname)
            print " tree is ", str(trees[s])
            if selection == self.selectionsNames[s]:
                trees[s].Branch(tname, f)
            if self.isEventBasedSelection(s):
                if selection == self.selectionNames[self.baseSelections[s]] :
                    trees[s].Branch(tname, f)

    def fillTreesSysts(self, trees, selection):
        for s in range(self.nSelections):
            if selection == self.selectionsNames[s] and not self.isEventBasedSelection(s) and self.eventBasedScenario == "nominal" :
                trees[s].Fill()
            if self.isEventBasedSelection(s):
                if self.eventBasedScenario in self.selectionsNames[s] and selection == self.selectionsNames[self.baseSelections[s]]:
                    trees[s].Fill()

    def writeTreesSysts(self, trees, tfile):
        tfile.cd()
        for s in range(self.nSelections):
            trees[s].Write()

    def prepareDefault(self, addDefault, addPDF, addQ2, addTopPt, addVHF, addTTSplit, numPDF=102):
        self.addPDF = copy.deepcopy(addPDF)
        self.addQ2 = copy.deepcopy(addQ2)
        self.addTopPt = copy.deepcopy(addTopPt)
        self.addVHF = copy.deepcopy(addVHF)
        self.addTTSplit = copy.deepcopy(addTTSplit)
        self.nPDF = copy.deepcopy(numPDF)
        self.nCategories = 1
        self.categoriesNames.append("")
        self.wCats[0] = 1.0
        self.nSelections = 0 
        self.eventBasedScenario = "nominal"

        if addDefault:
            self.weightedNames.append("")
            self.weightedNames.append("btagUp")
            self.weightedNames.append("btagDown")
            self.weightedNames.append("mistagUp")
            self.weightedNames.append("mistagDown")
            self.weightedNames.append("puUp")
            self.weightedNames.append("puDown")
            #self.weightedNames.append("lepUp")
            #self.weightedNames.append("lepDown")
            #self.weightedNames.append("isoUp")
            #self.weightedNames.append("isoDown")
            #self.weightedNames.append("trigUp")
            #self.weightedNames.append("trigDown")
            self.setMax(7)
            self.setMaxNonPDF(7)
            self.weightedNames.append("")

        if addQ2: 
            self.weightedNames[self.maxSysts] = "q2Up"
            self.weightedNames.append("q2Down")
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2) 
            self.weightedNames.append("")

        if addTopPt:
            self.weightedNames[self.maxSysts] = "topPtWeightUp"
            self.weightedNames.append("topPtWeightDown")
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2)
            self.weightedNames.append("")

        if addVHF:
            self.weightedNames[self.maxSysts]="VHFWeightUp"
            self.weightedNames.append("VHFWeightDown")
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2)
            self.weightedNames.append("")

        if addTTSplit:
            self.nCategories=4
            categoriesNames.append("TT0lep")
            categoriesNames.append("TT1lep")
            categoriesNames.append("TT2lep")
            self.wCats.append(1.0)
            self.wCats.append(1.0)
            self.wCats.append(1.0)

        if addPDF:
            self.weightedNames[self.maxSysts] = "pdf_totalUp"
            self.weightedNames.append("pdf_totalDown")
            self.weightedNames.append("pdf_asUp")
            self.weightedNames.append("pdf_asDown")
            self.weightedNames.append("pdf_zmUp")
            self.weightedNames.append("pdf_zmDown")
            self.setMax(self.maxSysts+6)
            self.setMaxNonPDF(self.maxSystsNonPDF+6)
            nPDF = self.nPDF
            for i in range(nPDF):
                ss = str(i+1)
                self.weightedNames.append("pdf" + str(ss))

            self.setMax(maxSysts+nPDF)
            self.weightedNames.append("")

    def addSyst(self, name):
        self.weightedNames[self.maxSysts] = copy.deepcopy(name)
        self.setMax(maxSysts+1)
        if "pdf" in name:
            self.setMaxNonPDF(maxSysts+1)
            self.weightedNames.append("")

    def addSystNonPDF(self, name):
        self.weightedNames[self.maxSystsNonPDF] = copy.deepcopy(name)
        self.setMaxNonPDF(maxSystsNonPDF+1)
        nPDF = self.nPDF
        for i in range(nPDF):
            ss = str(i+1)
            self.weightedNames.append("pdf"+str(ss))
        self.setMax(maxSystsNonPDF+nPDF)
        self.weightedNames.append("")

    def addTopTagSF(self, name):
        up = name + "Up"
        down = name + "Down"
        self.addSystNonPDF(up)
        self.addSystNonPDF(down)

    def addWTagSF(self, name):
        up = name + "Up"
        down = name + "Down"
        self.addSystNonPDF(up)
        self.addSystNonPDF(down)

    def addTrigSF(self, name):
        up = name + "Up"
        down = name + "Down"
        self.addSystNonPDF(up)
        self.addSystNonPDF(down)

    def setTopTagSF(self, name, SF_nom, SF_up, SF_down, mult=True):
        zerofact = 1.0
        if mult:
            zerofact = self.weightedSysts[0]
        up = name + "Up"
        down = name + "Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom
        
        self.setSystValue(up, valueup*zerofact)
        self.setSystValue(down, valuedown*zerofact)

    def setWTagSF(self, name, SF_nom, SF_up, SF_down, mult=True):
        zerofact = 1.0
        if mult:
           zerofact = self.weightedSysts[0]
        up = name+"Up"
        down = name+"Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom

        self.setSystValue(up, valueup*zerofact)
        self.setSystValue(down, valuedown*zerofact)

    def setTrigSF(self, name, SF_nom, SF_up, SF_down, mult=True):
        zerofact = 1.0
        if mult:
            zerofact = self.weightedSysts[0]
        up = name+"Up"
        down = name+"Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom
        if SF_nom == 0:
            valueup = 0
            valuedown = 0

        self.setSystValue(up, valueup*zerofact)
        self.setSystValue(down, valuedown*zerofact)

    def setPDFWeights(self, wpdfs, xsections, numPDFs, wzero=1.0, mult=True):
        zerofact = 1.0
        rms, mean = 0., 0.
        if mult:
            zerofact = self.weightedSysts[0]
        for i in range(numPDFs+1):
            if wzero != 0 and xsections[i] != 0:
                try:
                    pvalue = wpdfs[i] / (wzero*xsections[i])
                except math.isnan(pvalue):
                    pvalue = 1.
                self.setPDFValue(i, zerofact*wpdfs[i]/(wzero*xsections[i]) )
                mean += pvalue
            else:
                self.setPDFValue(i, wzero)
        mean = mean / numPDFs

        for i in range(numPDFs):
            if wzero != 0 and xsections[i] != 0:
                try:
                    pvalue = wpdfs[i] / (wzero*xsections[i])
                except math.isnan(pvalue):
                    pvalue = 1.
                rms += (mean-pvalue) * (mean-pvalue)
            else:
                rms += 0.

        if self.shortPDFFiles:
            self.setSystValue("pdf_asUp", self.getPDFValue(self.nPDF-2.)/wzero)
            self.setSystValue("pdf_asDown", zerofact)
            self.setSystValue("pdf_zmUp", self.getPDFValue(self.nPDF-1.)/wzero)
            self.setSystValue("pdf_zmDown", zerofact)
            if math.isnan(rms):
                rms += 0.
            self.setSystValue("pdf_totalUp", zerofact*(1.+rms))
            self.setSystValue("pdf_totalDown", zerofact*(1.-rms))

    def setTWeight(self, tweight, wtotsample=1.0, mult=True):
        zerofact = 1.0
        if mult:
            zerofact = self.weightedSysts[0]
        self.setSystValue("topPtWeightUp", zerofact*tweight/wtotsample)
        self.setSystValue("topPtWeightDown", zerofact/tweight*wtotsample)

    def setVHFWeight(self, vhf, mult=True, shiftval=0.65):
        zerofact = 1.0
        w_shift = 0.0
        if vhf > 1:
            w_shift = shiftval
        if mult: 
            zerofact = self.weightedSysts[0]
        
        self.setSystValue("VHFWeightUp", zerofact*(1+w_shift))
        self.setSystValue("VHFWeightDown", zerofact*(1-w_shift))

    def setQ2Weights(self, q2up, q2down, wzero=1.0, mult=True):
        zerofact = 1.0
        if mult:
            zerofact = self.weightedSysts[0]
  
        self.setSystValue("q2Up", zerofact*q2up/wzero)
        self.setSystValue("q2Down", zerofact*q2down/wzero)

    def getPDFValue(self, numPDF):
        if not self.addPDF:
            print "error! No PDF used, this will do nothing."
            return 0.
        MIN = self.maxSystsNonPDF
        return float(self.weightedSysts[numPDF+MIN])

    def setPDFValue(self, numPDF, w):
        if not self.addPDF:
            print "error! No PDF used, this will do nothing."
            return
        MIN = self.maxSystsNonPDF
        self.weightedSysts[numPDF+MIN] = w

    
    def calcPDFHisto(self, histo, singleHisto, scalefactor=1.0, c=0):
        #EXPERIMENTAL                                                                     
        if not addPDF:
            print "error! No PDF used, this will do nothing."
            return
        MAX = self.maxSysts
        MIN = self.maxSystsNonPDF + (MAX+1)*c
        for b in range(singleHisto.GetNbinsX()):
            val = singleHisto.GetBinContent(b)
            mean = 0
            devst = 0
            for i in range(self.nPDF):
                mean = mean + histo[i+MIN].GetBinContent(b)
            mean = mean/self.nPDF
  
            for i in range(self.nPDF):
                devst += (mean-histo[i+MIN].GetBinContent(b))*(mean-histo[i+MIN].GetBinContent(b))
            devst= sqrt(devst/self.nPDF)
            singleHisto.SetBinContent(b,val+devst*scalefactor)
    
    def isEventBasedSelection(self, sy):
        isEventBased = False
        for e in range(self.nEventBasedSysts):
            if self.eventBasedNames[e] in self.selectionsNames[sy]:
                isEventBased = True
                return True
        return isEventBased

    def initHistogramsSysts(self, histo, name, title, nbins, Min, Max):
        for c in range(nCategories):
            MAX = self.maxSysts
            useOnlyNominal = self.onlyNominal
            cname = ROOT.TString(str(self.categoriesNames[c]))
            for sy in range(MAX):
                ns = ROOT.TSring(str(self.weightedNames[sy]))
                if sy == 0:
                    if c == 0:
                        histo[sy+((MAX+1)*c)] = ROOT.TH1F(name, title, nbins, Min, Max)
                    else:
                        histo[sy+((MAX+1)*c)] = ROOT.TH1F(name+"_"+cname, title, nbins, Min, Max)
      
                if sy != 0 and not useOnlyNominal:
                    if c == 0:
                        histo[sy+((MAX+1)*c)] = ROOT.TH1F(name+"_"+ns,title,nbins,Min,Max)
                    else:
                        histo[sy+((MAX+1)*c)] = ROOT.TH1F(name+"_"+ns+"_"+cname,title,nbins,Min,Max)
    
    def setOnlyNominal(self, useOnlyNominal=False):
        self.onlyNominal = copy.deepcopy(useOnlyNominal)
  
    def setWCats(self, wcats):
        for i in range(self.nCategories):
            if i < (len(self.wCats) - 1):
                self.wCats[i] = copy.deepcopy(wcats[i])
            else:
                self.append(copy.deepcopy(wcats[i]))
                
    def fillHistogramsSysts(self, histo, v, w, systWeights=[], wcats=None):
        nFirstSysts = len(systWeights)
        if wcats == None:
            wcats = copy.deecopy(self.wCats)
        for c in range(self.nCategories):
            MAX = self.maxSysts
            useOnlyNominal = self.onlyNominal
            for sy in range(MAX):
                if sy != 0 and useOnlyNominal:
                    continue
                ws = 1.0
                if sy < nFirstSysts:
                    wcats[c] = 1.0
                    ws = systWeights[sy]*wcats[c]
                else:
                    if nFirstSysts != 0:
                        wcats[c] = 1.0
                    ws = self.weightedSysts[sy]*wcats[c]

                histo[sy+(MAX+1)*(c)].Fill(v, w * ws)
                            
    def createFilesSysts(self, allFiles, basename, opt="RECREATE"):
        for c in range(self.nCategories):
            MAX = self.maxSystsNonPDF
            MAXTOT = self.maxSystsNonPDF
            useOnlyNominal = self.onlyNominal
            cname = str(self.categoriesNames[c])

            if c != 0:
                cname = "_" + cname
            for sy in range(MAX):
                ns = str(self.weightedNames[sy])
                print " creating file for syst ", ns

                if c != 0:
                    print " category is ", str(c)
                    print "onlynominal is ", useOnlyNominal
                
                if sy == 0:
                    allFiles[sy+(MAX+1)*c] = ROOT.TFile.Open((basename+ns+cname+".root"), opt)
                else:
                    if not useOnlyNominal:
                        print " filename is ", basename, ns, cname, ".root"
                        allFiles[sy+(MAX+1)*c] = ROOT.TFile.Open((basename+"_"+ns+cname+".root"), opt)
                        print "ESCO dal create Sys "

            if self.addPDF:
                if not useOnlyNominal:
                   allFiles[MAX+((MAX+1)*c)]= ROOT.TFile.Open((basename+"_pdf"+cname+".root"), opt)

    def writeHistogramsSysts(self, histo, filesout):
        MAX = self.maxSystsNonPDF
        MAXTOT = self.maxSysts
        useOnlyNominal = self.onlyNominal
        for c in range(self.nCategories):
            cname = ROOT.TString(str(self.categoriesNames[c]))
            if c != 0:
                cname = "_" + cname
                for sy in range(MAX):
                    if not (not useOnlyNominal or sy==0):
                        continue
                    filesout[sy+(MAX+1)*(c)].cd()
                    if self.addPDF:
                        if self.weightedNames[sy] == "pdf_totalUp":
                            calcPDFHisto(histo, histo[sy+(MAXTOT+1)*(c)], 1.0, c)
                        if self.weightedNames[sy] == "pdf_totalDown":
                           calcPDFHisto(histo, histo[sy+(MAXTOT+1)*(c)], -1.0, c)
                    histo[sy+(MAXTOT+1)*c].Write(histo[0].GetName())
                if self.addPDF:
                    if not useOnlyNominal:
                        filesout[MAX+(MAX+1)*(c)].cd()
                        MAXPDF = self.maxSysts
                        for sy in range(MAXPDF):
                            histo[sy+(MAXTOT+1)*(c)].Write()

    def writeSingleHistogramSysts(self, histo, filesout):
        MAX= self.maxSystsNonPDF
        useOnlyNominal = self.onlyNominal
        for c in range(self.nCategories):
            cname = ROOT.TString(str(self.categoriesNames[c]))
            if c != 0:
                cname= "_"+cname
            for sy in range(MAX):
                if not (not useOnlyNominal or sy == 0):
                    continue
                filesout[sy+(MAX+1)*c].cd()
                histo.Write()
            if self.addPDF:
                if not useOnlyNominal:
                    filesout[MAX+(MAX+1)*c].cd()
                    MAXPDF = self.maxSysts
                    for sy in range(MAXPDF):
                        histo.Write()

    def setMax(self, Max):
        self.maxSysts = copy.deepcopy(Max)

    def setMaxNonPDF(self, Max):
        self.maxSystsNonPDF = copy.deepcopy(Max)

    def setSystValueName(self, name, value, mult=False):
        zerofact = 1.0
        if mult:
            zerofact = self.weightedSysts[0]
        MAX = self.maxSysts
        for sy in range(MAX):
            if self.weightedNames[sy] == name:
                self.weightedSysts[sy] = value*zerofact

    def setSystValuePlace(self, systPlace, value, mult=False):
        zerofact=1.0
        if mult:
            zerofact = self.weightedSysts[0]
        self.weightedSysts[place] = value*zerofact

    def setWeightName(self, name, value, mult=False):
        self.setSystValueName(name, value, mult)

    def setWeightPlace(self, place, value, mult=False):
        self.setSystValuePlace(place, value, mult)

    def closeFilesSysts(self, filesout):
        MAX = self.maxSystsNonPDF
        useOnlyNominal = self.onlyNominal
        for c in range(self.nCategories):
            cname = ROOT.TString(str(self.categoriesNames[c]))
            if c != 0:
                cname = "_" + cname

            for sy in range(MAX):
                if not (not useOnlyNominal or sy==0):
                    continue
                filesout[sy+(MAX+1)*(c)].Close()
            
            addPDF = self.addPDF
            if addPDF:
                if not useOnlyNominal:
                    filesout[MAX+(MAX+1)*(c)].Close()

systZero = systWeights()                        
maxSysts = 0
addPDF = False
addQ2 = False
addTopPt = False
addVHF = False
addTTSplit = False
addTopTagging = False
addWTagging = False
addTrigSF = False
addPDF = True
addQ2 = True
addTopTagging = True
addWTagging = True
addTopPt = True
addVHF = False
addTrigSF = False

nPDF = 102

systZero.prepareDefault(True, addQ2, addPDF, addTopPt, addVHF, addTTSplit)
print "max systs are ", systZero.maxSysts
'''
  if(addTopTagging) {
    systZero.addTopTagSF("topTag")
  }
  if(addWTagging){
    systZero.addWTagSF("wTag")
  }
  if(addTrigSF){
    systZero.addTrigSF("trigSF")
  }
  maxSysts= systZero.maxSysts
'''
