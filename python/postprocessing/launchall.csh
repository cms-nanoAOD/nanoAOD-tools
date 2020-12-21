#python makedd.py --pathin  /eos/user/a/adeiorio/Wprime/nosynch/v14/plot --pathout  /eos/user/a/adeiorio/Wprime/nosynch/v14/plot_rebin
#python makedd.py --pathin  /eos/user/a/adeiorio/Wprime/nosynch/v14/plot -c electron --pathout /eos/user/a/adeiorio/Wprime/nosynch/v14/plot_rebin
#python makedd.py --pathin localhisto/v14/ --plotpath plot_28_11 -c electron --pathout  localhisto/test_nonorm_v14/
#python makedd.py --pathin  /eos/user/a/adeiorio/Wprime/nosynch/v14/plot -c electron --pathout localhisto/test_2_v14/


#python makedd.py --pathin localhisto/v15/  --plotpath plot_11_12 -c muon --pathout localhisto/test_nonorm_v15/
#python makedd.py --pathin localhisto/v15/  -y 2017 --plotpath plot_11_12 -c muon --pathout localhisto/test_nonorm_v15/
#python makedd.py --pathin localhisto/v15/  -y 2018 --plotpath plot_11_12 -c muon --pathout localhisto/test_nonorm_v15/

python makedd.py --pathin $EOSSPACE/Wprime/nosynch/v15/plot4DD  --plotpath plot_11_12 -c electron --pathout localhisto/test_nonorm_v15/
python makedd.py --pathin $EOSSPACE/Wprime/nosynch/v15/plot4DD  -y 2017 --plotpath plot_11_12 -c electron --pathout localhisto/test_nonorm_v15/
python makedd.py --pathin $EOSSPACE/Wprime/nosynch/v15/plot4DD  -y 2018 --plotpath plot_11_12 -c electron --pathout localhisto/test_nonorm_v15/
