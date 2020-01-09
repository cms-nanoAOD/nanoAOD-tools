mcproduction ={
    '2016':'RunIISummer16',
    '2017':'RunIIFall17',
    '2018':'RunIIAutumn18',
}

def checkDatasets(datasetsNames, variableDict):
    return True
    failures = []
    alldatasets = set()
    for datasetsName in datasetsNames:
        datasets = variableDict[datasetsName]
        for sample in datasets.keys():
            for dataset in datasets[sample]:
                ok = False
                if dataset in alldatasets:
                    failures.append(dataset)
                else:
                    alldatasets.add(dataset)
                if datasetsName.startswith("data"):
                    year = datasetsName[len("data"):]
                    if year in sample:
                        run = sample[len("SingleMuon"):]
                        if run in dataset: ok = True
                elif datasetsName.startswith("mc"):
                    year = datasetsName[len("mc"):]
                    if year in sample and mcproduction[year] in dataset: ok = True
                if not ok: failures.append((datasetsName,sample,dataset))
    if len(failures)==0: 
        return True
    else:
        raise Exception("ERROR in checkDatasets(%s).\nProblems with %s"%(datasetsNames, failures))
        return False

def checkModuleSettings(moduleSettings,datamc,year,era):
    datamc_  = moduleSettings.split("201")[0]
    year_    = "201" + moduleSettings.split("201")[1]
    era_     = ''
    if len(year_) == 5:
        era_ = year_[4]
        year_ = year_[0:4]
    if datamc_ == datamc and year_ == str(year) and (era_ == era or era_ ==''):
        return True
    else:
        raise Exception("ERROR in checkModuleSettings(%s, %s, %s, %s)"%(moduleSettings,datamc,year,era))
        return False

def checkModulesToBeCalled(modulesToBeCalled):
    specialWords = [
        'mc', 'data'
    ]
    specialWords = specialWords + [''.join((i, j)) for i in ['2016','2017','2018'] for j in ['','A','B','C','D','E','F','G','H']]
    for run in modulesToBeCalled:
        for module in modulesToBeCalled[run]:
            for specialWord in specialWords:
                module = module.replace("All","")
                if specialWord.lower() in module.lower() and not specialWord.lower() in run.lower(): raise Exception("ERROR in checkModulesToBeCalled(%s).\nProblems with %s %s %s"%(modulesToBeCalled, run, module, specialWord))
    return True

def checkModuleSettingsFromFileName(filename, modulesettings):
    modulesettingsFile = ''
    if "RunIIAutumn18" in filename: modulesettingsFile =  'mc2018'
    elif "RunIIFall17" in filename: modulesettingsFile =  'mc2017'
    elif "RunIISummer16" in filename: modulesettingsFile =  'mc2016'
    elif "Run2016" in filename: modulesettingsFile =  'data2016'
    elif "Run2017" in filename: modulesettingsFile =  'data2017'
    elif "Run2018A" in filename: modulesettingsFile =  'data2018A'
    elif "Run2018B" in filename: modulesettingsFile =  'data2018B'
    elif "Run2018C" in filename: modulesettingsFile =  'data2018C'
    elif "Run2018D" in filename: modulesettingsFile =  'data2018D'
    if modulesettingsFile and modulesettingsFile!=modulesettings:
        raise Exception("ERROR in checkModuleSettingsFromFileName(%s, %s). modulesettingsFile is %s"%(filename, modulesettings, modulesettingsFile))
    print ("checkModuleSettingsFromFileName - Warning: Unable to find module settings for %s"%filename)
