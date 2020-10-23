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
from Variables_mt import Variable
from presel_2018_mt import pre_selection_files


s = time.time()
DEBUG=False
bkg = "all"

if (bkg == "Wjets" or bkg == "all") :
    ###### make SR and AR like histos ######
    for r in Regions[:2] :
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
                r["name"],
                r["selection"]
                )
            )
        pool.close()
        pool.join()

    ######## QCD estimation ######
    for var in Variable :
        util.Wjets_QCD_estimation(channel=pre_selection_files[0]["channel"], year=pre_selection_files[0]["year"], var=var) 

    ######## W+jets fractions in DR Wjets ######
    for var in Variable :
        util.CreateFractions(
            channel=pre_selection_files[0]["channel"], 
            year=pre_selection_files[0]["year"], 
            var=var, 
            region="DR_Wjets",
            ListOfFiles=["data","QCD","EMB","DY_J","DY_L","VV_J","VV_L","TT_J","TT_L"]
        )

    print "start heavy duty calculation"
    util.DR_creation(
        path=pre_selection_files[0]["path"], 
        pathRawFF=pre_selection_files[0]["pathRawFFWjets"], 
        pathClosCorr=pre_selection_files[0]["pathClosCorrWJets"],    
        name=pre_selection_files[0]["path"], 
        Variable=Variable, 
        cuts=cuts, 
        region=Regions[0]["name"], 
        DR_cuts=Regions[0]["selection"],
        channel=pre_selection_files[0]["channel"], 
        year=pre_selection_files[0]["year"],
        debug=DEBUG,
    ) 
    print "execution time: {}".format(time.time()-s)

if (bkg == "QCD" or bkg == "all") :
    print "QCD closure plots"
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
            Regions[2]["name"],
            Regions[2]["selection"]
            )
        )
    pool.close()
    pool.join()

    ######## QCD fractions in DR QCD ######
    for var in Variable :
        util.CreateFractions(
            channel=pre_selection_files[0]["channel"], 
            year=pre_selection_files[0]["year"], 
            var=var, 
            region="DR_QCD",
            ListOfFiles=["data","Wjets","EMB","DY_J","DY_L","VV_J","VV_L","TT_J","TT_L"]
        )

    print "start heavy duty calculation"
    util.DR_creationQCD(
        path=pre_selection_files[0]["path"], 
        pathRawFF=pre_selection_files[0]["pathRawFFQCD"], 
        pathClosCorr=pre_selection_files[0]["pathClosCorrQCD"],
        name=pre_selection_files[0]["path"], 
        Variable=Variable, 
        cuts=cuts, 
        region=Regions[2]["name"], 
        DR_cuts=Regions[2]["selection"],
        channel=pre_selection_files[0]["channel"], 
        year=pre_selection_files[0]["year"],
        debug=DEBUG,
    ) 
    print "execution time: {}".format(time.time()-s)

if (bkg == "TTbar" or bkg == "all") :
    print "TTbar closure plots"
    ###### make SR and AR like histos ######
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
            Regions[3]["name"],
            Regions[3]["selection"]
            )
        )
    pool.close()
    pool.join()

    ######## TTbar fractions in DR TTbar ######
    for var in Variable :
        util.CreateFractions(
            channel=pre_selection_files[0]["channel"], 
            year=pre_selection_files[0]["year"], 
            var=var, 
            region="DR_TTbar",
            ListOfFiles=["data","data","TT_J"],
            # ListOfFiles=["data","Wjets","EMB","DY_J","DY_L","VV_J","VV_L","TT_L"],
            TTbar=True
        )

    print "start heavy duty calculation"
    util.DR_creationTTbar(
        path=pre_selection_files[0]["path"], 
        pathRawFF=pre_selection_files[0]["pathRawFFTTbar"], 
        pathClosCorr=pre_selection_files[0]["pathClosCorrTTbar"],
        name=pre_selection_files[0]["path"], 
        Variable=Variable, 
        cuts=cuts, 
        region=Regions[3]["name"], 
        DR_cuts=Regions[3]["selection"],
        channel=pre_selection_files[0]["channel"], 
        year=pre_selection_files[0]["year"],
        debug=DEBUG,
    ) 
    print "execution time: {}".format(time.time()-s)
