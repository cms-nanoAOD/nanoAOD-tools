#//dasgoclient --query="file dataset=/ST_t-channel_top_4f_InclusiveDecays_mtop1785*/RunIIFall17NanoAOD*mc2017*/NANOAODSIM"//to get the files of a dataset
#include<iostream>
using namespace std;

#include"TCanvas.h"
#include "TH1D.h"
#include "TGaxis.h"
#include "TH2D.h"

void PU_distribution_MC(){


     TFile *fnew = new TFile("mcPileupUL2016preVFP_new_v2.root","RECREATE");
     string fileName;
     ifstream infile;
     infile.open("filename_ttbar_UL2016preVFP.txt");
     TH1F *h = new TH1F("pu_mc","pu_mc",99,0,99);h->Sumw2();
     //TH1F* h; 
     ULong64_t total_file=150;
     /*while(!infile.eof()){
           getline(infile,fileName);
           total_file++;
	   cout<<total_file<<endl;
     }*/
     ULong64_t count=0;

     while(!infile.eof()){
          getline(infile,fileName);
	  TString file = "root://cms-xrd-global.cern.ch//"+fileName;
	  cout<<count<<" : "<<total_file<<"  "<<file<<endl;
	  if(file=="root://cms-xrd-global.cern.ch//") continue;
          TFile *f = TFile::Open(file);
          TTree *tree;
          tree = (TTree*)gDirectory->Get("Events");
	  TH1F *temp = new TH1F("temp","temp",99,0,99);temp->Sumw2(); temp->Reset();
   	  tree->Project("temp","Pileup_nTrueInt");
	  h->Add(temp);
	  //f->Close();
	  delete temp; delete tree; delete f;
	  count++;
	  if(count%100==0) std::cout<<"# of files read = "<<count<<std::endl;
     }

     //h->Scale(1/h->Integral());
     fnew->cd();
     h->Write();
     fnew->Close();
  	
}
