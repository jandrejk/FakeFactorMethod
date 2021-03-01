year=2016
output_dir=$1
channel=$2

prefix=${output_dir}/${year}/${channel}


if [[ "${channel}" = "et" ]] 
then
    echo "hadd'ing et channel..."
    hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_Data.root ${prefix}/tmp/SingleElectron*.root 
    hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_EMB.root ${prefix}/tmp/Embedding2016*ElTau*.root 
fi

if [[ "${channel}" = "mt" ]] 
then
    echo "hadd'ing mt channel..."
    hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_Data.root ${prefix}/tmp/SingleMuon*.root &
    hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_EMB.root ${prefix}/tmp/Embedding2016*MuTau*.root &
fi

if [[ "${channel}" = "tt" ]] 
then
    echo "hadd'ing tt channel..."
    hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_Data.root ${prefix}/tmp/Tau*.root
    hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_EMB.root ${prefix}/tmp/Embedding2016*TauTau*.root
fi


hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_DY.root ${prefix}/tmp/DY*.root ${prefix}/tmp/EWKZ2Jets*.root 
hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_WJets.root ${prefix}/tmp/W*JetsToLNu*.root ${prefix}/tmp/EWKW*2JetsWToLNuM50*.root 
hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_TT.root ${prefix}/tmp/TTTo*.root 
hadd -f -n 4 ${prefix}/${channel}-NOMINAL_ntuple_VV.root ${prefix}/tmp/WZTo*.root ${prefix}/tmp/ZZTo*.root ${prefix}/tmp/VVTo*.root ${prefix}/tmp/STt*.root 

#cp ${prefix}/TT_*/*.root et-NOMINAL_ntuple_TT.root 


