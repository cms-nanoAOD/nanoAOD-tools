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
    public:
        class FeatureGroup
        {
            protected:
                std::string _name;
                int64_t _size;
            public:
                FeatureGroup(const std::string& name, int64_t size):
                    _name(name),
                    _size(size)
                {
                }
                
                inline const std::string name() const
                {   
                    return _name;
                }
                
                virtual std::unique_ptr<tensorflow::Tensor> createTensor() const = 0; 
                
                virtual void fillTensor(std::unique_ptr<tensorflow::Tensor>& tensor, int jetIndex) const = 0;
                
                virtual ~FeatureGroup()
                {
                }
        };
        
        class ValueFeatureGroup:
            public FeatureGroup
        {
            protected:
                std::vector<TTreeReaderArray<float>*> _branches;
            public:
                ValueFeatureGroup(const std::string& name, int64_t size):
                    FeatureGroup(name,size)
                {
                }
                
                ValueFeatureGroup(const ValueFeatureGroup& group):
                    FeatureGroup(group._name,group._size),
                    _branches(group._branches)
                {
                }
                
                ValueFeatureGroup& operator=(const ValueFeatureGroup& group)
                {
                    _name = group._name;
                    _size = group._size;
                    _branches = group._branches;
                    return *this;
                }
                
                virtual std::unique_ptr<tensorflow::Tensor> createTensor() const
                {
                     return std::unique_ptr<tensorflow::Tensor>(
                        new tensorflow::Tensor(tensorflow::DT_FLOAT, {1,_size})
                    );
                }
                
                void addFeature(TTreeReaderArray<float>* branch)
                {
                    _branches.push_back(branch);
                }
                
                virtual void fillTensor(std::unique_ptr<tensorflow::Tensor>& tensor, int jetIndex) const
                {
                    if ((int64_t)_branches.size()!=_size)
                    {
                        throw std::runtime_error("Mismatch in group '"+_name+"' between provided number of branches ("+std::to_string(_branches.size())+") and configured ones ("+std::to_string(_size)+")");
                    }
                    auto features = tensor->tensor<float,2>();
                    for (int64_t i = 0; i < _size; ++i)
                    {
                        if ((int)_branches[i]->GetSize()<jetIndex)
                        {
                            throw std::runtime_error("Trying to access non-existing element ("+std::to_string(jetIndex)+") for group '"+_name+"'");
                        }
                        features(0,i) = _branches[i]->At(jetIndex);
                    }
                }
                
                virtual ~ValueFeatureGroup()
                {
                }
        };
        
        class ArrayFeatureGroup:
            public FeatureGroup
        {
            protected:
                int64_t _max;
                std::vector<TTreeReaderArray<float>*> _branches;
                TTreeReaderArray<float>* _lengthBranch;
            public:
                ArrayFeatureGroup(const std::string& name, int64_t size, int64_t max):
                    FeatureGroup(name,size),
                    _max(max)
                {
                }
                
                virtual std::unique_ptr<tensorflow::Tensor> createTensor() const
                {
                    return std::unique_ptr<tensorflow::Tensor>(
                        new tensorflow::Tensor(tensorflow::DT_FLOAT, {1,_size,_max})
                    );
                }
                
                virtual void fillTensor(std::unique_ptr<tensorflow::Tensor>& tensor, int jetIndex) const
                {
                    if ((int64_t)_branches.size()!=_size)
                    {
                        throw std::runtime_error("Mismatch in group '"+_name+"' between provided number of branches ("+std::to_string(_branches.size())+") and configured ones ("+std::to_string(_size)+")");
                    }
                }
                
                virtual ~ArrayFeatureGroup()
                {
                }
        };
        
        
    private:
        std::vector<FeatureGroup*> _featureGroups;
    public:
        TFEval()
        {
        }
        /*
        TFEval(const TFEval& tfEval):
            _featureGroups(tfEval._featureGroups)
        {
            std::cout<<"copy"<<std::endl;
        }
        */
        bool loadGraph(const char* filePath, const char* predictionNode)
        {
            return true;
        }
        
        void addFeatureGroup(FeatureGroup* featureGroup)
        {
            _featureGroups.push_back(featureGroup);
        }
        
        std::vector<float> evaluate(int jetIndex)
        {
            //std::cout<<"evaluate on jet "<<jetIndex<<std::endl;
            //std::cout<<"got "<<_featureGroups.size()<<" feature groups"<<std::endl;
            
            std::unordered_map<std::string,std::unique_ptr<tensorflow::Tensor>> inputs;
            for (auto featureGroup: _featureGroups)
            {
                auto tensor = featureGroup->createTensor();
                featureGroup->fillTensor(tensor,jetIndex);
                inputs[featureGroup->name()] = std::move(tensor);
            }
            
            std::vector<float> result(2,0);
            
            for (const auto& it: inputs)
            {
                //std::cout<<it.first<<std::endl;
                //std::cout<<it.second->tensor<float,2>()(0,1)<<std::endl;
                
                result[0]=it.second->tensor<float,2>()(0,1);
            }
           
            

 
            return result;
        }
        
        ~TFEval()
        {
        }
        
};
