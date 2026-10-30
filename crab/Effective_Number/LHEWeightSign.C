//dasgoclient --query="file dataset=/ST_t-channel_top_4f_InclusiveDecays_mtop1785*/RunIIFall17NanoAOD*mc2017*/NANOAODSIM"//to get the files of a dataset
#include<iostream>
using namespace std;

#include"TCanvas.h"
#include "TH1D.h"
#include "TGaxis.h"
#include "TH2D.h"
#include "cmath"
void LHEWeightSign(){


     string fileName;
     ifstream infile;
     infile.open("filename.txt");
     TH1F *h = new TH1F("h","h",2,-5,5);h->Sumw2();
     //TH1F* h; 
     ULong64_t count=0;
     while(!infile.eof()){
          getline(infile,fileName);
	  TString file = "root://cms-xrd-global.cern.ch//"+fileName;
	  //cout<<file<<endl;
	  if(file=="root://cms-xrd-global.cern.ch//") continue;
          TFile *f = TFile::Open(file);
          TTree *tree;
          tree = (TTree*)gDirectory->Get("Events");
	  TH1F *temp = new TH1F("temp","temp",2,-5,5);temp->Sumw2(); temp->Reset();
   	  tree->Project("temp","LHEWeight_originalXWGTUP/abs(LHEWeight_originalXWGTUP)");
	  h->Add(temp);
	  delete temp; delete tree; delete f;
	  count++;
	  if(count%50==0) std::cout<<"# of files read = "<<count<<std::endl;
     }
     UInt_t EffectiveNo = h->GetBinContent(2)-h->GetBinContent(1);
     cout<<"Effective No. Events = "<<round(EffectiveNo/10000)/100<<endl;
     cout<<"Effective No. Events = "<<EffectiveNo<<endl;
     cout<<"totle files Evaluated = "<<count<<endl;
     delete h; 
	
}
