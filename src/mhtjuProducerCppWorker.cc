#include "../interface/mhtjuProducerCppWorker.h"

std::pair<float,float> mhtjuProducerCppWorker::getHT(){

  int Jet_clean[100];
  unsigned njet = (*nJet).Get()[0];
  unsigned nmuon = (*nMuon).Get()[0];
  unsigned nelectron = (*nElectron).Get()[0];

  for( unsigned jet = 0; jet < njet; jet++)   {
    Jet_clean[jet] = 1;      // default value: jet is supposed to be a good one
    if( fabs((*Jet_eta)[jet]) > 2.5 )  continue;
    
    // check nearest mu
    float DRmin = 999.;
    for( unsigned jmu = 0; jmu < nmuon; jmu++)   {
      if( (*Muon_mediumId)[jmu] == 0 ) continue; // only good muons
      if( (*Muon_pt)[jmu] < 5. )       continue;
      float deta =  (*Jet_eta)[jet] - (*Muon_eta)[jmu];
      float dphi =  fabs( (*Jet_phi)[jet] - (*Muon_phi)[jmu]);
      if(dphi > 3.1416 ) dphi = 6.2832 - dphi;
      float DR = sqrt(deta*deta + dphi*dphi);
      if( DR < DRmin ) DRmin = DR;
    } // next muon                                                                                                                                       

    // check nearest electron
    for( unsigned je = 0; je < nelectron; je++)   {
      if( (*Electron_cutBased)[je] == 0 )  continue; // only good electron
      if( (*Electron_pt)[je] < 15. )       continue;
      float deta =  (*Jet_eta)[jet] - (*Electron_eta)[je];
      float dphi =  fabs( (*Jet_phi)[jet] - (*Electron_phi)[je]);
      if(dphi > 3.1416 ) dphi = 6.2832 - dphi;
      float DR = sqrt(deta*deta + dphi*dphi);
      if( DR < DRmin ) DRmin = DR;
    } // next electron
    if( DRmin > 0.4 ) continue; // no near lepton; jet is clean
    // check energy fractions
    Jet_clean[jet] = 0;
    if( (*Jet_chHEF)[jet] > 0.1 )                         Jet_clean[jet] = 1;
    if( (*Jet_chHEF)[jet] < 0.1 && (*Jet_neHEF)[jet] > 0.2 ) Jet_clean[jet] = 1;
  } // next jet     

  // HT computation -------------------- 
  //math::XYZTLorentzVectorF ht(0,0,0,0);
  TLorentzVector ht(0,0,0,0);
  for( unsigned jet = 0; jet < njet; jet++)   { // loop on jets ----------
    if( (*Jet_pt)[jet] < 30.)    continue;
    if( (*Jet_puId)[jet]  == 4 ) continue;  // jet cleaning...                                                                                           
    if( Jet_clean[jet] == 0 ) continue;
    if( fabs((*Jet_eta)[jet]) > 2.5  ) continue;
    TLorentzVector j_add(0,0,0,0);
    j_add.SetPtEtaPhiM((*Jet_pt)[jet],0,(*Jet_phi)[jet],0);
    ht += j_add;
    //ht += math::PtEtaPhiMLorentzVectorF((*Jet_pt)[jet],0,(*Jet_phi)[jet],0);
    
  }   // next jet ---------------------------------

  return std::pair<float,float>(ht.Pt(),ht.Phi());
}

float mhtjuProducerCppWorker::ptZCorr(bool GENPART){
  float wgtZ = 1.;
  if (GENPART== true){
    unsigned nGen = (*nGenPart).Get()[0];
    int nGenZ = 0;
    for( unsigned j = 0; j < nGen; j++)   {
      if (  (*GenPart_pdgId)[j] != 23 )    continue;
      nGenZ++;
      float ptZ =  (*GenPart_pt)[j];
      if( nGenZ > 1) continue;
      if ( ptZ < 20.                ) wgtZ = 1.2;
      if ( ptZ >= 20. && ptZ < 30.  ) wgtZ = 1.;
      if ( ptZ >= 30. && ptZ < 40.  ) wgtZ = 0.75;
      if ( ptZ >= 40. && ptZ < 50.  ) wgtZ = 0.65;
      if ( ptZ >= 50. && ptZ < 200. ) wgtZ = 0.65 - 0.00034*ptZ;
      if ( ptZ >= 200.              ) wgtZ = 0.6;
    }
  }
  return wgtZ;
}
