#ifndef PhysicsTools_NanoAODTools_CollectionSkimmer_h
#define PhysicsTools_NanoAODTools_CollectionSkimmer_h
/** CollectionSkimmer
    C++ utility to quickly copy data from one collection to another skimming the list of elements 
*/

#include <memory>
#include <string>
#include <vector>
#include <cassert>
#include <algorithm>
class TTree;
#include <Rtypes.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>

class CollectionSkimmer {
    public:
        template<typename T1, typename T2> class CopyVar {
            public:
                CopyVar(const std::string &collName, const std::string &varName, TTreeReaderArray<T1> *src=0) :
                      collName_(collName), varName_(varName), in_(src) {}
                const std::string & collName() { return collName_; }
                const std::string & varName() { return varName_; }
                void setSrc(TTreeReaderArray<T1> *src) { in_ = src; }
                void copy(int ifrom, int ito) { out_[ito] = (*in_)[ifrom]; } 
                void branch(TTree *tree, unsigned int maxEntries) ; 
            private:
                std::string collName_, varName_;
                TTreeReaderArray<T1> *in_;
                std::unique_ptr<T2[]> out_;
        };
        typedef CopyVar<float,Float_t> CopyFloat;
        typedef CopyVar<int,Int_t> CopyInt;
	typedef CopyVar<unsigned char, UChar_t> CopyUChar;
	typedef CopyVar<bool, Bool_t> CopyBool;

        CollectionSkimmer(const std::string &outName, const std::string &collName, bool saveSelectedIndices = false, bool saveTagForAll = false) : outName_(outName), collName_(collName), hasBranched_(false), srcCount_(NULL), saveSelectedIndices_(saveSelectedIndices), saveTagForAll_(saveTagForAll), maxEntries_(0) {}
        CollectionSkimmer(const CollectionSkimmer &other) = delete;
        CollectionSkimmer &operator=(const CollectionSkimmer &other) = delete;

        /// to be called first to register the branches, and possibly re-called if the treeReaderArrays are remade
        void copyFloat(const std::string &varname, TTreeReaderArray<Float_t> * src = nullptr) ; 
        void copyInt(const std::string &varname, TTreeReaderArray<Int_t> * src = nullptr) ;
	void copyUChar(const std::string &varname, TTreeReaderArray<UChar_t> * src = nullptr) ;
	void copyBool(const std::string &varname, TTreeReaderArray<Bool_t> * src = nullptr) ;
	void srcCount(TTreeReaderValue<unsigned int> * src);

        /// to be called once on the tree, after a first call to copyFloat and copyInt
        void makeBranches(TTree *tree, unsigned int maxEntries, bool padSelectedIndicesCollection = false, int padSelectedIndicesCollectionWith = -1) ;

        //---- to be called on each event for copying ----
        /// clear the output collection
        void clear() {
	  nOut_ = 0;
	  nIn_ = 0;
	  if (iOut_.get()) std::fill_n(iOut_.get(),maxEntries_,padSelectedIndicesCollectionWith_);
	  if (saveTagForAll_){
	    assert (srcCount_); // pointer to srcCount TTreeReaderValue must be set
	    nIn_ = **srcCount_;
	    assert (uint(nIn_)<=maxEntries_);
	    if (iTagOut_.get()) std::fill_n(iTagOut_.get(),nIn_,0);
	  }
	}

        /// push back entry iSrc from input collection to output collection
        void push_back(unsigned int iSrc) {
	  assert (iSrc<maxEntries_);
	  assert (uint(nOut_)<maxEntries_);
	  for (auto & c : copyFloats_) c.copy(iSrc, nOut_);
	  for (auto & c : copyInts_) c.copy(iSrc, nOut_);
	  for (auto & c : copyUChars_) c.copy(iSrc, nOut_);
	  for (auto & c : copyBools_) c.copy(iSrc, nOut_);
	  if (saveSelectedIndices_) iOut_[nOut_] = iSrc;
	  if (saveTagForAll_) iTagOut_[iSrc] = 1;
	  nOut_++;
        }
        /// push back all entries in iSrcs
        void push_back(const std::vector<int> &iSrcs) {
            for (int i : iSrcs) push_back(i);
        }

        /// resize output collection to a fixed size
        void resize(unsigned int size) { nOut_ = size; }

        /// copy from iSrc into iTo (must be iTo < size())
        void copy(unsigned int iSrc, unsigned int iTo) {
            assert(unsigned(nOut_) > iTo);
            if (saveSelectedIndices_) iOut_[iTo] = iSrc;
	    iTagOut_[iSrc] = true; // careful if using with saveTagForAll_, do not overwrite with copy
            for (auto & c : copyFloats_) c.copy(iSrc, iTo);
            for (auto & c : copyInts_) c.copy(iSrc, iTo);
	    for (auto & c : copyUChars_) c.copy(iSrc, iTo);
	    for (auto & c : copyBools_) c.copy(iSrc, iTo);
        }

        /// number of selected output objects
        unsigned int size() const { return nOut_; }

    private:
        std::string outName_;
        std::string collName_;
        Int_t nOut_;
        bool hasBranched_;
        std::unique_ptr<int[]> iOut_;
	TTreeReaderValue<unsigned int> *srcCount_;
        std::vector<CopyFloat> copyFloats_;
        std::vector<CopyInt> copyInts_;
	std::vector<CopyUChar> copyUChars_;
	std::vector<CopyBool> copyBools_;
	bool saveSelectedIndices_;
	bool padSelectedIndicesCollection_;
	int padSelectedIndicesCollectionWith_;
	bool saveTagForAll_;
	unsigned int nIn_;
        std::unique_ptr<int[]> iTagOut_;
	uint maxEntries_;

        template<typename CopyVarVectorT, typename SrcT>
        void _copyVar(const std::string &varname, SrcT * src, CopyVarVectorT &copyVars) ; 
        void _checkNoBranchesYet() ;
};

#endif
