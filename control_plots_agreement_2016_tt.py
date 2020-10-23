import os
import ROOT
import multiprocessing as mp
ROOT.gROOT.SetBatch(True)
import time
import random
from Cuts import cuts
from Regions import Regions
import utilities as util

# change here the apropriate config file
from Variables_tt import Variable
from presel_2016_tt import pre_selection_files


s = time.time()
DEBUG=False
bkg = "QCD"
ttchan = True

if (bkg == "QCD" or bkg == "all") :
    print "QCD closure plots"
    if (ttchan == True) :   
        QCD_Region = Regions[4]
    else :
        QCD_Region = Regions[2]
    # ####### make SR and AR like histos ######
    pool = mp.Pool(3)
    for pre in pre_selection_files :
        pool.apply_async(util.SR_AR_Histos,
            args=(
            pre["path"],
            pre["name"],
            pre["channel"],
            pre["year"],
            Variable,
            cuts,
            QCD_Region["name"],
            QCD_Region["selection"]
            )
        )
    pool.close()
    pool.join()

    ####### QCD fractions in DR QCD ######
    for var in Variable :
        util.CreateFractions(
            channel=pre_selection_files[0]["channel"], 
            year=pre_selection_files[0]["year"], 
            var=var, 
            region=QCD_Region["name"],
            ListOfFiles=["data","Wjets","EMB","DY_J","DY_L","VV_J","VV_L","TT_J","TT_L"]
        )

    print "start heavy duty calculation"
    util.DR_creationQCDttchan(
        path=pre_selection_files[0]["path"], 
        pathRawFF=pre_selection_files[0]["pathRawFFQCD"], 
        pathClosCorr=pre_selection_files[0]["pathClosCorrQCD"],
        pathPtClosCorr=pre_selection_files[0]["pathClosCorrQCDPT"],
        name=pre_selection_files[0]["path"], 
        Variable=Variable, 
        cuts=cuts, 
        region=QCD_Region["name"], 
        DR_cuts=QCD_Region["selection"],
        channel=pre_selection_files[0]["channel"], 
        year=pre_selection_files[0]["year"],
        debug=DEBUG,
    ) 
    print "execution time: {}".format(time.time()-s)
