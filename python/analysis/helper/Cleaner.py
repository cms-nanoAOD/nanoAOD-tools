#!/usr/bin/env python
from math import fabs, cos, sqrt
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi, deltaR, closest
from ROOT import TLorentzVector

def deltaPhi(phi1,phi2):
    PHI = fabs(phi1-phi2)
    if (PHI<=3.14159265):
        return PHI
    else:
        return 2*3.14159265-PHI

def getPt(pO):
    return pO.pt

def bitwise(STATUS,BIT):

    myBIT = ( int(STATUS) >> int(BIT) ) & 0x1

    return myBIT

def cleanFromlepton(InList,leptonList,dR=0.4):
    
    for lepton in leptonList:
        for element in InList:
            if deltaR(lepton,element)<0.4:
                InList.remove(element)
    InList.sort(key=getPt, reverse=True)

#Find the last particle in the chain before decay 23 -> 23 -> *23* -> 13 -13, return an GEN Object/ RECO??
def FindGenParticle(InList, pdgid):

    newList=[]
    for element in InList:
        if element.pdgId in pdgid:
            #BIT 0; 8; 13; 14
            #if bitwise(element.statusFlags,0) and \
            #        bitwise(element.statusFlags,8) and \
            #        bitwise(element.statusFlags,13) and \
            #        bitwise(element.statusFlags,14):
            #if element.status in ['62','1']:
            newList.append(element)
    return newList

def FindGenParticlebyStatus(InList, pdgid, statusid1, statusid2):

    newList=[]
    for element in InList:
        if element.pdgId in pdgid and element.status==statusid1:
            moId=element.genPartIdxMother
            if InList[moId].status==statusid2:
                newList.append(element)
    return newList

def transverseMass(lepPt, lepPhi, met, metPhi):
    cosDPhi = cos(deltaPhi(lepPhi,metPhi))
    return sqrt(2*lepPt*met*(1-cosDPhi))

def invariantMass(p1_pt, p1_eta, p1_phi, p1_mass, p2_pt, p2_eta, p2_phi, p2_mass):

    if p1_pt<0 or p2_pt<0: return -1
    p1 = TLorentzVector()
    p2 = TLorentzVector()
    p1.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_mass)
    p2.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_mass)
    return (p1+p2).M()

def invariantMassPt(p1_pt, p1_eta, p1_phi, p1_mass, p2_pt, p2_eta, p2_phi, p2_mass):

    if p1_pt<0 or p2_pt<0: return -1
    p1 = TLorentzVector()
    p2 = TLorentzVector()
    p1.SetPtEtaPhiM(p1_pt, p1_eta, p1_phi, p1_mass)
    p2.SetPtEtaPhiM(p2_pt, p2_eta, p2_phi, p2_mass)
    return (p1+p2).Pt()

def invariantDoubleMass(Z_pt, Z_eta, Z_phi, jet1_pt, jet1_eta, jet1_phi, jet2_pt, jet2_eta, jet2_phi):

    if jet1_pt<0 or jet2_pt<0: return -1
    j1 = TLorentzVector()
    j2 = TLorentzVector()
    Z = TLorentzVector()
    Z.SetPtEtaPhiM(Z_pt, Z_eta, Z_phi, 91.)
    j1.SetPtEtaPhiM(jet1_pt, jet1_eta, jet1_phi, 5.)
    j2.SetPtEtaPhiM(jet2_pt, jet2_eta, jet2_phi, 5.)
    return (j1+j2+Z).M()
