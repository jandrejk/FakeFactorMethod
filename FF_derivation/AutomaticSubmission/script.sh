ERA=$1
CHANNEL=$2
PASS=$3
FAIL=$4
EXT=$5
source /cvmfs/grid.cern.ch/emi3ui-latest/etc/profile.d/setup-ui-example.sh
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
mkdir ${ERA}/${CHANNEL} -p
cd ${ERA}/${CHANNEL}
cmsrel CMSSW_8_0_25
cd CMSSW_8_0_25/src/; cmsenv

git clone https://github.com/jandrejk/FakeFactor.git -b FF_DeepTau_MSSM_${ERA}_v0 . #use of MSSM HTT analysis
# git clone https://github.com/jandrejk/FakeFactor.git -b FF_DeepTau_LQ_${ERA} . #use of LQ analysis
# git clone https://github.com/jandrejk/FakeFactor.git -b FF_DeepTau_${ERA}_v15_v7 . #use of SM HTT
git clone https://github.com/CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes
cd HTTutilities/Jet2TauFakes
git checkout v0.2.1
cd ../../
scram b -j 8
mkdir /ceph/jandrej/auto-fakefactors/${PASS}_${FAIL}_${ERA}_${EXT}/${CHANNEL} -p
mkdir /ceph/jandrej/auto-fakefactors/${PASS}_${FAIL}_${ERA}_${EXT}/${CHANNEL}/sim -p
mkdir /ceph/jandrej/auto-fakefactors/${PASS}_${FAIL}_${ERA}_${EXT}/${CHANNEL}/Images_EMB -p

if [ "$CHANNEL" == "et" ];  then f_chan="kEL"; fi
if [ "$CHANNEL" == "mt" ];  then f_chan="kMU"; fi
if [ "$CHANNEL" == "tt" ]; then f_chan="kTAU"; fi
sed -i 's#selCHAN\s*kMU#selCHAN      '${f_chan}'#g' ViennaTool/Settings.h
sed -i 's#selCHAN\s*kEL#selCHAN      '${f_chan}'#g' ViennaTool/Settings.h
sed -i 's#selCHAN\s*kTAU#selCHAN      '${f_chan}'#g' ViennaTool/Settings.h
sed -i 's#CHAN\s*=\s*kMU#CHAN     = '${f_chan}'#g' ViennaTool/Settings.h
sed -i 's#CHAN\s*=\s*kEL#CHAN     = '${f_chan}'#g' ViennaTool/Settings.h
sed -i 's#CHAN\s*=\s*kTAU#CHAN     = '${f_chan}'#g' ViennaTool/Settings.h
sed -i 's#wpTightFulfill.*#wpTightFulfill = '${PASS}';#g' ViennaTool/Settings.h
sed -i 's#wpLooseFulfill.*#wpLooseFulfill  = '${FAIL}';#g' ViennaTool/Settings.h
sed -i 's#wpLooseFail.*#wpLooseFail    = '${PASS}';#g' ViennaTool/Settings.h

sed -i 's#output_folder =.*#output_folder ="/ceph/jandrej/auto-fakefactors/'${PASS}'_'${FAIL}'_'${ERA}'_'${EXT}'/";#g' ViennaTool/Settings.h
sed -i 's#analysis.*#analysis ="'${PASS}'_'${FAIL}'_'${ERA}'_'${EXT}'";#g' ViennaTool/Settings.h
# sed -i 's#DEBUG=0#DEBUG    ='1'#g' ViennaTool/Settings.h

make -B
cd ViennaTool

echo -ne '\n' | ./steerAll.sh 1 KIT 0