from __future__ import absolute_import, print_function

import re
from optparse import OptionParser
from sys import argv, exit, stderr, stdout
import argparse as arg

from six.moves import range

# import ROOT with a fix to get batch mode (http://root.cern.ch/phpBB3/viewtopic.php?t=3198)
import ROOT

ROOT.gROOT.SetBatch(True)



def Get_Norm_N_error(errors=False,InFile = "",year = "UL2017"):
        Combine_year_tag={
                'UL2016preVFP' :  "_ULpre16",
                'UL2016postVFP' : "_ULpost16",
                'UL2017' : "_UL17",
                'UL2018' : "_UL18"}

        file = ROOT.TFile.Open(InFile)
        prefit = file.Get("norm_prefit")
        fit_s = file.Get("norm_fit_s")
        fit_b = file.Get("norm_fit_b")
        if prefit == None:
            stderr.write("Missing fit_s in %s. Did you run FitDiagnostics in a recent-enough version of combine and with --saveNorm?\n" % file)
        if fit_s == None:
            raise RuntimeError("Missing fit_s in %s. Did you run FitDiagnostics with --saveNorm?" % file)
        if fit_b == None:
            raise RuntimeError("Missing fit_b in %s. Did you run FitDiagnostics with --saveNorm?" % file)
        
        iter = fit_s.createIterator()
        # Headline = "%-30s %-30s     pre-fit   signal+background Fit  bkg-only Fit"%("Channel","Process") if (prefit and errors) else "%-30s %-30s  signal+background Fit  bkg-only Fit"%("Channel","Process")
        if prefit and errors:
            headrow = ["Channel", "Process", "Pre-Fit", "S+B-Fit", "B-Only-Fit"]
            headline = ("{:40} {:25} {:^25} {:^25} {:^25}").format(*headrow)
        elif prefit:
            headrow = ["Channel", "Process", "Pre-Fit", "S+B-Fit", "B-Only-Fit"]
            headline = ("{:40} {:25} {:>20} {:>20} {:>20}").format(*headrow)
        else:
            headrow = ["Channel", "Process", "S+B-Fit", "B-Only-Fit"]
            headline = ("{:40} {:25} {:>20} {:>20}").format(*headrow)
        
        line = "".join(["-" for i in range(len(headline))])
        print(headline)
        print(line)
        print(type(Combine_year_tag[year]))
        Norm_N_errors = {
                'eljets'+Combine_year_tag[year] :{ 
                        'EWK_bkg'+Combine_year_tag[year]:{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 } 
                        },
                        'QCD_DD'+Combine_year_tag[year]:{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }      
                        },
                        'top_sig_1725'+Combine_year_tag[year]:{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                        'top_bkg_1725'+Combine_year_tag[year]:{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                        'total_background':{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                        'total_signal':{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                        'total':{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                },
                'mujets'+Combine_year_tag[year]:{ 
                        'EWK_bkg'+Combine_year_tag[year]:{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 } 
                        },
                        'QCD_DD'+Combine_year_tag[year]:{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }      
                        },
                        'top_sig_1725'+Combine_year_tag[year]:{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                        'top_bkg_1725'+Combine_year_tag[year]:{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                        'total_background':{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                        'total_signal':{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                        'total':{
                                'Pre-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'S+B-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }, 'B-Only-Fit' :{ 'Norm': 0.0, 'Error': 0.0 }
                        },
                }
        }
        while True:
            norm_s = iter.Next()
            if norm_s == None:
                break
            norm_b = fit_b.find(norm_s.GetName())
            norm_p = prefit.find(norm_s.GetName()) if prefit else None
            # we have to replace any non-standard characters with "_" otherwise the matching will screw up
            proc_chan_name = (norm_s.GetName()).replace(".", "_").replace(":", "_").replace(",", "_")
            m = re.match(r"(\w+)/(\w+)", proc_chan_name)
            if m == None:
                m = re.match(r"n_exp_(?:final_)?(?:bin)+(\.\w+)_proc_(\.\w+)", proc_chan_name)
            if m == None:
                raise RuntimeError("Non-conforming object name %s" % norm_s.GetName())
            if norm_b == None:
                raise RuntimeError("Missing normalization %s for background fit" % norm_s.GetName())
            if prefit and norm_p and errors:
                if m.group(1) in Norm_N_errors.keys():
                        Norm_N_errors[m.group(1)][m.group(2)]['Pre-Fit']['Norm'] = round(norm_p.getVal(),3)
                        Norm_N_errors[m.group(1)][m.group(2)]['Pre-Fit']['Error'] = round(norm_p.getError(),3)
                        Norm_N_errors[m.group(1)][m.group(2)]['S+B-Fit']['Norm'] = round(norm_s.getVal(),3)
                        Norm_N_errors[m.group(1)][m.group(2)]['S+B-Fit']['Error'] = round(norm_s.getError(),3)
                        Norm_N_errors[m.group(1)][m.group(2)]['B-Only-Fit']['Norm'] = round(norm_b.getVal(),3)
                        Norm_N_errors[m.group(1)][m.group(2)]['B-Only-Fit']['Error'] = round(norm_b.getError(),3)
        
                row = [
                    "%-40s" % m.group(1),
                    "%-25s" % m.group(2),
                    "%10.3f +/- %-10.3f" % (norm_p.getVal(), norm_p.getError()),
                    "%10.3f +/- %-10.3f" % (norm_s.getVal(), norm_s.getError()),
                    "%10.3f +/- %-10.3f" % (norm_b.getVal(), norm_b.getError()),
                ]
                print(("{:<40} {:25} {:10} {:10} {:10}").format(*row))
        
                """row_check = [
                    "%-40s" % m.group(1),
                    "%-25s" % m.group(2),
                    "%10.3f +/- %-10.3f" % (Norm_N_errors[m.group(1)][m.group(2)]['Pre-Fit']['Norm'],Norm_N_errors[m.group(1)][m.group(2)]['Pre-Fit']['Error']),
                    "%10.3f +/- %-10.3f" % (Norm_N_errors[m.group(1)][m.group(2)]['S+B-Fit']['Norm'],Norm_N_errors[m.group(1)][m.group(2)]['S+B-Fit']['Error']),
                    "%10.3f +/- %-10.3f" % (Norm_N_errors[m.group(1)][m.group(2)]['B-Only-Fit']['Norm'],Norm_N_errors[m.group(1)][m.group(2)]['B-Only-Fit']['Error']),
                ]
                print(("{:<40} {:25} {:10} {:10} {:10}").format(*row_check))"""
        
                # print "%-30s %-30s % 7.3f +/- % 7.3f % 7.3f +/- % 7.3f  % 7.3f +/- % 7.3f" %
            else:
                if norm_p and prefit:
                    row = [
                        "%-40s" % m.group(1),
                        "%-25s" % m.group(2),
                        "%10.3f" % (norm_p.getVal()),
                        "%10.3f" % (norm_s.getVal()),
                        "%10.3f" % (norm_b.getVal()),
                    ]
                    print(("{:<40} {:25} {:>20} {:>20} {:>20}").format(*row))
                    # print "%-30s %-30s %7.3f %7.3f %7.3f" % (m.group(1), m.group(2), norm_p.getVal(),  norm_s.getVal(),  norm_b.getVal())
                else:
                    row = [
                        "%-40s" % m.group(1),
                        "%-25s" % m.group(2),
                        "%10.3f" % (norm_s.getVal()),
                        "%10.3f" % (norm_b.getVal()),
                    ]
                    print(("{:<40} {:25} {:>20} {:>20}").format(*row))
        print(Norm_N_errors,"\n")
        print("if all the entries are zeo the you muest to the cmsenv from here /home/mikumar/t3store3/workarea/Higgs_Combine/CMSSW_11_3_4/src/\n")
        return Norm_N_errors
if __name__ == "__main__":

        """parser = OptionParser(usage="usage: %prog [options] in.root  \nrun with --help to get list of options")
        parser.add_option(
        "-u",
        "--uncertainties",
        default=False,
        action="store_true",
        help="Report the uncertainties from the fit(s) too",
        )


        (options, args) = parser.parse_args()

        if len(args) == 0:
                parser.print_usage()
                exit(1)

        errors = False
        if options.uncertainties:
                errors = True"""

        parser = arg.ArgumentParser(description='inputs discription')
        parser.add_argument('-u', '--uncertainties', dest='uncertainties', type=bool, nargs=1, help=" includes errors as well 0 or 1")
        parser.add_argument('-y', '--years', dest='years', type=str, nargs=1, help=" UL2016preVFP, UL2016postVFP, UL2017, UL2018")
        parser.add_argument('-f', '--InFile ', dest='InFile', type=str, nargs=1, help="In put fitdiagnostic file  i.e /home/mikumar/t3store3/workarea/Higgs_Combine/CMSSW_11_3_4/src/Combine_Run2/fitDiagnostics_M1725_DNNfit_UL2017.root ")
        args = parser.parse_args()

        InFile = args.InFile[0]
        errors = args.uncertainties[0]
        year = args.years[0]
        print(args)
        Get_Norm_N_error(errors,InFile,year)
