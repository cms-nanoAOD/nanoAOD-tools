def get_DNNFit_rescale_parameters(DNNFit_rescale_file, year, lep, tag):
    """
    If a DNNFit rescale file is provided, read the normalization (postfit and prefit)
    values and compute new rescale parameters along with their constraints.
    
    Parameters:
      DNNFit_rescale_file (str or None): Path to the file with DNNFit rescale parameters.
      year (str): The data-taking year.
      lep (str): Lepton type (e.g. "el" or "mu").
      tag (str): A tag string used in the histogram naming (e.g. "_myTag").
      
    Returns:
      dict: A dictionary containing the following keys:
            - 'top_sig_DNNfitrescale'
            - 'top_bkg_DNNfitrescale'
            - 'EWK_bkg_DNNfitrescale'
            - 'QCD_bkg_DNNfitrescale'
            - 'top_sig_cons'
            - 'top_bkg_cons'
            - 'EWK_bkg_cons'
            - 'QCD_bkg_cons'
            
            If DNNFit_rescale_file is None, the function returns None.
    """

    print("===================== geting new DNNFit rescale parapmeters =================")
    print("Reading the Normalization form the " + DNNFit_rescale_file)
    Norm_and_error_from_fit = Get_Norm_N_error(errors=True, InFile=DNNFit_rescale_file, year=year)

    # Get postfit normalization values
    top_sig_norm_postfit = Norm_and_error_from_fit[lep + 'jets' + tag]['top_sig_1725' + tag]['S+B-Fit']['Norm']
    top_bkg_norm_postfit = Norm_and_error_from_fit[lep + 'jets' + tag]['top_bkg_1725' + tag]['S+B-Fit']['Norm']
    EWK_bkg_norm_postfit = Norm_and_error_from_fit[lep + 'jets' + tag]['EWK_bkg' + tag]['S+B-Fit']['Norm']
    QCD_bkg_norm_postfit = Norm_and_error_from_fit[lep + 'jets' + tag]['QCD_DD' + tag]['S+B-Fit']['Norm']

    print("\n new postfit Norms: \n top_sig_1725 : %s, top_bkg_1725 : %s, EWK_bkg : %s, QCD_DD : %s" %
          (top_sig_norm_postfit, top_bkg_norm_postfit, EWK_bkg_norm_postfit, QCD_bkg_norm_postfit))

    # Get prefit normalization values
    top_sig_norm_prefit = Norm_and_error_from_fit[lep + 'jets' + tag]['top_sig_1725' + tag]['Pre-Fit']['Norm']
    top_bkg_norm_prefit = Norm_and_error_from_fit[lep + 'jets' + tag]['top_bkg_1725' + tag]['Pre-Fit']['Norm']
    EWK_bkg_norm_prefit = Norm_and_error_from_fit[lep + 'jets' + tag]['EWK_bkg' + tag]['Pre-Fit']['Norm']
    QCD_bkg_norm_prefit = Norm_and_error_from_fit[lep + 'jets' + tag]['QCD_DD' + tag]['Pre-Fit']['Norm']

    print("\n new prefit Norms: \n top_sig_1725 : %s, top_bkg_1725 : %s, EWK_bkg : %s, QCD_DD : %s" %
          (top_sig_norm_prefit, top_bkg_norm_prefit, EWK_bkg_norm_prefit, QCD_bkg_norm_prefit))

    # Calculate constraints as percentage uncertainties (choose the worst-case from el and mu)
    top_sig_cons_el = (Norm_and_error_from_fit['eljets' + tag]['top_sig_1725' + tag]['S+B-Fit']['Error'] /
                       Norm_and_error_from_fit['eljets' + tag]['top_sig_1725' + tag]['S+B-Fit']['Norm']) * 100
    top_sig_cons_mu = (Norm_and_error_from_fit['mujets' + tag]['top_sig_1725' + tag]['S+B-Fit']['Error'] /
                       Norm_and_error_from_fit['mujets' + tag]['top_sig_1725' + tag]['S+B-Fit']['Norm']) * 100
    top_sig_cons = top_sig_cons_el if top_sig_cons_el >= top_sig_cons_mu else top_sig_cons_mu

    top_bkg_cons_el = (Norm_and_error_from_fit['eljets' + tag]['top_bkg_1725' + tag]['S+B-Fit']['Error'] /
                       Norm_and_error_from_fit['eljets' + tag]['top_bkg_1725' + tag]['S+B-Fit']['Norm']) * 100
    top_bkg_cons_mu = (Norm_and_error_from_fit['mujets' + tag]['top_bkg_1725' + tag]['S+B-Fit']['Error'] /
                       Norm_and_error_from_fit['mujets' + tag]['top_bkg_1725' + tag]['S+B-Fit']['Norm']) * 100
    top_bkg_cons = top_bkg_cons_el if top_bkg_cons_el >= top_bkg_cons_mu else top_bkg_cons_mu

    EWK_bkg_cons_el = (Norm_and_error_from_fit['eljets' + tag]['EWK_bkg' + tag]['S+B-Fit']['Error'] /
                       Norm_and_error_from_fit['eljets' + tag]['EWK_bkg' + tag]['S+B-Fit']['Norm']) * 100
    EWK_bkg_cons_mu = (Norm_and_error_from_fit['mujets' + tag]['EWK_bkg' + tag]['S+B-Fit']['Error'] /
                       Norm_and_error_from_fit['mujets' + tag]['EWK_bkg' + tag]['S+B-Fit']['Norm']) * 100
    EWK_bkg_cons = EWK_bkg_cons_el if EWK_bkg_cons_el >= EWK_bkg_cons_mu else EWK_bkg_cons_mu

    QCD_bkg_cons_el = (Norm_and_error_from_fit['eljets' + tag]['QCD_DD' + tag]['S+B-Fit']['Error'] /
                       Norm_and_error_from_fit['eljets' + tag]['QCD_DD' + tag]['S+B-Fit']['Norm']) * 100
    QCD_bkg_cons_mu = (Norm_and_error_from_fit['mujets' + tag]['QCD_DD' + tag]['S+B-Fit']['Error'] /
                       Norm_and_error_from_fit['mujets' + tag]['QCD_DD' + tag]['S+B-Fit']['Norm']) * 100
    QCD_bkg_cons = QCD_bkg_cons_el if QCD_bkg_cons_el >= QCD_bkg_cons_mu else QCD_bkg_cons_mu

    print("\n new constraints : \n top_sig_1725 : %s , top_bkg_1725 : %s , EWK_bkg : %s , QCD_DD : %s  \n" %
          (round(top_sig_cons, 2), round(top_bkg_cons, 2), round(EWK_bkg_cons, 2), round(QCD_bkg_cons, 2)))

    # Calculate the rescale factors (postfit/prefit)
    top_sig_DNNfitrescale = top_sig_norm_postfit / top_sig_norm_prefit
    top_bkg_DNNfitrescale = top_bkg_norm_postfit / top_bkg_norm_prefit
    EWK_bkg_DNNfitrescale = EWK_bkg_norm_postfit / EWK_bkg_norm_prefit
    QCD_bkg_DNNfitrescale = QCD_bkg_norm_postfit / QCD_bkg_norm_prefit

    print("===================== successfully got new DNNFit rescale parapmeters =================")

    # Return a dictionary with the rescale factors and constraints.
    return {
        'top_sig_DNNfitrescale': top_sig_DNNfitrescale,
        'top_bkg_DNNfitrescale': top_bkg_DNNfitrescale,
        'EWK_bkg_DNNfitrescale': EWK_bkg_DNNfitrescale,
        'QCD_bkg_DNNfitrescale': QCD_bkg_DNNfitrescale,
        'top_sig_cons': top_sig_cons,
        'top_bkg_cons': top_bkg_cons,
        'EWK_bkg_cons': EWK_bkg_cons,
        'QCD_bkg_cons': QCD_bkg_cons
    }
