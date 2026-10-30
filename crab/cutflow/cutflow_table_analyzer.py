import ROOT
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-l', '--lepton', dest='lepton', type=str, default='mu', help="lepton flavor [ el , mu ]")
parser.add_argument('-y', '--year', dest='year', type=str, default='UL2018', help=" UL2017 UL2016preVFP UL2016postVFP UL2018 ")
parser.add_argument('-data',"--ISDATA", action="store_true", help="enbale this feature to run on data")

args = parser.parse_args()
lep = args.lepton
year = args.year
MC_Data = "data" if args.ISDATA else "mc"
year_folder = {'UL2016preVFP': 'SIXTEEN_preVFP', 'UL2016postVFP': 'SIXTEEN_postVFP', 'UL2017': 'SEVENTEEN', 'UL2018': 'EIGHTEEN'}


if(MC_Data=="mc"):
    hist_names = ['Nocut_npvs', 'trig_sel_npvs', 'tight_lep_sel_npvs', 'losse_lep_veto_npvs', 'sec_lep_veto_npvs', 'jet_sel_npvs', 'b_tag_jet_sel_npvs','MET_filter_npvs']
    Channels = ['Tchannel','Tbarchannel','tw_top', 'tw_antitop','Schannel','ttbar_SemiLeptonic','ttbar_FullyLeptonic','WJetsToLNu_0J', 'WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L','QCD']
    if(year=='UL2017'): Channels = Channels + ['WJetsToLNu_0J_lagecy','WJetsToLNu_2J_lagecy','WJetsToLNu_2J_ext_lagecy']
#'ttbar_SemiLeptonic',
elif(MC_Data=="data"):
        hist_names = ['Nocut_npvs', 'trig_sel_npvs', 'tight_lep_sel_npvs', 'losse_lep_veto_npvs', 'sec_lep_veto_npvs', 'jet_sel_npvs', 'b_tag_jet_sel_npvs', 'MET_filter_npvs']
        if(year=='UL2016preVFP'): Channels = [ 'Run2016B_ver1_'+lep, 'Run2016B_ver2_'+lep, 'Run2016C_HIPM_'+lep, 'Run2016D_HIPM_'+lep, 'Run2016E_HIPM_'+lep, 'Run2016F_HIPM_'+lep]
        if(year=='UL2016postVFP'): Channels = [ 'Run2016F_'+lep, 'Run2016G_'+lep, 'Run2016H_'+lep]
        if(year=='UL2017'): Channels = [ 'Run2017B_'+lep, 'Run2017C_'+lep, 'Run2017D_'+lep, 'Run2017E_'+lep, 'Run2017F_'+lep]
        if(year=='UL2018'): Channels = [ 'Run2018A_'+lep,'Run2018B_'+lep, 'Run2018C_'+lep, 'Run2018D_'+lep] 
# Access the histogram

#Channels = ['ttbar_SemiLeptonic','ttbar_FullyLeptonic','DYJetsToLL','WWTo2L2Nu']
print(" histogrma itegral are printted in million")
for channel in Channels:
    # Open the ROOT file
    
    #file_name = "/nfs/home/common/RUN2_UL/Cutflow_crab_crosscheck/"+year_folder[year]+"/2J1T1/Cutflow_"+channel+"_2J1T1_"+lep+".root"
    file_name = "/nfs/home/common/RUN2_UL/Cutflow_crab_crosscheck/"+year_folder[year]+"/2J1T1/Cutflow_"+channel+"_2J1T1_"+lep+".root"
    print("\n"+channel+"\t"+file_name)
    file = ROOT.TFile(file_name , "READ")
    if(MC_Data=="mc"):
        minitree_file = ROOT.TFile("/nfs/home/common/RUN2_UL/Minitree/"+year_folder[year]+"/2J1T1/Minitree_"+channel+"_2J1T1_"+lep+".root", "READ")
        tree = minitree_file.Get("Events")
    for hist_name in hist_names:
        hist = file.Get("histograms/"+hist_name)  # Replace "histogram_name" with the actual name of the histogram
        #if(hist.Integral()/1000000 > 0.1): print(round(hist.Integral()/1000000,2)," M \t:\t"+hist_name)
        print(round(hist.Integral(),2),";\t ",end = '')
    if(MC_Data=="mc"):
        print("\n","hist entry : ",round(hist.GetEntries(),2),"\t tree Entry : ",round(tree.GetEntries(),2))
        #print("\n","\t tree Entry : ",round(tree.GetEntries(),2))

