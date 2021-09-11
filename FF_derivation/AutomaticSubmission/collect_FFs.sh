#!/bin/bash

version=$1

for YEAR in 2016 2017 2018
do 
    for CHANNEL in et mt tt
    do
        mkdir -p FF_${version}/${YEAR}/${CHANNEL}
        # ls -ltrh /ceph/jandrej/auto-fakefactors/16_4_${YEAR}_FF_LQ_${version}/${CHANNEL}/inclusive/fakeFactors_tight.root
        rsync -avztcp /ceph/jandrej/auto-fakefactors/16_4_${YEAR}_FF_LQ_${version}/${CHANNEL}/inclusive/fakeFactors_tight.root FF_${version}/${YEAR}/${CHANNEL}/fakeFactors.root
        ls -ltrh FF_${version}/${YEAR}/${CHANNEL}/fakeFactors.root
        echo "-----------------------------"
    
    done
done
