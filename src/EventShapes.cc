#include "../interface/EventShapes.h"

#include <iostream>

EventShapes::EventShapes()
{
}

void EventShapes::addObject(double pt, double eta, double phi, double mass)
{
    TLorentzVector vec;
    vec.SetPtEtaPhiM(pt, eta, phi, mass);
    inputVectors_.emplace_back(std::move(vec));
}

double EventShapes::isotropy(const unsigned int& numberOfSteps) const
{
  const double deltaPhi=2*TMath::Pi()/numberOfSteps;
  double phi = 0, eIn =-1., eOut=-1.;
  for(unsigned int i=0; i<numberOfSteps; ++i){
    phi+=deltaPhi;
    double sum=0;
    for(unsigned int j=0; j<inputVectors_.size(); ++j){
      // sum over inner product of unit vectors and momenta
      sum+=TMath::Abs(TMath::Cos(phi)*inputVectors_[j].Px()+TMath::Sin(phi)*inputVectors_[j].Py());
    }
    if( eOut<0. || sum<eOut ) eOut=sum;
    if( eIn <0. || sum>eIn  ) eIn =sum;
  }
  return (eIn-eOut)/eIn;
}

/// the return value is 1 for spherical and 0 linear events in r-phi. This function needs the
/// number of steps to determine how fine the granularity of the algorithm in phi should be
double EventShapes::circularity(const unsigned int& numberOfSteps) const
{
  const double deltaPhi=2*TMath::Pi()/numberOfSteps;
  double circularity=-1, phi=0, area = 0;
  for(unsigned int i=0;i<inputVectors_.size();i++) {
    area+=TMath::Sqrt(inputVectors_[i].Px()*inputVectors_[i].Px()+inputVectors_[i].Py()*inputVectors_[i].Py());
  }
  for(unsigned int i=0; i<numberOfSteps; ++i){
    phi+=deltaPhi;
    double sum=0, tmp=0.;
    for(unsigned int j=0; j<inputVectors_.size(); ++j){
      sum+=TMath::Abs(TMath::Cos(phi)*inputVectors_[j].Px()+TMath::Sin(phi)*inputVectors_[j].Py());
    }
    tmp=TMath::Pi()/2*sum/area;
    if( circularity<0 || tmp<circularity ){
      circularity=tmp;
    }
  }
  return circularity;
}

/// helper function to fill the 3 dimensional momentum tensor from the inputVecotrs where needed
TMatrixDSym EventShapes::compMomentumTensor(double r) const
{
  TMatrixDSym momentumTensor(3);
  momentumTensor.Zero();

  if ( inputVectors_.size() < 2 ){
    return momentumTensor;
  }

  // fill momentumTensor from inputVectors
  double norm = 0.;
  for ( int i = 0; i < (int)inputVectors_.size(); ++i ){
    double p2 = inputVectors_[i].P()*inputVectors_[i].P();
    double pR = ( r == 2. ) ? p2 : TMath::Power(p2, 0.5*r);
    norm += pR;
    double pRminus2 = ( r == 2. ) ? 1. : TMath::Power(p2, 0.5*r - 1.);
    momentumTensor(0,0) += pRminus2*inputVectors_[i].Px()*inputVectors_[i].Px();
    momentumTensor(0,1) += pRminus2*inputVectors_[i].Px()*inputVectors_[i].Py();
    momentumTensor(0,2) += pRminus2*inputVectors_[i].Px()*inputVectors_[i].Pz();
    momentumTensor(1,0) += pRminus2*inputVectors_[i].Py()*inputVectors_[i].Px();
    momentumTensor(1,1) += pRminus2*inputVectors_[i].Py()*inputVectors_[i].Py();
    momentumTensor(1,2) += pRminus2*inputVectors_[i].Py()*inputVectors_[i].Pz();
    momentumTensor(2,0) += pRminus2*inputVectors_[i].Pz()*inputVectors_[i].Px();
    momentumTensor(2,1) += pRminus2*inputVectors_[i].Pz()*inputVectors_[i].Py();
    momentumTensor(2,2) += pRminus2*inputVectors_[i].Pz()*inputVectors_[i].Pz();
  }
  /*
  std::cout << "momentumTensor:" << std::endl;
  std::cout << momentumTensor(0,0) << " " << momentumTensor(0,1) << " " << momentumTensor(0,2) << std::endl;
  std::cout << momentumTensor(1,0) << " " << momentumTensor(1,1) << " " << momentumTensor(1,2) << std::endl;
  std::cout << momentumTensor(2,0) << " " << momentumTensor(2,1) << " " << momentumTensor(2,2) << std::endl;
  */
  // return momentumTensor normalized to determinant 1
  return (1./norm)*momentumTensor;
}

/// helper function to fill the 3 dimensional vector of eigen-values;
/// the largest (smallest) eigen-value is stored at index position 0 (2)
TVectorD EventShapes::compEigenValues(double r) const
{
  TVectorD eigenValues(3);
  TMatrixDSym myTensor = compMomentumTensor(r);
  if( myTensor.IsSymmetric() ){
    if( myTensor.NonZeros() != 0 ) myTensor.EigenVectors(eigenValues);
  }

  // CV: TMatrixDSym::EigenVectors returns eigen-values and eigen-vectors
  //     ordered by descending eigen-values, so no need to do any sorting here...
  /*
  std::cout << "eigenValues(0) = " << eigenValues(0) << ","
  	      << " eigenValues(1) = " << eigenValues(1) << ","
  	      << " eigenValues(2) = " << eigenValues(2) << std::endl;
  */
  return eigenValues;
}

/// 1.5*(q1+q2) where 0<=q1<=q2<=q3 are the eigenvalues of the momentum tensor sum{p_j[a]*p_j[b]}/sum{p_j**2} 
/// normalized to 1. Return values are 1 for spherical, 3/4 for plane and 0 for linear events
double EventShapes::sphericity(double r) const
{
  TVectorD eigenValues = compEigenValues(r);
  return 1.5*(eigenValues(1) + eigenValues(2));
}

/// 1.5*q1 where 0<=q1<=q2<=q3 are the eigenvalues of the momentum tensor sum{p_j[a]*p_j[b]}/sum{p_j**2} 
/// normalized to 1. Return values are 0.5 for spherical and 0 for plane and linear events
double EventShapes::aplanarity(double r) const
{
  TVectorD eigenValues = compEigenValues(r);
  return 1.5*eigenValues(2);
}

/// 3.*(q1*q2+q1*q3+q2*q3) where 0<=q1<=q2<=q3 are the eigenvalues of the momentum tensor sum{p_j[a]*p_j[b]}/sum{p_j**2} 
/// normalized to 1. Return value is between 0 and 1 
/// and measures the 3-jet structure of the event (C vanishes for a "perfect" 2-jet event)
double EventShapes::C(double r) const
{
  TVectorD eigenValues = compEigenValues(r);
  return 3.*(eigenValues(0)*eigenValues(1) + eigenValues(0)*eigenValues(2) + eigenValues(1)*eigenValues(2));
}

/// 27.*(q1*q2*q3) where 0<=q1<=q2<=q3 are the eigenvalues of the momemtum tensor sum{p_j[a]*p_j[b]}/sum{p_j**2} 
/// normalized to 1. Return value is between 0 and 1 
/// and measures the 4-jet structure of the event (D vanishes for a planar event)
double EventShapes::D(double r) const
{
  TVectorD eigenValues = compEigenValues(r);
  return 27.*eigenValues(0)*eigenValues(1)*eigenValues(2);
}

double EventShapes::alphaT() const
{
    if (inputVectors_.size()<2)
    {
        return -1;
    }
    // Momentum sums in transverse plane
    double sum_et = 0;
    double sum_px = 0;
    double sum_py = 0;
    
    for (const auto& vec: inputVectors_)
    {
        sum_et += vec.Et();
        sum_px += vec.Px();
        sum_py += vec.Py();
    }
    
    // Minimum Delta Et for two pseudo-jets
    double min_delta_sum_et = -1.;
    for (unsigned i=1; i < unsigned(1<<(inputVectors_.size()-1)); i++ ) //@@ iterate through different combinations
    { 
        //std::cout<<"alphaT "<<i<<"/"<<(1<<(inputVectors_.size()-1))<<", et="<<sum_et<<": ";
        double delta_sum_et = 0.;
        for ( unsigned j=0; j < inputVectors_.size(); j++ ) //@@ iterate through jets
        {
            //if ((1 - 2 * (int(i>>j)&1))>0) std::cout<<"+";
            //else std::cout<<"-";
            delta_sum_et += inputVectors_[j].Et() * ( 1 - 2 * (int(i>>j)&1)); 
        }
        //std::cout<<" = "<<delta_sum_et<<std::endl;
        
        
        if ( ( fabs(delta_sum_et) < min_delta_sum_et || min_delta_sum_et < 0. ) ) 
        {
            min_delta_sum_et = fabs(delta_sum_et);
        }
    }
    
    if ( min_delta_sum_et < 0. )
    {
        return 0.;
    }
    
    // Alpha_T
    double result = ( 0.5 * ( sum_et - min_delta_sum_et ) / std::sqrt( sum_et*sum_et - (sum_px*sum_px+sum_py*sum_py) ) );
    return result;
}
