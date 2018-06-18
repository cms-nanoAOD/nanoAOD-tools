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

#include "Python.h"

#include<iostream>


class TFEval
{
    public:

        
        class Accessor
        {
            public:
                virtual float value(int64_t index) const = 0; 
                virtual int64_t size() const = 0; 
                virtual ~Accessor()
                {
                }
        };
        
        class BranchAccessor:
            public Accessor
        {
            protected:
                TTreeReaderArray<float>* _branch;
            public:
                BranchAccessor(TTreeReaderArray<float>* branch):
                    _branch(branch)
                {
                }
                
                virtual int64_t size() const
                {
                    return _branch->GetSize();
                }
                
                virtual float value(int64_t index) const
                {
                    return _branch->At(index);
                }
                
                virtual ~BranchAccessor()
                {
                }
        };
        
        class PyAccessor:
            public Accessor
        {
            protected:
                PyObject* _lengthFct;
                PyObject* _valueFct;
            public:
                PyAccessor(PyObject* lengthFct, PyObject* valueFct):  
                    _lengthFct(lengthFct),
                    _valueFct(valueFct)
                {
                }
                virtual float value(int64_t index) const
                {
                    PyObject* args = PyTuple_Pack(1,PyInt_FromLong(index));
                    PyObject* result = PyObject_CallObject(_valueFct,args);
                    float value = PyFloat_AsDouble(result);
                    return value;
                }
                virtual int64_t size() const
                {
                    return 100;
                    /*
                    PyObject* args = PyTuple_Pack(0);
                    PyObject* result = PyObject_CallObject(_lengthFct,args);
                    int64_t value = PyInt_AsLong(result);
                    return value;
                    */
                }
                virtual ~PyAccessor()
                {
                }
        };
    
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
                
                virtual std::vector<int64_t> getShape() const = 0;
                
                virtual void addFeature(Accessor* accessor) = 0;//TTreeReaderArray<float>* branch) = 0;
                
                virtual tensorflow::Tensor createTensor() const = 0; 
                
                virtual void fillTensor(tensorflow::Tensor& tensor, int64_t jetIndex) const = 0;
                
                virtual ~FeatureGroup()
                {
                }
        };
        
        class ValueFeatureGroup:
            public FeatureGroup
        {
            protected:
                std::vector<Accessor*> _branches;
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
                
                virtual std::vector<int64_t> getShape() const
                {
                    return std::vector<int64_t>({1,_size});
                }
                
                virtual tensorflow::Tensor createTensor() const
                {
                    return tensorflow::Tensor(tensorflow::DT_FLOAT, {1,_size});
                }
                
                virtual void addFeature(Accessor* accessor) //TTreeReaderArray<float>* branch)
                {
                    _branches.push_back(accessor);
                }
                
                virtual void fillTensor(tensorflow::Tensor& tensor, int64_t jetIndex) const
                {
                    if ((int64_t)_branches.size()!=_size)
                    {
                        throw std::runtime_error("Mismatch in group '"+_name+"' between provided number of branches ("+std::to_string(_branches.size())+") and configured ones ("+std::to_string(_size)+")");
                    }
                    auto features = tensor.tensor<float,2>();
                    for (int64_t ifeature = 0; ifeature < _size; ++ifeature)
                    {
                        if ((int)_branches[ifeature]->size()<jetIndex)
                        {
                            throw std::runtime_error("Trying to access non-existing element ("+std::to_string(jetIndex)+") for group '"+_name+"'");
                        }
                        features(0,ifeature) = _branches[ifeature]->value(jetIndex);
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
                std::vector<Accessor*> _branches;
                Accessor* _lengthBranch;
            public:
                ArrayFeatureGroup(const std::string& name, int64_t size, int64_t max, Accessor* lengthBranch):
                    FeatureGroup(name,size),
                    _max(max),
                    _lengthBranch(lengthBranch)
                {
                }
                
                virtual void addFeature(Accessor* accessor)//TTreeReaderArray<float>* branch)
                {
                    _branches.push_back(accessor);
                }
                
                virtual std::vector<int64_t> getShape() const
                {
                    return std::vector<int64_t>({1,_max,_size});
                }
                
                virtual tensorflow::Tensor createTensor() const
                {
                    return tensorflow::Tensor(tensorflow::DT_FLOAT, {1,_max,_size});
                }
                
                virtual void fillTensor(tensorflow::Tensor& tensor, int64_t jetIndex) const
                {
                    if ((int64_t)_branches.size()!=_size)
                    {
                        throw std::runtime_error("Mismatch in group '"+_name+"' between provided number of branches ("+std::to_string(_branches.size())+") and configured ones ("+std::to_string(_size)+")");
                    }
                    auto features = tensor.tensor<float,3>();
                    int offset = 0;
                    for (int64_t i = 0; i < jetIndex; ++i)
                    {
                        offset+=_lengthBranch->value(i);
                    }
                    for (int64_t icandidate = 0; icandidate < std::min<int64_t>(_max,_lengthBranch->value(jetIndex)); ++icandidate)
                    {
                        for (int64_t ifeature = 0; ifeature < _size; ++ifeature)
                        {
                            if ((int)_branches[ifeature]->size()<(offset+icandidate))
                            {
                                throw std::runtime_error("Trying to access non-existing element ("+std::to_string(jetIndex)+") for group '"+_name+"'");
                            }
                            features(0,icandidate,ifeature) = _branches[ifeature]->value(offset+icandidate);
                        }
                    }
                    for (int64_t icandidate = _lengthBranch->value(jetIndex); icandidate < _max; ++icandidate)
                    {
                        for (int64_t ifeature = 0; ifeature < _size; ++ifeature)
                        {
                            features(0,icandidate,ifeature) = 0.;
                        }
                    }
                }
                
                virtual ~ArrayFeatureGroup()
                {
                }
        };
        
        
        class Result
        {
            private:
                std::unordered_map<std::string,std::vector<float>> _result;
            public:
                Result()
                {
                }
                
                static Result fill(
                    std::vector<std::string> names, 
                    std::vector<tensorflow::Tensor>& tensorList
                )
                {
                    Result result;
                    if (names.size()!=tensorList.size())
                    {
                        throw std::runtime_error("Number of names and values do not match");
                    }
                    
                    for (size_t i = 0; i < names.size(); ++i)
                    {
                        auto values = tensorList[i].flat<float>();
                        std::vector<float> data;//(values.size());
                        data.assign(values.data(),values.data()+values.size());
                        result._result[names[i]] = data;
                    }
                    return result;
                }
                
                
                std::vector<float> get(const char* s)
                {
                    auto it = _result.find(std::string(s));
                    if (it==_result.end())
                    {
                        return std::vector<float>();
                    }
                    return it->second;
                }
        };
        
        
    private:
        std::vector<FeatureGroup*> _featureGroups;
        std::unique_ptr<tensorflow::Session> _session;
        tensorflow::GraphDef _graphDef;
        std::vector<std::string> _outputNodeNames;
        bool _doReallocation;
        std::string _graphFilePath;
        
        std::vector<std::pair<std::string, tensorflow::Tensor>> _inputs;
        
    public:
        TFEval():
            _session(nullptr),
            _doReallocation(true),
            _graphFilePath("")
        {
        }
        /*
        TFEval(const TFEval& tfEval):
            _featureGroups(tfEval._featureGroups)
        {
            std::cout<<"copy"<<std::endl;
        }
        */
        
        void addOutputNodeName(const char* nodeName)
        {
            _outputNodeNames.push_back(nodeName);
        }
        
        bool loadGraph(const char* filePath)
        {
            tensorflow::Status status;
            
            // load it
            status = ReadBinaryProto(
                tensorflow::Env::Default(), 
                std::string(filePath), 
                &_graphDef
            );
            tensorflow::graph::SetDefaultDevice("/cpu:0", &_graphDef);
            
            // check for success
            if (!status.ok())
            {
                std::cerr<<"Error while loading graph def: "+status.ToString()<<std::endl;
                return false;
            }
            tensorflow::SessionOptions opts;
            opts.config.set_intra_op_parallelism_threads(1);
            opts.config.set_inter_op_parallelism_threads(1);
            tensorflow::Session* session;
            status = tensorflow::NewSession(opts, &session);
            if (!status.ok())
            {
                std::cerr<<"Error while creating a new session: "+status.ToString()<<std::endl;
                return false;
            }
            _session.reset(session);
            status = _session->Create(_graphDef);
            if (!status.ok())
            {
                std::cerr<<"Error while loading graph into session: "+status.ToString()<<std::endl;
                return false;
            }
            _graphFilePath = std::string(filePath);
            return true;
        }
        
        void addFeatureGroup(FeatureGroup* featureGroup)
        {
            _doReallocation = true;
            _featureGroups.push_back(featureGroup);
        }
        
        void allocateInputs()
        {
            if (_doReallocation)
            {
                _inputs.clear();
                for (auto featureGroup: _featureGroups)
                {
                    auto tensor = featureGroup->createTensor();
                    _inputs.emplace_back(featureGroup->name(),tensor);
                    
                    //check input shapes
                    bool foundNode = false;
                    for (int inode = 0; inode < _graphDef.node_size(); inode++)
                    {
                        if (_graphDef.node(inode).name()==featureGroup->name())
                        {
                            foundNode = true;
                            auto tensor_shape = _graphDef.node(inode).attr().at("shape").shape();
                            auto group_shape = featureGroup->getShape();
                            //check rank
                            if (tensor_shape.dim_size()!=(int64_t)group_shape.size())
                            {
                                throw std::runtime_error("Mismatching input rank (config: "+std::to_string(group_shape.size())+"; pb: "+std::to_string(tensor_shape.dim_size())+") for feature group '"+featureGroup->name()+"'");
                            }
                            //check shape - ignore batch dim
                            for (size_t idim = 1; idim < group_shape.size(); ++idim)
                            {
                                if ((int64_t)tensor_shape.dim(idim).size()!=group_shape[idim])
                                {
                                    throw std::runtime_error("Mismatching input shapes in dimension '"+std::to_string(idim+1)+"' (config: "+std::to_string(group_shape[idim])+"; pb: "+std::to_string(tensor_shape.dim(idim).size())+") for feature group '"+featureGroup->name()+"'");
                                }
                            }
                            break;
                        }
                    }
                    if (not foundNode)
                    {
                        throw std::runtime_error("Cannot find input node '"+featureGroup->name()+"' in pb file '"+_graphFilePath+"'");
                    }
                }
                _doReallocation = false;
            }
        }
        
        void fillInputs(int64_t jetIndex)
        {
            if (_featureGroups.size()!=_inputs.size())
            {
                throw std::runtime_error("Logic error occured: input tensors should have been reallocated");
            }
            for (size_t i = 0; i < _inputs.size(); ++i)
            {
                _featureGroups[i]->fillTensor(_inputs[i].second,jetIndex);
            }
        }
        
        Result evaluate(int64_t jetIndex)
        {
            allocateInputs();
            fillInputs(jetIndex);
            
            std::vector<tensorflow::Tensor> outputs;
            
            if (not _session)
            {
                throw std::runtime_error("No graph/session loaded");
            }
            
            tensorflow::Status status = _session->Run(_inputs,_outputNodeNames,{},&outputs);
            if (!status.ok())
            {
                throw std::runtime_error("Error while loading graph into session: "+status.ToString());
            }

            return Result::fill(_outputNodeNames,outputs);
        }
        
        ~TFEval()
        {
        }
};
