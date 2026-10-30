#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducerJson import * 
btagSFUL2016preVFP = lambda: btagSFProducer("UL2016preVFP",'deepJet', ['shape_corr'])
btagSFUL2016postVFP = lambda: btagSFProducer("UL2016postVFP",'deepJet', ['shape_corr'])
btagSFUL2017 = lambda: btagSFProducer("UL2017",'deepJet', ['shape_corr']) #remeber for fix working point to evelavate weights for L, M, T there are saprate input file acc. to new recomadation which not in place in btv producer
btagSFUL2018 = lambda: btagSFProducer("UL2018",'deepJet', ['shape_corr']) #remeber for fix working point to evelavate weights for L, M, T there are saprate input file acc. to new recomadation which not in place in btv producer