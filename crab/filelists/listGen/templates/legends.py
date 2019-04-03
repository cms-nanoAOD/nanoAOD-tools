samples = {
    ##DATA
    'data_obs' : {
        'order' : 0,
        'files' : [
            ] + [
            ] + [
            ] + [
            ],
        'fillcolor' : 0,
        'fillstyle' : 1,
        'linecolor' : 1,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "Data",
        'weight': 1.,
        'plot': True,
    },
    ## DY
    'DYJetsToLL' : {
        'order' : 1,
        'files' : [
            ],
        'fillcolor' : 418,
        'fillstyle' : 1001,
        'linecolor' : 418,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "Z(ll) + jets",
        'weight': 1.,
        'plot': True,
    },
    'DYJetsToLL_Pt' : {
        'order' : 2,
        'files' : [
            ],
        'fillcolor' : 418,
        'fillstyle' : 1001,
        'linecolor' : 418,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "Z(ll) + jets",
        'weight': 1.,
        'plot': True,
        },
    ## WJET
    'WJetsToLNu' : {
        'order' : 3,
        'files' : [
            ],
        'fillcolor' : 881,
        'fillstyle' : 1001,
        'linecolor' : 881,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "W(l#nu) + jets",
        'weight': 1.,
        'plot': True,
    },
    ##TTBAR
    'TTbar' : {
        'order' : 4,
        'files' : [
            ],
        'fillcolor' : 798,
        'fillstyle' : 1001,
        'linecolor' : 798,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "t#bar{t}",#, single t
        'weight': 1.,
        'plot': True,
    },
    'TTbar-DiLep' : {
        'order' : 4,
        'files' : [
            ],
        'fillcolor' : 41,
        'fillstyle' : 1001,
        'linecolor' : 798,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "t#bar{t} di-lept",#, single t
        'weight': 1.,
        'plot': True,
    },
    'TTbar-SL' : {
        'order' : 4,
        'files' : [
            ],
        'fillcolor' : 798,
        'fillstyle' : 1001,
        'linecolor' : 798,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "t#bar{t} sing.lept",
        'weight': 1.,
        'plot': True,
    },
    #ST
    'ST' : {
        'order' : 5,
        'files' : [
            ],
        'fillcolor' : 801,
        'fillstyle' : 1001,
        'linecolor' : 801,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "Single-t",
        'weight': 1.,
        'plot': True,
        },
    #VV
    'WZ' : {
        'order' : 7,
        'files' : [  
            ],
        'fillcolor' : 602,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "WZ",
        'weight': 1.,
        'plot': True,
        },
     'WW' : {
        'order' : 9,
        'files' : [
            ],
        'fillcolor' : 7,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "W+W-",
        'weight': 1.,
        'plot': True,
        },
    'ZZ' : {
        'order' : 8,
        'files' : [
            ],
        'fillcolor' : 9,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "ZZ",
        'weight': 1.,
        'plot': True,
        },
    'VV' : {
        'order' : 8,
        'files' : [
            ],
        'fillcolor' : 9,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "WW, WZ, ZZ",
        'weight': 1.,
        'plot': True,
    },
    ## Ht
    'ttH' : {
        'order' : 10,
        'files' : [
            ],
        'fillcolor' : 30,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "ttH",
        'weight': 1.,
        'plot': True,
        },
    ##ttV
    'ttV' : {
        'order' : 10,
        'files' : [
            ],
        'fillcolor' : 38,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "ttW,ttZ,ttH",
        'weight': 1.,
        'plot': True,
        },
    #VVV
    'VVV' : {
        'order' : 11,
        'files' : [
            ],
        'fillcolor' : 46,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "WWW,WWZ",
        'weight': 1.,
        'plot': True,
        },
    'WWJJ' : {
        'order' : 9,
        'files' : [
            ],
        'fillcolor' : 8,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "W+W+,W-W-",
        'weight': 1.,
        'plot': True,
        },
    'VGamma' : {
        'order' : 6,
        'files' : [
            ],
        'fillcolor' : 42,
        'fillstyle' : 1001,
        'linecolor' : 602,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "W#gamma,Z#gamma",
        'weight': 1.,
        'plot': True,
        },
    #Signal
    'WHWW' : {
        'order' : 1001,
        'files' : [
            ],
        'fillcolor' : 623,
        'fillstyle' : 3005,
        'linecolor' : 632,
        'linewidth' : 3,
        'linestyle' : 1,
        'label' : "WHWW",
        'weight': 1.,
        'plot': True,
        },
    'QCD' : {
        'order' : 6,
        'files' : [
            ],
        'fillcolor' : 921,
        'fillstyle' : 1001,
        'linecolor' : 921,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "multijet",
        'weight': 1.,
        'plot': True,
    },
    #signal
    'VH': {
        'order' : 0,
        'files' : [
            ],
        'fillcolor' : 3,
        'fillstyle' : 3003,
        'linecolor' : 3,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "VH",
        'weight': 1.,
        'plot': True,
        },    
    # Dummy entry for background sum
    'BkgSum' : {
        'order' : 0,
        'files' : [],
        'fillcolor' : 3,
        'fillstyle' : 1001,
        'linecolor' : 3,
        'linewidth' : 2,
        'linestyle' : 1,
        'label' : "MC stat.",
        'weight': 1.,
        'plot': True,
    },
 
}
