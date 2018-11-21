#ifndef PhysicsTools_NanoAODTools_LHAInterface_h
#define PhysicsTools_NanoAODTools_LHAInterface_h

#include "LHAPDF/LHAPDF.h"

#include <string>
#include <memory>
#include <iostream>

class LHAInterface
{
    protected:
        int _members;
        double _qmax;
        bool _qmaxWarning;
	public:
	    LHAInterface():
	        _members(-1),
	        _qmax(0),
	        _qmaxWarning(false)
	    {
	    }
	    
	    void load(const char* pdfname, int members)
	    {
	        _members = members;
	        LHAPDF::setVerbosity(LHAPDF::SILENT);
	        //const LHAPDF::PDFSet set("NNPDF30_nlo_as_0118_nf_4.LHgrid");
	        for (int i = 0; i < members; ++i)
	        {
	            LHAPDF::initPDFSet(i, pdfname , i);
            }
	        //LHAPDF::setPDFPath("/home/whalley/local/share/lhapdf/PDFsets");
	        //LHAPDF::initPDFSetByName("NNPDF30_nlo_as_0118_nf_4.LHgrid");
            
            //const LHAPDF::PDF* pdf = LHAPDF::mkPDF("NNPDF30_nlo_as_0118_nf_4", 0);
            //x,Q,flavor
            LHAPDF::initPDF(0);
            _qmax = std::sqrt(LHAPDF::getQ2max(0))*0.9999;
            //std::cout<<"Q2 max: "<<_q2max<<std::endl;
            /*
            std::cout<<"test eval: "<<std::endl;
            for (int i = 0; i < members; ++i)
            {
                LHAPDF::usePDFMember(i);
                std::cout<<LHAPDF::xfx(0.01, 1000, 0)<<", ";
            }
            std::cout<<std::endl;
            */
	    }
	    
	    std::vector<double> getEigenvalues(double x,double q,int flavor)
	    {
	        if (not _qmaxWarning and q>_qmax)
	        {
	            std::cerr<<"Warning in evaluating PDF set: Q="<<q<<" outside validity of "<<_qmax<<std::endl;
	            _qmaxWarning = true;
	        }
	        std::vector<double> values(_members,0);
	        for (int i = 0; i < _members; ++i)
            {
                LHAPDF::usePDFMember(i);
                values[i] = std::max(1e-16,LHAPDF::xfx(x, std::min(_qmax,q), flavor));
            }
            return values;
	    }
	    
	    double evalPDF(double x, double q, int flavor,int member=0)
	    {
	        if (not _qmaxWarning and q>_qmax)
	        {
	            std::cerr<<"Warning in evaluating PDF set: Q="<<q<<" outside validity of "<<_qmax<<std::endl;
	            _qmaxWarning = true;
	        }
            LHAPDF::usePDFMember(member);
            return std::max(1e-16,LHAPDF::xfx(x, std::min(_qmax,q), flavor));
	    }
	    
	    double evalAlphas(double q, int member=0)
	    {
	        if (not _qmaxWarning and q>_qmax)
	        {
	            std::cerr<<"Warning in evaluating PDF set: Q="<<q<<" outside validity of "<<_qmax<<std::endl;
	            _qmaxWarning = true;
	        }
            return std::max(1e-16,LHAPDF::alphasPDF(std::min(_qmax,q)));
	    }
};

#endif
