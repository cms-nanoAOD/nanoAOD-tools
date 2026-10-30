#!/usr/bin/env python
import os, sys
import ROOT
import numpy as np
def Probability(pt,eta,SF_cent,SF_Up,SF_Down,WP,Deepcsv_score,hadron_flavour,syst,datayear):
    Effi_hist = []
    Effi_FIle = ROOT.TFile('QCD_Pt-20toInf_MuEnriched_Tagging_Efficiency.root')
    Tight_b_wp={
                '2016' : 0.7527,        #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
                '2017' : 0.8001,        #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
                '2018' : None}
    Medium_b_wp={
                '2016' : 0.4184,
                '2017' : 0.4941,
                '2018' : None}
    loose_b_wp={
                '2016' : 0.1241,
                '2017' : 0.1522,
                '2018' : None}
    if(WP=='T'):
        Effi_hist.append(Effi_FIle.Get("FlavourB_TagEffi_As_BT"))
        Effi_hist.append(Effi_FIle.Get("FlavourC_TagEffi_As_BT"))
        Effi_hist.append(Effi_FIle.Get("FlavourL_TagEffi_As_BT"))
        wpvalue = Tight_b_wp[datayear]
    if(WP=='M'):
        Effi_hist.append(Effi_FIle.Get("FlavourB_TagEffi_As_BM"))
        Effi_hist.append(Effi_FIle.Get("FlavourC_TagEffi_As_BM"))
        Effi_hist.append(Effi_FIle.Get("FlavourL_TagEffi_As_BM"))
        wpvalue = Medium_b_wp[datayear]
    if(WP=='L'):
        Effi_hist.append(Effi_FIle.Get("FlavourB_TagEffi_As_BL"))
        Effi_hist.append(Effi_FIle.Get("FlavourC_TagEffi_As_BL"))
        Effi_hist.append(Effi_FIle.Get("FlavourL_TagEffi_As_BL"))
        wpvalue = loose_b_wp[datayear]

    if(pt > Effi_hist[0].GetXaxis().GetXmax()): pt = Effi_hist[0].GetXaxis().GetXmax() - 1.0
    xbin = Effi_hist[0].GetXaxis().FindBin(pt) 
    ybin = Effi_hist[0].GetYaxis().FindBin(abs(eta))

    if(abs(hadron_flavour)==5): Efficiency = Effi_hist[0].GetBinContent(xbin,ybin)
    elif(abs(hadron_flavour)==4): Efficiency = Effi_hist[1].GetBinContent(xbin,ybin)
    else:Efficiency = Effi_hist[2].GetBinContent(xbin,ybin)

    p_mc_term = 0.0
    p_data_term = 0.0
   
    if(Deepcsv_score>=wpvalue):
        p_mc_term = Efficiency
        if(syst=='TagUp' and (abs(hadron_flavour)==5 or abs(hadron_flavour)==4)):
            p_data_term = SF_Up*Efficiency 
        elif(syst=='TagDown' and (abs(hadron_flavour)==5 or abs(hadron_flavour)==4)):
            p_data_term = SF_Down*Efficiency
        elif(syst=='MisTagUp' and abs(hadron_flavour)!=5 and abs(hadron_flavour)!=4): 
            p_data_term = SF_Up*Efficiency
        elif(syst=='MisTagDown' and abs(hadron_flavour)!=5 and abs(hadron_flavour)!=4):
            p_data_term = SF_Down*Efficiency 
        else:
            p_data_term = SF_cent*Efficiency

    if(Deepcsv_score<wpvalue):
        p_mc_term = 1-Efficiency 
        if(syst=='TagUp' and (abs(hadron_flavour)==5 or abs(hadron_flavour)==4)):
            p_data_term = 1-SF_Up*Efficiency 
        elif(syst=='TagDown' and (abs(hadron_flavour)==5 or abs(hadron_flavour)==4)):
            p_data_term = 1-SF_Down*Efficiency
        elif(syst=='MisTagUp' and abs(hadron_flavour)!=5 and abs(hadron_flavour)!=4): 
            p_data_term = 1-SF_Up*Efficiency
        elif(syst=='MisTagDown' and abs(hadron_flavour)!=5 and abs(hadron_flavour)!=4):
            p_data_term = 1-SF_Down*Efficiency 
        else:
            p_data_term = 1-SF_cent*Efficiency

    
    if(p_mc_term==0): p_mc_term = 0.000001
    if(p_data_term==0): p_data_term = 0.000001
    return [p_mc_term,p_data_term]

#[b,c]=Probability(40,1.2,2,0,0,'T',0.8,4,'central','2016')
#print b
#print c
def Probability_2(syst,selected_jet):
        shape_sf_product = 1
        if(syst=='jes_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_up_jes
        elif(syst=='jes_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_down_jes
        elif(syst=='hfstats2_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_up_hfstats2
        elif(syst=='hfstats2_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_down_hfstats2
        elif(syst=='hfstats1_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_up_hfstats1
        elif(syst=='hfstats1_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_down_hfstats1
        elif(syst=='lfstats2_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_up_lfstats2
        elif(syst=='lfstats2_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_down_lfstats2
        elif(syst=='lfstats1_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_up_lfstats1
        elif(syst=='lfstats1_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_down_lfstats1
        elif(syst=='cferr2_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_up_cferr2
        elif(syst=='cferr2_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_down_cferr2
        elif(syst=='cferr1_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_up_cferr1
        elif(syst=='cferr1_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_down_cferr1
        elif(syst=='hf_up'): 
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_up_hf
        elif(syst=='hf_down'): 
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepjet_shape_down_hf
        elif(syst=='lf_up'):
            for jet in selected_jet :
                #print("jet.btagSF_deepjet_shape_up_lf : ",jet.btagSF_deepjet_shape_up_lf)
                shape_sf_product *= jet.btagSF_deepjet_shape_up_lf
        elif(syst=='lf_down'):
            for jet in selected_jet :
                #print("jet.btagSF_deepjet_shape_down_lf : ",jet.btagSF_deepjet_shape_down_lf)
                shape_sf_product *= jet.btagSF_deepjet_shape_down_lf
        elif(syst=='Central'):
           for jet in selected_jet :
                #print("jet.btagSF_deepjet_shape : ",jet.btagSF_deepjet_shape)
                shape_sf_product *= jet.btagSF_deepjet_shape
                #print(jet.hadronFlavour)
        return shape_sf_product

#[b,c]=Probability_2(120,0.5,0.5,0,0,'M',1.5,5,'central','2016')
#print b
#print c
#print "Weight = ",c/b
sys_names = ['jesAbsoluteStat', 'jesAbsoluteMPFBias', 'jesFragmentation', 'jesSinglePionECAL', 'jesSinglePionHCAL', 'jesTimePtEta', 'jesRelativeJEREC1', 'jesRelativeJEREC2', 'jesRelativeJERHF', 'jesRelativePtBB', 'jesRelativePtEC1', 'jesRelativePtEC2', 'jesRelativePtHF', 'jesRelativeBal', 'jesRelativeSample' , 'jesRelativeFSR' , 'jesRelativeStatEC', 'jesRelativeStatHF' , 'jesPileUpDataMC', 'jesPileUpPtRef', 'jesPileUpPtBB', 'jesPileUpPtEC1' , 'jesPileUpPtEC2', 'jesPileUpPtHF', 'jesAbsoluteScale', 'jesFlavorQCD', 'jesRelativeStatFSR']
 
def get_battagging_jes_sys(jet,variation):
    btagging_jes_sys={}
    if(variation=="Central"):
        btagging_jes_sys={
        'jesAbsoluteStat': jet.btagSF_deepjet_shape,
        'jesAbsoluteMPFBias': jet.btagSF_deepjet_shape,
        'jesFragmentation':jet.btagSF_deepjet_shape,
        'jesSinglePionECAL':jet.btagSF_deepjet_shape,
        'jesSinglePionHCAL':jet.btagSF_deepjet_shape,
        'jesTimePtEta':jet.btagSF_deepjet_shape,
        'jesRelativeJEREC1':jet.btagSF_deepjet_shape,
        'jesRelativeJEREC2':jet.btagSF_deepjet_shape,
        'jesRelativeJERHF':jet.btagSF_deepjet_shape,
        'jesRelativePtBB':jet.btagSF_deepjet_shape,
        'jesRelativePtEC1':jet.btagSF_deepjet_shape,
        'jesRelativePtEC2':jet.btagSF_deepjet_shape,
        'jesRelativePtHF':jet.btagSF_deepjet_shape,
        'jesRelativeBal':jet.btagSF_deepjet_shape,
        'jesRelativeSample':jet.btagSF_deepjet_shape,
        'jesRelativeFSR':jet.btagSF_deepjet_shape,
        'jesRelativeStatEC':jet.btagSF_deepjet_shape,
        'jesRelativeStatHF':jet.btagSF_deepjet_shape,
        'jesPileUpDataMC':jet.btagSF_deepjet_shape,
        'jesPileUpPtRef':jet.btagSF_deepjet_shape,
        'jesPileUpPtBB':jet.btagSF_deepjet_shape,
        'jesPileUpPtEC1':jet.btagSF_deepjet_shape,
        'jesPileUpPtEC2':jet.btagSF_deepjet_shape,
        'jesPileUpPtHF':jet.btagSF_deepjet_shape,
        'jesAbsoluteScale':jet.btagSF_deepjet_shape,
        'jesFlavorQCD':jet.btagSF_deepjet_shape,
        'jesRelativeStatFSR':jet.btagSF_deepjet_shape
        }
    elif(variation=="up"):
        btagging_jes_sys={
        'jesAbsoluteStat': jet.btagSF_deepjet_shape_up_jesAbsoluteStat,
        'jesAbsoluteMPFBias': jet.btagSF_deepjet_shape_up_jesAbsoluteMPFBias,
        'jesFragmentation':jet.btagSF_deepjet_shape_up_jesFragmentation,
        'jesSinglePionECAL':jet.btagSF_deepjet_shape_up_jesSinglePionECAL,
        'jesSinglePionHCAL':jet.btagSF_deepjet_shape_up_jesSinglePionHCAL,
        'jesTimePtEta':jet.btagSF_deepjet_shape_up_jesTimePtEta,
        'jesRelativeJEREC1':jet.btagSF_deepjet_shape_up_jesRelativeJEREC1,
        'jesRelativeJEREC2':jet.btagSF_deepjet_shape_up_jesRelativeJEREC2,
        'jesRelativeJERHF':jet.btagSF_deepjet_shape_up_jesRelativeJERHF,
        'jesRelativePtBB':jet.btagSF_deepjet_shape_up_jesRelativePtBB,
        'jesRelativePtEC1':jet.btagSF_deepjet_shape_up_jesRelativePtEC1,
        'jesRelativePtEC2':jet.btagSF_deepjet_shape_up_jesRelativePtEC2,
        'jesRelativePtHF':jet.btagSF_deepjet_shape_up_jesRelativePtHF,
        'jesRelativeBal':jet.btagSF_deepjet_shape_up_jesRelativeBal,
        'jesRelativeSample':jet.btagSF_deepjet_shape_up_jesRelativeSample,
        'jesRelativeFSR':jet.btagSF_deepjet_shape_up_jesRelativeFSR,
        'jesRelativeStatEC':jet.btagSF_deepjet_shape_up_jesRelativeStatEC,
        'jesRelativeStatHF':jet.btagSF_deepjet_shape_up_jesRelativeStatHF,
        'jesPileUpDataMC':jet.btagSF_deepjet_shape_up_jesPileUpDataMC,
        'jesPileUpPtRef':jet.btagSF_deepjet_shape_up_jesPileUpPtRef,
        'jesPileUpPtBB':jet.btagSF_deepjet_shape_up_jesPileUpPtBB,
        'jesPileUpPtEC1':jet.btagSF_deepjet_shape_up_jesPileUpPtEC1,
        'jesPileUpPtEC2':jet.btagSF_deepjet_shape_up_jesPileUpPtEC2,
        'jesPileUpPtHF':jet.btagSF_deepjet_shape_up_jesPileUpPtHF,
        'jesAbsoluteScale':jet.btagSF_deepjet_shape_up_jesAbsoluteScale,
        'jesFlavorQCD':jet.btagSF_deepjet_shape_up_jesFlavorQCD,
        'jesRelativeStatFSR':jet.btagSF_deepjet_shape_up_jesRelativeStatFSR,
        }
    elif(variation=="down"):
        btagging_jes_sys={
        'jesAbsoluteStat': jet.btagSF_deepjet_shape_down_jesAbsoluteStat,
        'jesAbsoluteMPFBias': jet.btagSF_deepjet_shape_down_jesAbsoluteMPFBias,
        'jesFragmentation':jet.btagSF_deepjet_shape_down_jesFragmentation,
        'jesSinglePionECAL':jet.btagSF_deepjet_shape_down_jesSinglePionECAL,
        'jesSinglePionHCAL':jet.btagSF_deepjet_shape_down_jesSinglePionHCAL,
        'jesTimePtEta':jet.btagSF_deepjet_shape_down_jesTimePtEta,
        'jesRelativeJEREC1':jet.btagSF_deepjet_shape_down_jesRelativeJEREC1,
        'jesRelativeJEREC2':jet.btagSF_deepjet_shape_down_jesRelativeJEREC2,
        'jesRelativeJERHF':jet.btagSF_deepjet_shape_down_jesRelativeJERHF,
        'jesRelativePtBB':jet.btagSF_deepjet_shape_down_jesRelativePtBB,
        'jesRelativePtEC1':jet.btagSF_deepjet_shape_down_jesRelativePtEC1,
        'jesRelativePtEC2':jet.btagSF_deepjet_shape_down_jesRelativePtEC2,
        'jesRelativePtHF':jet.btagSF_deepjet_shape_down_jesRelativePtHF,
        'jesRelativeBal':jet.btagSF_deepjet_shape_down_jesRelativeBal,
        'jesRelativeSample':jet.btagSF_deepjet_shape_down_jesRelativeSample,
        'jesRelativeFSR':jet.btagSF_deepjet_shape_down_jesRelativeFSR,
        'jesRelativeStatEC':jet.btagSF_deepjet_shape_down_jesRelativeStatEC,
        'jesRelativeStatHF':jet.btagSF_deepjet_shape_down_jesRelativeStatHF,
        'jesPileUpDataMC':jet.btagSF_deepjet_shape_down_jesPileUpDataMC,
        'jesPileUpPtRef':jet.btagSF_deepjet_shape_down_jesPileUpPtRef,
        'jesPileUpPtBB':jet.btagSF_deepjet_shape_down_jesPileUpPtBB,
        'jesPileUpPtEC1':jet.btagSF_deepjet_shape_down_jesPileUpPtEC1,
        'jesPileUpPtEC2':jet.btagSF_deepjet_shape_down_jesPileUpPtEC2,
        'jesPileUpPtHF':jet.btagSF_deepjet_shape_down_jesPileUpPtHF,
        'jesAbsoluteScale':jet.btagSF_deepjet_shape_down_jesAbsoluteScale,
        'jesFlavorQCD':jet.btagSF_deepjet_shape_down_jesFlavorQCD,
        'jesRelativeStatFSR':jet.btagSF_deepjet_shape_down_jesRelativeStatFSR,
        }
    sys_SF = []
    for sys in sys_names:
        sys_SF.append(btagging_jes_sys[sys])
    return sys_SF

def Get_B_tagging_jes_sf(selected_jet):
    sf_up = np.ones_like(np.arange(len(sys_names)))
    sf_down = np.ones_like(np.arange(len(sys_names)))
    for jet in selected_jet :
        if(abs(jet.hadronFlavour)==4):
            #print("Central : ",get_battagging_jes_sys(jet,"Central"))
            sf_up = np.multiply(sf_up,np.array(get_battagging_jes_sys(jet,"Central")))
            sf_down = np.multiply(sf_down,np.array(get_battagging_jes_sys(jet,"Central")))
        else:
            #print("up :",get_battagging_jes_sys(jet,"up"))
            #print("down :",get_battagging_jes_sys(jet,"down"))
            sf_up   = np.multiply(sf_up,np.array(get_battagging_jes_sys(jet,"up")))
            sf_down = np.multiply(sf_down,np.array(get_battagging_jes_sys(jet,"down")))
    return sf_up,sf_down
    #print(sf_up)
    #print(sf_down)
    #print("-------------------------------------------------------------")

def Get_B_tagging_sys_sf(syst,selected_jet):
    
    #jet is considered a b jet if there is at least one b "ghost" hadron clustered inside it (hadronFlavour=5)
    #jet is considered a c jet if there is at least one c and no b "ghost" hadrons clustered inside it (hadronFlavour=4)
    #jet is considered a light-flavour jet if there are no b or c "ghost" hadrons clustered inside it (hadronFlavour=0) 
    shape_sf_product = 1
    if("cferr" in syst):
        for jet in selected_jet :
            if(syst=='cferr2_up'):     shape_sf_product *= jet.btagSF_deepjet_shape_up_cferr2
            elif(syst=='cferr2_down'): shape_sf_product *= jet.btagSF_deepjet_shape_down_cferr2
            elif(syst=='cferr1_up'):   shape_sf_product *= jet.btagSF_deepjet_shape_up_cferr1
            elif(syst=='cferr1_down'): shape_sf_product *= jet.btagSF_deepjet_shape_down_cferr1
    else:
        for jet in selected_jet :
            if(syst=='Central'):        shape_sf_product *= jet.btagSF_deepjet_shape
            elif(syst=='jes_up'):       shape_sf_product *= jet.btagSF_deepjet_shape_up_jes
            elif(syst=='jes_down'):     shape_sf_product *= jet.btagSF_deepjet_shape_down_jes
            elif(syst=='hfstats2_up'):  shape_sf_product *= jet.btagSF_deepjet_shape_up_hfstats2
            elif(syst=='hfstats2_down'):shape_sf_product *= jet.btagSF_deepjet_shape_down_hfstats2
            elif(syst=='hfstats1_up'):  shape_sf_product *= jet.btagSF_deepjet_shape_up_hfstats1
            elif(syst=='hfstats1_down'):shape_sf_product *= jet.btagSF_deepjet_shape_down_hfstats1
            elif(syst=='lfstats2_up'):  shape_sf_product *= jet.btagSF_deepjet_shape_up_lfstats2
            elif(syst=='lfstats2_down'):shape_sf_product *= jet.btagSF_deepjet_shape_down_lfstats2
            elif(syst=='lfstats1_up'):  shape_sf_product *= jet.btagSF_deepjet_shape_up_lfstats1
            elif(syst=='lfstats1_down'):shape_sf_product *= jet.btagSF_deepjet_shape_down_lfstats1
            elif(syst=='hf_up'):        shape_sf_product *= jet.btagSF_deepjet_shape_up_hf
            elif(syst=='hf_down'):      shape_sf_product *= jet.btagSF_deepjet_shape_down_hf
            elif(syst=='lf_up'):        shape_sf_product *= jet.btagSF_deepjet_shape_up_lf
            elif(syst=='lf_down'):      shape_sf_product *= jet.btagSF_deepjet_shape_down_lf
    return shape_sf_product
