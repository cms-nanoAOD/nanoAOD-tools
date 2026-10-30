#---------------------------------------------
#copy the output from remote machine to the lxplus
#this is specific code if hadd did not happen then we need to tranfer the skim files
#------------------------------------------------
transfer_FILE=tree.root
if [ -f "$transfer_FILE" ]; then
    echo "$transfer_FILE exists. Tranfering .... "
    xrdcp -f tree.root ${outputroot}
else
    echo "$transfer_FILE does not exist."
    path="${outputroot%/*}" # extact the file path
    echo "$transfer_FILE exists. Tranfering skim file to $path"
    for f in *_Skim.root; do xrdcp -f ${f} ${path}"/"${f}; done
    xrdcp -f *_Skim.root ${path}"/"
fi
