#include "PhysicsTools/NanoAODTools/interface/CollectionMerger.h"
#include <TTree.h>
#include <TTreeReaderArray.h>

template<typename T1, typename T2>
void CollectionMerger::CopyVar<T1,T2>::branch(TTree *tree, unsigned int maxLength) 
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
CollectionMerger::makeBranches(TTree *tree, unsigned int maxEntries) {
    maxEntries_ = maxEntries;
    tree->Branch(("n"+outName_).c_str(), &nOut_, ("n"+outName_+"/I").c_str());

    for (auto & c : copyFloats_) c.branch(tree, maxEntries);
    for (auto & c : copyInts_) c.branch(tree, maxEntries);
    for (auto & c : copyUChars_) c.branch(tree, maxEntries);
    for (auto & c : copyBools_) c.branch(tree, maxEntries);
    hasBranched_ = true;
}

void CollectionMerger::copyFloat(const std::string &varname, TTreeReaderArray<Float_t> * src1, TTreeReaderArray<Float_t> * src2) 
{ 
  _copyVar(varname, src1, src2, copyFloats_);
}

void CollectionMerger::copyInt(const std::string &varname, TTreeReaderArray<Int_t> * src1, TTreeReaderArray<Int_t> * src2) 
{
    _copyVar(varname, src1, src2, copyInts_);
}

void CollectionMerger::copyUChar(const std::string &varname, TTreeReaderArray<UChar_t> * src1, TTreeReaderArray<UChar_t> * src2) 
{
    _copyVar(varname, src1, src2, copyUChars_);
}
void CollectionMerger::copyBool(const std::string &varname, TTreeReaderArray<Bool_t> * src1, TTreeReaderArray<Bool_t> * src2) 
{
    _copyVar(varname, src1, src2, copyBools_);
}

void CollectionMerger::srcCount(TTreeReaderValue<unsigned int> * src1, TTreeReaderValue<unsigned int> * src2)
{
  srcCount1_ = src1;
  srcCount2_ = src2;
}

template<typename CopyVarVectorT, typename SrcT>
void CollectionMerger::_copyVar(const std::string &varname, SrcT * src1, SrcT * src2, CopyVarVectorT &copyVars) 
{ 
    bool found = false;
    for (auto &c : copyVars) {
        if (c.varName() == varname) {
            c.setSrc(src1,src2);
            found = true;
            break;
        }
    }
    if (!found) {
        _checkNoBranchesYet();
        copyVars.emplace_back(outName_, varname);
    }
}

void CollectionMerger::_checkNoBranchesYet() 
{
    if (hasBranched_) throw std::logic_error("Error, can't add a new variable after having set the output tree\n");
}


