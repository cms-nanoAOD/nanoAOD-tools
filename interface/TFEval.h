#include "tensorflow/core/framework/graph.pb.h"
#include "tensorflow/core/framework/tensor.h"

#include "tensorflow/core/public/session.h"
#include "tensorflow/core/framework/tensor.h"
#include "tensorflow/core/lib/io/path.h"

#include "tensorflow/core/graph/default_device.h"

#include <exception>

#include "TTree.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"

class TFEval
{
    private:
        TTree* tree_;
        
        static constexpr size_t NJETS = 25;
        
        unsigned int nglobal;
        float global_pt[NJETS];
        
        TTreeReaderArray<float>* branch_;
        
    public:
        TFEval():
            tree_(nullptr),
            branch_(nullptr)
        {
        }
        
        bool loadGraph(const char* name)
        {
            return true;
        }
        
        void addBranch(TTreeReaderArray<float> *branch)
        {
            branch_ = branch;
        }
        
        bool loadTree(TTree* tree)
        {
            tree_ = tree;
            std::cout<<tree_<<std::endl;
            tree_->SetBranchAddress("nglobal",&nglobal);
            tree_->SetBranchAddress("global_pt",&global_pt);
            return true;
        }
        
        std::vector<float> evaluate(unsigned int jet)
        {
            std::vector<float> result(2,0);
   
                
                //std::cout<<global_pt[jet]<<std::endl;
                //result[0] = global_pt[jet];
            if (branch_ and branch_->GetSize()>0)
            {
                result[0] = branch_->At(0);
            }
         
            return result;
        }
        
};
