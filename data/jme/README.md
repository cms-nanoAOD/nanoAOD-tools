# JEC and JER files

## 2018
Added 1.10.19 - [JEC - V19](https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC) and [JER - V7](https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution) 

### Data: Downloaded file Autumn18\_RunsABCD\_V19\_DATA.tar

Repackaged `.tar` because of different structure (sub archives for each run, each archive contains folder with files)
Also nanoAOD postprocessor is hardcoded to use compressed archives.

```bash
mkdir tmp
cd tmp
cp ../Autumn18_RunsABCD_V19_DATA.tar .
tar xvf Autumn18_RunsABCD_V19_DATA.tar
rm Autumn18_RunsABCD_V19_DATA.tar
for FILE in ./*; do tar xvf $FILE; rm $FILE; done
for FOLDER in ./*; do cp $FOLDER/* .; rm -rf $FOLDER; done
tar cvfz Autumn18_V19_DATA.tgz *.txt
mv Autumn18_V19_DATA.tgz ../
cd ..
rm -rf tmp
```

### Simulation

#### JEC: Downloaded file Autumn18\_V19\_MC.tar

Repackaged `.tar` to `.tgz` because nanoAOD expects compressed achives.

```bash
mkdir tmp
cd tmp
cp ../Autumn18_V19_MC.tar .
tar xvf Autumn18_V19_MC.tar
rm Autumn18_V19_MC.tar
tar cvfz Autumn18_V19_MC.tgz *.txt
cp Autumn18_V19_MC.tgz ../
cd ..
rm -rf tmp/
```
#### JER: Downloaded file Autumn18_V7_MC.tar

```bash
mkdir tmp
cd tmp/
mv ../Autumn18_V7_MC.tar  .
tar xvf Autumn18_V7_MC.tar
rm Autumn18_V7_MC.tar
tar cvfz Autumn18_V7_MC.tgz *.txt
mv Autumn18_V7_MC.tgz ../
cd ..
rm -rf tmp/
```
