#ifndef PhysicsTools_NanoAODTools_WeightCalculatorFromHistogram_h
#define PhysicsTools_NanoAODTools_WeightCalculatorFromHistogram_h

#include <iostream>
#include <iomanip>
#include <vector>
#include <TH1.h>

class WeightCalculatorFromHistogram {
 public:
  WeightCalculatorFromHistogram() {}
  // get the weight from the bin content of the passed histogram
  WeightCalculatorFromHistogram(TH1 *histogram, bool verbose=false) : histogram_(histogram), verbose_(verbose) {}
  // get the weight from the bin content of the ratio hist/targethist
  WeightCalculatorFromHistogram(TH1 *hist, TH1* targethist, bool norm=true, bool verbose=false);
  ~WeightCalculatorFromHistogram() {}
  
  float getWeight(float x, float y=0) const;
  float getWeightErr(float x, float y=0) const;
  
 private:
  std::vector<float> loadVals(TH1 *hist, bool norm=true);
  TH1* ratio(TH1 *hist, TH1* targethist);
  

  TH1* histogram_;
  bool verbose_;
  bool norm_;
};

WeightCalculatorFromHistogram::WeightCalculatorFromHistogram(TH1 *hist, TH1* targethist, bool norm, bool verbose) {
  norm_=norm;
  verbose_ = verbose;
  histogram_ = ratio(hist,targethist);
}

float WeightCalculatorFromHistogram::getWeight(float x, float y) const {
  if(histogram_==NULL) {
    std::cout << "ERROR! The weights input histogram is not loaded. Returning weight 0!" << std::endl;
    return 0.;
  }
  if(!histogram_->InheritsFrom("TH2")) {
    int bin = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(x)));
    return histogram_->GetBinContent(bin);
  } else {
    int binx = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(x)));
    int biny = std::max(1, std::min(histogram_->GetNbinsY(), histogram_->GetYaxis()->FindBin(y)));
    return histogram_->GetBinContent(binx,biny);
  }
}

float WeightCalculatorFromHistogram::getWeightErr(float x, float y) const {
  if(histogram_==NULL) {
    std::cout << "ERROR! The weights input histogram is not loaded. Returning weight error 1!" << std::endl;
    return 1.;
  }
  if(!histogram_->InheritsFrom("TH2")) {
    int bin = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(x)));
    return histogram_->GetBinError(bin);
  } else {
    int binx = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(x)));
    int biny = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(y)));
    return histogram_->GetBinError(binx,biny);
  }
}

std::vector<float> WeightCalculatorFromHistogram::loadVals(TH1 *hist, bool norm) {
  int nbins=hist->GetNcells();
  std::vector<float> vals;
  for(int i=0; i<nbins; ++i) vals.push_back(std::max(hist->GetBinContent(i),0.));
  if(verbose_) std::cout << "Normalization of " << hist->GetName() << ": " << hist->Integral() << std::endl;
  if(norm) {
    float scale = 1.0/hist->Integral();
    for(int i=0; i<nbins; ++i) vals[i] *= scale;
  }
  return vals;
}

TH1* WeightCalculatorFromHistogram::ratio(TH1 *hist, TH1* targethist) {
  TH1* ret=0;
  if(hist->GetNcells()!=targethist->GetNcells()) {
    std::cout << "ERROR! Numerator and denominator histograms have different number of bins!" << std::endl;
    return ret;
  }

  ret = (TH1*)hist->Clone("hweights");
  ret->SetDirectory(0);

  std::vector<float> vals = loadVals(hist,norm_);
  std::vector<float> targetvals = loadVals(targethist,norm_);
  int nbins = vals.size();
  if(verbose_) std::cout << "Weights for variable " << hist->GetName() << " with a number of bins equal to " << nbins << ":" << std::endl;
  for(int i=0; i<nbins; ++i) {
    float weight = targetvals[i] !=0 ? vals[i]/targetvals[i] : 1.;
    if(verbose_) std::cout << weight << " ";
    ret->SetBinContent(i,weight);
  }
  if(verbose_) std::cout << "." << std::endl;
  return ret;
}

#endif
