WP_pass='16'
WP_fail='4'
EXT='FF_LQ_v2p2'
VER='v2p2'
USER='janik.andrejkovic'

#switch back pre-sel and put 3 hours wall-time
for ERA in 2016 2018 #2016 2017 2018 
do
    for CHANNEL in "mt" #"et" "mt" "tt"
    do
        if [[ ("$CHANNEL" == "mt") && ($ERA -eq 2018) ]]
        then
            # 2018 mt needs more walltime and memory
            submit "sh first.sh $ERA $CHANNEL $WP_pass $WP_fail $EXT $VER $USER" --walltime 03:00:00 --memory 8 --title "FF_$ERA\_$CHANNEL\_$WP_pass\_$WP_fail\_$EXT"
        else
            submit "sh first.sh $ERA $CHANNEL $WP_pass $WP_fail $EXT $VER $USER" --walltime 02:00:00 --title "FF_$ERA\_$CHANNEL\_$WP_pass\_$WP_fail\_$EXT"

        fi
    done
done
# wait

# _VVVLOOSE         1 
# _VVLOOSE          2
# _VLOOSE           4 
# _LOOSE            8
# _MEDIUM          16
# _TIGHT           32 
# _VTIGHT          64
# _VVTIGHT        128