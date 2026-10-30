#!/usr/bin/env python
import os, sys
import ROOT

def Probability(pt,eta,SF_cent,SF_Up,SF_Down,WP,Deepcsv_score,hadron_flavour,syst,datayear):
    Effi_hist = []
    Effi_FIle = ROOT.TFile('QCD_Pt-20toInf_MuEnriched_Tagging_Efficiency.root')
    Tight_b_wp={
                '2016' : 0.7527,        #https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
                '2017' : 0.8001,	#https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
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
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_jes
        elif(syst=='jes_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_jes
	elif(syst=='hfstats2_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_hfstats2
        elif(syst=='hfstats2_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_hfstats2
        elif(syst=='hfstats1_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_hfstats1
        elif(syst=='hfstats1_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_hfstats1
	elif(syst=='lfstats2_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_lfstats2
        elif(syst=='lfstats2_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_lfstats2
	elif(syst=='lfstats1_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_lfstats1
        elif(syst=='lfstats1_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_lfstats1
	elif(syst=='cferr2_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_cferr2
        elif(syst=='cferr2_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_cferr2
	elif(syst=='cferr1_up'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_cferr1
        elif(syst=='cferr1_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_cferr1
	elif(syst=='hf_up'): 
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_hf
	elif(syst=='hf_down'): 
	    for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_hf
	elif(syst=='lf_up'):
	    for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_up_lf
	elif(syst=='lf_down'):
            for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape_down_lf
	elif(syst=='Central'):
	   for jet in selected_jet :
                shape_sf_product *= jet.btagSF_deepcsv_shape

    	return shape_sf_product

#[b,c]=Probability_2(120,0.5,0.5,0,0,'M',1.5,5,'central','2016')
#print b
#print c
#print "Weight = ",c/b
