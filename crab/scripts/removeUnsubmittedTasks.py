import os
version = "PROD_2_0"

crabFolder = "/home/users/sdonato/scratchssd/crab/"
command = "crab tasks | grep SUBMITFAILED -B2 | grep crab_%s"%(version)
print command
failedTasks = os.popen ( command ).read().split("\n")
for failedTask in failedTasks:
    if version in failedTask:
        failedTask = "crab_"+failedTask.split("_crab_")[-1]
        command = "rm -rf %s/%s"%(crabFolder, failedTask)
        print command
#        os.popen ( command ).read()
