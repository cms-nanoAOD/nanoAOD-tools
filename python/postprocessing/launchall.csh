#/eos/user/a/adeiorio/Wprime/nosynch/v15/plot/
#python makedd.py --pathin localhisto/v15/  -y 2017 --plotpath plot_11_12 -c muon --pathout localhisto/test_nonorm_v15/


python makedd.py --pathin localhisto/v15/  -y 2016 --plotpath plot_11_12 -c muon --pathout localhisto/test_nonorm_v15/
python makedd.py --pathin localhisto/v15/  -y 2018 --plotpath plot_11_12 -c muon --pathout localhisto/test_nonorm_v15/
python makedd.py --pathin localhisto/v15/  -y 2017 --year_sf 2018 --plotpath plot_11_12 -c muon --pathout localhisto/test_nonorm_v15/

python makedd.py --pathin localhisto/v15/  -y 2016 --plotpath plot_11_12 -c electron --pathout localhisto/test_nonorm_v15/
python makedd.py --pathin localhisto/v15/  -y 2018 --plotpath plot_11_12 -c electron --pathout localhisto/test_nonorm_v15/
python makedd.py --pathin localhisto/v15/  -y 2017 --year_sf 2018 --plotpath plot_11_12 -c electron --pathout localhisto/test_nonorm_v15/


