#ifndef PhysicsTools_NanoAODTools_EventShapes_h
#define PhysicsTools_NanoAODTools_EventShapes_h

#include "TLorentzVector.h"
#include "TMatrixT.h"
#include "TMatrixDEigen.h"
#include "TMatrixTSym.h"
#include "TVectorD.h"

#include <numeric>

class EventShapes
{
    private:
        std::vector<TLorentzVector> inputVectors_;
        TMatrixDSym compMomentumTensor(double = 2.) const;
        TVectorD compEigenValues(double = 2.) const;
        
    public:
        EventShapes();
        void addObject(double pt, double eta, double phi, double mass);
        
        /// the return value is 1 for spherical events and 0 for events linear in r-phi. This function 
        /// needs the number of steps to determine how fine the granularity of the algorithm in phi 
        /// should be
        double isotropy(const unsigned int& numberOfSteps = 1000) const;

        /// the return value is 1 for spherical and 0 linear events in r-phi. This function needs the 
        /// number of steps to determine how fine the granularity of the algorithm in phi should be
        double circularity(const unsigned int& numberOfSteps = 1000) const;

        /// 1.5*(q1+q2) where 0<=q1<=q2<=q3 are the eigenvalues of the momemtum tensor 
        /// sum{p_j[a]*p_j[b]}/sum{p_j**2} normalized to 1. Return values are 1 for spherical, 3/4 for 
        /// plane and 0 for linear events
        double sphericity(double = 2.)  const;
        
        /// 1.5*q1 where 0<=q1<=q2<=q3 are the eigenvalues of the momemtum tensor 
        /// sum{p_j[a]*p_j[b]}/sum{p_j**2} normalized to 1. Return values are 0.5 for spherical and 0 
        /// for plane and linear events
        double aplanarity(double = 2.)  const;
        
        /// 3.*(q1*q2+q1*q3+q2*q3) where 0<=q1<=q2<=q3 are the eigenvalues of the momemtum tensor 
        /// sum{p_j[a]*p_j[b]}/sum{p_j**2} normalized to 1. Return value is between 0 and 1 
        /// and measures the 3-jet structure of the event (C vanishes for a "perfect" 2-jet event)
        double C(double = 2.) const;
        
        /// 27.*(q1*q2*q3) where 0<=q1<=q2<=q3 are the eigenvalues of the momemtum tensor 
        /// sum{p_j[a]*p_j[b]}/sum{p_j**2} normalized to 1. Return value is between 0 and 1 
        /// and measures the 4-jet structure of the event (D vanishes for a planar event)
        double D(double = 2.) const;
        
        double alphaT() const;
        

};

#endif
