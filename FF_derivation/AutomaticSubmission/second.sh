WP_pass='16'
WP_fail='4'
EXT='FF_LQ_v2p2'
VER='v2p2'
USER='janik.andrejkovic'

for ERA in 2016 #2017 2018 
do
    for CHANNEL in et #mt tt
    do
       sh first.sh $ERA $CHANNEL $WP_pass $WP_fail $EXT $VER $USER &
    done
done
wait

# _VVVLOOSE         1 
# _VVLOOSE          2
# _VLOOSE           4 
# _LOOSE            8
# _MEDIUM          16
# _TIGHT           32 
# _VTIGHT          64
# _VVTIGHT        128