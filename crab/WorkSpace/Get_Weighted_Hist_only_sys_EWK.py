from Get_Histogram_after_DNN_cuts import get_histogram_with_DNN_cut
def get_Weight_sys_EWK(lep,year,Variable,channels_weight_sys,MCcut,DNNcut,hist_sys_name,File_with_mtwMassFit_weight_Iso,Fpaths_DNN_apply,EWK_cons,Fpaths_sys_samples=None):
    QCDcut=""
    Datacut=""
    if(Fpaths_sys_samples==None):
        if(Variable=="TMath::Log(topMass)"): Variable="lntopMass"
        hists_corr_weight_sys,hists_wron_weight_sys =  get_histogram_with_DNN_cut(
            lep=lep,
            year=year,
            Variable=Variable,
            channels=channels_weight_sys, 
            MCcut=MCcut ,
            QCDcut=QCDcut, 
            Datacut=Datacut , 
            DNNcut=DNNcut ,
            Filepaths_with_QCDWeight = File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_score = Fpaths_DNN_apply,
            Fpaths_sys_samples = Fpaths_sys_samples
        )
        if(Variable=="lntopMass"):   Variable="TMath::Log(topMass)"
    else:
        hists_corr_weight_sys,hists_wron_weight_sys =  get_histogram_with_DNN_cut(
            lep=lep,
            year=year,
            Variable=Variable,
            channels=channels_weight_sys, 
            MCcut=MCcut ,
            QCDcut=QCDcut, 
            Datacut=Datacut , 
            DNNcut=DNNcut ,
            Filepaths_with_QCDWeight = File_with_mtwMassFit_weight_Iso,
            Fpaths_DNN_score = Fpaths_DNN_apply,
            Fpaths_sys_samples = Fpaths_sys_samples
        )


    hist_corr_assig_weight_sys = {}
    hist_wron_assig_weight_sys = {}
    for channel_no,channel in enumerate(channels_weight_sys):
        hist_corr_assig_weight_sys[channel] = hists_corr_weight_sys[channel_no].Clone()
        hist_wron_assig_weight_sys[channel] = hists_wron_weight_sys[channel_no].Clone()
    del hists_corr_weight_sys
    del hists_wron_weight_sys

    EWK_weight_sys = hist_corr_assig_weight_sys['WJetsToLNu_0J'].Clone()
    EWK_weight_sys.Add(hist_wron_assig_weight_sys['WJetsToLNu_0J'])
    for channel in ['WJetsToLNu_1J', 'WJetsToLNu_2J', 'DYJetsToLL', 'WWTo2L2Nu', 'WZTo2Q2L', 'ZZTo2Q2L']:
        EWK_weight_sys.Add(hist_corr_assig_weight_sys[channel])
        EWK_weight_sys.Add(hist_wron_assig_weight_sys[channel])

    EWK_weight_sys.Print()

    return EWK_weight_sys