import ROOT
import array

edges_elex = array.array('f', [0.0, 0.8, 1.4442, 1.56, 2.0, 2.5])
nbins_elex = len(edges_elex)-1
edges_eley = array.array('f', [20., 30., 40., 50., 60., 100., 200., 500.])
nbins_eley = len(edges_eley)-1
value_ele = [0.999, 0.999, 0.999, 0.998, 0.999, 1.002, 1.001,
             1.005, 1.000, 1.000, 1.000, 1.000, 1.002, 0.999,
             1.030, 1.023, 1.006, 1.001, 1.020, 1.006, 1.073,
             0.992, 0.998, 0.997, 0.999, 0.999, 1.000, 0.998,
             0.978, 0.987, 0.993, 0.998, 1.001, 1.000, 0.997
         ]

err_ele = [0.008, 0.003, 0.002, 0.001, 0.002, 0.002, 0.002,
           0.012, 0.003, 0.001, 0.002, 0.001, 0.001, 0.001,
           0.110, 0.009, 0.002, 0.004, 0.021, 0.008, 0.038,
           0.011, 0.002, 0.001, 0.001, 0.001, 0.001, 0.002,
           0.005, 0.002, 0.001, 0.001, 0.001, 0.001, 0.002
       ]

histo_ele = ROOT.TH2F('EGamma_SF2D', 'e/#gamma scale factors: mini-iso < 0.1; SuperCluster |#eta|; p_{T} [GeV]', nbins_elex, edges_elex, nbins_eley, edges_eley)
for x in xrange(1, len(edges_elex)):
    for y in xrange(1, len(edges_eley)):
        #print x, y, (x-1)*(len(edges_eley)-1)+y-1, value_ele[(x-1)*(len(edges_eley)-1)+y-1]
        histo_ele.SetBinContent(x, y, value_ele[(x-1)*(len(edges_eley)-1)+y-1])
        histo_ele.SetBinError(x, y, err_ele[(x-1)*(len(edges_eley)-1)+y-1])

outele = ROOT.TFile('EGM2D_MiniIso_SF_2016.root', 'RECREATE')
histo_ele.Write()
outele.Close()


edges_mux = array.array('f', [0.0, 0.9, 1.2, 2.1, 2.4])
nbins_mux = len(edges_mux)-1
edges_muy = array.array('f', [30., 40., 50., 60., 100., 1000.])
nbins_muy = len(edges_muy)-1
value_mu = [0.999708, 0.998914, 0.999181, 0.999594, 1.00003,
            0.999764, 0.999142, 0.999393, 0.999992, 0.999797,
            0.999537, 0.999084, 0.999276, 0.999704, 0.99981,
            0.999363, 0.999475, 0.999611, 0.99999, 0.999982
            ]

err_mu = [0.00012323, 7.86379e-05, 0.000126404, 0.000102055, 0.00016077,
          0.000234586, 0.000134662, 0.000214667, 0.000249322, 0.000229799,
          0.000142461, 7.4588e-05, 0.00139617, 0.000109978, 0.000176191,
          0.000208569, 0.000118931, 0.000201856, 0.000225058, 0.000473922
          ]

histo_mu = ROOT.TH2F('pt_abseta_ratio', '#mu scale factors: mini-iso < 0.1; muon |#eta|; muon p_{T} [GeV]', nbins_mux, edges_mux, nbins_muy, edges_muy)
for x in xrange(len(edges_mux)):
    for y in xrange(len(edges_muy)):
        histo_mu.SetBinContent(x, y, value_mu[(x-1)*(len(edges_muy)-1)+y-1])
        histo_mu.SetBinError(x, y, err_mu[(x-1)*(len(edges_muy)-1)+y-1])

outmu = ROOT.TFile('Mu_RunBCDEFGH_SF_MiniIso_2016.root', 'RECREATE')
outmu.mkdir('NUM_TightMiniIso_DEN_TightIDandIPCut')
outmu.cd('NUM_TightMiniIso_DEN_TightIDandIPCut')
histo_mu.Write()
outmu.Close()
