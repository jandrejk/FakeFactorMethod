WP=$1
for YEAR in 2016 2017 2018
do 
    for CHANNEL in et mt tt
    do
        mkdir -p plots_${WP}/FF/${YEAR}/${CHANNEL}
        rsync -avztcp ${YEAR}/${CHANNEL}/CMSSW_8_0_25/src/ViennaTool/Images_EMB/data_${CHANNEL}/ff_*.pdf plots_${WP}/FF/${YEAR}/${CHANNEL}/
        rsync -avztcp ${YEAR}/${CHANNEL}/CMSSW_8_0_25/src/ViennaTool/Images_EMB/data_${CHANNEL}/ff_*.png plots_${WP}/FF/${YEAR}/${CHANNEL}/
        rsync -avztcp ${YEAR}/${CHANNEL}/CMSSW_8_0_25/src/ViennaTool/Images_EMB/data_${CHANNEL}/corr_*.png plots_${WP}/FF/${YEAR}/${CHANNEL}/
        rsync -avztcp ${YEAR}/${CHANNEL}/CMSSW_8_0_25/src/ViennaTool/Images_EMB/data_${CHANNEL}/corr_*.pdf plots_${WP}/FF/${YEAR}/${CHANNEL}/
        rsync -avztcp ${YEAR}/${CHANNEL}/CMSSW_8_0_25/src/ViennaTool/Images_EMB/data_${CHANNEL}/uncertainties*.png plots_${WP}/FF/${YEAR}/${CHANNEL}/
        rsync -avztcp ${YEAR}/${CHANNEL}/CMSSW_8_0_25/src/ViennaTool/Images_EMB/data_${CHANNEL}/uncertainties*.pdf plots_${WP}/FF/${YEAR}/${CHANNEL}/
    done
done


