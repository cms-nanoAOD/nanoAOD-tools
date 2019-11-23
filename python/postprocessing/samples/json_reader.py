import json

def json_reader(json_name):
    file_coll = []
    redirect = 'root://cms-xrd-global.cern.ch/'
    with open(json_name) as f:
        filenames = json.load(f)
    for filename in filenames: 
        file_coll.append(redirect+str(filename['file'][0]['name']))
    #print file_coll
    return file_coll
