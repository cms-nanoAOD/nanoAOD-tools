import ROOT
import ROOT.TMath as TMath
import math
import cmath
import copy as copy
from os import path
import array
import types
ROOT.PyConfig.IgnoreCommandLineOptions = True

def Chi_TopMass(mT):
  sigma = 28.8273
  mST = 174.729
  chi = ( TMath.Power((mST-mT), 2.) ) / ( TMath.Power(sigma, 2.))
  return chi

###############################################
###         Begin of generic utils          ###   
###############################################
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch()        # don't pop up canvases                                                                                                                                              
ROOT.TH1.SetDefaultSumw2()
ROOT.TGaxis.SetMaxDigits(3)

colors = [ROOT.kBlue,
          ROOT.kBlack,
          ROOT.kRed,
          ROOT.kGreen+2,
          ROOT.kMagenta+2,
          ROOT.kAzure+6
]

#### ========= UTILITIES =======================
def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    ## Otherwise
    dphi = (phi1-phi2)
    while dphi >  math.pi: dphi -= 2*math.pi
    while dphi < -math.pi: dphi += 2*math.pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise
    return math.hypot(eta1-eta2, deltaPhi(phi1,phi2))

def closest(obj,collection,presel=lambda x,y: True):
    ret = None; drMin = 999
    for x in collection:
        if not presel(obj,x): continue
        dr = deltaR(obj,x)
        if dr < drMin: 
            ret = x; drMin = dr
    return (ret,drMin)

def add_to_hemisphere(selobj, obj, pos, neg):
    px_obj = obj.pt*ROOT.TMath.Cos(obj.phi)
    py_obj = obj.pt*ROOT.TMath.Sin(obj.phi)
    if obj == selobj:
        pos.append([copy.deepcopy(px_obj), copy.deepcopy(py_obj)])
        neg.append([copy.deepcopy(px_obj), copy.deepcopy(py_obj)])
    elif 0. < deltaPhi(selobj, obj) < math.pi:
        pos.append([copy.deepcopy(px_obj), copy.deepcopy(py_obj)])
    elif -math.pi < deltaPhi(selobj, obj) < 0.:
        neg.append([copy.deepcopy(px_obj), copy.deepcopy(py_obj)])

def hemisphere_pt(objs):
    thrust_px = 0.
    thrust_py = 0.
    num = 0.
    den = 0.
    for obj in objs:
        obj_px = copy.deepcopy(obj[0])
        thrust_px += obj_px
        obj_py = copy.deepcopy(obj[1])
        thrust_py += obj_py
    #den = copy.deepcopy(total_pt)
    mod = math.hypot(thrust_px, thrust_py)
    return thrust_px, thrust_py, mod
    '''
    thrust_px = thrust_px / mod
    thrust_py = thrust_py / mod
    for obj in objs:
        num += math.fabs(thrust_px*obj[0] + thrust_py*obj[1])
    #print "num: ", num
    thrust = * num / den
    #print "thrust: ", thrust
    return thrust
    '''

def event_thrust(lep, jets, met):
    ovr_thrust = 0.
    had_thrust = 0.
    ovr_pt = 0.
    had_pt = 0.
    for jet in jets:
        had_pt += math.fabs(jet.pt)

    ovr_pt = copy.deepcopy(had_pt)
    ovr_pt += math.fabs(lep.pt) + math.fabs(met.pt)

    had_max_hempt = 0.
    had_thrust_ax_x = 0.
    had_thrust_ax_y = 0.
    ovr_max_hempt = 0.
    ovr_thrust_ax_x = 0.
    ovr_thrust_ax_y = 0.
    for i, seljet in enumerate(jets): #build hemispheres for every jet
        neg_ovr = []
        neg_had = []
        pos_ovr = []
        pos_had = []
        neg_ovr_res = []
        neg_had_res = []
        pos_ovr_res = []
        pos_had_res = []
        for j, jet in enumerate(jets):
            add_to_hemisphere(seljet, jet, pos_had, neg_had)
        pos_ovr = copy.deepcopy(pos_had)
        neg_ovr = copy.deepcopy(neg_had)
        add_to_hemisphere(seljet, lep, pos_ovr, neg_ovr)
        add_to_hemisphere(seljet, met, pos_ovr, neg_ovr)

        pos_had_res = list(hemisphere_pt(pos_had))
        neg_had_res = list(hemisphere_pt(neg_had))

        if had_max_hempt < pos_had_res[2]:
            had_max_hempt = copy.deepcopy(pos_had_res[2])
            had_thrust_ax_x = copy.deepcopy(pos_had_res[0]/pos_had_res[2])
            had_thrust_ax_y = copy.deepcopy(pos_had_res[1]/pos_had_res[2])        
        if had_max_hempt < neg_had_res[2]:
            had_max_hempt = copy.deepcopy(neg_had_res[2])
            had_thrust_ax_x = copy.deepcopy(neg_had_res[0]/neg_had_res[2])
            had_thrust_ax_y = copy.deepcopy(neg_had_res[1]/neg_had_res[2])        

        pos_ovr_res = list(hemisphere_pt(pos_ovr))
        neg_ovr_res = list(hemisphere_pt(neg_ovr))

        if ovr_max_hempt < pos_ovr_res[2]:
            ovr_max_hempt = copy.deepcopy(pos_ovr_res[2])
            ovr_thrust_ax_x = copy.deepcopy(pos_ovr_res[0]/pos_ovr_res[2])
            ovr_thrust_ax_y = copy.deepcopy(pos_ovr_res[1]/pos_ovr_res[2])        
        if ovr_max_hempt < neg_ovr_res[2]:
            ovr_max_hempt = copy.deepcopy(neg_ovr_res[2])
            ovr_thrust_ax_x = copy.deepcopy(neg_ovr_res[0]/neg_ovr_res[2])
            ovr_thrust_ax_y = copy.deepcopy(neg_ovr_res[1]/neg_ovr_res[2])
  
    for jet in jets:
        jpx = jet.pt*ROOT.TMath.Cos(jet.phi)
        jpy = jet.pt*ROOT.TMath.Sin(jet.phi)
        had_thrust += math.fabs(jpx*had_thrust_ax_x + jpy*had_thrust_ax_y)
        ovr_thrust += math.fabs(jpx*ovr_thrust_ax_x + jpy*ovr_thrust_ax_y)
    ovr_thrust += math.fabs(lep.pt*(ROOT.TMath.Cos(lep.phi)*ovr_thrust_ax_x + ROOT.TMath.Sin(lep.phi)*ovr_thrust_ax_y))
    ovr_thrust += math.fabs(met.pt*(ROOT.TMath.Cos(met.phi)*ovr_thrust_ax_x + ROOT.TMath.Sin(met.phi)*ovr_thrust_ax_y))
    had_thrust = had_thrust / had_pt
    ovr_thrust = ovr_thrust / ovr_pt
    
    return round(ovr_thrust, 5), round(had_thrust, 5)

'''
def event_thrust(lep, jets, met):
    ovr_thrust = []
    had_thrust = []
    ovr_pt = 0.
    had_pt = 0.
    for jet in jets:
        had_pt += math.fabs(jet.pt)
    #print "had_pt: ", had_pt
    ovr_pt = copy.deepcopy(had_pt)
    ovr_pt += math.fabs(lep.pt) + math.fabs(met.pt)
    #print "ovr_pt: ", ovr_pt
    for i, seljet in enumerate(jets): #build hemispheres for every jet
        neg_ovr = []
        neg_had = []
        pos_ovr = []
        pos_had = []
        for j, jet in enumerate(jets):
            add_to_hemisphere(seljet, jet, pos_had, neg_had)
        pos_ovr = copy.deepcopy(pos_had)
        neg_ovr = copy.deepcopy(neg_had)
        add_to_hemisphere(seljet, lep, pos_ovr, neg_ovr)
        add_to_hemisphere(seljet, met, pos_ovr, neg_ovr)
        ovr_thrust.append(copy.deepcopy(hemisphere_thrust(pos_ovr, ovr_pt)))
        ovr_thrust.append(copy.deepcopy(hemisphere_thrust(neg_ovr, ovr_pt)))
        had_thrust.append(copy.deepcopy(hemisphere_thrust(pos_had, had_pt)))
        had_thrust.append(copy.deepcopy(hemisphere_thrust(neg_had, had_pt)))

    ovr_thrust.sort(reverse = True)
    had_thrust.sort(reverse = True)
    return round(ovr_thrust[0], 5), round(had_thrust[0], 5)
'''

def matchObjectCollection(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {}
    if len(objs)==0:
        return pairs
    if len(collection)==0:
        return dict( list(zip(objs, [None]*len(objs))) )
    for obj in objs:
        ( bm, dR ) = closest(obj, [ mobj for mobj in collection if presel(obj,mobj) ])
        if dR < dRmax:
            pairs[obj] = bm
        else:
            pairs[obj] = None
    return pairs

def matchObjectCollectionMultiple(objs,collection,dRmax=0.4,presel=lambda x,y: True):
    pairs = {}
    if len(objs)==0:
        return pairs
    if len(collection)==0:
        return dict( list(zip(objs, [None]*len(objs))) )
    for obj in objs:
        matched = [] 
        for c in collection :
            if presel(obj,c) and deltaR( obj, c ) < dRmax :
                matched.append( c )
        pairs[obj] = matched
    return pairs

def pass_MET(flag): #returns the True if the event pass the MET Filter requiriments otherwise False
    return flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter

def get_Mu(muons): #returns a collection of muons that pass the selection performed by the filter function
    return list(filter(lambda x : x.tightId and abs(x.eta) < 2.4 and x.miniPFRelIso_all < 0.1, muons))

def get_LooseMu(muons): #returns a collection of muons that pass the selection performed by the filter function
    return list(filter(lambda x : x.looseId and not x.tightId and x.pt > 35 and x.miniPFRelIso_all < 0.4 and abs(x.eta) < 2.4, muons))

def get_Ele(electrons): #returns a collection of electrons that pass the selection performed by the filter function
    return list(filter(lambda x : x.mvaFall17V2noIso_WP90 and x.miniPFRelIso_all < 0.1 and ((abs(x.eta) < 1.4442) or (abs(x.eta) > 1.566 and abs(x.eta) < 2.5)), electrons))

def get_LooseEle(electrons): #returns a collection of electrons that pass the selection performed by the filter function
    return list(filter(lambda x : x.mvaFall17V2noIso_WPL and not x.mvaFall17V2noIso_WP90 and x.miniPFRelIso_all < 0.4 and x.pt > 35 and ((abs(x.eta) < 1.4442) or (abs(x.eta) > 1.566 and abs(x.eta)< 2.5)), electrons))

def get_Jet(jets, pt): #returns a collection of jets that pass the selection performed by the filter function
    return list(filter(lambda x : x.jetId >= 2 and abs(x.eta) < 2.4 and x.pt > pt, jets))

def bjet_filter(jets, tagger, WP): #returns collections of b jets and no b jets (discriminated with btaggers)
    # b-tag working points: mistagging efficiency tight = 0.1%, medium 1% and loose = 10% 
    WPbtagger = {'DeepFlv_T': 0.7264, 'DeepFlv_M': 0.2770, 'DeepFlv_L': 0.0494, 'DeepCSV_T': 0.7527, 'DeepCSV_M': 0.4184, 'DeepCSV_L': 0.1241}
    if(tagger == 'DeepFlv'):
        threshold = WPbtagger[str(tagger) + '_' + str(WP)]
        return list(filter(lambda x : x.btagDeepFlavB >= threshold, jets)), list(filter(lambda x : x.btagDeepFlavB < threshold, jets))
    elif(tagger == 'DeepCSV'):
        threshold = WPbtagger[str(tagger) + '_' + str(WP)]
        return list(filter(lambda x : x.btagDeepB >= threshold, jets)), list(filter(lambda x : x.btagDeepB < threshold, jets))
    else:
        print('Only DeepFlv and DeepCSV accepted! Pleae implement other taggers if you want them.')

def mcbjet_filter(jets): #returns a collection of only b-gen jets (to use only for MC samples)
    return list(filter(lambda x : x.partonFlavour == -5 or x.partonFlavour == 5, jets))

def sameflav_filter(jets, flav): #returns a collection of only b-gen jets (to use only forMC samples)                       
    return list(filter(lambda x : x.partonFlavour == flav, jets))

def get_HT(jets):
    HT = 0.
    for jet in jets:
        HT += jet.pt
    return HT

def trig_map(HLT, year, runPeriod):
    passMu = False
    passEle = False
    passHT = False
    noTrigger = False
    if(year == 2016 and runPeriod != 'H'):
        if(HLT.Mu50 or HLT.TkMu50):
            passMu = True
        if(HLT.Ele115_CaloIdVT_GsfTrkIdT):
            passEle = True  
        if(HLT.PFHT800 or HLT.PFHT900):
            passHT = True
        if not(passMu and passEle and passHT):
            noTrigger = True
    elif(year == 2016 and runPeriod == 'H'):
        if(HLT.Mu50 or HLT.TkMu50):
            passMu = True
        if(HLT.Ele115_CaloIdVT_GsfTrkIdT):
            passEle = True  
        if(HLT.PFHT900):
            passHT = True
        if not(passMu and passEle and passHT):
            noTrigger = True
    elif(year == 2017 and runPeriod != 'B' or year == 2018):
        if(HLT.Mu50):
            passMu = True
        if(HLT.Ele115_CaloIdVT_GsfTrkIdT):
            passEle = True  
        if(HLT.PFHT780 or HLT.PFHT890):
            passHT = True
        if not(passMu and passEle and passHT):
            noTrigger = True
    elif(year == 2017 and runPeriod == 'B'):
        if(HLT.Mu50):
            passMu = True
        if(HLT.PFHT780 or HLT.PFHT890):
            passHT = True
        if not(passMu and passEle and passHT):
            noTrigger = True
    else:
        print('Wrong year! Please enter 2016, 2017, or 2018')
    return passMu, passEle, passHT, noTrigger

def get_ptrel(lepton, jet):
    ptrel = ((jet.p4()-lepton.p4()).Vect().Cross(lepton.p4().Vect())).Mag()/(jet.p4().Vect().Mag())
    return ptrel
 
def presel(PV, muons, electrons, jets): #returns three booleans: goodEvent assure the presence of at least a good lepton vetoing the presence of additional loose leptons, goodMuEvt is for good muon event, goodEleEvt is for good muon event   
    isGoodPV = (PV.ndof>4 and abs(PV.z)<20 and math.hypot(PV.x, PV.y)<2) #basic requirements on the PV's goodness
    VetoMu = get_LooseMu(muons)
    goodMu = get_Mu(muons)
    VetoEle = get_LooseEle(electrons)
    goodEle = get_Ele(electrons)
    goodJet = get_Jet(jets, 25)

    isGoodEvent = ((((len(goodMu) >= 1) and (len(goodEle) == 0)) or ((len(goodMu) == 0) and (len(goodEle) >= 1))) and len(VetoMu) == 0 and len(VetoEle) == 0 and len(goodJet) >= 2)
    isMuon = (len(goodMu) >= 1) and (len(goodEle) == 0) and len(VetoMu) == 0 and len(VetoEle) == 0 and len(goodJet) >= 2
    isElectron = (len(goodMu) == 0) and (len(goodEle) >= 1) and len(VetoMu) == 0 and len(VetoEle) == 0 and len(goodJet) >= 2
    goodEvent = isGoodPV and isGoodEvent
    goodMuEvt = isGoodPV and isMuon
    goodEleEvt = isGoodPV and isElectron
    return goodEvent, goodMuEvt, goodEleEvt
 
def print_hist(infile, plotpath, hist, option = "HIST", log = False, stack = False):
    if not(isinstance(hist, list)):
        c1 = ROOT.TCanvas(infile + "_" + hist.GetName(), "c1", 50,50,700,600)
        hist.Draw(option)            
        c1.Print(plotpath + "/" + infile + "_" + hist.GetName() + ".png")
        c1.Print(plotpath + "/" + infile + "_" + hist.GetName() + ".root")
    elif isinstance(hist, list):
        c1 = ROOT.TCanvas(infile + "_" + hist[0].GetName(), "c1", 50,50,700,600)
        if not (infile == "") or len(hist) > 1:
            c1 = ROOT.TCanvas(infile + "_" + hist[0].GetName() + '_comparison', "c1", 50,50,700,600)
         #else:
            #c1 = ROOT.TCanvas('comparison', "c1", 50,50,700,600)

        if isinstance(hist[0], ROOT.TGraph) or isinstance(hist[0], ROOT.TGraphAsymmErrors):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].GetXaxis().GetTitle()+';'+hist[0].GetYaxis().GetTitle())
            for h in hist:
                h.SetLineColor(colors[i])
                mg.Add(h)
                i += 1
            print mg
            
            #cap = hist[0].GetXaxis().GetTitle()
            mg.SetMinimum(0.001)
            mg.Draw(option)
            Low = hist[0].GetXaxis().GetBinLowEdge(1)
            Nbin = hist[0].GetXaxis().GetNbins()
            High = hist[0].GetXaxis().GetBinUpEdge(Nbin)
            mg.GetXaxis().Set(Nbin, Low, High)
            
            for i in range(hist[0].GetXaxis().GetNbins()):
                u = i + 1
                mg.GetXaxis().SetBinLabel(u, hist[0].GetXaxis().GetBinLabel(u))
            
        elif isinstance(hist[0], ROOT.TEfficiency):
            i = 0
            mg = ROOT.TMultiGraph('mg', hist[0].GetTitle()+';'+hist[0].CreateGraph().GetXaxis().GetTitle()+';'+hist[0].CreateGraph().GetYaxis().GetTitle())

            for h in hist:
                print h
                h.SetLineColor(colors[i])
                mg.Add(h.CreateGraph())
                i += 1
            mg.SetMaximum(1.1)
            mg.SetMinimum(0.001)
            mg.Draw(option)
            
        elif isinstance(hist[0], ROOT.TH1F):
            mg = ROOT.THStack()
            i = 0
            for h in hist:
                h.SetLineColor(colors[i])
                if stack:
                    h.SetFillColor(colors[i])
                    mg.Add(h)
                    i += 1
                    mg.Draw(option)
                    mg.GetXaxis().SetTitle(hist[0].GetXaxis().GetTitle())
                    mg.GetYaxis().SetTitle(hist[0].GetYaxis().GetTitle())
                else:
                  for h in hist:
                    h.Draw(option+'SAME')

        #c1.Modified()
        #c1.Update()
        if log:
            c1.SetLogy(1)
        c1.Pad().Modified()
        c1.Pad().Update()
        c1.BuildLegend()
        #c1.Modified()
        #c1.Update()
        c1.Pad().Modified()
        c1.Pad().Update()
        
        if not (infile == ""):
            c1.Print(plotpath + "/" + infile + "_" + hist[0].GetName() + '_comparison.png')
            c1.Print(plotpath + "/" + infile + "_" + hist[0].GetName() + '_comparison.root')
        else:
            c1.Print(plotpath + "/" + 'comparison.png')
            c1.Print(plotpath + "/" + 'comparison.root')

def save_hist(infile, plotpath, hist, option = "HIST"):
     fout = ROOT.TFile.Open(plotpath + "/" + infile +".root", "UPDATE")
     fout.cd()
     hist.Write()
     fout.Close()

def miniisoscan(isMu,threshold, lepton):
    for lepton in leptons:
        if(isMC and (lepton.genPartFlav == 1 or lepton.genPartFlav == 15)):
            totalMClep += 1.
            if (lepton.miniPFRelIso_all < threshold):
                if (lepton.pt > 50):
                    lepmatch_iso0p1_pt_50 += 1.
                if (lepton.pt > 75):
                    lepmatch_iso0p1_pt_75 += 1.
                if (lepton.pt > 100):
                    lepmatch_iso0p1_pt_100 += 1.
                if (lepton.pt > 125):
                    lepmatch_iso0p1_pt_125 += 1.
        if not(isMC and (lepton.genPartFlav == 1 or lepton.genPartFlav == 15)):
            totalnoMClep += 1.
            if (lepton.miniPFRelIso_all < threshold):
                if (lepton.pt > 50):
                    lepnomatch_iso0p1_pt_50 += 1.
                if (lepton.pt > 75):
                    lepnomatch_iso0p1_pt_75 += 1.
                if (lepton.pt > 100):
                    lepnomatch_iso0p1_pt_100 += 1.
                if (lepton.pt > 125):
                    lepnomatch_iso0p1_pt_125 += 1.
    return totalMClep,lepmatch_iso0p1_pt_50,lepmatch_iso0p1_pt_75,lepmatch_iso0p1_pt_100,lepmatch_iso0p1_pt_125,totalnoMClep,lepnomatch_iso0p1_pt_50,lepnomatch_iso0p1_pt_75,lepnomatch_iso0p1_pt_100,lepnomatch_iso0p1_pt_125
###############################################
###          End of generic utils           ###   
###############################################

###############################################
###         Begin of topreco_utils          ###   
###############################################
def EqSolv(a1, a2, a3, a4):
    if type(a1) != float and type(a1) != int:
        if type(a1) == list:
            a = a1[0]
            b = a1[1]
            c = a1[2]
            d = a1[3]
            result = []
        elif type(a1) == dict:
            a = a1['a']
            b = a1['b']
            c = a1['c']
            d = a1['d']
            result = {}
    else:
        a = a1
        b = a2
        c = a3
        d = a4
        result = []
   
    if a != 0.:
        q = (3.*a*c - b*b)/(9.*a*a)
        r = (9.*a*b*c - 27.*a*a*d - 2.*b**3.)/(54.*a**3.)
        Delta = q**3. + r**2.
    
        if Delta <= 0: #da testare
            rho = (-(q**(3)))**(0.5)
            theta = math.acos(r/rho)
            s = cmath.rect((-q)**(0.5), theta/3.0)
            t = cmath.rect((-q)**(0.5), -theta/3.0)
        if Delta > 0:
            args = r+(Delta)**(0.5)
            argt = r-(Delta)**(0.5)
            signs = math.copysign(1, args)
            signt = math.copysign(1, argt)
            s = complex(signs*TMath.Power(abs(args), 1./3), 0)
            t = complex(signt*TMath.Power(abs(argt), 1./3), 0)
        
        rpar = b/(3.*a)
        x1 = s + t + complex(-rpar, 0)
        x2 = (s+t)*complex(-0.5, 0) - complex(rpar, 0) + (s-t)*(1j)*complex((3.**(0.5))/2., 0)
        x3 = (s+t)*complex(-0.5, 0) - complex(rpar, 0) - (s-t)*(1j)*complex((3.**(0.5))/2., 0)

        if abs(x1.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x1': x1.real})
            else:
                result.append(x1.real)
        if abs(x2.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x2': x2.real})
            else:
                result.append(x2.real)
        if abs(x3.imag)<0.0001:
            if type(a1)==dict:
                result.update({'x3': x3.real})
            else:
                result.append(x3.real)            
        return result
    else:
        print 'p1'
        result = None
        return result

class TopUtilities():
    def __init__(self):
        if False:
            print'ok'

    def NuMomentum(self,  leptonPx, leptonPy, leptonPz, leptonPt, leptonE, metPx, metPy):
        mW = 80.399

        MisET2 = (metPx**2. + metPy**2.)
        mu = (mW**2.)/2. + metPx*leptonPx + metPy*leptonPy
        
        a = mu*leptonPz/leptonPt**2
        a2 = a**2.
        b = (leptonE**2.*MisET2 - mu**2.)/leptonPt**2
        
        IsNegative = False

        p4nu_rec = []
        p4W_rec = ROOT.TLorentzVector()
        p4b_rec = ROOT.TLorentzVector()
        p4Top_rec = ROOT.TLorentzVector()
        p4lep_rec = ROOT.TLorentzVector()
        #neutrino = None#ROOT.TLorentzVector()
        #neutrino = ROOT.TLorentzVector()

        p4lep_rec.SetPxPyPzE(leptonPx, leptonPy, leptonPz, leptonE)
        p40_rec = ROOT.TLorentzVector(0.0, 0.0, 0.0, 0.0)

        if (a2-b) > 0:
            
            isNegative = False
        else:
            IsNegative = True

        root = TMath.Power((a2-b), 0.5)
        pz = []
        pz.append((a + root).real)
        #pz1 = a + root
        pz.append((a - root).real)
        #pz2 = a - root
        nNuSol = 2
        pznu = 0.0

        for i in range(nNuSol):
          Enu = TMath.Power((MisET2 + pz[i]**2), 0.5)
          #Enu = TMath.Power((MisET2 + pznu**2), 0.5)
          p4nu = ROOT.TLorentzVector()
          p4nu.SetPxPyPzE(metPx, metPy, pznu, Enu)
          #p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu)
          p4nu_rec.append(p4nu)

        neutrino = copy.deepcopy(p4nu_rec)
        return neutrino, IsNegative
        '''
            
            #Enu = (MisET2 + pznu**2)**0.5
            #p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu)
            #neutrino = p4nu_rec
            
            EquationCoeff1 = [1,
                              (-3 * leptonPy * mW / leptonPt),
                              (((mW**2.) * (2. * leptonPy**2.) / (leptonPt**2)) + mW**2. - (4. * leptonPx**3. * metPx / leptonPt**2) - (4. * leptonPx**2. * leptonPy * metPy / leptonPt**2)),
                              ((4. * leptonPx**2. * mW * metPy / leptonPt) - leptonPy * mW**3. / leptonPt)
                              ]

            EquationCoeff2 = copy.copy(EquationCoeff1)
            EquationCoeff2[1] = - EquationCoeff2[1]
            EquationCoeff2[3] = - EquationCoeff2[3]
            #solutions1 = EquationSolver.EqSolv(EquationCoeff1,'','','')
            #solutions2 = EquationSolver.EqSolv(EquationCoeff2,'','','')

            solutions = [EqSolv(EquationCoeff1,'','',''), EqSolv(EquationCoeff2,'','','')]

            deltaMin = 14000.**2.
            zeroValue = - mW**2./(4.*leptonPx)
            minPx = 0.
            minPy = 0.

            ncoeff = ['x1', 'x2', 'x3']

            for j in range(2):
                for value in solutions[j]:
                    if value < 0.:
                        continue
                    p_x = (value**2. - mW**2.) / (4.*leptonPx)
                    p_y = ((mW**2.)*leptonPy + 2.*leptonPx*leptonPy*p_x - mW*leptonPt*value) / (2*leptonPx**2.)
                    Delta2 = (p_x - metPx)**2. + (p_y - metPy)**2.
                    if Delta2 < deltaMin and Delta2 > 0:
                        deltaMin = copy.copy(Delta2)
                        minPx = copy.copy(p_x)
                        minPy = copy.copy(p_y)

            pyZeroValue = mW**2.*leptonPx + 2.*leptonPy*zeroValue
            delta2ZeroValue = (zeroValue - metPx)**2. + (pyZeroValue - metPy)**2.

            if deltaMin == 14000.**2. :
              neutrino = None
              return neutrino, IsNegative

            if delta2ZeroValue < deltaMin :
                deltaMin = copy.copy(delta2ZeroValue)
                minPx = copy.copy(zeroValue)
                minPy = copy.copy(pyZeroValue)

            mu_Minimum = mW**2./2. + minPx*leptonPx*minPy*leptonPy
            a_Minimum = (mu_Minimum*leptonPz) / (leptonE**2. - leptonPz**2.)
            pznu = a_Minimum
            Enu = TMath.Power((minPx**2. + minPy**2. + pznu**2.), 0.5)
            p4nu = ROOT.TLorentzVector()
            p4nu.SetPxPyPzE(minPx, minPy, pznu, Enu)
            #p4nu_rec.SetPxPyPzE(minPx, minPy, pznu, Enu)
            p4nu_rec.append(p4nu)
            neutrino = copy.deepcopy(p4nu)
        '''
        #return neutrino, IsNegative

    def top4Momentum(self, lepton, jet, metPx, metPy):
        #topMt = self.topMtw(lepton, jet, metPx, metPy)
        '''if topMt == None:
        self.reco_topqv = None
        self.neutrino = None
        return None'''
        dR_lepjet = None
        dR_lepjet = deltaR(jet.Eta(), jet.Phi(), lepton.Eta(), lepton.Phi())
        neutrino, IsNeg  = self.NuMomentum(lepton.Px(), lepton.Py(), lepton.Pz(), lepton.Pt(), lepton.Energy(), metPx, metPy)
        besttop = None
        #recochi = []
        chi2 = 100000000.

        rtop = ROOT.TLorentzVector()
        if isinstance(neutrino, list):
          for i in range(len(neutrino)):
            if dR_lepjet > 0.4:
              rtop = lepton + jet + neutrino[i]
            else:
              rtop = jet + neutrino[i]
            rchi = Chi_TopMass(rtop.M())
            if rchi < chi2:
              besttop = copy.deepcopy(rtop)
        elif isinstance(neutrino, ROOT.TLorentzVector):
          if dR_lepjet > 0.4:
            rtop = lepton + jet + neutrino
          else:
            rtop = jet + neutrino
          rchi = Chi_TopMass(rtop.M())
          besttop = copy.deepcopy(rtop)
        elif neutrino is None:
          besttop = None
        
        #top = lepton + jet + neutrino
        return besttop, IsNeg, dR_lepjet

    def topMtw(self, lepton, jet, metPx, metPy):
        lb = lepton + jet
        mlb2 = lb.M2()
        ptlb = lb.Pt()
        pxlb = lb.Px()
        pylb = lb.Py() 
        '''
        if mlb2 < 0.:
            self.reco_topMt = None
            self.IsParticle = False
            return None
        '''
        etlb = TMath.Power((mlb2 + ptlb**2.), 0.5)
        metPt = TMath.Power((metPx**2. + metPy**2.), 0.5)

        return TMath.Power((mlb2 + 2.*(etlb*metPt - pxlb*metPx - pylb*metPy)), 0.5)
###############################################
###          End of topreco_utils           ###   
###############################################

###############################################
### Begin of framework/treeReaderArrayTools ###   
###############################################
def InputTree(tree,entrylist=None):
    """add to the PyROOT wrapper of a TTree a TTreeReader and methods readBranch, arrayReader, valueReader""" 
    if hasattr(tree, '_ttreereader'): return tree # don't initialize twice
    tree.entry = -1
    tree._entrylist = entrylist
    tree._ttreereader = ROOT.TTreeReader(tree,tree._entrylist)
    tree._ttreereader._isClean = True
    tree._ttrvs = {}
    tree._ttras = {}
    tree._leafTypes = {}
    tree._ttreereaderversion = 1
    tree.arrayReader = types.MethodType(getArrayReader, tree)
    tree.valueReader = types.MethodType(getValueReader, tree)
    tree.readBranch = types.MethodType(readBranch, tree)
    tree.gotoEntry = types.MethodType(_gotoEntry, tree)
    tree.readAllBranches = types.MethodType(_readAllBranches, tree)
    tree.entries = tree._ttreereader.GetEntries(False)
    tree._extrabranches={}
    return tree

def getArrayReader(tree, branchName):
    """Make a reader for branch branchName containing a variable-length value array."""
    if branchName not in tree._ttras:
       if not tree.GetBranch(branchName): raise RuntimeError, "Can't find branch '%s'" % branchName
       leaf = tree.GetBranch(branchName).GetLeaf(branchName)
       if not bool(leaf.GetLeafCount()): raise RuntimeError, "Branch %s is not a variable-length value array" % branchName
       typ = leaf.GetTypeName()
       tree._ttras[branchName] = _makeArrayReader(tree, typ, branchName)
    return tree._ttras[branchName]

def getValueReader(tree, branchName):
    """Make a reader for branch branchName containing a single value."""
    if branchName not in tree._ttrvs:
       if not tree.GetBranch(branchName): raise RuntimeError, "Can't find branch '%s'" % branchName
       leaf = tree.GetBranch(branchName).GetLeaf(branchName)
       if bool(leaf.GetLeafCount()) or leaf.GetLen()!=1 : raise RuntimeError, "Branch %s is not a value" % branchName
       typ = leaf.GetTypeName()
       tree._ttrvs[branchName] = _makeValueReader(tree, typ, branchName)
    return tree._ttrvs[branchName]

def clearExtraBranches(tree):
    tree._extrabranches = {}

def setExtraBranch(tree,name,val):
    tree._extrabranches[name] = val

def readBranch(tree, branchName):
    """Return the branch value if the branch is a value, and a TreeReaderArray if the branch is an array"""
    if tree._ttreereader._isClean: raise RuntimeError, "readBranch must not be called before calling gotoEntry"
    if branchName in tree._extrabranches:
        return tree._extrabranches[branchName]
    elif branchName in tree._ttras:
        return tree._ttras[branchName]
    elif branchName in tree._ttrvs: 
        ret = tree._ttrvs[branchName].Get()[0]
        return ord(ret) if type(ret)==str else ret
    else:
        branch = tree.GetBranch(branchName)
        if not branch: raise RuntimeError, "Unknown branch %s" % branchName
        leaf = branch.GetLeaf(branchName)
        typ = leaf.GetTypeName()
        if leaf.GetLen() == 1 and not bool(leaf.GetLeafCount()): 
            _vr = _makeValueReader(tree, typ, branchName)
            tree.gotoEntry(tree.entry,forceCall=True) # force calling SetEntry as a new ValueReader was created
            ret = _vr.Get()[0]
            return ord(ret) if type(ret)==str else ret
        else:
            _ar = _makeArrayReader(tree, typ, branchName)
            tree.gotoEntry(tree.entry,forceCall=True) # force calling SetEntry as a new ArrayReader was created
            return _ar

####### PRIVATE IMPLEMENTATION PART #######

def _makeArrayReader(tree, typ, nam):
    if not tree._ttreereader._isClean: _remakeAllReaders(tree)
    ttra = ROOT.TTreeReaderArray(typ)(tree._ttreereader, nam)
    tree._leafTypes[nam] = typ
    tree._ttras[nam] = ttra;
    return tree._ttras[nam]

def _makeValueReader(tree, typ, nam):
    if not tree._ttreereader._isClean: _remakeAllReaders(tree)
    ttrv = ROOT.TTreeReaderValue(typ)(tree._ttreereader, nam)
    tree._leafTypes[nam] = typ
    tree._ttrvs[nam] = ttrv
    return tree._ttrvs[nam]

def _remakeAllReaders(tree):
    _ttreereader = ROOT.TTreeReader(tree, getattr(tree, '_entrylist', None))
    _ttreereader._isClean = True
    _ttrvs = {}
    for k in tree._ttrvs.iterkeys():
        _ttrvs[k] = ROOT.TTreeReaderValue(tree._leafTypes[k])(_ttreereader,k)
    _ttras = {}
    for k in tree._ttras.iterkeys():
        _ttras[k] = ROOT.TTreeReaderArray(tree._leafTypes[k])(_ttreereader,k)
    tree._ttrvs = _ttrvs
    tree._ttras = _ttras
    tree._ttreereader = _ttreereader
    tree._ttreereaderversion += 1

def _readAllBranches(tree):
    tree.GetEntry(_currentTreeEntry(tree))

def _currentTreeEntry(tree):
    if tree._entrylist:
        return tree._entrylist.GetEntry(tree.entry)
    else:
        return tree.entry

def _gotoEntry(tree, entry, forceCall=False):
    tree._ttreereader._isClean = False
    if tree.entry != entry or forceCall:
        if (tree.entry == entry-1 and entry!=0):
            tree._ttreereader.Next()
        else:
            tree._ttreereader.SetEntry(entry)
        tree.entry = entry
###############################################
###  End of framework/treeReaderArrayTools  ###
###############################################

###############################################
###      Begin of framework/datamodel       ###
###############################################
class Event:
    """Class that allows seeing an entry of a PyROOT TTree as an Event"""
    def __init__(self,tree,entry):
        self._tree = tree
        self._entry = entry
        self._tree.gotoEntry(entry)
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        return self._tree.readBranch(name)
    def __getitem__(self,attr):
        return self.__getattr__(attr)
    def eval(self,expr):
        """Evaluate an expression, as TTree::Draw would do. 

           This is added for convenience, but it may perform poorly and the implementation is not bulletproof,
           so it's better to rely on reading values, collections or objects directly
        """ 
        if not hasattr(self._tree, '_exprs'):
            self._tree._exprs = {}
            # remove useless warning about EvalInstance()
            import warnings
            warnings.filterwarnings(action='ignore', category=RuntimeWarning, 
                                    message='creating converter for unknown type "const char\*\*"$')
            warnings.filterwarnings(action='ignore', category=RuntimeWarning, 
                                    message='creating converter for unknown type "const char\*\[\]"$')
        if expr not in self._tree._exprs:
            formula = ROOT.TTreeFormula(expr,expr,self._tree)
            if formula.IsInteger():
                formula.go = formula.EvalInstance64
            else:
                formula.go = formula.EvalInstance
            self._tree._exprs[expr] = formula
            # force sync, to be safe
            self._tree.GetEntry(self._entry)
            self._tree.entry = self._entry
            #self._tree._exprs[expr].SetQuickLoad(False)
        else:
            self._tree.gotoEntry(entry)
            formula = self._tree._exprs[expr]
        if "[" in expr: # unclear why this is needed, but otherwise for some arrays x[i] == 0 for all i > 0
            formula.GetNdata()
        return formula.go()

class Object:
    """Class that allows seeing a set branches plus possibly an index as an Object"""
    def __init__(self,event,prefix,index=None):
        self._event = event
        if not (prefix == 'LHEPdfWeight' or prefix == 'LHEScaleWeight' or prefix == 'PSWeight'):
            self._prefix = prefix+"_"
        else:
            self._prefix = prefix
        self._index = index
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        if name[:2] == "__" and name[-2:] == "__":
            raise AttributeError
        val = getattr(self._event,self._prefix+name)
        if self._index != None:
            val = val[self._index]
        val = ord(val) if type(val)==str else val # convert char to integer number
        self.__dict__[name] = val ## cache
        return val
    def __getitem__(self,attr):
        return self.__getattr__(attr)
    def p4(self):
        ret = ROOT.TLorentzVector()
        ret.SetPtEtaPhiM(self.pt,self.eta,self.phi,self.mass)
        return ret
    def DeltaR(self,other):
        if isinstance(other,ROOT.TLorentzVector):
          deta = abs(other.Eta()-self.eta)
          dphi = abs(other.Phi()-self.phi)
        else:
          deta = abs(other.eta-self.eta)
          dphi = abs(other.phi-self.phi)
        while dphi > math.pi:
          dphi = abs(dphi - 2*math.pi)
        return math.sqrt(dphi**2+deta**2)
    def subObj(self,prefix):
        return Object(self._event,self._prefix+prefix)
    def __repr__(self):
        return ("<%s[%s]>" % (self._prefix[:-1],self._index)) if self._index != None else ("<%s>" % self._prefix[:-1])
    def __str__(self):
        return self.__repr__()

class Collection:
    def __init__(self,event,prefix,lenVar=None):
        self._event = event
        self._prefix = prefix
        if lenVar != None:
            self._len = getattr(event,lenVar)
        else:
            self._len = getattr(event,"n"+prefix)
        self._cache = {}
    def __getitem__(self,index):
        if type(index) == int and index in self._cache: return self._cache[index]
        if index >= self._len: raise IndexError, "Invalid index %r (len is %r) at %s" % (index,self._len,self._prefix)
        ret = Object(self._event,self._prefix,index=index)
        if type(index) == int: self._cache[index] = ret
        return ret
    def __len__(self):
        return self._len
###############################################
###        End of framework/datamodel       ###
###############################################



###############################################
###       Begin of tree_skimmer_utlis       ###
###############################################
def pytocpptypes(typ):
    if type(typ) == int:
        return "/I"
    elif type(typ) == float:
        return "/F"
    elif type(typ) == str:
        return "/C"
    elif type(typ) == array.array:
        single = pytocpptypes(typ[0])
        return "[" + str(len(typ)) + "]" + single

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
        self.weightedSysts = []
        for i in range(150):
            self.weightedSysts.append(array.array('f', [0.]))
        self.eventBasedScenario = ""
        self.wCats = []
        for i in range(10):
            self.wCats.append(array.array('f', [0.]))
        self.eventBasedNames = []
        for i in range(10):
            self.eventBasedNames.append("")
        self.baseSelections = []
        for i in range(20):
            self.baseSelections.append(array.array('i', [0]))
        self.weightedNames = []
        for i in range(150):
            self.weightedNames.append("")
        self.selectionsNames = []
        for i in range(20):
            self.selectionsNames.append("")
        self.categoriesNames = []
        for i in range(10):
            self.categoriesNames.append("")

    def initTreesSysts(self, trees, tfile):
        tfile.cd()

        for s in range(self.nSelections):
            trees[s] = ROOT.TTree(str("events_"+self.selectionsNames[s]), "")
            isEventBasedSelection = self.isEventBasedSelection(s)
            #print trees[s], isEventBasedSelection
            self.initTreesSysts2S(trees[s], isEventBasedSelection)
            
    def initTreesSysts2S(self, tree, isEventBasedSyst):
        isEventBasedSyst = False
        Max = self.maxSysts
        if self.shortPDFFiles:
            Max = self.maxSystsNonPDF
        for sy in range(Max):
            if isEventBasedSyst and sy > 0:
                continue
            ns = str(self.weightedNames[sy])
            if sy == 0:
                ns = "w_nominal"
            #print "Branch: ", ns
            tystring = str(ns + pytocpptypes(self.weightedSysts[int(sy)]))
            tree.Branch(ns, self.weightedSysts[int(sy)], tystring)
        for c in range(self.nCategories):         
            cname = str(self.categoriesNames[c])
            tystring = str(cname + pytocpptypes(self.wCats[c]))
            #print "Branch: ", ns
            if c > 1: tree.Branch(cname, self.wCats[c], tystring)

    def addSelection(self, selection):
        self.selectionsNames[self.nSelections] = (str(selection))
        initSelection = self.nSelections
        self.nSelections += 1
        for sc in range(self.nEventBasedSysts):
            self.selectionsNames[self.nSelections] = (str(selection) + "_" + str(self.eventBasedNames[sc]))
            self.baseSelections[self.nSelections][0] = initSelection
            self.nSelections += 1

    def setSelectionsNames(self, selections):
        for s in range(self.nSelections):
            if s < (len(self.selectionNames) - 1):
                self.selectionsNames[s] = copy.deepcopy(selections[s])
            else:
                self.selectionsNames[s] = copy.deepcopy(selections[s])

    def branchTreesSysts(self, trees, selection, name, tfile, f):
        tfile.cd()
        tname = ROOT.TString(name)
        for s in range(self.nSelections):
            #print " selection # ", str(s), " name ", str(self.selectionsNames[s]), " name ", str(tname)
            #print " tree is ", str(trees[s])
            tystring = str(name + pytocpptypes(f))
            if selection == self.selectionsNames[s]:
                trees[s].Branch(name, f, tystring)
            if self.isEventBasedSelection(s):
                if selection == self.selectionNames[self.baseSelections[s][0]] :
                    trees[s].Branch(name, f, tystring)

    def fillTreesSysts(self, trees, selection):
        for s in range(self.nSelections):
            if selection == self.selectionsNames[s] and not self.isEventBasedSelection(s) and self.eventBasedScenario == "nominal" :
                if isinstance(trees[s], ROOT.TTree):
                    trees[s].Fill()
            if self.isEventBasedSelection(s):
                if self.eventBasedScenario in self.selectionsNames[s] and selection == self.selectionsNames[self.baseSelections[s][0]]:
                    if isinstance(trees[s], ROOT.TTree):
                        trees[s].Fill()

    def writeTreesSysts(self, trees, tfile):
        tfile.cd()
        for s in range(self.nSelections):
            if isinstance(trees[s], ROOT.TTree):
                trees[s].Write()

    def prepareDefault(self, addDefault, addPDF, addQ2, addTopPt, addVHF, addTTSplit, numPDF=102):
        self.addPDF = copy.deepcopy(addPDF)
        self.addQ2 = copy.deepcopy(addQ2)
        self.addTopPt = copy.deepcopy(addTopPt)
        self.addVHF = copy.deepcopy(addVHF)
        self.addTTSplit = copy.deepcopy(addTTSplit)
        self.nPDF = copy.deepcopy(numPDF)
        self.nCategories = 1
        self.categoriesNames[0] = ""
        self.wCats[0] = array.array('f', [1.0])
        self.nSelections = 0 
        self.eventBasedScenario = "nominal"

        if addDefault:
            self.weightedNames[0] = "w_nominal"
            self.weightedNames[1] = "lepSF"
            self.weightedNames[2] = "lepUp"
            self.weightedNames[3] = "lepDown"
            self.weightedNames[4] = "puSF"
            self.weightedNames[5] = "puUp"
            self.weightedNames[6] = "puDown"
            self.weightedNames[7] = "PFSF"
            self.weightedNames[8] = "PFUp"
            self.weightedNames[9] = "PFDown"
            #self.weightedNames[1] = "btagUp"
            #self.weightedNames[2] = "btagDown"
            #self.weightedNames[3] = "mistagUp"
            #self.weightedNames[4] = "mistagDown"
            #self.weightedNames[10] = "isoDown"
            #self.weightedNames[11] = "trigUp"
            #self.weightedNames[12] = "trigDown"
            self.setMax(10)
            self.setMaxNonPDF(9)
            self.weightedNames[self.maxSysts] = ""

        if addQ2: 
            self.weightedNames[self.maxSysts] = "q2Up"
            self.weightedNames[self.maxSysts+1] = "q2Down"
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2) 
            self.weightedNames[self.maxSysts] = ""

        if addTopPt:
            self.weightedNames[self.maxSysts] = "topPtWeightUp"
            self.weightedNames[self.maxSysts+1] = "topPtWeightDown"
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2)
            self.weightedNames[self.maxSysts] = ""

        if addVHF:
            self.weightedNames[self.maxSysts]="VHFWeightUp"
            self.weightedNames[self.maxSysts+1] = "VHFWeightDown"
            self.setMax(self.maxSysts+2)
            self.setMaxNonPDF(self.maxSystsNonPDF+2)
            self.weightedNames[self.maxSysts] = ""

        if addTTSplit:
            self.nCategories = 4
            categoriesNames[1] = "TT0lep"
            categoriesNames[2] = "TT1lep"
            categoriesNames[3] = "TT2lep"
            self.wCats[1] = array.array('f', [1.0])
            self.wCats[2] = array.array('f', [1.0])
            self.wCats[3] = array.array('f', [1.0])

        if addPDF:
            self.weightedNames[self.maxSysts] = "pdf_totalUp"
            self.weightedNames[self.maxSysts+1] = "pdf_totalDown"
            self.weightedNames[self.maxSysts+2] = "pdf_asUp"
            self.weightedNames[self.maxSysts+3] = "pdf_asDown"
            self.weightedNames[self.maxSysts+4] = "pdf_zmUp"
            self.weightedNames[self.maxSysts+5] = "pdf_zmDown"
            self.setMax(self.maxSysts+6)
            self.setMaxNonPDF(self.maxSystsNonPDF+6)
            nPDF = self.nPDF
            for i in range(nPDF):
                ss = str(i+1)
                self.weightedNames[i+self.maxSysts] = "pdf" + str(ss)

            self.setMax(maxSysts+nPDF)
            self.weightedNames[self.maxSysts] = ""

    def addSyst(self, name):
        self.weightedNames[self.maxSysts] = copy.deepcopy(name)
        self.setMax(maxSysts+1)
        if "pdf" in name:
            self.setMaxNonPDF(maxSysts+1)
        self.weightedNames[self.maxSysts] = ""

    def addSystNonPDF(self, name):
        self.weightedNames[self.maxSystsNonPDF] = copy.deepcopy(name)
        self.setMaxNonPDF(maxSystsNonPDF+1)
        nPDF = self.nPDF
        for i in range(nPDF):
            ss = str(i+1)
            self.weightedNames[i+self.maxSystsNonPDF] = "pdf" + str(ss)
        self.setMax(maxSystsNonPDF+nPDF)
        self.weightedNames[self.maxSysts] = ""

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
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        up = name + "Up"
        down = name + "Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom
        
        self.setSystValue(up, valueup*zerofact[0])
        self.setSystValue(down, valuedown*zerofact[0])

    def setWTagSF(self, name, SF_nom, SF_up, SF_down, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
           zerofact = self.weightedSysts[0]
        up = name+"Up"
        down = name+"Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom

        self.setSystValue(up, valueup*zerofact[0])
        self.setSystValue(down, valuedown*zerofact[0])

    def setTrigSF(self, name, SF_nom, SF_up, SF_down, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        up = name+"Up"
        down = name+"Down"
        valueup = SF_up/SF_nom
        valuedown = SF_down/SF_nom
        if SF_nom == 0:
            valueup = 0
            valuedown = 0

        self.setSystValue(up, valueup*zerofact[0])
        self.setSystValue(down, valuedown*zerofact[0])

    def setPDFWeights(self, wpdfs, xsections, numPDFs, wzero=1.0, mult=True):
        zerofact = array.array('f', [1.0])
        rms, mean = 0., 0.
        if mult:
            zerofact = self.weightedSysts[0]
        for i in range(numPDFs+1):
            if wzero != 0 and xsections[i] != 0:
                try:
                    pvalue = wpdfs[i] / (wzero*xsections[i])
                except math.isnan(pvalue):
                    pvalue = 1.
                self.setPDFValue(i, zerofact[0]*wpdfs[i]/(wzero*xsections[i]) )
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
            self.setSystValue("pdf_asDown", zerofact[0])
            self.setSystValue("pdf_zmUp", self.getPDFValue(self.nPDF-1.)/wzero)
            self.setSystValue("pdf_zmDown", zerofact[0])
            if math.isnan(rms):
                rms += 0.
            self.setSystValue("pdf_totalUp", zerofact[0]*(1.+rms))
            self.setSystValue("pdf_totalDown", zerofact[0]*(1.-rms))

    def setTWeight(self, tweight, wtotsample=1.0, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        self.setSystValue("topPtWeightUp", zerofact[0]*tweight/wtotsample)
        self.setSystValue("topPtWeightDown", zerofact[0]/tweight*wtotsample)

    def setVHFWeight(self, vhf, mult=True, shiftval=0.65):
        zerofact = array.array('f', [1.0])
        w_shift = 0.0
        if vhf > 1:
            w_shift = shiftval
        if mult: 
            zerofact[0] = self.weightedSysts[0]
        
        self.setSystValue("VHFWeightUp", zerofact[0]*(1+w_shift))
        self.setSystValue("VHFWeightDown", zerofact[0]*(1-w_shift))

    def setQ2Weights(self, q2up, q2down, wzero=1.0, mult=True):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact[0] = self.weightedSysts[0]
  
        self.setSystValue("q2Up", zerofact[0]*q2up/wzero)
        self.setSystValue("q2Down", zerofact[0]*q2down/wzero)

    def getPDFValue(self, numPDF):
        if not self.addPDF:
            print "error! No PDF used, this will do nothing."
            return 0.
        MIN = self.maxSystsNonPDF
        return float(self.weightedSysts[numPDF+MIN][0])

    def setPDFValue(self, numPDF, w):
        if not self.addPDF:
            print "error! No PDF used, this will do nothing."
            return
        MIN = self.maxSystsNonPDF
        self.weightedSysts[numPDF+MIN][0] = w

    
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
            arwcats = array.array('f', [wcats[i]])
            self.wCats[i] = copy.deepcopy(arwcats)
                
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
                    wcats[c] = array.array('f', 1.0)
                    ws = systWeights[sy]*wcats[c][0]
                else:
                    if nFirstSysts != 0:
                        wcats[c] = array.array('f', 1.0)
                    ws = self.weightedSysts[sy][0]*wcats[c][0]

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
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        MAX = self.maxSysts
        for sy in range(MAX):
            if self.weightedNames[sy] == name:
                self.weightedSysts[sy][0] = value*zerofact[0]

    def setSystValuePlace(self, place, value, mult=False):
        zerofact = array.array('f', [1.0])
        if mult:
            zerofact = self.weightedSysts[0]
        self.weightedSysts[place][0] = value*zerofact[0]

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
###############################################
###        End of tree_skimmer_utlis        ###
###############################################
