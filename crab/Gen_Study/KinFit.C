#include "PhysicsTools/KinFitter/interface/TFitConstraintM.h"
#include "PhysicsTools/KinFitter/interface/TFitConstraintEp.h"
#include "PhysicsTools/KinFitter/interface/TFitParticleEtEtaPhi.h"
#include "PhysicsTools/KinFitter/interface/TFitParticleEScaledMomDev.h"
#include "PhysicsTools/KinFitter/interface/TFitParticleMCMomDev.h"
#include "PhysicsTools/KinFitter/interface/TKinFitter.h"

#include <iostream>

double Jet_ErrEta(float Et, float Eta) {
  double InvPerr2, a, b, c;
  if(fabs(Eta) < 1.4){
    a = 1.215;
    b = 0.037;
    c = 7.941 * 0.0001;
  }
  else{
    a = 1.773;
    b = 0.034;
    c = 3.56 * 0.0001;
  }
  InvPerr2 = a/(Et * Et) + b/Et + c;
  return InvPerr2;
}

double Jet_ErrEt(float Et, float Eta) {
  double InvPerr2, a, b, c;
  if(fabs(Eta) < 1.4){
    a = 5.6;
    b = 1.25;
    c = 0.033;
  }
  else{
    a = 4.8;
    b = 0.89;
    c = 0.043;
  }
  InvPerr2 = (a * a) + (b * b) * Et + (c * c) * Et * Et;
  return InvPerr2;
}

double Jet_ErrPhi(float Et, float Eta) {
  double InvPerr2, a, b, c;
  if(fabs(Eta) < 1.4){
    a = 6.65;
    b = 0.04;
    c = 8.49 * 0.00001;
  }
  else{
    a = 2.908;
    b = 0.021;
    c = 2.59 * 0.0001;
  }
  InvPerr2 = a/(Et * Et) + b/Et + c;
  return InvPerr2;
}

int muonResolution(double et, double eta, double& resEt, double& resEta, double& resPhi)
{

  double abseta = fabs(eta) ;
  

  if ( 0.000 <= abseta and abseta < 0.100 ) {
    resEt   = et * (0.00517 + 0.000143 * et) ;
    resEta  = TMath::Sqrt( TMath::Power(0.000433,2) + TMath::Power(0.000161/TMath::Sqrt(et),2) + TMath::Power(0.00334/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(7.21e-05,2) + TMath::Power(7e-05/TMath::Sqrt(et),2) + TMath::Power(0.00296/et,2) ) ; 
  }

  else if ( 0.100 <= abseta and abseta < 0.200 ) {
    resEt   = et * (0.00524 + 0.000143 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000381,2) + TMath::Power(0.000473/TMath::Sqrt(et),2) + TMath::Power(0.00259/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.79e-05,2) + TMath::Power(0.000245/TMath::Sqrt(et),2) + TMath::Power(0.00274/et,2) ) ; 
  }

  else if ( 0.200 <= abseta and abseta < 0.300 ) {
    resEt   = et * (0.00585 + 0.000138 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000337,2) + TMath::Power(0.000381/TMath::Sqrt(et),2) + TMath::Power(0.0023/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(7.08e-05,2) + TMath::Power(6.75e-05/TMath::Sqrt(et),2) + TMath::Power(0.00307/et,2) ) ; 
  }

  else if ( 0.300 <= abseta and abseta < 0.400 ) {
    resEt   = et * (0.0065 + 0.000133 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000308,2) + TMath::Power(0.000166/TMath::Sqrt(et),2) + TMath::Power(0.00249/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.59e-05,2) + TMath::Power(0.000301/TMath::Sqrt(et),2) + TMath::Power(0.00281/et,2) ) ; 
  }

  else if ( 0.400 <= abseta and abseta < 0.500 ) {
    resEt   = et * (0.0071 + 0.000129 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000289,2) + TMath::Power(5.37e-09/TMath::Sqrt(et),2) + TMath::Power(0.00243/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.27e-05,2) + TMath::Power(0.000359/TMath::Sqrt(et),2) + TMath::Power(0.00278/et,2) ) ; 
  }

  else if ( 0.500 <= abseta and abseta < 0.600 ) {
    resEt   = et * (0.00721 + 0.00013 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000279,2) + TMath::Power(0.000272/TMath::Sqrt(et),2) + TMath::Power(0.0026/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.46e-05,2) + TMath::Power(0.00036/TMath::Sqrt(et),2) + TMath::Power(0.00285/et,2) ) ; 
  }

  else if ( 0.600 <= abseta and abseta < 0.700 ) {
    resEt   = et * (0.00757 + 0.000129 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000282,2) + TMath::Power(3.63e-10/TMath::Sqrt(et),2) + TMath::Power(0.00288/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.54e-05,2) + TMath::Power(0.000348/TMath::Sqrt(et),2) + TMath::Power(0.00301/et,2) ) ; 
  }

  else if ( 0.700 <= abseta and abseta < 0.800 ) {
    resEt   = et * (0.0081 + 0.000127 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000265,2) + TMath::Power(0.000609/TMath::Sqrt(et),2) + TMath::Power(0.00212/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.2e-05,2) + TMath::Power(0.000402/TMath::Sqrt(et),2) + TMath::Power(0.00304/et,2) ) ; 
  }

  else if ( 0.800 <= abseta and abseta < 0.900 ) {
    resEt   = et * (0.00916 + 0.000131 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000241,2) + TMath::Power(0.000678/TMath::Sqrt(et),2) + TMath::Power(0.00221/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.26e-05,2) + TMath::Power(0.000458/TMath::Sqrt(et),2) + TMath::Power(0.0031/et,2) ) ; 
  }

  else if ( 0.900 <= abseta and abseta < 1.000 ) {
    resEt   = et * (0.0108 + 0.000151 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000228,2) + TMath::Power(0.000612/TMath::Sqrt(et),2) + TMath::Power(0.00245/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(7.18e-05,2) + TMath::Power(0.000469/TMath::Sqrt(et),2) + TMath::Power(0.00331/et,2) ) ; 
  }

  else if ( 1.000 <= abseta and abseta < 1.100 ) {
    resEt   = et * (0.0115 + 0.000153 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000217,2) + TMath::Power(0.000583/TMath::Sqrt(et),2) + TMath::Power(0.00307/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.98e-05,2) + TMath::Power(0.000507/TMath::Sqrt(et),2) + TMath::Power(0.00338/et,2) ) ; 
  }

  else if ( 1.100 <= abseta and abseta < 1.200 ) {
    resEt   = et * (0.013 + 0.000136 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000195,2) + TMath::Power(0.000751/TMath::Sqrt(et),2) + TMath::Power(0.00282/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.21e-05,2) + TMath::Power(0.000584/TMath::Sqrt(et),2) + TMath::Power(0.00345/et,2) ) ; 
  }

  else if ( 1.200 <= abseta and abseta < 1.300 ) {
    resEt   = et * (0.0144 + 0.000131 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000183,2) + TMath::Power(0.000838/TMath::Sqrt(et),2) + TMath::Power(0.00227/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(5.37e-05,2) + TMath::Power(0.000667/TMath::Sqrt(et),2) + TMath::Power(0.00352/et,2) ) ; 
  }

  else if ( 1.300 <= abseta and abseta < 1.400 ) {
    resEt   = et * (0.0149 + 0.000141 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000196,2) + TMath::Power(0.000783/TMath::Sqrt(et),2) + TMath::Power(0.00274/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(5.37e-05,2) + TMath::Power(0.000711/TMath::Sqrt(et),2) + TMath::Power(0.00358/et,2) ) ; 
  }

  else if ( 1.400 <= abseta and abseta < 1.500 ) {
    resEt   = et * (0.014 + 0.000155 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.0002,2) + TMath::Power(0.000832/TMath::Sqrt(et),2) + TMath::Power(0.00254/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(5.98e-05,2) + TMath::Power(0.000713/TMath::Sqrt(et),2) + TMath::Power(0.00362/et,2) ) ; 
  }

  else if ( 1.500 <= abseta and abseta < 1.600 ) {
    resEt   = et * (0.0132 + 0.000169 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000205,2) + TMath::Power(0.0007/TMath::Sqrt(et),2) + TMath::Power(0.00304/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.21e-05,2) + TMath::Power(0.000781/TMath::Sqrt(et),2) + TMath::Power(0.00348/et,2) ) ; 
  }

  else if ( 1.600 <= abseta and abseta < 1.700 ) {
    resEt   = et * (0.0129 + 0.0002 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000214,2) + TMath::Power(0.000747/TMath::Sqrt(et),2) + TMath::Power(0.00319/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(6.92e-05,2) + TMath::Power(0.000865/TMath::Sqrt(et),2) + TMath::Power(0.00337/et,2) ) ; 
  }

  else if ( 1.700 <= abseta and abseta < 1.800 ) {
    resEt   = et * (0.0135 + 0.000264 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000238,2) + TMath::Power(0.000582/TMath::Sqrt(et),2) + TMath::Power(0.00343/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(9.13e-05,2) + TMath::Power(0.000896/TMath::Sqrt(et),2) + TMath::Power(0.00348/et,2) ) ; 
  }

  else if ( 1.800 <= abseta and abseta < 1.900 ) {
    resEt   = et * (0.0144 + 0.00034 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000263,2) + TMath::Power(0.000721/TMath::Sqrt(et),2) + TMath::Power(0.00322/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000102,2) + TMath::Power(0.000994/TMath::Sqrt(et),2) + TMath::Power(0.00337/et,2) ) ; 
  }

  else if ( 1.900 <= abseta and abseta < 2.000 ) {
    resEt   = et * (0.0147 + 0.000441 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000284,2) + TMath::Power(0.000779/TMath::Sqrt(et),2) + TMath::Power(0.0031/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000123,2) + TMath::Power(0.00108/TMath::Sqrt(et),2) + TMath::Power(0.00315/et,2) ) ; 
  }

  else if ( 2.000 <= abseta and abseta < 2.100 ) {
    resEt   = et * (0.0154 + 0.000604 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000316,2) + TMath::Power(0.000566/TMath::Sqrt(et),2) + TMath::Power(0.00384/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000169,2) + TMath::Power(0.000947/TMath::Sqrt(et),2) + TMath::Power(0.00422/et,2) ) ; 
  }

  else if ( 2.100 <= abseta and abseta < 2.200 ) {
    resEt   = et * (0.0163 + 0.000764 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000353,2) + TMath::Power(0.000749/TMath::Sqrt(et),2) + TMath::Power(0.0038/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000176,2) + TMath::Power(0.00116/TMath::Sqrt(et),2) + TMath::Power(0.00423/et,2) ) ; 
  }

  else if ( 2.200 <= abseta and abseta < 2.300 ) {
    resEt   = et * (0.0173 + 0.000951 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000412,2) + TMath::Power(0.00102/TMath::Sqrt(et),2) + TMath::Power(0.00351/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000207,2) + TMath::Power(0.00115/TMath::Sqrt(et),2) + TMath::Power(0.00469/et,2) ) ; 
  }

  else if ( 2.300 <= abseta and abseta < 2.400 ) {
    resEt   = et * (0.0175 + 0.00126 * et); 
    resEta  = TMath::Sqrt( TMath::Power(0.000506,2) + TMath::Power(0.000791/TMath::Sqrt(et),2) + TMath::Power(0.0045/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.00027,2) + TMath::Power(0.00113/TMath::Sqrt(et),2) + TMath::Power(0.00528/et,2) ) ; 
  }

  return true;
}
int metResolution(double et, double& resEt, double& resEta, double& resPhi)
{
  resEt   = et * TMath::Sqrt( TMath::Power(0.0337,2) + TMath::Power(0.888/TMath::Sqrt(et),2) + TMath::Power(19.6/et,2) ) ;
  resEta  = TMath::Sqrt( TMath::Power(0,2) + TMath::Power(0/TMath::Sqrt(et),2) + TMath::Power(0/et,2) ) ;
  resPhi  = TMath::Sqrt( TMath::Power(1.28e-08,2) + TMath::Power(1.45/TMath::Sqrt(et),2) + TMath::Power(1.03/et,2) );
  
  return true;
}
int elecResolution(double et, double eta, double& resEt, double& resEta, double& resPhi)
{

  double abseta = fabs(eta) ;


  if ( 0.000 <= abseta and abseta < 0.174 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00534,2) + TMath::Power(0.079/TMath::Sqrt(et),2) + TMath::Power(0.163/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000452,2) + TMath::Power(0.000285/TMath::Sqrt(et),2) + TMath::Power(0.00376/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000101,2) + TMath::Power(0.0011/TMath::Sqrt(et),2) + TMath::Power(0.00346/et,2) ) ; 
  }

  else if ( 0.174 <= abseta and abseta < 0.261 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00518,2) + TMath::Power(0.0749/TMath::Sqrt(et),2) + TMath::Power(0.227/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.00038,2) + TMath::Power(0.000571/TMath::Sqrt(et),2) + TMath::Power(0.00276/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(9.3e-05,2) + TMath::Power(0.00115/TMath::Sqrt(et),2) + TMath::Power(0.0035/et,2) ) ; 
  }

  else if ( 0.261 <= abseta and abseta < 0.348 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00332,2) + TMath::Power(0.0879/TMath::Sqrt(et),2) + TMath::Power(0.12/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000351,2) + TMath::Power(1.36e-09/TMath::Sqrt(et),2) + TMath::Power(0.00324/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000103,2) + TMath::Power(0.00117/TMath::Sqrt(et),2) + TMath::Power(0.00333/et,2) ) ; 
  }

  else if ( 0.348 <= abseta and abseta < 0.435 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00445,2) + TMath::Power(0.0895/TMath::Sqrt(et),2) + TMath::Power(0.186/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000319,2) + TMath::Power(0.00061/TMath::Sqrt(et),2) + TMath::Power(0.00182/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.00011,2) + TMath::Power(0.00115/TMath::Sqrt(et),2) + TMath::Power(0.00365/et,2) ) ; 
  }

  else if ( 0.435 <= abseta and abseta < 0.522 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00453,2) + TMath::Power(0.0893/TMath::Sqrt(et),2) + TMath::Power(0.21/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000301,2) + TMath::Power(0.000612/TMath::Sqrt(et),2) + TMath::Power(0.00146/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000105,2) + TMath::Power(0.00122/TMath::Sqrt(et),2) + TMath::Power(0.00343/et,2) ) ; 
  }

  else if ( 0.522 <= abseta and abseta < 0.609 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00308,2) + TMath::Power(0.0886/TMath::Sqrt(et),2) + TMath::Power(0.188/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000297,2) + TMath::Power(0.000791/TMath::Sqrt(et),2) + TMath::Power(2.09e-08/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000102,2) + TMath::Power(0.00129/TMath::Sqrt(et),2) + TMath::Power(0.00328/et,2) ) ; 
  }

  else if ( 0.609 <= abseta and abseta < 0.696 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00308,2) + TMath::Power(0.0914/TMath::Sqrt(et),2) + TMath::Power(0.182/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.00032,2) + TMath::Power(0.000329/TMath::Sqrt(et),2) + TMath::Power(0.00325/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000103,2) + TMath::Power(0.00139/TMath::Sqrt(et),2) + TMath::Power(0.00253/et,2) ) ; 
  }

  else if ( 0.696 <= abseta and abseta < 0.783 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00442,2) + TMath::Power(0.0914/TMath::Sqrt(et),2) + TMath::Power(0.231/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000309,2) + TMath::Power(0.000821/TMath::Sqrt(et),2) + TMath::Power(0.00119/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000115,2) + TMath::Power(0.00139/TMath::Sqrt(et),2) + TMath::Power(0.00293/et,2) ) ; 
  }

  else if ( 0.783 <= abseta and abseta < 0.870 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00455,2) + TMath::Power(0.0949/TMath::Sqrt(et),2) + TMath::Power(0.335/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000293,2) + TMath::Power(0.000767/TMath::Sqrt(et),2) + TMath::Power(0.00211/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000121,2) + TMath::Power(0.00158/TMath::Sqrt(et),2) + TMath::Power(0.00151/et,2) ) ; 
  }

  else if ( 0.870 <= abseta and abseta < 0.957 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00181,2) + TMath::Power(0.102/TMath::Sqrt(et),2) + TMath::Power(0.333/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000275,2) + TMath::Power(0.000765/TMath::Sqrt(et),2) + TMath::Power(0.00227/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000128,2) + TMath::Power(0.00169/TMath::Sqrt(et),2) + TMath::Power(1.93e-08/et,2) ) ; 
  }

  else if ( 0.957 <= abseta and abseta < 1.044 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.000764,2) + TMath::Power(0.108/TMath::Sqrt(et),2) + TMath::Power(0.42/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000274,2) + TMath::Power(0.000622/TMath::Sqrt(et),2) + TMath::Power(0.00299/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000145,2) + TMath::Power(0.00179/TMath::Sqrt(et),2) + TMath::Power(1.69e-08/et,2) ) ; 
  }

  else if ( 1.044 <= abseta and abseta < 1.131 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00114,2) + TMath::Power(0.128/TMath::Sqrt(et),2) + TMath::Power(0.55/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000269,2) + TMath::Power(0.000929/TMath::Sqrt(et),2) + TMath::Power(0.00183/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000185,2) + TMath::Power(0.00182/TMath::Sqrt(et),2) + TMath::Power(2.99e-09/et,2) ) ; 
  }

  else if ( 1.131 <= abseta and abseta < 1.218 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(4.14e-09,2) + TMath::Power(0.155/TMath::Sqrt(et),2) + TMath::Power(0.674/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000268,2) + TMath::Power(0.000876/TMath::Sqrt(et),2) + TMath::Power(0.00234/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000194,2) + TMath::Power(0.002/TMath::Sqrt(et),2) + TMath::Power(2.39e-08/et,2) ) ; 
  }

  else if ( 1.218 <= abseta and abseta < 1.305 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(8.03e-09,2) + TMath::Power(0.144/TMath::Sqrt(et),2) + TMath::Power(0.8/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000258,2) + TMath::Power(0.000782/TMath::Sqrt(et),2) + TMath::Power(0.00246/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000226,2) + TMath::Power(0.00206/TMath::Sqrt(et),2) + TMath::Power(5.88e-08/et,2) ) ; 
  }

  else if ( 1.305 <= abseta and abseta < 1.392 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00842,2) + TMath::Power(0.118/TMath::Sqrt(et),2) + TMath::Power(0.951/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000269,2) + TMath::Power(0.000817/TMath::Sqrt(et),2) + TMath::Power(0.00278/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000247,2) + TMath::Power(0.00225/TMath::Sqrt(et),2) + TMath::Power(1.47e-09/et,2) ) ; 
  }

  else if ( 1.392 <= abseta and abseta < 1.479 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.00684,2) + TMath::Power(0.144/TMath::Sqrt(et),2) + TMath::Power(0.892/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000267,2) + TMath::Power(0.000734/TMath::Sqrt(et),2) + TMath::Power(0.00327/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000234,2) + TMath::Power(0.00233/TMath::Sqrt(et),2) + TMath::Power(4.92e-09/et,2) ) ; 
  }

  else if ( 1.479 <= abseta and abseta < 1.653 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.0245,2) + TMath::Power(0.196/TMath::Sqrt(et),2) + TMath::Power(0.555/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000268,2) + TMath::Power(0.000757/TMath::Sqrt(et),2) + TMath::Power(0.00295/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.00025,2) + TMath::Power(0.00268/TMath::Sqrt(et),2) + TMath::Power(7.5e-09/et,2) ) ; 
  }

  else if ( 1.653 <= abseta and abseta < 1.740 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.0174,2) + TMath::Power(0.127/TMath::Sqrt(et),2) + TMath::Power(0.894/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000274,2) + TMath::Power(1.77e-09/TMath::Sqrt(et),2) + TMath::Power(0.00435/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000284,2) + TMath::Power(0.00275/TMath::Sqrt(et),2) + TMath::Power(6.56e-09/et,2) ) ; 
  }

  else if ( 1.740 <= abseta and abseta < 1.830 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.0144,2) + TMath::Power(0.133/TMath::Sqrt(et),2) + TMath::Power(0.708/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000274,2) + TMath::Power(0.00101/TMath::Sqrt(et),2) + TMath::Power(0.000982/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000356,2) + TMath::Power(0.00279/TMath::Sqrt(et),2) + TMath::Power(0.00261/et,2) ) ; 
  }

  else if ( 1.830 <= abseta and abseta < 1.930 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.0149,2) + TMath::Power(0.126/TMath::Sqrt(et),2) + TMath::Power(0.596/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000299,2) + TMath::Power(0.000686/TMath::Sqrt(et),2) + TMath::Power(0.00341/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000347,2) + TMath::Power(0.00298/TMath::Sqrt(et),2) + TMath::Power(1.02e-08/et,2) ) ; 
  }

  else if ( 1.930 <= abseta and abseta < 2.043 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.0143,2) + TMath::Power(0.12/TMath::Sqrt(et),2) + TMath::Power(0.504/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000329,2) + TMath::Power(3.05e-10/TMath::Sqrt(et),2) + TMath::Power(0.00439/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000302,2) + TMath::Power(0.00322/TMath::Sqrt(et),2) + TMath::Power(5.22e-08/et,2) ) ; 
  }

  else if ( 2.043 <= abseta and abseta < 2.172 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.0162,2) + TMath::Power(0.0965/TMath::Sqrt(et),2) + TMath::Power(0.483/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.00037,2) + TMath::Power(1.32e-08/TMath::Sqrt(et),2) + TMath::Power(0.00447/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000287,2) + TMath::Power(0.00349/TMath::Sqrt(et),2) + TMath::Power(3e-11/et,2) ) ; 
  }

  else if ( 2.172 <= abseta and abseta < 2.322 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.0122,2) + TMath::Power(0.13/TMath::Sqrt(et),2) + TMath::Power(0.207/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000442,2) + TMath::Power(4.03e-10/TMath::Sqrt(et),2) + TMath::Power(0.00544/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(0.000214,2) + TMath::Power(0.00436/TMath::Sqrt(et),2) + TMath::Power(2.98e-09/et,2) ) ; 
  }

  else if ( 2.322 <= abseta and abseta < 2.500 ) {
    resEt   = et * TMath::Sqrt( TMath::Power(0.0145,2) + TMath::Power(0.127/TMath::Sqrt(et),2) + TMath::Power(0.0782/et,2) ) ; 
    resEta  = TMath::Sqrt( TMath::Power(0.000577,2) + TMath::Power(0.000768/TMath::Sqrt(et),2) + TMath::Power(0.00331/et,2) ) ; 
    resPhi  = TMath::Sqrt( TMath::Power(8.02e-05,2) + TMath::Power(0.00525/TMath::Sqrt(et),2) + TMath::Power(0.00581/et,2) ) ; 
  }
  return true;
}
vector<float> PerfomFit(TLorentzVector lep,TLorentzVector nu){
	// vec1 and vec2 and vec3 = 4-vect to be fitted
	// m1 and m2 and m3 covariant matrix
	TMatrixD m_lep(3,3);
	TMatrixD m_nu(3,3);
	m_lep.Zero();
	m_nu.Zero();


	//In this example the covariant matrix depends on the transverse energy and eta of the jets
	double	resEt, resEta, resPhi;
	muonResolution(lep.Et(), lep.Eta(), resEt, resEta, resPhi);
	m_lep(0,0) = resEt*resEt; // et
	m_lep(1,1) = resEta*resEta; // eta
	m_lep(2,2) = resPhi*resPhi; // phii

	metResolution(nu.Et(), resEt, resEta, resPhi);
	resEta	= 9999.;
	m_nu(0,0) = resEt*resEt; // et
	m_nu(1,1) = resEta*resEta; // eta
	m_nu(2,2) = resPhi*resPhi; // phi

	//cout<<"cov m trac = [et (m(0,0)), eta (m(1,1)), phi (m(2,2))"<<endl;
	//cout<<"lepton cov m trac = ["<<m_lep(0,0)<<","<<m_lep(1,1)<<","<<m_lep(2,2)<<"]"<<endl;
	//cout<<"neutrino cov m trac = ["<<m_nu(0,0)<<","<<m_nu(1,1)<<","<<m_nu(2,2)<<"]"<<endl;
	
	TAbsFitParticle* _lep;
	TAbsFitParticle* _nu;

	_lep = new TFitParticleEtEtaPhi( "lepton", "lepton", &lep, &m_lep );
	_nu = new TFitParticleEtEtaPhi( "neutrino", "neutrino", &nu, &m_nu );
	
	TFitConstraintM* _MCons;
	//vec1 and vec2 must make a W boson
	_MCons = new TFitConstraintM( "WMassConstraint", "WMass-Constraint", 0, 0 , 80.41);
	_MCons->addParticles1( _lep, _nu );

	//Definition of the fitter
	//Add one measured particles(lep)
	//Add one constraints
	TKinFitter* _fitter;
	_fitter = new TKinFitter( "TtHFit", "TtHFit" );
	_fitter->addMeasParticle( _lep );
	_fitter->addMeasParticle( _nu );
	_fitter->addConstraint( _MCons );

	//Set convergence criteria
	_fitter->setMaxNbIter( 30 );
	_fitter->setMaxDeltaS( 1e-2 );
	_fitter->setMaxF( 1e-1 );
	_fitter->setVerbosity(0);
	
	//Perform the fit
	_fitter->fit();
	//cout<<"fit status : "<<_fitter->getStatus()<<endl;
	// Build up the event after the kinematic fit
	/*RawParticle Lepton = RawParticle(_lep->getCurr4Vec()->X(),
					 _lep->getCurr4Vec()->Y(),
					 _lep->getCurr4Vec()->Z(),
					 _lep->getCurr4Vec()->E());
	RawParticle Neutrino = RawParticle(_nu->getCurr4Vec()->X(),
					   _nu->getCurr4Vec()->Y(),
					   _nu->getCurr4Vec()->Z(),
					   _nu->getCurr4Vec()->E());*/
	//cout<<"lep = ["<<_lep->getCurr4Vec()->X()<<","<<_lep->getCurr4Vec()->Y()<<","<<_lep->getCurr4Vec()->Z()<<","<<_lep->getCurr4Vec()->E()<<"]"<<endl;
	//cout<<"nu = ["<<_nu->getCurr4Vec()->X()<<","<<_nu->getCurr4Vec()->Y()<<","<<_nu->getCurr4Vec()->Z()<<","<<_nu->getCurr4Vec()->E()<<"]"<<endl;
	
	vector<float> New_LoretzVectors_XYZE;
	New_LoretzVectors_XYZE.reserve(8);

	New_LoretzVectors_XYZE.push_back(_lep->getCurr4Vec()->X());
	New_LoretzVectors_XYZE.push_back(_lep->getCurr4Vec()->Y());
	New_LoretzVectors_XYZE.push_back(_lep->getCurr4Vec()->Z());
	New_LoretzVectors_XYZE.push_back(_lep->getCurr4Vec()->E());


	New_LoretzVectors_XYZE.push_back(_nu->getCurr4Vec()->X());
        New_LoretzVectors_XYZE.push_back(_nu->getCurr4Vec()->Y());
        New_LoretzVectors_XYZE.push_back(_nu->getCurr4Vec()->Z());
        New_LoretzVectors_XYZE.push_back(_nu->getCurr4Vec()->E());
	
	return New_LoretzVectors_XYZE;
	 
}
void KinFit(){
	cout<<"begin event ....."<<endl;
	Double_t Chi2 = 11.;
	TLorentzVector lep(-77.92, 16.24, 117.64, 142.87);
	TLorentzVector nu(15.41, 28.78, 6.06, 34.08);
	cout<<"lep = ["<<lep.X()<<","<<lep.Y()<<","<<lep.Z()<<","<<lep.E()<<"]"<<endl;
        cout<<"nu = ["<<nu.X()<<","<<nu.Y()<<","<<nu.Z()<<","<<nu.E()<<"]"<<endl;
	cout<<"Fitting ...."<<endl;

	vector<float> new_lep;
	new_lep.reserve(4);
	new_lep = PerfomFit(lep,nu);

	cout<<"lep = ["<<new_lep.at(0)<<","<<new_lep.at(1)<<","<<new_lep.at(2)<<","<<new_lep.at(3)<<"]"<<endl;




	cout<<"..... end event"<<endl;
	
}
