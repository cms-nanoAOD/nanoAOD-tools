#!/usr/bin/env python
 
FIXME="1"
 
processes =    {
	'BBbarDMJets_pseudo_LO_Mchi-0_Mphi-20_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-100_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-100_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-100_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-100_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-1_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-1_Mphi-20_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-1_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-1_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-1_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-200_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-350_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-350_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-40_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-450_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-50_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-50_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-50_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_LO_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-100_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-100_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-100_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-100_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-100_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-10_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-1_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-200_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-350_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-350_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-40_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-450_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-50_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-50_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-50_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-50_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudo_NLO_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-10_Mphi-100_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-10_Mphi-10_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-10_Mphi-15_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-10_Mphi-50_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-1_Mphi-10000_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-1_Mphi-10_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-1_Mphi-200_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-1_Mphi-20_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-1_Mphi-300_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-1_Mphi-500_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-1_Mphi-50_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-50_Mphi-10_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-50_Mphi-200_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-50_Mphi-300_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-50_Mphi-50_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_pseudoscalar_Mchi-50_Mphi-95_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-100_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-100_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-100_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-100_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-100_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-10_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-1_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-1_Mphi-20_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-1_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-1_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-200_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-350_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-350_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-40_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-450_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-50_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-50_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-50_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-50_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_LO_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-10_Mphi-100_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-10_Mphi-10_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-10_Mphi-15_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-10_Mphi-50_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-1_Mphi-10000_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-1_Mphi-100_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-1_Mphi-10_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-1_Mphi-200_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-1_Mphi-20_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-1_Mphi-300_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-1_Mphi-500_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-1_Mphi-50_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-50_Mphi-10_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-50_Mphi-200_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-50_Mphi-300_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-50_Mphi-50_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_Mchi-50_Mphi-95_TuneCUETP8M1_v2_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-100_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-100_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-100_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-100_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-100_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-10_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-1_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-200_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-200_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-350_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-350_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-40_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-450_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-50_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-50_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-50_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-50_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BBbarDMJets_scalar_NLO_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'BprimeTToZB_M-1000_LH_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',300000,1.0,1.0,1.0),
	'BprimeTToZB_M-1000_RH_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',300000,1.0,1.0,1.0),
	'BprimeTToZB_M-700_LH_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',300000,1.0,1.0,1.0),
	'BprimeTToZB_M-700_RH_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',300000,1.0,1.0,1.0),
	'BprimeTToZB_M-800_LH_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',300000,1.0,1.0,1.0),
	'BprimeTToZB_M-800_RH_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',300000,1.0,1.0,1.0),
	'BprimeTToZB_M-900_LH_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',300000,1.0,1.0,1.0),
	'BprimeTToZB_M-900_RH_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',300000,1.0,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-1000_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-1200_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-1400_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-1600_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-1800_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-2000_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-2500_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-3000_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-3500_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-4000_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-4500_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-600_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZhadZinv_narrow_M-800_13TeV-madgraph-v1':('MC',100000,0.27964,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-1000_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-1200_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-1400_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-1800_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-2000_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-2500_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-3000_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-3500_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-4000_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-4500_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-600_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-650_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-700_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-750_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'BulkGravToZZToZlepZhad_narrow_M-800_13TeV-madgraph-v1':('MC',100000,0.1411818468,1.0,1.0),
	'GluGluToHHTo4B_node_10_13TeV-madgraph-v1':('MC',300000,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_11_13TeV-madgraph-v1':('MC',300000,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_12_13TeV-madgraph-v1':('MC',299400,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_13_13TeV-madgraph-v1':('MC',300000,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_2_13TeV-madgraph-v1':('MC',299600,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_3_13TeV-madgraph-v1':('MC',299800,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_4_13TeV-madgraph-v1':('MC',297000,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_5_13TeV-madgraph-v1':('MC',300000,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_6_13TeV-madgraph-v1':('MC',300000,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_7_13TeV-madgraph-v1':('MC',300000,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_8_13TeV-madgraph-v1':('MC',300000,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_9_13TeV-madgraph-v1':('MC',298200,0.332929,1.0,1.0),
	'GluGluToHHTo4B_node_SM_13TeV-madgraph-v1':('MC',299800,0.01113647505,1.0,1.0),
	'GluGluToHHTo4B_node_box_13TeV-madgraph-v1':('MC',278600,0.332929,1.0,1.0),
	'HWminusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1':('MC',299994,0.000149132066544,1.0,1.0),
	'HWminusJ_HToWW_M125_13TeV_powheg_pythia8-v1':('MC',299997,0.11385936,1.0,1.0),
	'HWplusJ_HToWWTo2L2Nu_WToLNu_M125_13TeV_powheg_pythia8-v1':('MC',299795,0.000234952174368,1.0,1.0),
	'HWplusJ_HToWW_M125_13TeV_powheg_pythia8-v1':('MC',299799,0.179508,1.0,1.0),
	'HZJ_HToWW_M125_13TeV_powheg_pythia8-v1':('MC',295529,0.18888943,1.0,1.0),
	'HZJ_HToWW_ZTo2L_M125_13TeV_powheg_pythia8-v1':('MC',479288,0.0190379012045,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-1000_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-1200_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-1400_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-1800_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-2000_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-2500_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-3000_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-3500_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-4000_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-4500_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-600_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'RadionToZZToZlepZhad_narrow_M-800_13TeV-madgraph-v1':('MC',50000,0.1411818468,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-100_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-100_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-100_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-100_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-100_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v3':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-1_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-200_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-200_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-200_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-300_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-300_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-400_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_SMM_Mchi-400_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v2':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-10_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-10_Mphi-15_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-10000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-20_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-50_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_Mchi-50_Mphi-95_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-0_Mphi-20_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-100_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-200_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-350_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-40_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-50_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-50_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_pseudoscalar_NLO_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-10_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-10_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-10_Mphi-15_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-10000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-100_13TeV-madgraph_ext2-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-10_13TeV-madgraph_ext2-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-20_13TeV-madgraph_ext2-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-20_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v4':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-50_13TeV-madgraph_ext2-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-50_Mphi-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_Mchi-50_Mphi-95_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-0_Mphi-20_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-100_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-100_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-100_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-100_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-100_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-10_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-10_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-1000_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-20_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-1_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-200_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-350_Mphi-750_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-40_Mphi-100_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-50_Mphi-10_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-50_Mphi-200_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-50_Mphi-300_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-50_Mphi-350_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-50_Mphi-400_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-50_Mphi-500_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'TTbarDMJets_scalar_NLO_Mchi-50_Mphi-50_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'VBFHHTo4B_CV_1_C2V_1_C3_1_13TeV-madgraph-v1':('MC',297969,0.332929,1.0,1.0),
	'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1':('MC',6103817,FIXME,FIXME,FIXME),
	'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1':('MC',6103817,FIXME,FIXME,FIXME),
	'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext2-v1':('MC',FIXME,FIXME,FIXME,FIXME),
	'WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext3-v1':('MC',FIXME,FIXME,FIXME,FIXME),
	'WmWmJJ_13TeV-powheg-pythia8_TuneCUETP8M1-v1':('MC',150000,FIXME,FIXME,FIXME),
	'WpWpJJ_13TeV-powheg-pythia8_TuneCUETP8M1-v1':('MC',146600,FIXME,FIXME,FIXME),
	'WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',FIXME,FIXME,FIXME,FIXME),
	'WpWpJJ_EWK_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',FIXME,FIXME,FIXME,FIXME),
	'WpWpJJ_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8-v1':('MC',FIXME,FIXME,FIXME,FIXME),
	'WprimeToWZToWhadZinv_narrow_M-1000_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-1200_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-1400_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-1600_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-1800_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-2000_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-2500_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-3000_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-3500_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-4000_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-4500_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-600_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZinv_narrow_M-800_13TeV-madgraph-v1':('MC',100000,0.13482,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-1000_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-1200_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-1400_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-1600_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-1800_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-2000_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-2500_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-3000_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-3500_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-4000_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-4500_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-600_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'WprimeToWZToWhadZlep_narrow_M-800_13TeV-madgraph-v1':('MC',100000,0.068258424,1.0,1.0),
	'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-v1':('MC',2307158,FIXME,FIXME,FIXME),
	'ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_ext1-v1':('MC',FIXME,FIXME,FIXME,FIXME),
	'ZprimeToTT_M-1000_W-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'ZprimeToTT_M-1000_W-10_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'ZprimeToTT_M-500_W-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'ZprimeToTT_M-500_W-5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'ZprimeToTT_M-750_W-75_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
	'ZprimeToTT_M-750_W-7p5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1':('MC',100000,1.0,1.0,1.0),
 
}
