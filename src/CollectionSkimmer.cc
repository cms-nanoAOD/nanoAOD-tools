#include "PhysicsTools/NanoAODTools/interface/CollectionSkimmer.h"
#include <TTree.h>
#include <TTreeReaderArray.h>

template<typename T1, typename T2>
void CollectionSkimmer::CopyVar<T1,T2>::branch(TTree *tree, unsigned int maxLength) 
{
    out_.reset(new T2[maxLength]);
    std::string typecode = "?";
    if      (typeid(T2) == typeid(int))   typecode = "I";
    else if (typeid(T2) == typeid(float)) typecode = "F";
    else if (typeid(T2) == typeid(unsigned char)) typecode = "b";
    else if (typeid(T2) == typeid(bool)) typecode = "O";
    else throw std::logic_error("Unsupported type");
    tree->Branch( (collName_ + "_" + varName_).c_str(),
                  out_.get(),
                  (collName_ + "_" + varName_ + "[n" + collName_ + "]/" + typecode).c_str() );
}

void 
CollectionSkimmer::makeBranches(TTree *tree, unsigned int maxEntries, bool padSelectedIndicesCollection, int padSelectedIndicesCollectionWith) {
    maxEntries_ = maxEntries;
    padSelectedIndicesCollection_ = padSelectedIndicesCollection;
    padSelectedIndicesCollectionWith_ = padSelectedIndicesCollectionWith;
    if (saveTagForAll_) {
      iTagOut_.reset(new int[maxEntries]);
      tree->Branch(("n"+collName_).c_str(), &nIn_, ("n"+collName_+"/I").c_str());
      tree->Branch((collName_+"_is"+outName_).c_str(), iTagOut_.get(), (collName_+"_is"+outName_+"[n"+collName_+"]/I").c_str());
    }
    tree->Branch(("n"+outName_).c_str(), &nOut_, ("n"+outName_+"/I").c_str());
    if (saveSelectedIndices_) {
      iOut_.reset(new int[maxEntries]);
      if (padSelectedIndicesCollection_) tree->Branch(("i"+outName_).c_str(), iOut_.get(), ("i"+outName_+"[" + std::to_string(maxEntries) + "]/I").c_str());
      else tree->Branch(("i"+outName_).c_str(), iOut_.get(), ("i"+outName_+"[n" + outName_ + "]/I").c_str());
    }
    for (auto & c : copyFloats_) c.branch(tree, maxEntries);
    for (auto & c : copyInts_) c.branch(tree, maxEntries);
    for (auto & c : copyUChars_) c.branch(tree, maxEntries);
    for (auto & c : copyBools_) c.branch(tree, maxEntries);
    hasBranched_ = true;
}

void CollectionSkimmer::copyFloat(const std::string &varname, TTreeReaderArray<Float_t> * src) 
{ 
    _copyVar(varname, src, copyFloats_);
}

void CollectionSkimmer::copyInt(const std::string &varname, TTreeReaderArray<Int_t> * src) 
{
    _copyVar(varname, src, copyInts_);
}

void CollectionSkimmer::copyUChar(const std::string &varname, TTreeReaderArray<UChar_t> * src) 
{
    _copyVar(varname, src, copyUChars_);
}
void CollectionSkimmer::copyBool(const std::string &varname, TTreeReaderArray<Bool_t> * src) 
{
    _copyVar(varname, src, copyBools_);
}

void CollectionSkimmer::srcCount(TTreeReaderValue<unsigned int> * src)
{
  srcCount_ = src;
}

template<typename CopyVarVectorT, typename SrcT>
void CollectionSkimmer::_copyVar(const std::string &varname, SrcT * src, CopyVarVectorT &copyVars) 
{ 
    bool found = false;
    for (auto &c : copyVars) {
        if (c.varName() == varname) {
            c.setSrc(src);
            found = true;
            break;
        }
    }
    if (!found) {
        _checkNoBranchesYet();
        copyVars.emplace_back(outName_, varname);
    }
}

void CollectionSkimmer::_checkNoBranchesYet() 
{
    if (hasBranched_) throw std::logic_error("Error, can't add a new variable after having set the output tree\n");
}


