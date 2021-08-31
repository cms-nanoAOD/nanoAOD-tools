'''
Class to get Tau Trigger SF based on 2017 Rereco data
and MCv2 (re-miniaod).
T. Ruggles
5 February, 2018
Updated 12 August, 2018
Updated 16 Feb, 2019
Source: https://github.com/cms-tau-pog/TauTriggerSFs
'''
import os
import ROOT
from math import sqrt
datapath  = os.path.join(os.environ.get('CMSSW_BASE','CMSSW_BASE'),"src/PhysicsTools/NanoAODTools/python/postprocessing/data/tau")


class TauTriggerSFTool :
    

    def __init__( self, trigger, year=2017, tauWP='medium', wpType='MVAv2', path=datapath ):

        self.trigger = trigger
        assert( self.trigger in ['ditau', 'mutau', 'etau'] ), "Choose from: 'ditau', 'mutau', 'etau' triggers."
        self.year = year
        # Default to loading the Tau MVAv2 Medium ID based WPs
        self.tauWP = tauWP
        self.wpType = wpType
        assert( self.tauWP in ['vloose', 'loose', 'medium', 'tight', 'vtight', 'vvtight'] ), "You must choose a WP from: vloose, loose, medium, tight, vtight, or vvtight"
        assert( self.wpType in ['MVAv2', 'dR0p3'] ), "Choose from two provided ID types: 'MVAv2', 'dR0p3'. 'MVAv2' uses dR0p5, and 'dR0p3' is also an MVA-based ID."
        assert( self.wpType == 'MVAv2' ), "Tau POG is currently only providing efficiencies for MVAv2, sorry."
        assert( self.year in [2016, 2017, 2018] ), "Choose which year trigger efficiencies you need."
        print("Loading Efficiencies for trigger %s usingTau %s ID WP %s for year %i" % (self.trigger, self.wpType, self.tauWP, self.year))

        # Assume this is in CMSSW with the below path structure
        self.f = ROOT.TFile(os.path.join(path,'tauTriggerEfficiencies%i.root'%self.year),'r')


        ## Load the TF1s containing the analytic best-fit results.
        ## This is done per decay mode: 0, 1, 10.
        self.fitDataMap = {}
        self.fitMCMap = {}
        self.fitDataMap[ 0 ] = ROOT.gDirectory.Get('%s_%s%s_dm0_DATA_fit' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitDataMap[ 1 ] = ROOT.gDirectory.Get('%s_%s%s_dm1_DATA_fit' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitDataMap[ 10 ] = ROOT.gDirectory.Get('%s_%s%s_dm10_DATA_fit' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitMCMap[ 0 ] = ROOT.gDirectory.Get('%s_%s%s_dm0_MC_fit' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitMCMap[ 1 ] = ROOT.gDirectory.Get('%s_%s%s_dm1_MC_fit' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitMCMap[ 10 ] = ROOT.gDirectory.Get('%s_%s%s_dm10_MC_fit' % (self.trigger, self.tauWP, self.wpType ) )
        

        # Load the TH1s containing the analytic best-fit result in 1 GeV incriments and the associated uncertainty.
        # This is done per decay mode: 0, 1, 10.
        self.fitUncDataMap = {}
        self.fitUncMCMap = {}
        self.fitUncDataMap[ 0 ] = self.f.Get('%s_%s%s_dm0_DATA_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitUncDataMap[ 1 ] = self.f.Get('%s_%s%s_dm1_DATA_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitUncDataMap[ 10 ] = self.f.Get('%s_%s%s_dm10_DATA_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitUncMCMap[ 0 ] = self.f.Get('%s_%s%s_dm0_MC_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitUncMCMap[ 1 ] = self.f.Get('%s_%s%s_dm1_MC_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        self.fitUncMCMap[ 10 ] = self.f.Get('%s_%s%s_dm10_MC_errorBand' % (self.trigger, self.tauWP, self.wpType ) )
        
         # Load the TH1s containing the bin by bin values
        self.binnedSFMap = {}
        self.binnedSFMap[ 0 ] = self.f.Get('%s_%s%s_dm0_CoarseBinSF' % (self.trigger, self.tauWP, self.wpType) )
        self.binnedSFMap[ 1 ] = self.f.Get('%s_%s%s_dm1_CoarseBinSF' % (self.trigger, self.tauWP, self.wpType) )
        self.binnedSFMap[ 10 ] = self.f.Get('%s_%s%s_dm10_CoarseBinSF' % (self.trigger, self.tauWP, self.wpType) )

        # Because of low statistics in the problem region of the barrel, we apply the Eta-Phi corrections
        # based on taus firing mutau trigger and passing the vloose MVA WP. This provides the most statistically
        # robust measurement for the correction. Considering the three Eta-Phi regions should not have significantly
        # different SF adjustments for different MVA WPs, this should also be a safe choice.
        etaPhiWP = 'vloose'
        etaPhiTrigger = 'mutau'
        # Load the TH2s containing the eta phi efficiency corrections
        # This is done per decay mode: 0, 1, 10.
        self.effEtaPhiDataMap = {}
        self.effEtaPhiMCMap = {}
        self.effEtaPhiDataMap[ 0 ] = self.f.Get('%s_%s%s_dm0_DATA' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiDataMap[ 1 ] = self.f.Get('%s_%s%s_dm1_DATA' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiDataMap[ 10 ] = self.f.Get('%s_%s%s_dm10_DATA' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiMCMap[ 0 ] = self.f.Get('%s_%s%s_dm0_MC' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiMCMap[ 1 ] = self.f.Get('%s_%s%s_dm1_MC' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiMCMap[ 10 ] = self.f.Get('%s_%s%s_dm10_MC' % (etaPhiTrigger, etaPhiWP, self.wpType) )


        # Eta Phi Averages
        # This is done per decay mode: 0, 1, 10.
        self.effEtaPhiAvgDataMap = {}
        self.effEtaPhiAvgMCMap = {}
        self.effEtaPhiAvgDataMap[ 0 ] = self.f.Get('%s_%s%s_dm0_DATA_AVG' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiAvgDataMap[ 1 ] = self.f.Get('%s_%s%s_dm1_DATA_AVG' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiAvgDataMap[ 10 ] = self.f.Get('%s_%s%s_dm10_DATA_AVG' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiAvgMCMap[ 0 ] = self.f.Get('%s_%s%s_dm0_MC_AVG' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiAvgMCMap[ 1 ] = self.f.Get('%s_%s%s_dm1_MC_AVG' % (etaPhiTrigger, etaPhiWP, self.wpType) )
        self.effEtaPhiAvgMCMap[ 10 ] = self.f.Get('%s_%s%s_dm10_MC_AVG' % (etaPhiTrigger, etaPhiWP, self.wpType) )


    # Make sure we stay on our histograms
    def ptCheck( self, pt ) :
        if pt > 450 : pt = 450
        elif pt < 20 : pt = 20
        return pt

    # Make sure to have only old DMs, DM0, DM1, DM10
    def dmCheck( self, dm ) :
        if dm == 2 : dm = 1   # Originally, DM=2 was included in oldDM, but with the dynamic strip clustering the second strip was reconstructed together with the first one. So it ends up to DM=1. But, there are still some cases where DM=2 survives.
        return dm

    def getEfficiency( self, pt, eta, phi, fit, uncHist, etaPhiHist, etaPhiAvgHist, uncert='Nominal') :
        pt = self.ptCheck( pt )
        eff = fit.Eval( pt )

        # Shift the pt dependent efficiency by the fit uncertainty if requested
        if uncert != 'Nominal' :
            assert( uncert in ['Up', 'Down'] ), "Uncertainties are provided using 'Up'/'Down'"
            if uncert == 'Up' :
                eff += uncHist.GetBinError( uncHist.FindBin( pt ) )
            else : # must be Down
                eff -= uncHist.GetBinError( uncHist.FindBin( pt ) )

        # Adjust SF based on (eta, phi) location
        # keep eta barrel boundaries within SF region
        # but, for taus outside eta limits or with unralistic
        # phi values, return zero SF
        if eta == 2.1 : eta = 2.09
        elif eta == -2.1 : eta = -2.09

        etaPhiVal = etaPhiHist.GetBinContent( etaPhiHist.FindBin( eta, phi ) )
        etaPhiAvg = etaPhiAvgHist.GetBinContent( etaPhiAvgHist.FindBin( eta, phi ) )
        if etaPhiAvg <= 0.0 :
            print("One of the provided tau (eta, phi) values (%3.3f, %3.3f) is outside the boundary of triggering taus"%(eta,phi))
            print("Returning efficiency = 0.0")
            return 0.0

        eff *= etaPhiVal / etaPhiAvg
        if eff > 1. : eff = 1.
        if eff < 0. : eff = 0. # Some efficiency fits go negative at very low tau pT, prevent that.
        return eff


    # return the data efficiency or the +/- 1 sigma uncertainty shifted efficiency
    def getTriggerEfficiencyData( self, pt, eta, phi, dm) :
        dm = self.dmCheck( dm )
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitDataMap[ dm ], self.fitUncDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ], 'Nominal')
    def getTriggerEfficiencyDataUncertUp( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency(  pt, eta, phi, self.fitDataMap[ dm ], self.fitUncDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ], 'Up' )
    def getTriggerEfficiencyDataUncertDown( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitDataMap[ dm ], self.fitUncDataMap[ dm ], \
            self.effEtaPhiDataMap[ dm ], self.effEtaPhiAvgDataMap[ dm ], 'Down' )


    # return the MC efficiency or the +/- 1 sigma uncertainty shifted efficiency
    def getTriggerEfficiencyMC( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], self.fitUncMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ], 'Nominal')
    def getTriggerEfficiencyMCUncertUp( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], self.fitUncMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ], 'Up'  )
    def getTriggerEfficiencyMCUncertDown( self, pt, eta, phi, dm ) :
        dm = self.dmCheck( dm )
        assert( dm in [0, 1, 10] ), "Efficiencies only provided for DMs 0, 1, 10.  You provided DM %i" % dm
        return self.getEfficiency( pt, eta, phi, self.fitMCMap[ dm ], self.fitUncMCMap[ dm ], \
            self.effEtaPhiMCMap[ dm ], self.effEtaPhiAvgMCMap[ dm ], 'Down' )


    def getBinnedScaleFactor (self, pt, dm, sfHisto) :
        pt = self.ptCheck( pt )
        dm = self.dmCheck( dm )
        sf = sfHisto.GetBinContent(sfHisto.FindBin( pt ))
        return sf

    def getBinnedScaleFactorUnc(self, pt,  dm, sfHisto) :
        pt = self.ptCheck( pt )
        dm = self.dmCheck( dm )
        SFunc = sfHisto.GetBinError( sfHisto.FindBin( pt ) )
        return SFunc

	# return the data/MC scale factor
    def getTriggerScaleFactor( self, pt, eta, phi, dm) :
        pt = self.ptCheck( pt )
        dm = self.dmCheck( dm )
        effData = self.getTriggerEfficiencyData( pt, eta, phi, dm )
        effMC = self.getTriggerEfficiencyMC( pt, eta, phi, dm )
        if effMC < 1e-5 :
            print("Eff MC is suspiciously low. Please contact Tau POG.")
            print(" - %s Trigger SF for Tau ID: %s   WP: %s   pT: %f   eta: %s   phi: %f"%(self.trigger,self.wpType,self.tauWP,pt,eta,phi))
            print(" - MC Efficiency = %f"%effMC)
            return 0.0

        if(self.year == 2016):
            if(self.trigger == 'ditau'): pt_recommended = 40
            elif(self.trigger == 'mutau' or self.trigger  == 'etau'): pt_recommended = 25

            if( pt > pt_recommended):
                if(effMC!=0): sf = effData / effMC
                else:
                    sf = 0
                    print("The efficiency is zero in either Data or MC histogram, so SF is set to zero")
            else:
                sf = self.getBinnedScaleFactor(pt, dm, self.binnedSFMap[ dm])

        elif(self.year==2017 or self.year == 2018):
            if(effData!=0 and effMC!=0): sf = effData / effMC
            else:
                sf = 0
                print("The efficiency is zero in either Data or MC histogram, so SF is set to zero")

        return sf


    # return the data/MC scale factor with +1/-1 sigma uncertainty.
    # Data and MC fit uncertainties are treated as uncorrelated.
    # The calculated uncertainties are symmetric. Do error propagation
    # for simple division. Using getTriggerEfficiencyXXXUncertDown instead
    # of Up ensures we have the full uncertainty reported. Up sometimes
    # is clipped by efficiency max of 1.0.
    def getTriggerScaleFactorUncert( self, pt, eta, phi, dm, uncert) :
        assert( uncert in ['Up', 'Down'] ), "Uncertainties are provided using 'Up'/'Down'"
        pt = self.ptCheck( pt )
        dm = self.dmCheck( dm )
        effData = self.getTriggerEfficiencyData( pt, eta, phi, dm )
        effDataDown = self.getTriggerEfficiencyDataUncertDown( pt, eta, phi, dm )
        if(effData!=0): relDataDiff = (effData - effDataDown) / effData

        effMC = self.getTriggerEfficiencyMC( pt, eta, phi, dm)
        effMCDown = self.getTriggerEfficiencyMCUncertDown( pt, eta, phi, dm )
        if effMC < 1e-5 :
            # already printed an error for the nominal case...
            return 0.0
        if(effMC!=0): relMCDiff = (effMC - effMCDown) / effMC

        sf_fit = effData / effMC
        sf_binned =  self.getBinnedScaleFactor(pt, dm, self.binnedSFMap[ dm])

        deltaSF_fit = sqrt( relDataDiff**2 + relMCDiff**2 )
        deltaSF_binned =  self.getBinnedScaleFactorUnc(pt, dm, self.binnedSFMap[ dm])

        if(effMC!=0): relMCDiff = (effMC - effMCDown) / effMC
        if(self.year == 2016):
            if(self.trigger == 'ditau'): pt_recommended = 40
            elif(self.trigger == 'mutau' or self.trigger  == 'etau'): pt_recommended = 25

            if( pt > pt_recommended):
                sf = sf_fit
                deltaSF = deltaSF_fit
            else:
                sf= sf_binned
                deltaSF = deltaSF_binned
        else:
            sf = sf_fit
            deltaSF = deltaSF_fit

        if uncert == 'Up' :
            return sf * (1. + deltaSF)
        else : # must be Down
            return sf * (1. - deltaSF)
    

