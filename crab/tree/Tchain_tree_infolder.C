#include<iostream>
using namespace std;

#include"TCanvas.h"
#include "TH1F.h"
#include "TGaxis.h"

#include <glob.h>
std::vector<std::string> glob(const char *pattern) {
    glob_t g;
    glob(pattern, GLOB_TILDE, nullptr, &g); // one should ensure glob returns 0!
    std::vector<std::string> filelist;
    filelist.reserve(g.gl_pathc);
    for (size_t i = 0; i < g.gl_pathc; ++i) {
        filelist.emplace_back(g.gl_pathv[i]);
    }
    globfree(&g);
    return filelist;
}

void check(){
TChain chain("Events");
for (const auto &filename : glob("*.root")) {
    chain.Add(filename.c_str());
}
    //chain.Print();i
    TString cut="(Sum$(Electron_pt>35 && abs(Electron_eta)<2.4 && Electron_cutBased==4 && (abs(Electron_EtaSC)<1.4442 || abs(Electron_EtaSC)>1.5660) && ((abs(Electron_EtaSC)<=1.479 && abs(Electron_dz)< 0.10 && abs(Electron_dxy)< 0.05) || (abs(Electron_EtaSC)> 1.479 && abs(Electron_dz)< 0.20 && abs(Electron_dxy)< 0.10)))==1) && (Sum$(Electron_cutBased>=1 && Electron_pt>15 && abs(Electron_eta)<2.5 && ((abs(Electron_EtaSC)<=1.479 && abs(Electron_dz)< 0.10 && abs(Electron_dxy)< 0.05) || (abs(Electron_EtaSC)> 1.479 && abs(Electron_dz)< 0.20 && abs(Electron_dxy)< 0.10)))==1) && (Sum$(Muon_looseId==1 && Muon_pt>10 && abs(Muon_eta)<2.4 && Muon_pfRelIso04_all<0.2)==0) && (Sum$(Jet_pt>40 && abs(Jet_eta)<4.7 && Jet_jetId!=0 && Jet_puId>0 && Jet_dR_Ljet_Isoel>0.4)==2) && (Sum$(Jet_pt>40 && Jet_jetId!=0 && Jet_puId>0 && abs(Jet_eta)<2.4 && Jet_dR_Ljet_Isoel>0.4 && Jet_btagDeepFlavB>0.7476)==1)";
    int entirs=chain.GetEntries();
    cout<<"entirs = "<<entirs<<endl;
    entirs=chain.GetEntries("((TrigObj_filterBits & 1024) != 0 && TrigObj_id==11 && HLT_Ele32_WPTight_Gsf_L1DoubleEG==1) && "+cut);
    cout<<"entirs = "<<entirs<<endl;
    entirs=chain.GetEntries("(HLT_Ele35_WPTight_Gsf==1 || HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned ==1) && "+cut);
    cout<<"entirs = "<<entirs<<endl;
}
