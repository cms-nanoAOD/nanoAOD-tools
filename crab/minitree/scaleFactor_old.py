#!/usr/bin/env python
import os, sys
import ROOT

def elScaleFactor(pt, scEta, lead_Jet_pt, wp, syst,ID_Tight_fSFName,Trigger_Tight_fSFName,veto_fSFName,dataYear):

    ROOT.gStyle.SetOptStat(0)
    elSF=1.0
    SF = ROOT.TString("") 

    if(wp == "Tight"):
        #print "wp = ",wp
        Xbin=[] 
        Ybin=[]
        hSFIso=[]
        fSFIso=[]
        sfs=["ID","Trigger"]

        for sf_ in range(0,len(sfs)):
            SF=sfs[sf_]
            #print "SF = ",SF
            if(SF=="ID"): fSFName=ID_Tight_fSFName
            else: fSFName=Trigger_Tight_fSFName
            fSFIso.append(ROOT.TFile(fSFName,"Read"))
                 
            if(SF=="ID"): hSFIso.append(fSFIso[sf_].Get("EGamma_SF2D"))
            elif(SF=="Trigger" and dataYear!='UL2018'): hSFIso.append(fSFIso[sf_].Get("SF"))
            elif(SF=="Trigger" and dataYear=='UL2018'): hSFIso.append(fSFIso[sf_].Get("EGamma_SF2D"))

            if((dataYear=='2017' or dataYear=='UL2017') and SF=="Trigger"): #2017 has cross trigger with jet
                if(abs(lead_Jet_pt) > hSFIso[sf_].GetYaxis().GetXmax()): lead_Jet_pt = hSFIso[sf_].GetYaxis().GetXmax() - 0.01
            else:
                if(scEta > hSFIso[sf_].GetXaxis().GetXmax()): scEta = hSFIso[sf_].GetXaxis().GetXmax() - 0.01
                if(scEta < hSFIso[sf_].GetXaxis().GetXmin()): scEta = hSFIso[sf_].GetXaxis().GetXmin() + 0.01

            #print "scEta = ",scEta
            if((dataYear=='2017' or dataYear=='UL2017') and SF=="Trigger"):
                if(pt > hSFIso[sf_].GetXaxis().GetXmax()): pt = hSFIso[sf_].GetXaxis().GetXmax() - 1.0
            else:
                if(pt > hSFIso[sf_].GetYaxis().GetXmax()): pt = hSFIso[sf_].GetYaxis().GetXmax() - 1.0

            if((dataYear=='2017' or dataYear=='UL2017') and SF=="Trigger"):
                Xbin.append(hSFIso[sf_].GetXaxis().FindBin(pt))
                Ybin.append(hSFIso[sf_].GetYaxis().FindBin(abs(lead_Jet_pt)))
            else: 
                Xbin.append(hSFIso[sf_].GetXaxis().FindBin(scEta)) 
                Ybin.append(hSFIso[sf_].GetYaxis().FindBin(pt))
        #print "%s;%s;%s;%s;%s;%s" %(wp,syst,Xbin[0],Ybin[0],Xbin[1],Ybin[1])#"%s;%s;%s;%s;%s;%s" % (wp,syst,Xbin[0],Ybin[0],Xbin[1],Ybin[1]) 
        if(syst=="noSyst"): elSF = hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) * hSFIso[1].GetBinContent(Xbin[1],Ybin[1])
        if(syst=="IDUp"): 
            elSF = (hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) + hSFIso[0].GetBinErrorUp(Xbin[0],Ybin[0])) * hSFIso[1].GetBinContent(Xbin[1],Ybin[1])
            #print "%s;%s;%s;%s;%s;%s;%s%s"%(Xbin[0],Ybin[0],Xbin[1],Ybin[1],hSFIso[0].GetBinContent(Xbin[0],Ybin[0]),hSFIso[0].GetBinErrorUp(Xbin[0],Ybin[0]),hSFIso[1].GetBinContent(Xbin[1],Ybin[1]),elSF)
        if(syst=="IDDown"): elSF = ( hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) - hSFIso[0].GetBinErrorLow(Xbin[0],Ybin[0]) ) * hSFIso[1].GetBinContent(Xbin[1],Ybin[1])
        if(syst=="TrigUp"): elSF = hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) * ( hSFIso[1].GetBinContent(Xbin[1],Ybin[1]) + hSFIso[1].GetBinErrorUp(Xbin[1],Ybin[1]) )
        if(syst=="TrigDown"): elSF = hSFIso[0].GetBinContent(Xbin[0],Ybin[0]) * ( hSFIso[1].GetBinContent(Xbin[1],Ybin[1]) - hSFIso[1].GetBinErrorLow(Xbin[1],Ybin[1]) )
        #print "%s;%s;%s" % (syst,round(hSFIso[0].GetBinErrorUp(Xbin[0],Ybin[0]),8),round(hSFIso[1].GetBinErrorUp(Xbin[1],Ybin[1]),8))
        for sf_ in range(0,len(sfs)):
            hSFIso[sf_].Delete()
            fSFIso[sf_].Delete()
        
    elif(wp == "Veto"):
        fSFName=veto_fSFName
        fSFSB=ROOT.TFile.Open(fSFName,"Read")
        hSFSB=fSFSB.Get("EGamma_SF2D")

        if(scEta > hSFSB.GetXaxis().GetXmax()): scEta = hSFSB.GetXaxis().GetXmax() - 0.01
        if(scEta < hSFSB.GetXaxis().GetXmin()): scEta = hSFSB.GetXaxis().GetXmin() + 0.01
        if(pt > hSFSB.GetYaxis().GetXmax()): pt = hSFSB.GetYaxis().GetXmax() - 1.0
        #print "scEta = ",scEta
        binX=hSFSB.GetXaxis().FindBin(scEta)
        binY=hSFSB.GetYaxis().FindBin(pt)
        #print "Xbin = %s ; Ybin = %s" % (binX,binY)i
        #print hSFSB.GetBinError(binX,binY) ,';',hSFSB.GetBinErrorUp(binX,binY), ';', hSFSB.GetBinErrorLow(binX,binY)
        if(syst=="noSyst"): elSF = hSFSB.GetBinContent(binX,binY)
        if(syst=="IDUp"): elSF =  hSFSB.GetBinContent(binX,binY) + hSFSB.GetBinErrorUp(binX,binY)
        if(syst=="IDDown"): elSF = hSFSB.GetBinContent(binX,binY) - hSFSB.GetBinErrorLow(binX,binY)
        if(syst=="TrigUp" or syst=="TrigDown"): elSF=1.0
        #print "hSFSB.GetBinContent(binX,binY) = %s " % (hSFSB.GetBinContent(binX,binY))
        hSFSB.Delete() 
        fSFSB.Delete()
    else:
        elSF = -999
        #print("WP is nither 'Tight' nor 'Veto'")    
    return elSF
def muonScaleFactor(files,pt,eta,iso,lumiTotal,syst,dataYear):
    eta = abs(eta)
    if(iso >0.06 and iso<0.2): return -999
    ROOT.gStyle.SetOptStat(0)
    muSF=1.0
    idSF=[] 
    idSFErrUp=[]
    idSFErrDown=[]
    isoSF=[] 
    isoSFErrUp=[] 
    isoSFErrDown=[] 
    trigSF=[] 
    trigSFErrUp=[]
    trigSFErrDown=[]

    if(eta >= 2.4): eta = 2.39
    if(eta <=0.0): eta = 0.01
   
    if(dataYear=='2016'):
        binX=[[0,0],[0,0],[0,0]] 
        binY=[[0,0],[0,0],[0,0]]

    if(dataYear=='2017'):
        binX=[[0,0,0],[0,0,0],[0,0,0]]
        binY=[[0,0,0],[0,0,0],[0,0,0]]
   
    if(dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP' or dataYear=='UL2017' or dataYear=='UL2018' ):
        binX=[[0],[0],[0]]
        binY=[[0],[0],[0]]
        
    lumi=[];
    if(dataYear=='2016'):
        lumi.append((19.636*1000.0)/lumiTotal) 
        lumi.append((16.219*1000.0)/lumiTotal)
    if(dataYear=='UL2016preVFP'):
        lumi.append((19.521*1000.0)/lumiTotal)
    if(dataYear=='UL2016postVFP'):
        lumi.append((16.812*1000.0)/lumiTotal)
    if(dataYear=='UL2017'):
        lumi.append((41.52*1000.0)/lumiTotal)
    if(dataYear=='UL2018'):
        lumi.append((59.22*1000.0)/lumiTotal)
    
    if(dataYear=='2017'):
        lumi.append((14.42*1000.0)/lumiTotal)
        lumi.append((13.56*1000.0)/lumiTotal)
        lumi.append((13.54*1000.0)/lumiTotal)

    periods=[]
    if(dataYear=='2016'):
        periods.append("BCDEF")
        periods.append("GH")
    if(dataYear=='UL2016preVFP'):
        periods.append("HIPM_") #BCDEF
    if(dataYear=='UL2016postVFP'):
        periods.append("") #GH
    if(dataYear=='UL2017'):
        periods.append("")
    if(dataYear=='UL2018'):
        periods.append("")
    if(dataYear=='2017'):
        periods.append("BC")
        periods.append("DE")
        periods.append("F")

    sfs=[]
    sfs.append("ID")
    sfs.append("ISO")
    if(dataYear=='2016' or dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP' or dataYear=='UL2017'  or dataYear=='UL2018'):sfs.append("Trigger") # since for iso<0.06 we are using lagecy sample created files only
    if(dataYear=='2017'): sfs.append("TRI")

    #TString fSFName, SF, Period, dirName;
    if(dataYear=='2016' ):
        fSF=[[0,0],[0,0],[0,0]]
        hSF=[[0,0],[0,0],[0,0]]
    if(dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP' or dataYear=='UL2017' or dataYear=='UL2018' ):
        fSF=[[0],[0],[0]]
        hSF=[[0],[0],[0]]
    if(dataYear=='2017'):
        fSF=[[0,0,0],[0,0,0],[0,0,0]]
        hSF=[[0,0,0],[0,0,0],[0,0,0]]

#Histogram collection
    for sf_ in range(0,len(sfs)):

        SF=sfs[sf_]
        if(iso >=0.2 and SF!="ID"): continue
        #print SF
        if(iso <=0.06):
            if(SF=="ID"): dirName="NUM_TightID_DEN_TrackerMuons_abseta_pt_syst"
            elif(SF=="ISO"): dirName="NUM_VeryTightRelIso_DEN_TightIDandIPCut_abseta_pt_syst"
            elif(SF=="Trigger" and (dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP')): dirName="NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdTight_and_PFIsoVeryTight_abseta_pt_syst"
            elif(SF=="Trigger" and dataYear=='UL2017'): dirName="NUM_IsoMu27_DEN_CutBasedIdTight_and_PFIsoVeryTight_abseta_pt_syst"
            elif(SF=="Trigger" and dataYear=='UL2018'): dirName="NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoVeryTight_abseta_pt_syst"
            elif(SF=='TRI'):dirName="IsoMu27_from_Tight2012_and_dBeta_0p06_pteta"
         
            for prod in range(0,len(periods)):
                Period=periods[prod]
                #print Period
                #print files
                if(dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP' or dataYear=='UL2017'or dataYear=='UL2018'): fSFName=next(filter(lambda x: Period+SF+"_SF_0p06.root" in x,files))#[0] #filter function gave a list which has 1 file name always i.e [0]
                else: fSFName=next(filter(lambda x: Period+"_"+SF+"_SF_0p06.root" in x,files))#[0] #filter function gave a list which has 1 file name always i.e [0]
                #fSFName=filepath+Period+"_"+SF+"_SF_0p06.root"
                #print fSFName
                #print  SF , " " ,fSFName , dirName 
                #print  "hSF[",sf_,"][",prod,"]"
                fSF[sf_][prod]=ROOT.TFile.Open(fSFName,"Read")
                hSF[sf_][prod]=fSF[sf_][prod].Get(dirName)
                #hSF[sf_][prod].Print()
        if(iso>=0.2):
            if(dataYear=='2016'):dirName="MC_NUM_TightID_DEN_genTracks_PAR_pt_eta"
         
            for prod in range(0,len(periods)):
                Period=periods[prod]
                #print Period
                if(dataYear=='2016'):fSFName=next(filter(lambda x: Period+"_"+SF+".root" in x,files))#[0] #filter function gave a list which has 1 file name always i.e [0]
                elif(dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP'):fSFName=next(filter(lambda x: "UL_"+Period+SF+".root" in x,files))#[0] #filter function gave a list which has 1 file name always i.e [0]
                #if(dataYear=='2016'):fSFName=filepath+Period+"_"+SF+".root"
                #print  "hSF[",sf_,"][",prod,"]"
                elif(dataYear=='2017' or dataYear=='UL2018'):fSFName=next(filter(lambda x: Period+"_SF_"+SF+".root" in x,files))#[0] #filter function gave a list which has 1 file name always i.e [0]
                elif(dataYear=='UL2017'):fSFName=next(filter(lambda x: Period+"_SF_"+SF+"_syst.root" in x,files))#[0] #filter function gave a list which has 1 file name always i.e [0]
         
                #if(dataYear=='2017'):fSFName=filepath+Period+"_SF_"+SF+".root"
                #print  SF , " " ,fSFName 
                fSF[sf_][prod]=ROOT.TFile.Open(fSFName,"Read")
                #print  SF , " " ,fSFName , dirName , "/pt_abseta_ratio"
                if(dataYear=='2016'):hSF[sf_][prod]=fSF[sf_][prod].Get(dirName+"/pt_abseta_ratio")
                elif(dataYear=='2017'):hSF[sf_][prod]=fSF[sf_][prod].Get("NUM_TightID_DEN_genTracks")
                elif(dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP'): hSF[sf_][prod]=fSF[sf_][prod].Get("NUM_TightID_DEN_TrackerMuons_abseta_pt_syst")
                elif(dataYear=='UL2017'): hSF[sf_][prod]=fSF[sf_][prod].Get("NUM_TightID_DEN_genTracks_pt_abseta_syst")
                elif(dataYear=='UL2018'): hSF[sf_][prod]=fSF[sf_][prod].Get("NUM_TightID_DEN_TrackerMuons_pt_abseta_syst")
                #print( hSF[sf_][prod].Print())
    #print "-----------------------------------"                        
#Scale factor collection   
    for sf_ in range(0,len(sfs)):

        SF=sfs[sf_]
        if(iso >=0.2 and SF!="ID"): continue
        for prod in range(0,len(periods)):
            Period=periods[prod]
            if((dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP') and iso >=0.2): # for iso<0.06 we are using persionlly created file axies are reverted
                if(pt >= hSF[sf_][prod].GetYaxis().GetXmax()): pt = hSF[sf_][prod].GetYaxis().GetXmax() - 1.0
            elif((dataYear=='UL2017' or dataYear=='UL2018') and iso >=0.2):
                if(pt >= hSF[sf_][prod].GetXaxis().GetXmax()): pt = hSF[sf_][prod].GetXaxis().GetXmax() - 1.0
            else:
                if(pt >= hSF[sf_][prod].GetYaxis().GetXmax()): pt = hSF[sf_][prod].GetYaxis().GetXmax() - 1.0
            #print "SF = ", SF
            #print "Period = ", Period
            #print "pt = ",pt
            #print "eta = ",eta
            #print "hSF[",sf_,"][",prod,"]"
            if((dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP') and iso >=0.2): # for iso<0.06 we are using persionlly created file axies are reverted
                binX[sf_][prod]=hSF[sf_][prod].GetXaxis().FindBin(eta)
                binY[sf_][prod]=hSF[sf_][prod].GetYaxis().FindBin(pt)
            elif( (dataYear=='UL2017' or dataYear=='UL2018') and iso >=0.2):
                binX[sf_][prod]=hSF[sf_][prod].GetXaxis().FindBin(pt)
                binY[sf_][prod]=hSF[sf_][prod].GetYaxis().FindBin(eta)
            else:
                binX[sf_][prod]=hSF[sf_][prod].GetXaxis().FindBin(eta)
                binY[sf_][prod]=hSF[sf_][prod].GetYaxis().FindBin(pt)
            #print "histogram = ", hSF[sf_][prod].GetName()
            #print "binpt[",sf_,"][",prod,"] for pt (", pt,") = ",hSF[sf_][prod].GetYaxis().FindBin(pt)
            #print "bineta[",sf_,"][",prod,"] for eta (",eta,") = ",hSF[sf_][prod].GetXaxis().FindBin(eta)
            if(SF=="ID"):
                #print "hSF[",sf_,"][",prod,"] = ", hSF[sf_][prod].GetBinContent(binX[sf_][prod],binY[sf_][prod])
                idSF.append(hSF[sf_][prod].GetBinContent(binX[sf_][prod],binY[sf_][prod]))
                idSFErrUp.append(hSF[sf_][prod].GetBinErrorUp(binX[sf_][prod],binY[sf_][prod]))
                idSFErrDown.append(hSF[sf_][prod].GetBinErrorLow(binX[sf_][prod],binY[sf_][prod]))
            if(SF=="ISO"):
                isoSF.append(hSF[sf_][prod].GetBinContent(binX[sf_][prod],binY[sf_][prod]))
                isoSFErrUp.append(hSF[sf_][prod].GetBinErrorUp(binX[sf_][prod],binY[sf_][prod]))
                isoSFErrDown.append(hSF[sf_][prod].GetBinErrorLow(binX[sf_][prod],binY[sf_][prod]))
            if(SF=="Trigger" or SF=="TRI"):
                trigSF.append(hSF[sf_][prod].GetBinContent(binX[sf_][prod],binY[sf_][prod]))
                trigSFErrUp.append(hSF[sf_][prod].GetBinErrorUp(binX[sf_][prod],binY[sf_][prod]))
                trigSFErrDown.append(hSF[sf_][prod].GetBinErrorLow(binX[sf_][prod],binY[sf_][prod]))
   # print "idSF = ",idSF
   # print "isoSF = ",isoSF
   # print "trigSF = ", trigSF
   # print "lumi = ",lumi
#Scale factor Evaluation

    if(iso >= 0.2 and dataYear=='2016'):
        #print "idSF[0] = ", idSF[0], "idSF[1] = ", idSF[1] 
        if(syst=="noSyst"): muSF =  idSF[0]*lumi[0]  + idSF[1]*lumi[1] 
        elif(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*lumi[0]  + (idSF[1] + idSFErrUp[1])*lumi[1]
        elif(syst=="IDDown"): muSF =  (idSF[0] - idSFErrDown[0])*lumi[0]  + (idSF[1] - idSFErrDown[1])*lumi[1]
        elif(syst=="IsoUp" or syst=="IsoDown" or syst=="TrigUp" or syst=="TrigDown"): muSF = 1.0
    elif(iso >= 0.2 and (dataYear=='UL2016preVFP' or  dataYear=='UL2016postVFP' or dataYear=='UL2017' or dataYear=='UL2018')):
        #print "idSF[0] = ", idSF[0], "idSF[1] = ", idSF[1]
        if(syst=="noSyst"): muSF =  idSF[0]*lumi[0]  
        elif(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*lumi[0]  
        elif(syst=="IDDown"): muSF =  (idSF[0] - idSFErrDown[0])*lumi[0]  
        elif(syst=="IsoUp" or syst=="IsoDown" or syst=="TrigUp" or syst=="TrigDown"): muSF = 1.0

    elif(iso >= 0.2 and dataYear=='2017'):
        if(syst=="noSyst"): muSF =  idSF[0]*lumi[0]  + idSF[1]*lumi[1] + idSF[2]*lumi[2] 
        elif(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*lumi[0]  + (idSF[1] + idSFErrUp[1])*lumi[1] + (idSF[2] + idSFErrUp[2])*lumi[2]
        elif(syst=="IDDown"): muSF =  (idSF[0] - idSFErrDown[0])*lumi[0]  + (idSF[1] - idSFErrDown[1])*lumi[1] + (idSF[2] - idSFErrDown[2])*lumi[2]
        elif(syst=="IsoUp" or syst=="IsoDown" or syst=="TrigUp" or syst=="TrigDown"): muSF = 1.0

    #if(iso >= 0.2 and dataYear=='UL2017'):
        #if(syst=="noSyst"): muSF =  idSF[0]*lumi[0]  #+ idSF[1]*lumi[1] + idSF[2]*lumi[2] #since UL recomadation gave only one file for full lumi
        #if(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*lumi[0]  #+ (idSF[1] + idSFErrUp[1])*lumi[1] + (idSF[2] + idSFErrUp[2])*lumi[2]
        #if(syst=="IDDown"): muSF =  (idSF[0] - idSFErrDown[0])*lumi[0]  #+ (idSF[1] - idSFErrDown[1])*lumi[1] + (idSF[2] - idSFErrDown[2])*lumi[2]
        #if(syst=="IsoUp" or syst=="IsoDown" or syst=="TrigUp" or syst=="TrigDown"): muSF = 1.0


    elif(iso <=0.06 and dataYear=='2016' ):
        if(syst=="noSyst"): muSF =  idSF[0]*isoSF[0]*trigSF[0]*lumi[0] + idSF[1]*isoSF[1]*trigSF[1]*lumi[1]
        elif(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*isoSF[0]*trigSF[0]*lumi[0] + (idSF[1] + idSFErrUp[1])*isoSF[1]*trigSF[1]*lumi[1]
        elif(syst=="IDDown"): muSF = (idSF[0] - idSFErrDown[0])*isoSF[0]*trigSF[0]*lumi[0] + (idSF[1] - idSFErrDown[1])*isoSF[1]*trigSF[1]*lumi[1]
        elif(syst=="IsoUp"): muSF = idSF[0]*(isoSF[0] + isoSFErrUp[0])*trigSF[0]*lumi[0] + idSF[1]*(isoSF[1] + isoSFErrUp[1])*trigSF[1]*lumi[1]
        elif(syst=="IsoDown"): muSF= idSF[0]*(isoSF[0] - isoSFErrDown[0])*trigSF[0]*lumi[0] + idSF[1]*(isoSF[1] - isoSFErrDown[1])*trigSF[1]*lumi[1]
        elif(syst=="TrigUp"): muSF= idSF[0]*isoSF[0]*(trigSF[0] + trigSFErrUp[0])*lumi[0] + idSF[1]*isoSF[1]*(trigSF[1] + trigSFErrUp[1])*lumi[1]
        elif(syst=="TrigDown"): muSF= idSF[0]*isoSF[0]*(trigSF[0] - trigSFErrDown[0])*lumi[0] + idSF[1]*isoSF[1]*(trigSF[1] - trigSFErrDown[1])*lumi[1]

    elif(iso <=0.06 and (dataYear=='UL2016preVFP' or  dataYear=='UL2016postVFP' or dataYear=='UL2017' or dataYear=='UL2018')):
        #print "id : ",idSF[0],"iso : ",isoSF[0],"trg : ",trigSF[0],"lumi : ",lumi[0] 
        if(syst=="noSyst"): muSF =  idSF[0]*isoSF[0]*trigSF[0]*lumi[0] 
        elif(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*isoSF[0]*trigSF[0]*lumi[0] 
        elif(syst=="IDDown"): muSF = (idSF[0] - idSFErrDown[0])*isoSF[0]*trigSF[0]*lumi[0] 
        elif(syst=="IsoUp"): muSF = idSF[0]*(isoSF[0] + isoSFErrUp[0])*trigSF[0]*lumi[0] 
        elif(syst=="IsoDown"): muSF= idSF[0]*(isoSF[0] - isoSFErrDown[0])*trigSF[0]*lumi[0] 
        elif(syst=="TrigUp"): muSF= idSF[0]*isoSF[0]*(trigSF[0] + trigSFErrUp[0])*lumi[0] 
        elif(syst=="TrigDown"): muSF= idSF[0]*isoSF[0]*(trigSF[0] - trigSFErrDown[0])*lumi[0] 

    elif(iso <=0.06 and (dataYear=='2017')):
        if(syst=="noSyst"): muSF =  idSF[0]*isoSF[0]*trigSF[0]*lumi[0] + idSF[1]*isoSF[1]*trigSF[1]*lumi[1]+idSF[2]*isoSF[2]*trigSF[2]*lumi[2]
        elif(syst=="IDUp"): muSF = (idSF[0] + idSFErrUp[0])*isoSF[0]*trigSF[0]*lumi[0] + (idSF[1] + idSFErrUp[1])*isoSF[1]*trigSF[1]*lumi[1]+(idSF[2] + idSFErrUp[2])*isoSF[2]*trigSF[2]*lumi[2]
        elif(syst=="IDDown"): muSF = (idSF[0] - idSFErrDown[0])*isoSF[0]*trigSF[0]*lumi[0] + (idSF[1] - idSFErrDown[1])*isoSF[1]*trigSF[1]*lumi[1]+(idSF[2] - idSFErrDown[2])*isoSF[2]*trigSF[2]*lumi[2]
        elif(syst=="IsoUp"): muSF = idSF[0]*(isoSF[0] + isoSFErrUp[0])*trigSF[0]*lumi[0] + idSF[1]*(isoSF[1] + isoSFErrUp[1])*trigSF[1]*lumi[1]+idSF[2]*(isoSF[2] + isoSFErrUp[2])*trigSF[2]*lumi[2]
        elif(syst=="IsoDown"): muSF= idSF[0]*(isoSF[0] - isoSFErrDown[0])*trigSF[0]*lumi[0] + idSF[1]*(isoSF[1] - isoSFErrDown[1])*trigSF[1]*lumi[1]+idSF[2]*(isoSF[2] - isoSFErrDown[2])*trigSF[2]*lumi[2]
        elif(syst=="TrigUp"): muSF= idSF[0]*isoSF[0]*(trigSF[0] + trigSFErrUp[0])*lumi[0] + idSF[1]*isoSF[1]*(trigSF[1] + trigSFErrUp[1])*lumi[1]+idSF[2]*isoSF[2]*(trigSF[2] + trigSFErrUp[2])*lumi[2]
        elif(syst=="TrigDown"): muSF= idSF[0]*isoSF[0]*(trigSF[0] - trigSFErrDown[0])*lumi[0] + idSF[1]*isoSF[1]*(trigSF[1] - trigSFErrDown[1])*lumi[1]+idSF[2]*isoSF[2]*(trigSF[2] - trigSFErrDown[2])*lumi[2]
    for sf_ in range(0,len(sfs)):
        if(iso >=0.2 and sf_!=0): continue
        for prod in range(0,len(periods)):
            hSF[sf_][prod].Delete()
            fSF[sf_][prod].Delete()
    
    return muSF 
    #canvas = ROOT.TCanvas(" canvas ")
    #canvas.cd()
    #print hSF[0][0].GetName()
    #hSF[0][0].Draw("colz")
    #canvas.Print("plots.pdf")

el_InFiles = {
                '2016':{
                        'TightID': 'ElectronSF/2016postVFP/ElectronSF_tightID.root',
                        'vetoID' : 'ElectronSF/2016postVFP/ElectronSF_vetoID.root',
                        'TRI'    : 'ElectronSF/2016postVFP/SF_HLT_Ele32_eta2p1.root'
                },

                '2017':{
                        'TightID': 'ElectronSF/2017/2017_ElectronTight.root',
                        'vetoID' : 'ElectronSF/2017/2017_ElectronWPVeto_Fall17V2.root',
                        'TRI'    : 'ElectronSF/2017/HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned_OR_HLT_Ele35_WPTight_Gsf.root' 
                },
                'UL2016preVFP':{
                        'TightID': 'ElectronSF/2016preVFP/UL/egammaEffi.txt_Ele_Tight_preVFP_EGM2D.root',
                        'vetoID' : 'ElectronSF/2016preVFP/UL/egammaEffi.txt_Ele_Veto_preVFP_EGM2D.root',
                        'TRI'    : 'ElectronSF/2016postVFP/SF_HLT_Ele32_eta2p1.root' #need to update
                },
                'UL2016postVFP':{
                        'TightID': 'ElectronSF/2016postVFP/UL/egammaEffi.txt_Ele_Tight_postVFP_EGM2D.root',
                        'vetoID' : 'ElectronSF/2016postVFP/UL/egammaEffi.txt_Ele_Veto_postVFP_EGM2D.root',
                        'TRI'    : 'ElectronSF/2016postVFP/SF_HLT_Ele32_eta2p1.root'  #need to update
                },
                'UL2017':{
                        'TightID': 'ElectronSF/2017/UL/egammaEffi.txt_EGM2D_Tight_UL17.root',
                        'vetoID' : 'ElectronSF/2017/UL/egammaEffi.txt_EGM2D_Veto_UL17.root',
                        'TRI'    : 'ElectronSF/2017/HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned_OR_HLT_Ele35_WPTight_Gsf.root' #need to update
                },
                'UL2018':{
                        'TightID': 'ElectronSF/2018/UL/egammaEffi.txt_Ele_Tight_EGM2D.root',
                        'vetoID' : 'ElectronSF/2018/UL/egammaEffi.txt_Ele_Veto_EGM2D.root',
                        'TRI'    : 'ElectronSF/2018/UL/trig_2018.root' # need to update
                },
             }
def create_elSF(dataYear,pt_, scEta_, lead_Jet_pt_, wp_, syst_):
    dataYear = str(dataYear)
    ID_Tight_el_fSFName_ = el_InFiles[dataYear]['TightID']
    Trigger_Tight_el_fSFName_ = el_InFiles[dataYear]['TRI']
    veto_el_fSFName_ = el_InFiles[dataYear]['vetoID']
    elSF = elScaleFactor(pt_, scEta_, lead_Jet_pt_, wp_, syst_,ID_Tight_el_fSFName_,Trigger_Tight_el_fSFName_,veto_el_fSFName_,dataYear)
    return elSF 

mu_InFiles = {'2016' : [
                        'MuonSF/2016/EfficienciesAndSF_BCDEF_ID_SF_0p06.root',
                        'MuonSF/2016/EfficienciesAndSF_GH_ID_SF_0p06.root',

                        'MuonSF/2016/EfficienciesAndSF_BCDEF_ID.root',
                        'MuonSF/2016/EfficienciesAndSF_GH_ID.root',

                        'MuonSF/2016/EfficienciesAndSF_BCDEF_ISO_SF_0p06.root',
                        'MuonSF/2016/EfficienciesAndSF_GH_ISO_SF_0p06.root',

                        'MuonSF/2016/EfficienciesAndSF_BCDEF_Iso.root',
                        'MuonSF/2016/EfficienciesAndSF_GH_Iso.root',

                        'MuonSF/2016/EfficienciesAndSF_BCDEF_Trigger_SF_0p06.root',
                        'MuonSF/2016/EfficienciesAndSF_GH_Trigger_SF_0p06.root',
                       ],
              '2017' : [
                        'MuonSF/2017/EfficienciesAndSF_BC_ID_SF_0p06.root',   
                        'MuonSF/2017/EfficienciesAndSF_DE_ID_SF_0p06.root',
                        'MuonSF/2017/EfficienciesAndSF_F_ID_SF_0p06.root',
 
                        'MuonSF/2017/EfficienciesAndSF_BC_SF_ID.root',
                        'MuonSF/2017/EfficienciesAndSF_DE_SF_ID.root',
                        'MuonSF/2017/EfficienciesAndSF_F_SF_ID.root',

                        'MuonSF/2017/EfficienciesAndSF_BC_ISO_SF_0p06.root',
                        'MuonSF/2017/EfficienciesAndSF_DE_ISO_SF_0p06.root',  
                        'MuonSF/2017/EfficienciesAndSF_F_ISO_SF_0p06.root',

                        'MuonSF/2017/EfficienciesAndSF_BC_SF_ISO.root',
                        'MuonSF/2017/EfficienciesAndSF_DE_SF_ISO.root',
                        'MuonSF/2017/EfficienciesAndSF_F_SF_ISO.root',

                        'MuonSF/2017/EfficienciesAndSF_BC_TRI_SF_0p06.root',
                        'MuonSF/2017/EfficienciesAndSF_F_TRI_SF_0p06.root',
                        'MuonSF/2017/EfficienciesAndSF_DE_TRI_SF_0p06.root',
                       ],
              '2018' : 'filepath',

              'UL2016':[
                        'MuonSF/2016/UL/EfficienciesAndSF_Run2016_UL_HIPM_ID_SF_0p06.root', # need to update this file for lagecy samples
                        'MuonSF/2016/UL/EfficienciesAndSF_Run2016_UL_ID_SF_0p06.root', # need to update this file for lagecy samples

                        'MuonSF/2016/UL/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ID.root', # UL recomdation
                        'MuonSF/2016/UL/Efficiencies_muon_generalTracks_Z_Run2016_UL_ID.root', # UL recomdation
                        
                        'MuonSF/2016/UL/EfficienciesAndSF_Run2016_UL_HIPM_ISO_SF_0p06.root', # need to update this file for lagecy samples
                        'MuonSF/2016/UL/EfficienciesAndSF_Run2016_UL_ISO_SF_0p06.root',  # need to update this file for lagecy samples


                        #'MuonSF/2016/UL/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ISO.root', # UL recomdation (not required to us)
                        #'MuonSF/2016/UL/Efficiencies_muon_generalTracks_Z_Run2016_UL_ISO.root', # UL recomdation (not required to us)

                        'MuonSF/2016/UL/EfficienciesAndSF_Run2016_UL_HIPM_Trigger_SF_0p06.root',  # need to update this file for lagecy samples
                        'MuonSF/2016/UL/EfficienciesAndSF_Run2016_UL_Trigger_SF_0p06.root',   # need to update this file for lagecy samples
                        ],
             'UL2016preVFP':[
                        'MuonSF/UL2016preVFP/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ID_SF_0p06.root', # from matteo
                        'MuonSF/UL2016preVFP/Efficiencies_muon_generalTracks_Z_Run2016_UL_HIPM_ID.root', # UL recomdation for antiIso
                        'MuonSF/UL2016preVFP/NUM_VeryTightRelIso_DEN_TightIDandIPCut_abseta_pt_HIPM_ISO_SF_0p06.root', # from matteo 
                        'MuonSF/UL2016preVFP/NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdTight_and_PFIsoVeryTight_abseta_pt_HIPM_Trigger_SF_0p06.root' # from matteo
                        ],
             'UL2016postVFP':[
                        'MuonSF/UL2016postVFP/Efficiencies_muon_generalTracks_Z_Run2016_UL_ID_SF_0p06.root', # from matteo
                        'MuonSF/UL2016postVFP/Efficiencies_muon_generalTracks_Z_Run2016_UL_ID.root', # UL recomdation for antiIso
                        'MuonSF/UL2016postVFP/NUM_VeryTightRelIso_DEN_TightIDandIPCut_abseta_pt_ISO_SF_0p06.root', # from matteo
                        'MuonSF/UL2016postVFP/NUM_IsoMu24_or_IsoTkMu24_DEN_CutBasedIdTight_and_PFIsoVeryTight_abseta_pt_Trigger_SF_0p06.root' # from matteo
                        ],
             'UL2017':[
                        'MuonSF/UL2017/Efficiencies_muon_generalTracks_Z_Run2017_UL_ID_SF_0p06.root', # from matteo
                        'MuonSF/UL2017/RunBCDEF_SF_ID_syst.root',  # UL recomdation     for antiIso
                        'MuonSF/UL2017/NUM_VeryTightRelIso_DEN_TightIDandIPCut_abseta_pt_ISO_SF_0p06.root', # from matteo
                        'MuonSF/UL2017/NUM_IsoMu27_DEN_CutBasedIdTight_and_PFIsoVeryTight_abseta_pt_Trigger_SF_0p06.root' # from matteo

                        
                      ],
            'UL2018':[
                        'MuonSF/UL2018/Efficiencies_muon_generalTracks_Z_Run2018_UL_ID_SF_0p06.root', # from matteo
                        'MuonSF/UL2018/RunABCD_SF_ID.root',  # UL recomdation for antiIso
                        'MuonSF/UL2018/NUM_VeryTightRelIso_DEN_TightIDandIPCut_abseta_pt_ISO_SF_0p06.root', # from matteo
                        'MuonSF/UL2018/NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoVeryTight_abseta_pt_Trigger_SF_0p06.root',# from matteo
                     ]  

}
def create_muSF(dataYear,pt_,eta_,iso_,lumiTotal_,syst_):
        #if(dataYear=='UL2016preVFP' or dataYear=='UL2016postVFP'): dataYear='UL2016'
        dataYear = str(dataYear)
        sf_InFiles= mu_InFiles[dataYear]
        #print sf_InFiles
        muSF = muonScaleFactor(sf_InFiles,pt_,eta_,iso_,lumiTotal_,syst_,dataYear)
        return muSF     
#print "-------------------------------------------------------"
#print create_elSF('UL2016preVFP',300,-1.3,50,'Tight','noSyst')
#print create_elSF('UL2016preVFP',300,-1.3,50,'Veto','noSyst')
#create_muSF('2016',21.1176013947,0.6142578125,0.3,3485,'noSyst')
#print create_muSF('UL2017',60.1176013947,-2.0142578125,0.3,59222,'noSyst')
#print create_muSF('UL2018',29.2907962799,0.0283164978027,0.297331474721,59222,'IDUp')#19521,16812,41520,59222
print(create_elSF('UL2018',300,-1.3,50,'Tight','noSyst'))
print(create_elSF('UL2018',300,-1.3,50,'Veto','noSyst'))
#print "-------------------------------------------------------"                        
