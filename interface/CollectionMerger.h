#ifndef PhysicsTools_NanoAODTools_CollectionMerger_h
#define PhysicsTools_NanoAODTools_CollectionMerger_h
/** CollectionMerger
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

class CollectionMerger {
    public:
        template<typename T1, typename T2> class CopyVar {
            public:
	CopyVar(const std::string &collName, const std::string &varName, TTreeReaderArray<T1> *src1=0, TTreeReaderArray<T1> *src2=0) :
                      collName_(collName), varName_(varName), in1_(src1), in2_(src2){}
                const std::string & collName() { return collName_; }
                const std::string & varName() { return varName_; }
                void setSrc(TTreeReaderArray<T1> *src1,TTreeReaderArray<T1> *src2) { in1_ = src1; in2_ = src2; }
                void copy(int ifrom, int ito, unsigned int col) { 
		  float defaultValue = 0;
		  if (col == 0){
		    if (!in1_) out_[ito] = defaultValue;
		    else       out_[ito] = (*in1_)[ifrom]; 
		  }
		  else if (col == 1){
		    if (!in2_) out_[ito] = defaultValue;
		    else       out_[ito] = (*in2_)[ifrom]; 
		  }
		  else
		    throw std::logic_error("Error, trying to add more than two collections");
		} 
                void branch(TTree *tree, unsigned int maxEntries) ; 
            private:
                std::string collName_, varName_;
                TTreeReaderArray<T1> *in1_;
		TTreeReaderArray<T1> *in2_;
                std::unique_ptr<T2[]> out_;
        };
        typedef CopyVar<float,Float_t> CopyFloat;
        typedef CopyVar<int,Int_t> CopyInt;
	typedef CopyVar<unsigned char, UChar_t> CopyUChar;
	typedef CopyVar<bool, Bool_t> CopyBool;

 CollectionMerger(const std::string &outName, const std::string &collName, const std::string &collName2) : outName_(outName), collName_(collName), collName2_(collName2), hasBranched_(false), srcCount1_(NULL),srcCount2_(NULL), maxEntries_(0) {}
        CollectionMerger(const CollectionMerger &other) = delete;
        CollectionMerger &operator=(const CollectionMerger &other) = delete;

        /// to be called first to register the branches, and possibly re-called if the treeReaderArrays are remade
        void copyFloat(const std::string &varname, TTreeReaderArray<Float_t> * src1 = nullptr, TTreeReaderArray<Float_t> * src2 = nullptr) ; 
        void copyInt(const std::string &varname  , TTreeReaderArray<Int_t>   * src1 = nullptr, TTreeReaderArray<Int_t>   * src2 = nullptr) ;
	void copyUChar(const std::string &varname, TTreeReaderArray<UChar_t> * src1 = nullptr, TTreeReaderArray<UChar_t> * src2 = nullptr) ;
	void copyBool(const std::string &varname , TTreeReaderArray<Bool_t>  * src1 = nullptr, TTreeReaderArray<Bool_t>  * src2 = nullptr) ;
	void srcCount(TTreeReaderValue<unsigned int> * src1, TTreeReaderValue<unsigned int> * src2);

        /// to be called once on the tree, after a first call to copyFloat and copyInt
        void makeBranches(TTree *tree, unsigned int maxEntries) ;

        //---- to be called on each event for copying ----
        /// clear the output collection
        void clear() {
	  nOut_ = 0;
	  if (iOut_.get()) std::fill_n(iOut_.get(),maxEntries_,padSelectedIndicesCollectionWith_);

	}

        /// push back entry iSrc from input collection to output collection
        void push_back(unsigned int iSrc, unsigned int col) {
	  assert (iSrc<maxEntries_);
	  assert (uint(nOut_)<maxEntries_);
	  for (auto & c : copyFloats_) c.copy(iSrc, nOut_, col);
	  for (auto & c : copyInts_)   c.copy(iSrc, nOut_, col);
	  for (auto & c : copyUChars_) c.copy(iSrc, nOut_, col);
	  for (auto & c : copyBools_)  c.copy(iSrc, nOut_, col);
	  nOut_++;
        }
        /// push back all entries in iSrcs
        void push_back(const std::vector<std::pair<int,int>> &iSrcs) {
	  for (auto& i : iSrcs) push_back(i.first,i.second);
        }

        /// resize output collection to a fixed size
        void resize(unsigned int size) { nOut_ = size; }

        /// copy from iSrc into iTo (must be iTo < size())
        void copy(unsigned int iSrc, unsigned int iTo, unsigned int col) {
            assert(unsigned(nOut_) > iTo);
	    iTagOut_[iSrc] = true; // careful if using with saveTagForAll_, do not overwrite with copy
            for (auto & c : copyFloats_) c.copy(iSrc, iTo, col);
            for (auto & c : copyInts_)   c.copy(iSrc, iTo, col);
	    for (auto & c : copyUChars_) c.copy(iSrc, iTo, col);
	    for (auto & c : copyBools_)  c.copy(iSrc, iTo, col);
        }

        /// number of selected output objects
        unsigned int size() const { return nOut_; }

    private:
        std::string outName_;
        std::string collName_;
        std::string collName2_;
        Int_t nOut_;
        bool hasBranched_;
        std::unique_ptr<int[]> iOut_;
	TTreeReaderValue<unsigned int> *srcCount1_;
	TTreeReaderValue<unsigned int> *srcCount2_;
        std::vector<CopyFloat> copyFloats_;
        std::vector<CopyInt> copyInts_;
	std::vector<CopyUChar> copyUChars_;
	std::vector<CopyBool> copyBools_;
	bool padSelectedIndicesCollection_;
	int padSelectedIndicesCollectionWith_;
	unsigned int nIn_;
        std::unique_ptr<int[]> iTagOut_;
	uint maxEntries_;

        template<typename CopyVarVectorT, typename SrcT>
	void _copyVar(const std::string &varname, SrcT * src1, SrcT * src2, CopyVarVectorT &copyVars) ; 
        void _checkNoBranchesYet() ;
};

#endif
