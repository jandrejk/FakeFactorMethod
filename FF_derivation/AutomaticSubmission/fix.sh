#!/bin/bash

chan='mt'
channel='kMU'

# chan='et'
# channel='kEL'

# chan='tt'
# channel='kTAU'

echo "This script needs manual adjustments"
exit


for year in 2016 2017 2018
do

    cd ${year}/${chan}/CMSSW_8_0_25/src
    ./convert_inputs
    python cpTDHaftPublic.py --destination /ceph/jandrej/auto-fakefactors/16_4_${year}_FF_LQ_v1p1/ --channel ${channel} --doNjetBinning 0
    python producePublicFakeFactors.py --input /ceph/jandrej/auto-fakefactors/16_4_${year}_FF_LQ_v1p1/ --channel ${channel} --njetbinning 0
    cd -
done 


exit
for year in 2016 2017 2018
do
    for CHAN in et mt tt 
    do
        cd ${year}/${CHAN}/CMSSW_8_0_25/src
        make -B -j 4
        ./fitFakeFactors
        cd -
    done
done 
