import subprocess

with open('mc.list', 'r') as f:
    for line in f.readlines():
        line = line.replace('\n','').split('/')
        _,prefix,middle,end = line
        batcmd="dasgoclient --query='dataset=/{}/{}/{}'".format(prefix[:5]+"*",'*RunIISummer16NanoAODv7*',end)
        print(batcmd)
        result = subprocess.check_output(batcmd, shell=True)
        print(result)
        #with open(prefix+'.list', 'w') as f:
        #    f.write(result)

