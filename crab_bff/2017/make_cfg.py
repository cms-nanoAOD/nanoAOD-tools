from crab_cfg_mc import template
from crab_cfg_data import template_data
import re

with open('data.list', 'r') as f:
    for fname in f.readlines():
        post = "{}_{}".format(fname.split('/')[1], fname.split('/')[2])
        crab_dict = {
       'NanoPost1':post,
       'NanoTestPost':post,
       'das':fname.replace('\n','')} 

        with open('cfg/'+post+'_cfg.py', 'w') as f2:
            f2.write(template_data.format(**crab_dict))

with open('mc.list', 'r') as f:
    for fname in f.readlines():
        post = "{}_{}".format(fname.split('/')[1], fname.split('/')[2])[:50]
        crab_dict = {
        'NanoPost1':post,
        'NanoTestPost':post,
        'das':fname.replace('\n','')} 

        with open('cfg/'+post[:95]+'_cfg.py', 'w') as f2:
            f2.write(template.format(**crab_dict))
