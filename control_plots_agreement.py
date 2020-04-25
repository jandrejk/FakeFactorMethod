import os
import ROOT
import multiprocessing as mp
ROOT.gROOT.SetBatch(True)
import time
import random
from Cuts import cuts
from Variables import Variable
from Regions import Regions

def RenameCutForDraw (cut_string) :
    return cut_string.replace("tree.","")



pre_selection_files = [
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_Wjets.root",
        "name" : "Wjets",
        "channel" : "mt",
        "year" : "2018"
    },
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_EMB.root",
        "name" : "EMB",
        "channel" : "mt",
        "year" : "2018"
    },
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_data.root",
        "name" : "data",
        "channel" : "mt",
        "year" : "2018"
    },
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_DY_J_EMB.root",
        "name" : "DY_J",
        "channel" : "mt",
        "year" : "2018"
    },
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_DY_L_EMB.root",
        "name" : "DY_L",
        "channel" : "mt",
        "year" : "2018"
    },
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_TT_J_EMB.root",
        "name" : "TT_J",
        "channel" : "mt",
        "year" : "2018"
    },
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_TT_L_EMB.root",
        "name" : "TT_L",
        "channel" : "mt",
        "year" : "2018"
    }, 
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_VV_J_EMB.root",
        "name" : "VV_J",
        "channel" : "mt",
        "year" : "2018"
    }, 
    {
        "path" : "/ceph/jandrej/fakefactors/2018_v15_test_puppi/preselection/mt/preselection_VV_L_EMB.root",
        "name" : "VV_L",
        "channel" : "mt",
        "year" : "2018"
    },
    
]

 
def FillHistos (histograms, variables, weight, tree) :
    for iv, v in enumerate(variables) :
        for h,w in list(zip(histograms,weight)) :
            h[iv].Fill( eval(v["name"]),
            w
            )  

def DR_creation(path, name, Variable, cuts) :
    preselection_file = ROOT.TFile(path)
    tree = preselection_file.Get("Events") 

    DR_cuts = " * ".join([cuts["-OS-"],cuts["-2L-"],cuts["-3L-"],cuts["-LepIso-"],cuts["-MT_DR-"],cuts["-Bpt_1-"]])
    extension = "_{}".format(name)

    print "-"*90
    print "DR cut: {}".format(DR_cuts)
    print "-"*90


    FF_Wjets = ROOT.TFile("/home/jandrej/DeepTauFFproduction/2018_v15/CMSSW_8_0_25/src/ViennaTool/fakefactor/data_mt/FF_corr_Wjets_MCsum_noGen_fitted.root") 

    Tgraph_FF_Wjets_0jet = FF_Wjets.Get("dm0_njet0")
    Tgraph_FF_Wjets_1jet = FF_Wjets.Get("dm0_njet1")
    region = "DR_Wjets"


    histogram_iso_tau           = [ROOT.TH1D(v["hist_name"]+region+"_pass","{} distribution passing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau      = [ROOT.TH1D(v["hist_name"]+region+"_fail","{} distribution failing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted = [ROOT.TH1D(v["hist_name"]+region+"_pred","{} distribution predicted in isolated tau-region".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_0jet           = [ROOT.TH1D(v["hist_name"]+region+"_pass_0jet","{} distribution passing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_0jet      = [ROOT.TH1D(v["hist_name"]+region+"_fail_0jet","{} distribution failing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet = [ROOT.TH1D(v["hist_name"]+region+"_pred_0jet","{} distribution predicted tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_1jet           = [ROOT.TH1D(v["hist_name"]+region+"_pass_1jet","{} distribution passing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_1jet      = [ROOT.TH1D(v["hist_name"]+region+"_fail_1jet","{} distribution failing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet = [ROOT.TH1D(v["hist_name"]+region+"_pred_1jet","{} distribution predicted tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    

    

    # move one indent left 
    selection_cut = DR_cuts

    nEntries = tree.GetEntries()

    passing = 0
    failing = 0



    for i in range(0, nEntries) : 
        tree.GetEntry(i)

        if ( eval(selection_cut.replace(" * ", " and ")) ) : # passes DR selection criteria

            
            if ( eval(cuts["-TauIsoPass-"]) ) : # passes tau isolation requirement
                FillHistos(tree=tree, histograms=[histogram_iso_tau], variables=Variable, weight=[tree.weight_sf])
                passing += 1
                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_geq1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])

            elif ( eval(cuts["-TauIsoFail-"])  ) : # fails tau isolation requirement
                
                # retrieve FF value
                raw_FF_value = 0
                if ( tree.njets==0 ) :
                    raw_FF_value = Tgraph_FF_Wjets_0jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                else :
                    raw_FF_value = Tgraph_FF_Wjets_1jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                
                FillHistos(tree=tree, histograms=[histogram_anti_iso_tau,histogram_iso_tau_predicted], variables=Variable, weight=[tree.weight_sf,(tree.weight_sf * raw_FF_value)])
                failing += 1
                

                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_0jet,histogram_iso_tau_predicted_0jet], variables=Variable, weight=[tree.weight_sf,(tree.weight_sf * raw_FF_value)])
                elif ( eval(cuts["-NJET_geq1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_1jet,histogram_iso_tau_predicted_1jet], variables=Variable, weight=[tree.weight_sf,(tree.weight_sf * raw_FF_value)])
                    
                
                if (tree.weight_sf * raw_FF_value < 0) :
                    print "problematic weight: {}".format(tree.weight_sf * raw_FF_value)
                    
                    

        if (i%50000 == 0) :
            print "{:8.1f} % processed".format(i/float(nEntries)*100.)  
            # if i > 100 :
            #     break      

    for iv, v in enumerate(Variable) :
        output = ROOT.TFile("{0}/{1}{2}.root".format(region,v["hist_name"],extension),"RECREATE") 

        histogram_iso_tau[iv].Write()
        histogram_iso_tau_0jet[iv].Write()
        histogram_iso_tau_1jet[iv].Write()
        
        histogram_anti_iso_tau[iv].Write()
        histogram_anti_iso_tau_0jet[iv].Write()
        histogram_anti_iso_tau_1jet[iv].Write()
    
        histogram_iso_tau_predicted[iv].Write()
        histogram_iso_tau_predicted_0jet[iv].Write()
        histogram_iso_tau_predicted_1jet[iv].Write()
    

        output.Close()


    print("# events passing tau ID: {}").format(passing)
    print("# events failing tau ID: {}").format(failing)

    print "done"
    preselection_file.Close()
    FF_Wjets.Close()


def SR_AR_Histos(path, process, channel, year, Variable, cuts, region, DR_cuts) :
    preselection_file = ROOT.TFile(path)
    tree = preselection_file.Get("Events") 
    print "events in {0}: {1}".format(process, tree.GetEntries())
    selection_cut = RenameCutForDraw(DR_cuts)
    extension = "_{}".format(process)


    histogram_iso_tau           = [ROOT.TH1D(v["hist_name"]+region+"_pass","{} distribution passing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_0jet      = [ROOT.TH1D(v["hist_name"]+region+"_pass_0jet","{} distribution passing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_1jet      = [ROOT.TH1D(v["hist_name"]+region+"_pass_1jet","{} distribution passing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_2jet      = [ROOT.TH1D(v["hist_name"]+region+"_pass_2jet","{} distribution passing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
   
    histogram_anti_iso_tau      = [ROOT.TH1D(v["hist_name"]+region+"_fail","{} distribution failing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_0jet = [ROOT.TH1D(v["hist_name"]+region+"_fail_0jet","{} distribution failing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_1jet = [ROOT.TH1D(v["hist_name"]+region+"_fail_1jet","{} distribution failing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_2jet = [ROOT.TH1D(v["hist_name"]+region+"_fail_2jet","{} distribution failing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    

    
    
    for iv, v in enumerate(Variable) :
        for h_njet, cut_njet in [["","1"],["_0jet",cuts["-NJET_0-"]],["_1jet",cuts["-NJET_1-"]],["_2jet",cuts["-NJET_geq2-"]]] :
            tree.Draw("{variable_name}>>{hist_name}".format(variable_name=RenameCutForDraw(v["name"]),hist_name=(v["hist_name"]+region+"_pass"+h_njet)),
        " * ".join([(selection_cut),RenameCutForDraw(cuts["-TauIsoPass-"]),RenameCutForDraw(cut_njet),"weight_sf"]) )
        
            tree.Draw("{variable_name}>>{hist_name}".format(variable_name=RenameCutForDraw(v["name"]),hist_name=(v["hist_name"]+region+"_fail"+h_njet)),
        " * ".join([(selection_cut),RenameCutForDraw(cuts["-TauIsoFail-"]),RenameCutForDraw(cut_njet),"weight_sf"]) ) 

            
      
    directory="{0}/{1}/{2}/".format(region,year,channel)
    if not os.path.exists(directory) :
        os.makedirs(directory)
    for iv, v in enumerate(Variable) :
        output = ROOT.TFile("{0}/{1}/{2}/{3}{4}.root".format(region,year,channel,v["hist_name"],extension),"RECREATE") 
        histogram_iso_tau[iv].Write()
        histogram_iso_tau_0jet[iv].Write()
        histogram_iso_tau_1jet[iv].Write()
        histogram_iso_tau_2jet[iv].Write()
        
        histogram_anti_iso_tau[iv].Write()
        histogram_anti_iso_tau_0jet[iv].Write()
        histogram_anti_iso_tau_1jet[iv].Write()
        histogram_anti_iso_tau_2jet[iv].Write()
        
        output.Close()
    
    preselection_file.Close()
    return 1

def Wjets_QCD_estimation(channel, year, var) :
    
    for i, sub in enumerate(["data","Wjets","EMB","DY_J","DY_L","VV_J","VV_L","TT_J","TT_L"]) :
        _file = ROOT.TFile("{0}/{1}/{2}/{3}{4}.root".format("DR_Wjets_SS",year,channel,var["hist_name"],"_{}".format(sub))) 
        if (i==0) :
            histogram_iso_tau           = _file.Get( var["hist_name"]+"DR_Wjets_SS"+"_pass").Clone(var["hist_name"]+"DR_Wjets"+"_pass")
            histogram_iso_tau_0jet      = _file.Get( var["hist_name"]+"DR_Wjets_SS"+"_pass_0jet").Clone(var["hist_name"]+"DR_Wjets"+"_pass_0jet")
            histogram_iso_tau_1jet      = _file.Get( var["hist_name"]+"DR_Wjets_SS"+"_pass_1jet").Clone(var["hist_name"]+"DR_Wjets"+"_pass_1jet")
            histogram_iso_tau_2jet      = _file.Get( var["hist_name"]+"DR_Wjets_SS"+"_pass_2jet").Clone(var["hist_name"]+"DR_Wjets"+"_pass_2jet")

            histogram_anti_iso_tau      = _file.Get( var["hist_name"]+"DR_Wjets_SS"+"_fail").Clone(var["hist_name"]+"DR_Wjets"+"_fail")
            histogram_anti_iso_tau_0jet = _file.Get( var["hist_name"]+"DR_Wjets_SS"+"_fail_0jet").Clone(var["hist_name"]+"DR_Wjets"+"_fail_0jet")
            histogram_anti_iso_tau_1jet = _file.Get( var["hist_name"]+"DR_Wjets_SS"+"_fail_1jet").Clone(var["hist_name"]+"DR_Wjets"+"_fail_1jet")
            histogram_anti_iso_tau_2jet = _file.Get( var["hist_name"]+"DR_Wjets_SS"+"_fail_2jet").Clone(var["hist_name"]+"DR_Wjets"+"_fail_2jet")

            for h in [histogram_iso_tau, histogram_iso_tau_0jet, histogram_iso_tau_1jet, histogram_iso_tau_2jet, histogram_anti_iso_tau, histogram_anti_iso_tau_0jet, histogram_anti_iso_tau_1jet, histogram_anti_iso_tau_2jet] :
                h.SetDirectory(0)
        else :
            histogram_iso_tau.Add(_file.Get( var["hist_name"]+"DR_Wjets_SS"+"_pass"),-1)
            histogram_iso_tau_0jet.Add(_file.Get( var["hist_name"]+"DR_Wjets_SS"+"_pass_0jet"),-1)
            histogram_iso_tau_1jet.Add(_file.Get( var["hist_name"]+"DR_Wjets_SS"+"_pass_1jet"),-1)
            histogram_iso_tau_2jet.Add(_file.Get( var["hist_name"]+"DR_Wjets_SS"+"_pass_2jet"),-1)

            histogram_anti_iso_tau.Add(_file.Get( var["hist_name"]+"DR_Wjets_SS"+"_fail"),-1)
            histogram_anti_iso_tau_0jet.Add(_file.Get( var["hist_name"]+"DR_Wjets_SS"+"_fail_0jet"),-1)
            histogram_anti_iso_tau_1jet.Add(_file.Get( var["hist_name"]+"DR_Wjets_SS"+"_fail_1jet"),-1)
            histogram_anti_iso_tau_2jet.Add(_file.Get( var["hist_name"]+"DR_Wjets_SS"+"_fail_2jet"),-1)
        _file.Close()
    
    output = ROOT.TFile("{0}/{1}/{2}/{3}{4}.root".format("DR_Wjets",year,channel,var["hist_name"],"_{}".format("QCD")),"RECREATE") 
    for h in [histogram_iso_tau, histogram_iso_tau_0jet, histogram_iso_tau_1jet, histogram_iso_tau_2jet, histogram_anti_iso_tau, histogram_anti_iso_tau_0jet, histogram_anti_iso_tau_1jet, histogram_anti_iso_tau_2jet] :
        h.Write()
    output.Close()   
    

    return 1

def CreateFractions(channel, year, var, region) :
    for i, proc in enumerate(["data","QCD","EMB","DY_J","DY_L","VV_J","VV_L","TT_J","TT_L"]) :
        _file = ROOT.TFile("{0}/{1}/{2}/{3}{4}.root".format(region,year,channel,var["hist_name"],"_{}".format(proc))) 
        if (i==0) :
            histogram_anti_iso_tau      = _file.Get( var["hist_name"]+region+"_fail").Clone(var["hist_name"]+region+"_ARfraction")
            histogram_anti_iso_tau_0jet = _file.Get( var["hist_name"]+region+"_fail_0jet").Clone(var["hist_name"]+region+"_ARfraction_0jet")
            histogram_anti_iso_tau_1jet = _file.Get( var["hist_name"]+region+"_fail_1jet").Clone(var["hist_name"]+region+"_ARfraction_1jet")
            histogram_anti_iso_tau_2jet = _file.Get( var["hist_name"]+region+"_fail_2jet").Clone(var["hist_name"]+region+"_ARfraction_2jet")
            
            tot      = _file.Get( var["hist_name"]+region+"_fail").Clone()
            tot_0jet = _file.Get( var["hist_name"]+region+"_fail_0jet").Clone()
            tot_1jet = _file.Get( var["hist_name"]+region+"_fail_1jet").Clone()
            tot_2jet = _file.Get( var["hist_name"]+region+"_fail_2jet").Clone()

            

            for h in [histogram_anti_iso_tau, histogram_anti_iso_tau_0jet, histogram_anti_iso_tau_1jet, histogram_anti_iso_tau_2jet, tot, tot_0jet, tot_1jet, tot_2jet] :
                h.SetDirectory(0)
        else :
            histogram_anti_iso_tau.Add(_file.Get( var["hist_name"]+region+"_fail").Clone(var["hist_name"]+region+"_ARfraction"),-1)
            histogram_anti_iso_tau_0jet.Add(_file.Get( var["hist_name"]+region+"_fail_0jet").Clone(var["hist_name"]+region+"_ARfraction_0jet"),-1)
            histogram_anti_iso_tau_1jet.Add(_file.Get( var["hist_name"]+region+"_fail_1jet").Clone(var["hist_name"]+region+"_ARfraction_1jet"),-1)
            histogram_anti_iso_tau_2jet.Add(_file.Get( var["hist_name"]+region+"_fail_2jet").Clone(var["hist_name"]+region+"_ARfraction_2jet"),-1)
        
        _file.Close()
    
    histogram_anti_iso_tau.Divide(tot)
    histogram_anti_iso_tau_0jet.Divide(tot_0jet)
    histogram_anti_iso_tau_1jet.Divide(tot_1jet)
    histogram_anti_iso_tau_2jet.Divide(tot_2jet)
    
    output = ROOT.TFile("{0}/{1}/{2}/{3}{4}.root".format("DR_Wjets",year,channel,var["hist_name"],"_{}".format("fracWjets")),"RECREATE") 
    for h in [histogram_anti_iso_tau, histogram_anti_iso_tau_0jet, histogram_anti_iso_tau_1jet, histogram_anti_iso_tau_2jet] :
        h.Write()
    output.Close()   
    

    return 1

   


def PrintAndWait (path, path2, value=0) :
    n = random.randint(1,5)
    print "file: {} wait for: {} sec".format(path,n)
    time.sleep(n)
    print "file: {} ----- finished".format(path)
# start = time.time()
# pool = mp.Pool(2)
# for pre in pre_selection_files[:5] :
#     pool.apply_async(PrintAndWait,args=(pre["name"],pre["path"]))
# pool.close()
# pool.join()
# print "execution time: {}".format(time.time()-start)

s = time.time()
######## make SR and AR like histos ######
# pool = mp.Pool(3)
# for pre in pre_selection_files :
#     pool.apply_async(SR_AR_Histos,
#         args=(
#         pre["path"],
#         pre["name"],
#         pre["channel"],
#         pre["year"],
#         Variable[:1],
#         cuts,
#         Regions[0]["name"],
#         Regions[0]["selection"]
#         )
#     )
# pool.close()
# pool.join()

######## QCD estimation ######
# for var in Variable :
#     Wjets_QCD_estimation(channel=pre_selection_files[0]["channel"], year=pre_selection_files[0]["year"], var=var) 

######## W+jets fractions in DR Wjets ######
for var in Variable :
    CreateFractions(channel=pre_selection_files[0]["channel"], year=pre_selection_files[0]["year"], var=var, region="DR_Wjets")

print "execution time: {}".format(time.time()-s)
