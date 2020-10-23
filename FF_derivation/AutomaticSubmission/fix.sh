#!/bin/bash

chan='mt'
channel='kMU'

# for year in 2016 #2017 2018
# do
    
#     cd ${year}/${chan}/CMSSW_8_0_25/src
#     ./convert_inputs
#     python cpTDHaftPublic.py --destination /ceph/jandrej/auto-puppi-fakefactors/16_4_${year}_v7/ --channel ${channel} --doNjetBinning 0
#     python producePublicFakeFactors.py --input /ceph/jandrej/auto-puppi-fakefactors/16_4_${year}_v7/ --channel ${channel} --njetbinning 0
#     cd -
# done 

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