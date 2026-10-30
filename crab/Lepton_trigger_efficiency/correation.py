import ROOT as R

file = R.TFile.Open("/grid_mnt/t3storage3/mikumar/UL_Run2/SEVENTEEN/Lepton_Trig_Effi/v10/Ele_trigger_ttbar_FullyLeptonic_mu.root")

Events_hist_total = file.Get("Events_2D_hist/Event_total")

Events_hist_mu_trigger = file.Get("Events_2D_hist/Event_HLT_IsoMu27")
Events_hist_el_trigger = file.Get("Events_2D_hist/Event_HLT_Ele35")
Events_hist_el_jet_cross_trigger = file.Get("Events_2D_hist/Event_HLT_Ele30_eta2p1_crossJet")
Events_hist_els_trigger = file.Get("Events_2D_hist/Event_Event_HLT_Ele35_HLT_Ele30_eta2p1_crossJet")
Events_hist_els_mu_trigger = file.Get("Events_2D_hist/Event_HLT_Ele30_eta2p1_crossJet_HLT_IsoMu27_HLT_Ele30_eta2p1_crossJet")

print "Events_total : ",  Events_hist_total.Integral()
print "Events_mu_trigger : ",  Events_hist_mu_trigger.Integral()
print "Events_el_trigger : ",  Events_hist_el_trigger.Integral()
print "Events_el_jet_cross_trigger : ",  Events_hist_el_jet_cross_trigger.Integral()
print "Events_els_trigger : ",  Events_hist_els_trigger.Integral()
print "Events_els_mu_trigger : ",  Events_hist_els_mu_trigger.Integral()

effi_mu_trigger = Events_hist_mu_trigger.Integral()/Events_hist_total.Integral()
effi_el_trigger = Events_hist_el_trigger.Integral()/Events_hist_total.Integral()
effi_el_jet_cross_trigger = Events_hist_el_jet_cross_trigger.Integral()/Events_hist_total.Integral()
effi_els_trigger = Events_hist_els_trigger.Integral()/Events_hist_total.Integral()
effi_els_mu_trigger = Events_hist_els_mu_trigger.Integral()/Events_hist_total.Integral()

print "mu_tri_effi = ",effi_mu_trigger
print "el_tri_effi = ",effi_el_trigger
print "el_jet_cross_trigger_effi = ",effi_el_jet_cross_trigger
print "els_mu_tri_effi = ",effi_els_mu_trigger

correlation = (effi_mu_trigger*effi_els_trigger)/effi_els_mu_trigger
print "correlation = ", correlation
