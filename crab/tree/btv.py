#!/usr/bin/env python3
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *

btagSFUL2016preVFP = lambda: btagSFProducer("UL2016preVFP",'deepjet', ['shape_corr'])
btagSFUL2016postVFP = lambda: btagSFProducer("UL2016postVFP",'deepjet', ['shape_corr'])
btagSFUL2017 = lambda: btagSFProducer("UL2017",'deepjet', ['shape_corr']) #remeber for fix working point to evelavate weights for L, M, T there are saprate input file acc. to new recomadation which not in place in btv producer
btagSFUL2018 = lambda: btagSFProducer("UL2018",'deepjet', ['shape_corr']) #remeber for fix working point to evelavate weights for L, M, T there are saprate input file acc. to new recomadation which not in place in btv producer

