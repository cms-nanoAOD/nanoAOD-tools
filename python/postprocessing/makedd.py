import os, commands
import math
import optparse
from ROOT import *
from array import array
import copy 

usage = 'python BkgEst_TTW.py'
parser = optparse.OptionParser(usage)
#parser.add_option('--pathin', dest='pathin', type='string', default='/eos/user/a/adeiorio/Wprime/nosynch/v13/plot/', help='the folder where the root files are')
parser.add_option('--pathin', dest='pathin', type='string', default='./localhisto/', help='the folder where the root files are')
parser.add_option('-o','--pathout', dest='pathout', type='string', default='./localhisto/v14_rebin', help='the folder where the output root files should be stored')
parser.add_option('-c','--category', dest='category', type='string', default='muon', help='muon or electron, in case different thresholds need to be set')
parser.add_option('-y','--year', dest='year', type='string', default='2016', help='year of data taking')
parser.add_option('--date', dest='date', type='string', default='', help='the date of the folder folder where the root file is stored')
#parser.add_option('-o','--outpath', dest='outpath', type='string', default='alphaRatioPlots', help='the folder whre the plot will be stored')
parser.add_option('', '--skipJesJer', dest='skipJesJer', action="store_true", default = False, help='skip jes/jer systematics')
parser.add_option('', '--test', dest='test', action="store_true", default = False, help='do test version')
parser.add_option('', '--scenario', dest='scenario', type='string', default='', help='scenario for checks')
parser.add_option('', '--bkgmodel', dest='bkgmodel', type='string', default='ttw_zjets', help='bkgmodel for clustering backgrounds')
parser.add_option('', '--extraunc', dest='extraunc', action="store_true", default = False, help='uncertainty envelope a la resolved + smoothing')
parser.add_option('', '--docrosscheck', dest='docrosscheck', action="store_true", default = False, help='do cross check on CR')
parser.add_option('', '--symJesJer', dest='symJesJer', action="store_true", default = False, help='add symmetrized jes/jer')
parser.add_option('', '--doaddsig', dest='doaddsig', action="store_true", default = False, help='add signal to cr')
parser.add_option('', '--plotpath', dest='plotpath',type='string', default='./plots/', help='the folder where the plots are stored')

(opt, args) = parser.parse_args()
categories =[""]
systs=[""]
#systs = ["","_btagUp","_btagDown","_mistagUp","_mistagDown","_pdf_totalUp","_pdf_totalDown","_puUp","_puDown","_q2TTUp","_q2QCDUp","_q2ZJetsUp","_q2WJetsUp","_q2TprimeUp","_q2TTDown","_q2QCDDown","_q2ZJetsDown","_q2WJetsDown","_q2TprimeDown","_jesUp","_jesDown","_jerUp","_jerDown","_topTagUp", "_topTagDown","_wTagUp", "_wTagDown","_topPtWeightDown","_topPtWeightUp"]

plotpath=opt.plotpath
if not os.path.exists(plotpath):
    os.system("mkdir -p "+plotpath)
if not plotpath[-1]=="/": plotpath=plotpath+"/" 
#wjets_veto_threshold=400
wjets_veto_threshold=200

lepcut=""
#lepcut="lep180_"
    
namemap={}
namemap["SR2B"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SR2B_I"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_G_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SR2B_II"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

namemap["SRW"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SRW_I"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_G_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SRW_II"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

namemap["SRT"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SRT_I"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_G_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["SRT_II"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_AND_best_Wpjet_isbtag_EQ_0_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

namemap["CR0B"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["CR0B_I"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_G_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["CR0B_II"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_0_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"

namemap["CR1B"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_1_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["CR1B_I"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_1_AND_best_top_m_G_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_L_60"
namemap["CR1B_II"]="h_jets_best_Wprime_m_selection_"+lepcut+"AND_best_topjet_isbtag_EQ_0_AND_best_Wpjet_isbtag_EQ_0_AND_nbjet_pt100_EQ_1_AND_best_top_m_L_"+str(wjets_veto_threshold)+"_AND_deltaR_bestWAK4_closestAK8_L_0p4_AND_WprAK8_mSD_G_60"
#
#wjets_veto_map = {"CR0B":"CR0B_I","CR1B":"CR1B_I"}
#wjets_veto_map = {"SR2B":"SR2B_I"}
#wjets_veto_map = {"SR2B":"SR2B_I","SRW":"SRW_I","SRT":"SRT_I","CR0B":"CR0B_I","CR1B":"CR1B_I"}
wjets_veto_map = {"SR2B":"SR2B_I","SRW":"SRW_I","SRT":"SRT_I"}
#
ttbar_veto_map= {"SR2B":"SR2B_II","SRW":"SRW_II","SRT":"SRT_II","CR0B":"CR0B_II","CR1B":"CR1B_II"}
srcr_map = {"SR2B":"SRT","SR2B_I":"SRT_I","SRW":"CR1B","SRW_I":"CR1B_I"}
srcr_map_2 = {"SR2B":"SRW","SR2B_I":"SRW_I","SRW":"CR0B","SRW_I":"CR0B_I"}
srcr_map_3 = {"SR2B":"CR1B","SR2B_I":"CR1B_I"}
srcr_map_4 = {"SRT":"CR1B","SRT_I":"CR1B_I"}


fexp2=TF1("fexp2","[0]*exp(-([1]+x*[2]+x*x*[3]))",1000,5000)
fexp2.SetParameters(310,0.1,0.001,0.0000002)

fexp1=TF1("fexp1","[0]*exp(-(x*[1]))",1000,5000)
fexp1.SetParameters(310,0.001)

fexp1plus2=TF1("fexp1plus2","[0]*exp(-(x*[1]))+[2]*exp(-([3]+x*[4]+x*x*[5]))",1000,5000)
fexp1plus2.SetParameters(310,0.001,210,0.1,0.001,0.0000002)

fpoly3= TF1("fpoly3","[0]+x*[1]+x*x*[2]+x*x*x*[3]",1000,5000)
fpoly3.SetParameters(310,10,1.,0.1)

fexp2data=TF1("fexp2data","[0]*exp(-([1]+x*[2]+x*x*[3]))",1000,5000)
fexp2data.SetParameters(310,0.1,0.01,0.0000002)

#fexp1plus2data=TF1("fexp1plus2","TMath::LogNormal(x,[0],[1],[2])",1000,5000)
fexp1plus2data=TF1("fexp1plus2data","landau",1000,5000)
fexp1plus2data.SetParameters(1000,1100,1002)
#fexp1plus2data=TF1("fexp1plus2","[3]*TMath::GammaDist(x,[0],[1],[2])",1000,5000)
#fexp1plus2data.SetParameters(1000,0,2,1000)

#fexp1plus2ele=TF1("fexp1plus2ele","[0]*exp(-([1]+x*[2]+x*x*[3]))",1000,5000)
fexp1plus2ele=TF1("fexp1plus2ele","[0]*exp(-(x*[1]))+[2]*exp(-([3]+x*[4]+x*x*[5]))",1000,5000)
#Fexp1plus2ele.SetParameters(310,0.001,210,0.1,-0.001,-0.0000002)
fexp1plus2ele.SetParameters(310,0.001,20,0.1,0.001,0.0000002)

fexp1ele=TF1("fexp1ele","[0]*exp(-(x*[2])+[1])",1000,5000)
fexp1ele.SetParameters(310,0.010,0.001)


#fexp2data=TF1("fexp2data","[0]+x*[1]+x*x*[2]+x*x*x*[3]+[4]*exp(-([5]+x*[6]+x*x*[7]))",1000,5000)
#fexp2data.SetParameters(1000,10,1,0.1,1000,0.1,0.01,0.0000002)


expo2_fit_map={"SR2B":fexp1plus2,"SRW":fexp1plus2,"SRT":fexp1plus2,"CR1B":fexp1plus2,"CR0B":fexp1plus2}
expo1_fit_map={"SR2B":fexp1,"SRW":fexp1,"SRT":fexp1,"CR1B":fexp1,"CR0B":fexp1,"CR1B":fexp1}
poly3_fit_map={"SR2B":fpoly3,"SRW":fpoly3,"SRT":fpoly3,"CR1B":fpoly3,"CR0B":fpoly3,"CR1B":fpoly3}

expo2ele_fit_map={"SR2B":fexp1plus2ele,"SRW":fexp1plus2,"SRT":fexp2,"CR1B":fexp1plus2ele,"CR0B":fexp1plus2ele}

#fexp1=TF1("fexp1","[0]*exp(-(x*[1]))",1000,5000)
#fexp1.SetParameters(310,0.001)

expo2_cr_fit_map={"SR2B_I":fpoly3,"SRW_I":fpoly3,"SRT_I":fpoly3,"CR1B_I":fpoly3,"CR0B_I":fexp2}
expo2_cr_fit_map={"SR2B_I":fexp2data,"SRW_I":fexp2data,"SRT_I":fexp2data,"CR1B_I":fexp2data,"CR0B_I":fexp2data}
expo2_cr_fit_map={"SR2B_I":fexp1plus2data,"SRW_I":fexp1plus2data,"SRT_I":fexp1plus2data,"CR1B_I":fexp1plus2data,"CR0B_I":fexp1plus2data}

#wjets_veto_map = {"SR2B":"SR2B_I","SRW":"SRW_I","SRT":"SRT_I"}

class namecollection(object):
    def __init__(self,namemap):
        self.__namemap=namemap
    def getmap(self):
        return self.__namemap

map_names=namecollection(namemap)

#print map_names.getmap()

#min,max,rebin
bins=[1000,5000,1,"uniform"]
binsvariable=[1000,1250,1500,1750,2000,2250,2500,2750,3000,3500,4000,5000]

binsv=[1000,5000,binsvariable,"variablenorm"]
binsv=[1000,5000,binsvariable,"variable"]

#[binsv=bins

from histoUtils import resizeHisto,fittedHisto
xcheck=False
if(xcheck):
    test= TH1F("test","test",61,0,5000)
    test.Fill(500)            
    test.Fill(1220)            
    test.Fill(4980)            
    test.Fill(5130)            
    test.Fill(5330)            
    test.Fill(5330)            
    bc,be = resizeHisto(test,binsvariable,addOverflow=False)[3:5]
    print bc,"\n\n",be
    bc,be = resizeHisto(test,binsvariable,addOverflow=True)[3:5]
    print "adding overflow \n",bc,"\n\n",be
    bc,be = resizeHisto(test,binsvariable,addOverflow=True,addUnderflow=True)[3:5]
    print "adding underflow \n",bc,"\n\n",be
    
    #c1=TCanvas("c1")
    #test.Draw()
    #c1.SaveAs("test.png")
    h_ret=resizeHisto(test,binsvariable,addOverflow=True)[0]
    #h_ret.Draw()
    #c1.SaveAs("test2.png")

    fexp2=TF1("fexp2","[0]*exp(-([1]+x*[2]+x*x*[3]))",1000,5000)
    fexp2.SetParameters(310,0.1,0.001,0.0000002)
    #fexp2=TF1("fexp2","[0]*exp(-(x*[1]))",1000,5000)
    #fexp2.SetParameters(310,0.001)
    h_ret.Reset("ICES")
    for i in xrange(1000):
        nr = fexp2.GetRandom()
        #    print "extraction i ",i, " is ", nr
        h_ret.Fill(nr)
        #h_ret.FillRandom("fexp2",100)

    fittedTest = fittedHisto(h_ret,fexp2,npars=-1,behavior="shape_only",doRemove=False)
    print fittedTest
    fittedTest[0].SetLineColor(kGreen+2)
    fittedTest[0].Draw("e")
    npars= fexp2.GetNpar()

    for ft in xrange(-npars,npars+1):
        print " file at ",ft
        print" scenario integral ",fittedTest[ft].Integral()
        if abs(ft)>1 and fittedTest[ft].Integral() !=0:
            print "drawing!"
            if(ft>0): fittedTest[ft].SetLineColor(kRed+abs(ft))
            if(ft<0): fittedTest[ft].SetLineColor(kBlue+abs(ft))
            fittedTest[ft].SetLineStyle(abs(ft))
            #        fittedTest[ft].Scale( fittedTest[0].Integral()/fittedTest[ft].Integral())
            fittedTest[ft].Draw("hist same")

    c1.SetLogy()
    c1.SaveAs("testfit.png")



class single_process(namecollection):
    def __init__(self,namemap,sample, path="./",category="muon",year="2016",syst=None,tag=None,bins=None,verbose=False):
        super(single_process,self).__init__(namemap)#initialize the parent class with the map names
#        print "map is " ,self.getmap()
        self.__sample=sample
        self.__category=category
        self.__year=year
        self.__verbose=verbose
        self.__path=path
        if(verbose):print "printing now ====",path,sample,category,year
        self.__syst=syst
        self.__tag=tag
        suffix = ""
        if not (syst is None):
            suffix = suffix+"_"+syst
        if not (tag is None):
            suffix = suffix+"_"+tag
        self.__filename=self.__path+self.__category+"/"+self.__sample+"_"+self.__year+"_"+self.__category+suffix+".root"
        if(verbose):        print "filename ==== ",self.__filename
        self.__bins=bins
        self.__missingno={}
    def getHistoByName(self,histoname,verbose=False):
        h_ret=TH1F
        if(verbose):
            print " looking for histo ", histoname , " in file ", self.__filename
        h_ret=TH1
        f=TFile(self.__filename,"OPEN")
        try:
            h_ret=f.Get(histoname).Clone(histoname)
        except:
            if(verbose):print "no histogram", histoname, " in file ", self.__filename
            f.Close()
            return 0
        h_ret.SetDirectory(0)
        print self.__bins
        if self.__bins!=None:
            if(self.__bins[3]=="uniform"):
                h_ret.GetXaxis().SetRangeUser(self.__bins[0],self.__bins[1])
                h_ret.Rebin(self.__bins[2])
            if("variable" in self.__bins[3]):
                if(verbose):
                    print "trying variable binning!"
                    print h_ret, " integral before" , h_ret.Integral(1,10000)
                    print(resizeHisto(h_ret,self.__bins[2],verbose=verbose))
                nbw=False
                if("norm" in self.__bins[3]):nbw=True
                h_ret=resizeHisto(h_ret,self.__bins[2],verbose=verbose,normalizeToBinWidth=nbw)[0]
                if(verbose):
                    print h_ret," integral ",h_ret.Integral()
                h_ret.SetDirectory(0)
        f.Close()
        if(verbose):
            print " returning  ",h_ret," name ", h_ret.GetName()
        return h_ret

    def getHistoR(self,region,verbose=False):
        
        if(verbose):
            print "gethisto keys "
            print self.getmap().keys()
        if region in self.getmap().keys():
            hname= self.getmap()[region] 
            if(verbose):
                print "getting from region ",region, "hname ",hname
            h_ret =TH1
            try:
                h_ret=self.getHistoByName(hname,verbose).Clone()
                if h_ret==0:
                    print "no histogram in ",region
                    return 0
            except (ValueError): 
                print "no histogram in ",region
                return 0
            h_ret.SetDirectory(0)
            if(verbose):print "returning ",h_ret," name ",h_ret.GetName()
            return h_ret
        else:
            print " no histo found in maps!"
            return None

    def transfer_factors(self,regions_map,onlyCentral=False,mapFitFunction=None,plot=True,syst=None,tag=None,verbose=False):
        histomap={}
        removeFunction=not plot
        if syst is None:
            syst=self.__syst
        if tag is None:
            tag=self.__tag
        for sr,cr in regions_map.iteritems():
            hname_sr= self.getmap()[sr] if sr in self.getmap().keys() else " no sr histo found in map names!"
            hname_cr= self.getmap()[cr] if sr in self.getmap().keys() else " no cr histo found in map names!"
            print "test, filename ",self.__filename
            if(verbose):
                print "sr is ", sr, " histo ", hname_sr
                print "cr is ", cr, " histo ", hname_cr
            try:
                print ("now trying to get them ")
                hsr=self.getHistoR(region=sr,verbose=verbose)
                hbg=self.getHistoR(region=cr,verbose=verbose)
                #hsr=self.getHisto(sr,verbose)  
                #hbg=self.getHisto(cr)
                if hsr==0:
                    self.__missingno[sr]=self.getmap()[sr]
                if hbg==0:
                    self.__missingno[cr]=self.getmap()[cr]
                if(verbose):
                    print " histo sr found ", hsr
                    print " histo cr found ", hbg
            except (TypeError):
                print "warning! Histos not found sr,cr ",sr,cr, " names ", hname_sr, " \n ",hname_cr 
            try:
                historatio=hsr.Clone(self.__sample+"_"+sr+"_over_"+cr)
                historatio.Divide(hbg) 
                historatio_coll={}
                historatio_coll.update({str(historatio.GetName()+"central"):historatio})
                if not (mapFitFunction is None):
                    try:
                        hs_ret = fittedHisto(historatio,mapFitFunction[sr],onlyCentral=onlyCentral,doRemove=removeFunction,npars=-1,behavior="shape_only")
                        historatio_coll.update(hs_ret)
                    except (ValueError):
                        print "fit mode failed! Only nominal will be saved"
                histomap[sr]=historatio_coll
                print historatio_coll
                print("swobul")
                c=TCanvas("c")
                if(plot):
                    print("zugzug")
                    historatio.Draw()
                    print("daboo")
                    suffix="_"+self.__year+"_"+self.__category
                    if not syst is None:
                        suffix = suffix+ "_"+syst
                    if not tag is None:
                        suffix=suffix+"_"+tag
                    namepng=plotpath+historatio.GetName()+suffix+".png"
                    c.SetLogy()
                    c.SaveAs(namepng)
            except (TypeError):
                print "nothing done for ",hname_sr,hname_cr
            if(verbose):print "missingno are", self.__missingno
        return histomap
    def get_missing(self):
        print "missingno are ", self.__missingno

class data_driven(single_process):
    def __init__(self,samples,namemap=namemap,path=opt.pathin,sample="Data",category="muon",year="2016",bins=bins,pathout=opt.pathout,syst=None,tag=None,verbose=False):
        self.__verbose=verbose

        self.__samples=samples        

        if not path[-1]=="/":
            path=path+"/"
        self.__path=path

        self.__bins=bins
        self.__missingno={}
        self.__namemap=namemap


        if pathout is None:
            self.__pathout=self.__path # if no pathout is given, use input path
        else:
            if not pathout[-1]=="/":
                pathout=pathout+"/"
            self.__pathout=pathout

        self.__syst=syst
        self.__tag=tag
        self.__sample=sample        
        self.__category=category
        self.__year=year
        self.__defaults = {"sample":sample,"category":category,"year":year,"syst":syst}
        self.update_single_channel(namemap)
        self.update_filename()

    def update_single_channel(self,namemap=None):
        if (namemap is None):
            namemap =self.__namemap
        print "tag is ",self.__tag, " syst ", self.__syst, " path ",self.__path
        super(data_driven,self).__init__(namemap=namemap,sample=self.__sample,path=self.__path,category=self.__category,year=self.__year,syst=self.__syst,tag=self.__tag,bins=self.__bins,verbose=self.__verbose)#initialize the parent class with the map names     
    def set_maps(self,namemap=namemap):
        self.__namemap=namemap
    def set_sample(self,sample="Data"):
        self.__sample=sample
    def set_year(self,year="year"):
        self.__year=year
    def set_syst(self,syst=None):
        self.__syst=syst
    def set_tag(self,tag=None):
        self.__tag=tag
    def set_path(self,path=None):
        if not (path is None):
            self.__path=path
    def set_category(self,category="muon"):
        self.__category=category
    def set_defaults(self,defaults):
        self.__defaults=defaults
    def reset_info(self):
#        self.set_syst(self.__defaults["syst"])
        self.set_category(self.__defaults["category"])
        self.set_year(self.__defaults["year"])
        self.set_sample(self.__defaults["sample"])
    def reset_syst(self):
        self.set_syst(self.__defaults["syst"])
    def update_filename(self):
        suffix=""
        if not self.__syst is None:
            sufffix=suffix+"_"+self.__syst
        if not self.__tag is None:
            sufffix=suffix+"_"+self.__tag
        self.__filename=self.__path+self.__category+"/"+self.__sample+"_"+self.__year+"_"+self.__category+suffix+".root"

    def get_filename(self):
        return self.__filename

    def writeHistoToFile(self,histo,region,pathout=None,sample=None,syst=None,tag=None,verbose=False):
        histoname = self.__namemap[region] 
        if syst is None:
            syst= self.__syst
        if tag is None:
            tag=self.__tag
        suffix=""
        if not (syst is None):
            suffix = suffix+"_"+syst
        if not (tag is None):
            suffix = suffix+ "_"+tag
        if sample==None:
            sample=self.__sample
        if pathout is None:
            pathout=self.__pathout
        else :
            if not pathout[-1]=="/":
                pathout=pathout+"/"
            if not os.path.exists(pathout+self.__category):
                os.system("mkdir -p "+pathout+self.__category)
        filename=pathout+self.__category+"/"+sample+"_"+self.__year+"_"+self.__category+suffix+".root"
        #print "saving name ", histoname
        #print "to file ", filename
        if os.path.exists(filename):
            fw=TFile(filename,"UPDATE")
        else:
            fw=TFile(filename,"NEW")
        fw.cd()
        histo.Write(histoname)
        fw.Close()
    def getHisto(self,region,sample,nominaltag=False,nominalsyst=False,verbose=False):
        if(verbose):print "crosscheck"
        self.set_sample(sample)
        systtmp=self.__syst
        tagtmp=self.__tag
        if nominaltag:
            self.set_tag(None)
        if nominalsyst:
            self.set_syst(None)
        if(sample=="Data"):
            self.set_syst(None)
            self.set_tag(None)
        self.update_filename()
        self.update_single_channel()
        #print "getting histo now!!! sample ",sample, "region",region,"syst",self.__syst
        hs=super(data_driven,self).getHistoR(region=region,verbose=verbose)
        self.reset_info()
        self.set_syst(systtmp)        
        self.set_tag(tagtmp)        
        self.update_filename()
        self.update_single_channel()
        return hs
    def set_samples(self,samples):
        self.__samples=samples

    def transfer_factor(self,regions,sample,path=None,sampleweights=None,namemap=None,onlyCentral=False,mapFitFunction=None,syst_sf=False,savecr=True,category=None,year=None,plot=True,syst=None,tag=None,verbose=False):
        if (namemap is None):
           namemap= self.__namemap
        systtmp=syst
        if syst_sf==True:
            syst=None
        self.set_syst(syst)
        print "sample tfratio ",sample
        print "path before super",path
        pathtmp=self.__path
        if path is None:
            path=self.__pathout#not a mistake: by default taking the path where multiprocess below will write it. This avoids overwriting local files as default behavior 
        self.set_path(path)
        print self.__path
        if syst_sf==True:
            syst=None
        self.set_syst(syst)
        if not(sample is None):    
            if isinstance(sample,list):
                if len(sample)>1:
                    print "making internal multiprocess"
                    sp=self.make_multiprocess(regions=regions,pathout=path, samplelist=sample,sampleweights=sampleweights,syst=syst,syst_sf=syst_sf,savecr=savecr,tag=tag)
                    print "got it "
                if len(sample)==1:
                    sp=sample[0]
            if isinstance(sample,str):
                sp= sample
            self.set_sample(sp)
        if not(year is None):
            self.set_year(year)
        if not(category is None):
            self.set_category(category)
        
        self.update_filename()
        self.update_single_channel(namemap)
           
        #print "filename is ",self.__filename
        print "calling super  method"
        histomap = super(data_driven,self).transfer_factors(regions_map=regions,onlyCentral=onlyCentral, mapFitFunction=mapFitFunction,tag=tag,plot=plot,verbose=verbose)
        self.reset_info()
        self.set_syst(systtmp)
        self.set_path(pathtmp)
        self.update_single_channel()
        self.update_filename()
        return histomap

    def make_multiprocess(self,regions,samplelist,sampleweights=None,namemap=None,category=None,year=None,syst=None,tag=None,syst_sf=False,savecr=True,pathout=None,verbose=False ):
        if (namemap is None):
           namemap= self.__namemap
        if not(year is None):
            self.set_year(year)
        if not(category is None):
            self.set_category(category)
        sample= "".join(samplelist)
        samplenom=self.__sample
        if syst is None:
            syst=self.__syst
        else: self.set_syst(syst)
        tagtmp=self.__tag
        if tag is None:
            tag=self.__tag
        suffix=""
        if not (syst is None):
            suffix=suffix+"_"+syst
        if not (tag is None):
            suffix=suffix+"_"+tag
        if pathout is None:
            pathout=self.__pathout
        else :
            if not pathout[-1]=="/":
                pathout=pathout+"/"
            if not os.path.exists(pathout+self.__category):
                os.system("mkdir -p "+pathout+self.__category)
        fileout=pathout+self.__category+"/"+sample+"_"+self.__year+"_"+self.__category+suffix+".root"
        if not os.path.exists(fileout): 
            fout =  TFile (fileout,"NEW")
        else:
            fout =  TFile (fileout,"UPDATE")
        for sr,cr in regions.iteritems():
            for s in self.__samples:
#                print "porting sample ",s," in samplelist ", (s in samplelist)
                if not s in samplelist:
 #                   print "porting now"
                    self.set_tag(None)
                    h_srout=(self.getHisto(region=sr,sample=s,verbose=False)).Clone()
#                    self.writeHistoToFile(histo=h_srout,pathout=self.__path,region=sr,sample=s,tag=tag)
                    self.writeHistoToFile(histo=h_srout,pathout=pathout,region=sr,sample=s,tag=tag)
                    if savecr:
                        if(syst_sf):self.set_syst(None)
                        self.set_tag(None)
                        h_crout=(self.getHisto(region=sr,sample=s,verbose=False)).Clone()
                        self.writeHistoToFile(histo=h_crout,pathout=pathout,region=cr,sample=s,tag=tag)
#                        self.writeHistoToFile(histo=h_crout,pathout=self.__path,region=cr,sample=s,tag=tag)
                        if(syst_sf):self.set_syst(syst)
                    self.set_tag(tag)

            self.set_tag(None)
            h_sr=(self.getHisto(region=sr,sample=self.__sample,verbose=False)).Clone()
            self.set_tag(tag)
            h_sr.Reset("ICES")
            if savecr:
                if(syst_sf):self.set_syst(None)
                self.set_tag(None)
                #print "just before sr, srname is  ",h_sr.GetName()
                h_cr=(self.getHisto(region=cr,sample=self.__sample,verbose=False)).Clone()
                #print "just aftr cr, crname is  ",h_cr.GetName()
                self.set_tag(tag)
                h_cr.Reset("ICES")
                h_cr.SetDirectory(0)
                if(syst_sf):self.set_syst(syst)
            for sl in samplelist:
                self.set_sample(sl)
                self.update_filename()
                self.set_tag(None)
                #print "sample, ",sl," making multiprocess sr ", sr, " cr ", cr
                htempsr=(self.getHisto(region=sr,sample=sl,verbose=False))
                self.set_tag(tag)
#                self.writeHistoToFile(histo=htempsr,pathout=self.__path,region=sr,sample=sl,tag=tag)
                self.writeHistoToFile(histo=htempsr,pathout=pathout,region=sr,sample=sl,tag=tag)
                if savecr:
                    if(syst_sf):self.set_syst(None)
                    self.set_tag(None)
                    htempcr=(self.getHisto(region=cr,sample=sl,verbose=False))
                    if(syst_sf):self.set_syst(syst)
                    self.set_tag(tag)
                    self.writeHistoToFile(histo=htempcr,pathout=pathout,region=cr,sample=sl,tag=tag)
#                    self.writeHistoToFile(histo=htempcr,pathout=self.__path,region=cr,sample=sl,tag=tag)
                    #print "in savecr, integral",htempcr.Integral()

                wsr=1.0
                wcr=1.0
                if not (sampleweights is None):
                    wsr=sampleweights[sl]
                    wcr=sampleweights[sl]
                h_sr.Add(htempsr,wsr)
                if savecr:
                    h_cr.Add(htempcr,wcr)
                    #print "in savecr, integral after sum",h_cr.Integral()
            fout.cd()
            h_sr.Write()
            
            if savecr:
                fout.cd()
                h_cr.SetDirectory(fout)
                #print "hcr name",h_cr.GetName()
                h_cr.Write()
                fout.Write(h_cr.GetName())
                #print "in savecr, integral after sum",h_cr.Integral()
                #print "in savecr, saving to fileout ",fout ," name ", fout.GetName()
        fout.Close()
        self.reset_syst()
        self.set_tag(tagtmp)
        return sample

    def tfratio(self,regions,samplelist,ddMapFitFunction=None, tfMapFitFunction=None,sampleweights=None,onlyCentral=False,savecr=True,option="histo",namemap=None,category=None,year=None,plot=False,syst_sf=False,syst=None,tag=None,pathout=None,portname="",verbose=False): 
        #Subtract
        if (namemap is None):
            namemap= self.__namemap
        if year is None:
            year=self.__defaults["year"]
        #print "intag is ",tag
        if tag is None:
            tag=self.__tag
        systtmp=self.__syst
        tagtmp=self.__tag
        self.set_tag(tag)
        self.set_year(year)
        #print "tag is ",self.__tag 
        if syst is None:
            syst=self.__syst
        print "syst is ",self.__syst 
        self.set_syst(syst)
        self.update_filename()
        print "filename is ", self.__filename
        if category is None:
            category=self.__defaults["category"] 
        self.set_category(category)
        c1 = TCanvas("c1canvas")  
        fout = TFile("tffile.root","RECREATE")
        #        c = TCanvas("c")  
        if pathout is None:
            pathout=self.__pathout
        if pathout==self.__path:
            portname=""
        print "pathout is ",pathout
        if len(samplelist)>1:
            mp=self.make_multiprocess(regions=regions,samplelist=samplelist,pathout=pathout,sampleweights=sampleweights,syst_sf=syst_sf,syst=syst,tag=tag)#hwere we produce this in the input file directory
        self.set_syst(syst)
        print "after multiprocess, syst",self.__syst
        hs_proj_ss={}
        #if len(samplelist)==1:

#        for sl in samplelist:
#            hs_proj_ss[sl] = self.transfer_factor(regions,sl,namemap=namemap,onlyCentral=onlyCentral,mapFitFunction=tfMapFitFunction,category=category,year=year,plot=plot,syst=syst,tag=tag,syst_sf=syst_sf,verbose=False)
        print "pathout is ",pathout, " mp is ",mp
        hs_proj_multiprocess = self.transfer_factor(regions,mp,path=pathout,namemap=namemap,onlyCentral=onlyCentral,mapFitFunction=tfMapFitFunction,category=category,year=year,plot=plot,syst=syst,tag=tag,syst_sf=syst_sf,verbose=False)

        
        self.set_syst(syst)
        print "before regions syst is" ,self.__syst
        for sr,cr in regions.iteritems():
#            print "getting data"
            h_data_sr=self.getHisto(region=sr,sample="Data")
            h_data_cr=self.getHisto(region=cr,sample="Data")
            print "before fit syst is" ,self.__syst
            h_data_cr_fit=fittedHisto(self.getHisto(region=sr,sample="Data"),ddMapFitFunction[cr],doRemove=True,npars=-1,behavior="shape_only")[0]
            print "after fit syst is" ,self.__syst

            doskip=False
            if(h_data_sr==0):
                self.__missingno[sr]=self.__namemap[sr]
                doskip=True
            if(h_data_cr==0):
                self.__missingno[cr]=self.__namemap[cr]
                doskip=True
            if(doskip):
                continue
            
            #SR
            h_data_sr.SetLineColor(kBlack)
            #samples to control
            h_sr=h_data_sr.Clone("".join(samplelist)+"_"+sr+"_"+category)
            h_sr.Reset("ICES")
            for sl in samplelist:
                h_sr.Add(self.getHisto(region=sr,sample=sl,nominaltag=True))
            #data driven one
            h_dd_sr=h_data_sr.Clone("DD"+"".join(samplelist)+"_"+sr+"_"+category)

            #CR
            h_data_cr.SetLineColor(kBlack)
            #samples to control
            h_cr=h_data_cr.Clone("".join(samplelist)+"_"+cr+"_"+category)
            h_cr.Reset("ICES")
            if not savecr:
                self.set_syst(None)
            for sl in samplelist:
                    h_cr.Add(self.getHisto(region=cr,sample=sl,nominaltag=True))
            self.set_syst(syst)
                
            #data driven one
            h_dd_cr=h_data_cr.Clone("DD"+"".join(samplelist)+"_"+cr+"_"+category)
            

            #            h_dd_cr_fit=fittedHisto(h_dd_cr,ddMapFitFunction[cr],doRemove=False,npars=-1,behavior="shape_only")[0]
            #h_dd_cr_fit=fittedHisto(h_dd_cr,ddMapFitFunction[cr],doRemove=False,npars=-1,behavior="shape_only")[0]
            #h_dd_cr_fit.SetName("DDFit"+"".join(samplelist)+"_"+cr+"_"+category)
            h_dd_cr_fit=h_data_cr_fit.Clone("DDFit"+"".join(samplelist)+"_"+cr+"_"+category)
            print "data integral before selection in sr is ",h_dd_sr.Integral(), " and in cr", h_dd_cr.Integral()
            samples = self.__samples
            print "samples are",samples
            for s in samples:
                if (s=="Data"):continue
                if (s in samplelist):continue
                try:
                    print "sample is ",s,"syst is" ,self.__syst
                                
                    print "adding hsr and hcr for sample ",s, " regions are ",sr,cr, " "
                    hsr= self.getHisto(region=sr,sample=s,verbose=False,nominaltag=True)
                    
                    print "hsr integral",hsr.Integral()
                    h_dd_sr.Add(hsr,-1)
                    print "data integral sr is ",h_dd_sr.Integral()
                    self.writeHistoToFile(histo=hsr,pathout=pathout,region=sr,sample=s+portname,syst=syst,tag=tag)

                    if not savecr:
                        self.set_syst(None)
                    hcr= self.getHisto(region=cr,sample=s,verbose=False,nominaltag=True)

                    print "hcr integral",hcr.Integral()
                    h_dd_cr.Add(hcr,-1)
                    h_dd_cr_fit.Add(hsr,-1)
                    
                    print "data integral cr is ",h_dd_cr.Integral()
                    
                    self.writeHistoToFile(histo=hcr,pathout=pathout,region=cr,sample=s+portname,syst=syst,tag=tag)
                    self.set_syst(syst)
                except (TypeError): 
                    print "hsr or hcr not found!",hsr,hcr
            
                
                
            if len(samplelist)>1:
                #make composite sample as well:
                histoproj =hs_proj_multiprocess
#            if len(samplelist)==1:
#                histoproj =hs_proj_ss[samplelist[0]]
            print "histproj is", histoproj 

            histo_res={}   

            if(plot):
                h_sr.Draw()
                if(verbose): print " h_sr ",h_sr," integral ",h_sr.Integral()," bin1 ",h_sr.GetBinContent(1)," bin4 ",h_sr.GetBinContent(4)

            fout.cd()
            c2= TCanvas("c2")
            h_dd_cr.Write()
            h_dd_cr_fit.Write()
            print "ischanigng cr 1",h_dd_cr.Integral()
            if(plot):
                h_dd_cr_fit.Draw()
                h_data_sr.Write(str("Data"+sr+"_"+category))
                c2.SetLogy()
                c2.SaveAs(str(plotpath+"h_dd_cr"+h_dd_cr_fit.GetName()+".png"))

            print "ischanigng cr 2",h_dd_cr.Integral()
            for sc,hp in histoproj[sr].iteritems():
                if(verbose):
                    # if(True):
                    print " checking sc hp"
                    print "  sc ",sc," \n\n"
                    print " hp ",hp," integral ",hp.Integral()," bin1 ",hp.GetBinContent(1)," bin4 ",hp.GetBinContent(4)
                    
                h_dd_sr_proj=copy.deepcopy(hp)#.Clone(str(hp.GetName()+"mult"))
               
                h_dd_sr_proj.SetName(str(hp.GetName()+"mult_dd"))
                h_dd_sr_proj.Reset("ICES")
                h_dd_sr_proj.Add(hp)
#                h_dd_sr_proj.SetDirectory(0)
                h_dd_sr_proj.Multiply(h_dd_cr)
                h_dd_sr_proj.Write()

                h_dd_fit_sr_proj=copy.deepcopy(hp)#.Clone(str(hp.GetName()+"mult"))
              
                h_dd_fit_sr_proj.SetName(str(hp.GetName()+"mult_dd_ddfit"))
                h_dd_fit_sr_proj.Reset("ICES")
                h_dd_fit_sr_proj.Add(hp)
#                h_dd_fit_sr_proj.SetDirectory(0)
                h_dd_fit_sr_proj.Multiply(h_dd_cr_fit)
                h_dd_fit_sr_proj.Write()
                histo_res[sc]=h_dd_sr_proj
                #histo_res[sc]=h_dd_fit_sr_proj
                print " hp ",h_dd_sr_proj," integral ",h_dd_sr_proj.Integral()," bin1 ",h_dd_sr_proj.GetBinContent(1)," bin4 ",h_dd_sr_proj.GetBinContent(4)
                if(plot):
                    if(verbose):print "plotting, is sc ", sc , " string ",isinstance(sc,str)
                    if(not isinstance(sc,str)):
                        #c1.cd()
                        print "hist 0 integral ",h_dd_sr_proj.Integral(), " max ",h_dd_sr_proj.GetMaximum()
                        for b in xrange(1,h_dd_sr_proj.GetNbinsX()+1):
                            print "hist 0 content",h_dd_sr_proj.GetBinContent(b), " edge ",h_dd_sr_proj.GetBinLowEdge(b) 
                        if (int(sc)==0): 
                        #    c1.cd()
                            h_dd_sr_proj.SetLineColor(kBlack)
                        #    h_dd_sr_proj.Scale(22./27)
                            h_dd_sr_proj.Draw("")
                           
                        if (int(sc)!=0): 
                        #    c1.cd()
                            print " plotting sc !=0 "
                            if(int(sc)>0):h_dd_sr_proj.SetLineColor(kRed)
                            if(int(sc)<0):h_dd_sr_proj.SetLineColor(kBlue)
                            #h_dd_sr_proj.SetLineStyle(abs(int(sc)))
                            h_dd_sr_proj.Draw("esame")
                            print("printed ")
                    else:
                        h_dd_sr_proj.SetLineColor(kViolet)
                        h_dd_sr_proj.Draw("samee")
            if(plot):
                c1.SetLogy()
                c1.SaveAs((str(plotpath+"DDvTF_alluncs"+"".join(samplelist)+"_"+sr+"_"+year+"_"+category+".png")))

            h_sr.Write()
            if(plot):
                h_sr.Draw()
                print " h_sr ",h_sr," integral ",h_sr.Integral()," bin1 ",h_sr.GetBinContent(1)," bin4 ",h_sr.GetBinContent(4)
            for sc,hp in histoproj[sr].iteritems():
                
                h_sr_proj=hp.Clone()
                h_sr_proj.SetName(str(hp.GetName()+"mult_mc"))
                h_sr_proj.Multiply(h_cr)
                #h_sr_proj.SetDirectory(0)
                h_sr_proj.Write()

                if(True):
                    print " checking sc hp"
                    print "  sc ",sc," \n\n"
                    print " hp ",hp," integral ",hp.Integral()," bin1 ",hp.GetBinContent(1)," bin4 ",hp.GetBinContent(4)
                if(plot):
                    if(verbose): print ("plotting ")
                    if(not isinstance(sc,str)):
                        if (sc==0): 
                            h_sr_proj.SetLineColor(kBlue)
                            h_sr_proj.Draw("histo same")
                        if (sc!=0): 
                            if(sc>0):h_sr_proj.SetLineColor(kRed)
                            if(sc<0):h_sr_proj.SetLineColor(kBlue)
                            h_sr_proj.SetLineStyle(abs(int(sc)))
                            h_sr_proj.Draw("histo same")
                    else:
                        h_sr_proj.SetLineColor(kViolet)
                        h_sr_proj.Draw("histo samee")
                            
            if(plot):
                c1.SetLogy()
                c1.SaveAs((str(plotpath+"MCvTF_alluncs"+"".join(samplelist)+"_"+sr+"_"+year+"_"+category+".png")))

            if(plot):
                c = TCanvas("c")  
                #print ("plotting ")
                h_dd_sr.Draw("e")
                h_sr.Draw("same hist")
                #namepng=plotpath+historatio.GetName()+".png"
                c.SaveAs(str(plotpath+"DDvsMC"+"".join(samplelist)+"_"+sr+"_"+year+"_"+category+".png"))
                h_dd_cr.Draw("e")
                h_cr.Draw("same hist")
                c.SaveAs(str(plotpath+"DDvsMC"+"".join(samplelist)+"_"+cr+"_"+year+"_"+category+".png"))
            print "ischanigng cr 3",h_dd_cr.Integral()
            #filename put it herer
            self.writeHistoToFile(histo=h_data_sr,pathout=pathout,region=sr,sample="Data"+portname,syst=syst,tag=tag)
            self.writeHistoToFile(histo=h_data_cr,pathout=pathout,region=cr,sample="Data"+portname,syst=syst,tag=tag) 
            self.writeHistoToFile(histo=h_dd_cr,pathout=pathout,region=cr,sample="DD_counting"+"".join(samplelist),syst=syst,tag=tag)
            self.writeHistoToFile(histo=h_dd_sr,pathout=pathout,region=sr,sample="DD_counting"+"".join(samplelist),syst=syst,tag=tag)
            self.writeHistoToFile(histo=histo_res[0],pathout=pathout,region=sr,sample="DD"+"".join(samplelist),syst=syst,tag=tag)
            #if not (pathout is None):
            srregions=regions
        print "syst sf is ", savecr, " regions bef",srregions
        if not savecr:
            srregions={}
            for sr,cr in regions.iteritems():
                srregions[sr]=sr #in case, only save sr files
        print "regions after ",srregions

        self.make_multiprocess(regions=srregions,samplelist=samplelist,pathout=pathout,sampleweights=sampleweights,syst_sf=syst_sf,syst=syst,tag=tag)
        
        fout.Close()
        self.reset_info()
#        self.reset_syst()
        self.set_tag(tagtmp)
        self.set_syst(systtmp)

    def portSamples(self,regions,samplelist,sampleweights=None,namemap=None,category=None,year=None,syst=None,tag=None,savecr=True,syst_sf=False,pathout=None,portname="",tagout=None,verbose=False ):
        if (namemap is None):
            namemap= self.__namemap
        if not(year is None):
            self.set_year(year)
        if not(category is None):
            self.set_category(category)
        samplenom=self.__sample

        systtmp=self.__syst
        tagtmp=self.__tag
        if syst is None:
            syst=self.__syst
        else: self.set_syst(syst)
        if tag is None:
            tag=self.__tag
        if tagout==None:            
            tagout=tag
        if pathout==self.__path:
            portname="_rebin"
        for s in samplelist:
            for sr,cr in regions.iteritems():
                print "sample is ",s,"syst is" ,self.__syst
                hsr= self.getHisto(region=sr,sample=s,verbose=True)
                self.writeHistoToFile(histo=hsr,pathout=pathout,region=sr,sample=s+portname,syst=syst,tag=tagout)
                if(savecr):
                    if(syst_sf):self.set_syst(None)
                    hcr= self.getHisto(region=cr,sample=s,verbose=False)
                    self.writeHistoToFile(histo=hcr,pathout=pathout,region=cr,sample=s+portname,syst=syst,tag=tagout)
                self.set_syst(syst)
        self.set_syst(systtmp)
        self.set_tag(tagtmp)

wjets=single_process(namemap=namemap,sample="WJets",path=opt.pathin,category=opt.category,bins=bins)    
ttbar=single_process(namemap=namemap,sample="TT_Mtt",path=opt.pathin,category=opt.category,bins=bins)    


samples=["Data","TT_Mtt","WJets","ST","QCD"]
samplesnoqcd=["Data","TT_Mtt","WJets","ST"]
#dd = data_driven(samplesnoqcd,bins=binsv)
#dd = data_driven(samples=samples,bins=binsv)
dd = data_driven(namemap=namemap,samples=samples,year=opt.year,category=opt.category,bins=binsv)
#wjets.transfer_factors(srcr_map_3)ex
sampleweights_wup={"WJets":2.0,"TT_Mtt":1.}
sampleweights_wdown={"WJets":0.5,"TT_Mtt":1.}

sampleweights_ttup={"WJets":1.0,"TT_Mtt":1.33}
sampleweights_ttdown={"WJets":1.0,"TT_Mtt":0.75}

signalsamples=[ "WP_M"+str(x)+"000W"+str(x)+"0_RH" for x in xrange(2,5)]

print signalsamples

testnominal=True
copysignals=True
altwjetstt=True
systs=["jesUp","jesDown","jerUp","jerDown","PFUp","PFDown","puUp","puDown"]
doTFPlots=True

systs=[]
#testnominal=False
altwjetstt=False
doTFPlots=False
copysignals=False

mapTFFunctions= expo2_fit_map
if opt.category=="electron" :
    mapTFFunctions= expo2ele_fit_map


if testnominal:
    dd.portSamples(samplelist=signalsamples,regions=wjets_veto_map,syst_sf=True,savecr=True,tag=None) #this takes CR as from nominal always
    dd.tfratio(wjets_veto_map,ddMapFitFunction=expo2_cr_fit_map,onlyCentral=True,tfMapFitFunction=mapTFFunctions,samplelist=["WJets","TT_Mtt"],savecr=True,syst_sf=False,plot=False)
    dd.transfer_factor(wjets_veto_map,namemap=namemap,mapFitFunction=mapTFFunctions,onlyCentral=True,tag=None,sample=["WJets","TT_Mtt"],plot=True,verbose=False)
#        dd.portSamples(samplelist=signalsamples,regions=wjets_veto_map,syst_sf=True,savecr=True,tag=None,tagout="WJetsUp") #this takes CR as from nominal always


if(altwjetstt):
    dd.tfratio(wjets_veto_map,ddMapFitFunction=expo2_cr_fit_map,sampleweights=sampleweights_wup,onlyCentral=True,tfMapFitFunction=mapTFFunctions,samplelist=["WJets","TT_Mtt"],tag="WJetsUp",plot=False)
    dd.tfratio(wjets_veto_map,ddMapFitFunction=expo2_cr_fit_map,sampleweights=sampleweights_wdown,onlyCentral=True,tfMapFitFunction=mapTFFunctions,samplelist=["WJets","TT_Mtt"],tag="WJetsDown",plot=False)
    dd.tfratio(wjets_veto_map,ddMapFitFunction=expo2_cr_fit_map,sampleweights=sampleweights_wup,onlyCentral=True,tfMapFitFunction=mapTFFunctions,samplelist=["WJets","TT_Mtt"],tag="TT_MttUp",plot=False)
    dd.tfratio(wjets_veto_map,ddMapFitFunction=expo2_cr_fit_map,sampleweights=sampleweights_wdown,onlyCentral=True,tfMapFitFunction=mapTFFunctions,samplelist=["WJets","TT_Mtt"],tag="TT_MttDown",plot=False)

    if copysignals:
        dd.portSamples(samplelist=signalsamples,regions=wjets_veto_map,syst_sf=True,savecr=True,tag=None,tagout="WJetsUp") #this takes CR as from nominal always
        dd.portSamples(samplelist=signalsamples,regions=wjets_veto_map,syst_sf=True,savecr=True,tag=None,tagout="WJetsDown") #this takes CR as from nominal always
        dd.portSamples(samplelist=signalsamples,regions=wjets_veto_map,syst_sf=True,savecr=True,tag=None,tagout="TT_MttUp") #this takes CR as from nominal always
        dd.portSamples(samplelist=signalsamples,regions=wjets_veto_map,syst_sf=True,savecr=True,tag=None,tagout="TT_MttDown") #this takes CR as from nominal always



for s in systs:
    dd.tfratio(wjets_veto_map,ddMapFitFunction=expo2_cr_fit_map,onlyCentral=True,tfMapFitFunction=mapTFFunctions,samplelist=["WJets","TT_Mtt"],syst=s,savecr=False,syst_sf=True,tag=None)#this should take the pathout default, which is the v14_rebin folder
    if(copysignals):
        dd.portSamples(samplelist=signalsamples,regions=wjets_veto_map,syst=s,syst_sf=True,savecr=True) #this takes CR as from nominal always

##Transfer factors
#doTFPlots=False
#doTFPlots=True

if(doTFPlots):
    dd.transfer_factor(wjets_veto_map,namemap=namemap,mapFitFunction=mapTFFunctions,onlyCentral=True,sampleweights=sampleweights_wup,tag="wjetsUp",sample=["WJets","TT_Mtt"],plot=True,verbose=False)
    dd.transfer_factor(wjets_veto_map,namemap=namemap,mapFitFunction=mapTFFunctions,onlyCentral=True,sampleweights=sampleweights_wdown,tag="wjetsDown",sample=["WJets","TT_Mtt"],plot=True,verbose=False)
    dd.transfer_factor(wjets_veto_map,namemap=namemap,mapFitFunction=mapTFFunctions,onlyCentral=True,sampleweights=sampleweights_ttup,tag="ttUp",sample=["WJets","TT_Mtt"],plot=True,verbose=False)
    dd.transfer_factor(wjets_veto_map,namemap=namemap,mapFitFunction=mapTFFunctions,onlyCentral=True,sampleweights=sampleweights_ttdown,tag="ttDown",sample=["WJets","TT_Mtt"],plot=True,verbose=False)
#
