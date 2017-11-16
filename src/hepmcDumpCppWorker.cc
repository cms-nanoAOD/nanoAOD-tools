#include "../interface/hepmcDumpCppWorker.h"
#include "HepMC/GenEvent.h"
#include <iostream>
#include <cmath>

hepmcDumpCppWorker::hepmcDumpCppWorker(const std::string fileName){
  signalParticlePdgIds_ = {6, -6, 25, 24, -24, 23, -23};

  fout_ = new HepMC::IO_GenEvent(fileName);
}

void hepmcDumpCppWorker::setGenEventInfo(TTreeReaderValue<unsigned long long> *eventNumber,
                                         TTreeReaderValue<float> *Generator_x1, TTreeReaderValue<float> *Generator_x2,
                                         TTreeReaderValue<float> *genWeight,
                                         TTreeReaderValue<unsigned> *nLHEScaleWeight, TTreeReaderArray<float> *LHEScaleWeight,
                                         TTreeReaderValue<unsigned> *nLHEPdfWeight, TTreeReaderArray<float> *LHEPdfWeight){
  b_eventNumber     = eventNumber;
  b_genWeight       = genWeight;
  b_Generator_x1    = Generator_x1;
  b_Generator_x2    = Generator_x2;
  b_nLHEScaleWeight = nLHEScaleWeight;
  b_LHEScaleWeight  = LHEScaleWeight;
  b_nLHEPdfWeight   = nLHEPdfWeight;
  b_LHEPdfWeight    = LHEPdfWeight;
}

void hepmcDumpCppWorker::setGenParticles(TTreeReaderValue<unsigned> *nGenPart,
                                         TTreeReaderArray<float> *GenPart_pt, TTreeReaderArray<float> *GenPart_eta, TTreeReaderArray<float> *GenPart_phi, TTreeReaderArray<float> *GenPart_mass,
                                         TTreeReaderArray<int> *GenPart_pdgId, TTreeReaderArray<int> *GenPart_status,
                                         TTreeReaderArray<int> *GenPart_genPartIdxMother){
  b_nGenPart = nGenPart;  
  b_GenPart_pt = GenPart_pt;
  b_GenPart_eta = GenPart_eta;
  b_GenPart_phi = GenPart_phi;
  b_GenPart_mass = GenPart_mass;
  b_GenPart_pdgId = GenPart_pdgId;
  b_GenPart_status = GenPart_status;
  b_GenPart_genPartIdxMother = GenPart_genPartIdxMother;
}

void hepmcDumpCppWorker::genEvent(){
  using namespace std;

  const unsigned int nGenPart = **b_nGenPart;

  HepMC::GenEvent* genEvent = new HepMC::GenEvent();
  genEvent->set_event_number(**b_eventNumber);
  //genEvent->set_signal_process_id(0);
  //genEvent->set_event_scale(0);
  //genEvent->set_alphaQED(0);
  //genEvent->set_alphaQCD(0);
  //genEvent->pdf_info()->set_x1(**b_Generator_x1);
  //genEvent->pdf_info()->set_x2(**b_Generator_x2);
  genEvent->weights().clear();
  genEvent->weights().push_back(**b_genWeight);
  if ( b_LHEScaleWeight != nullptr ) {
    for ( int i=0, n=**b_nLHEScaleWeight; i<n; ++i ) {
      genEvent->weights().push_back(b_LHEScaleWeight->At(i));
    }
  }
  if ( b_nLHEPdfWeight != nullptr ) {
    for ( int i=0, n=**b_nLHEPdfWeight; i<n; ++i ) {
      genEvent->weights().push_back(b_LHEPdfWeight->At(i));
    }
  }

  std::vector<HepMC::GenParticle*> particles;
  std::vector<std::pair<HepMC::GenParticle*, double>> orphans;
  std::map<int, std::vector<HepMC::GenParticle*>> mother2DaughtersMap;
  for ( unsigned i=0; i<nGenPart; ++i ) {
    const double pt = b_GenPart_pt->At(i), eta = b_GenPart_eta->At(i), phi = b_GenPart_phi->At(i);
    const double mass = b_GenPart_mass->At(i);
    const int pdgId = b_GenPart_pdgId->At(i), status = b_GenPart_status->At(i);
    const int mother = b_GenPart_genPartIdxMother->At(i);

    const double px = pt*cos(phi), py = pt*sin(phi);
    // Note on the pz & energy assignment at very high eta:
    // Incident beam particles have very large eta (>50000) therefore sinh/cosh fails
    // Put a safety cut for them here, the values will be fixed after this loop
    const double pz = std::abs(eta) > 100 ? eta : pt*sinh(eta);
    const double energy = std::abs(eta) > 100 ? pt : hypot(mass, pt*cosh(eta));
    HepMC::FourVector p4(px, py, pz, energy);
    HepMC::GenParticle* particle = new HepMC::GenParticle(p4, pdgId, status);

    particles.push_back(particle);
    auto assoc = mother2DaughtersMap.find(mother);
    if ( assoc == mother2DaughtersMap.end() ) assoc = mother2DaughtersMap.insert(std::make_pair(mother, std::vector<HepMC::GenParticle*>())).first;
    assoc->second.push_back(particle);

    if ( mother < 0 ) orphans.push_back(std::make_pair(particle, mass));
  }

  // Find incident beam particles
  HepMC::GenParticle *particle1 = nullptr, *particle2 = nullptr;
  double mass1 = 0, mass2 = 0;
  for ( auto pp : orphans ) {
    HepMC::GenParticle *particle = pp.first;
    const double p = particle->momentum().rho(), eta = particle->momentum().eta();
    if ( p > 100 and std::abs(eta) > 5 ) {
      if ( !particle1 ) {
        particle1 = particle;
        mass1 = pp.second;
      }
      else if ( !particle2 ) {
        particle2 = particle;
        mass2 = pp.second;
      }
    }
  }
  if ( particle1 and particle2 and particle1->momentum().pz() < 0 ) {
    std::swap(particle1, particle2);
    std::swap(mass1, mass2);
  }

  // Build the primary vertex
  HepMC::GenVertex *vertex0 = new HepMC::GenVertex(HepMC::FourVector(0,0,0,0));
  genEvent->add_vertex(vertex0);
  const double pz1 = cmEnergy_*(**b_Generator_x1), pz2 = -cmEnergy_*(**b_Generator_x2);
  if ( particle1 ) {
    // Redo the pz of the incident parton
    const double energy = std::sqrt(particle1->momentum().perp2() + pz1*pz1 + mass1*mass1);
    HepMC::FourVector p4 = particle1->momentum();
    p4.setPz(pz1);
    p4.setE(energy);
    particle1->set_momentum(p4);
    vertex0->add_particle_in(particle1);
  }
  if ( particle2 ) {
    // Redo the pz of the incident parton
    const double energy = std::sqrt(particle2->momentum().perp2() + pz2*pz2 + mass2*mass2);
    HepMC::FourVector p4 = particle2->momentum();
    p4.setPz(pz2);
    p4.setE(energy);
    particle2->set_momentum(p4);
    vertex0->add_particle_in(particle2);
  }

  // Finish with singles - put them under the production vertex
  for ( auto pp : orphans ) {
    HepMC::GenParticle* particle = pp.first;
    if ( particle == particle1 or particle == particle2 ) continue;
    vertex0->add_particle_out(particle);
  }

  // Prepare vertex list

  for ( auto x = mother2DaughtersMap.begin(); x != mother2DaughtersMap.end(); ++x ) {
    const int motherIdx = x->first;
    const auto& daughters = x->second;
    HepMC::GenParticle* mother = motherIdx < 0 ? nullptr : particles[motherIdx];

    HepMC::GenVertex *vertex = nullptr;
    if ( mother == nullptr or mother == particle1 or mother == particle2 ) {
      vertex = vertex0;
    }
    else {
      vertex = new HepMC::GenVertex(HepMC::FourVector(0,0,0,0));
      genEvent->add_vertex(vertex);
      vertex->add_particle_in(mother);
    }
    for ( auto dau : daughters ) {
      vertex->add_particle_out(dau);
    }
  }

  // Set the signal vertex
  bool hasSignalVertex = false;
  if ( !signalParticlePdgIds_.empty() ) {
    for ( auto v = genEvent->vertices_begin(); v != genEvent->vertices_end(); ++v ) {
      for ( auto p = (*v)->particles_begin(HepMC::children);
            p != (*v)->particles_end(HepMC::children); ++p ) {
        const int pdgId = (*p)->pdg_id();
        if ( std::find(signalParticlePdgIds_.begin(), signalParticlePdgIds_.end(), pdgId) != signalParticlePdgIds_.end() ) {
          genEvent->set_signal_process_vertex(*v);
          hasSignalVertex = true;
          break;
        }
      }
      if ( hasSignalVertex ) break;
    }
  }
  if ( !hasSignalVertex ) genEvent->set_signal_process_vertex(vertex0);

  // Finalize HepMC event record
  genEvent->set_beam_particles(particle1, particle2);
  fout_->write_event(genEvent);
}

hepmcDumpCppWorker::~hepmcDumpCppWorker(){
}
