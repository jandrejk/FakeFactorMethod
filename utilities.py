import os
import ROOT
ROOT.gROOT.SetBatch(True)
from Cuts import cuts
# from Variables import Variable
# from Regions import Regions
# from presel_2016_mt4 import pre_selection_files

def RenameCutForDraw (cut_string) :
    return cut_string.replace("tree.","") 

def FillHistos (histograms, variables, weight, tree) :
    for iv, v in enumerate(variables) :
        for h,w in list(zip(histograms,weight)) :
            h[iv].Fill( eval(v["name"]),
            w 
            )  

def FillHistosPredicted (histograms, variables, weight, fractions, tree) :
    for iv, v in enumerate(variables) :
        fraction_weight = GetFractionFromHistogram(fractions[iv],eval(v["name"]))
        # h_index = 0
        for h,w in list(zip(histograms,weight)) :
            # if (h_index == 2 ) :
            #     # print "fill measured FF histo"
            #     pt = eval(v["name"])
            #     if ( pt > 60 and pt < 110 ) :
            #         # print pt
            #         w = weight[1] # use FFfit
            # h_index += 1
            h[iv].Fill( eval(v["name"]),
            w * fraction_weight
            )    

def GetFractionFromHistogram (histogram, xvalue) :
    return histogram.GetBinContent(histogram.GetXaxis().FindBin(xvalue))

def GetFFfromHistogram (histogram, xvalue) :
    return histogram.GetBinContent(histogram.GetXaxis().FindBin(xvalue))

def DR_creation(path, pathRawFF, pathClosCorr, channel, year, name, Variable, cuts, region, DR_cuts, debug=False) :
    preselection_file = ROOT.TFile(path)
    tree = preselection_file.Get("Events") 
    pathFractions="{0}/{1}/{2}".format(region,year,channel)
    extension = "_{}".format(name)

    FF_Wjets = ROOT.TFile(pathRawFF) 
    Tgraph_FF_Wjets_0jet = FF_Wjets.Get("dm0_njet0")
    Tgraph_FF_Wjets_1jet = FF_Wjets.Get("dm0_njet1")
    Tgraph_FF_Wjets_2jet = FF_Wjets.Get("dm0_njet2")
    
    FFhistFile = ROOT.TFile("{0}/h_tau_pt_FFbinningWjets_frac.root".format(pathFractions))
    Thist_FF_Wjets_0jet = FFhistFile.Get("h_tau_pt_FFbinningWjetsDR_Wjets_FF_0jet")
    Thist_FF_Wjets_1jet = FFhistFile.Get("h_tau_pt_FFbinningWjetsDR_Wjets_FF_1jet")
    Thist_FF_Wjets_2jet = FFhistFile.Get("h_tau_pt_FFbinningWjetsDR_Wjets_FF_2jet")

    NonClosureCorr = ROOT.TFile(pathClosCorr)
    Tgraph_nonclosure = NonClosureCorr.Get("nonclosure_Wjets")

    frac_0j = []
    frac_1j = []
    frac_2j = []
    for v in Variable :
        fractionFile = ROOT.TFile("{0}/{1}_frac.root".format(pathFractions,v["hist_name"]))
        frac_0j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_0jet"))
        frac_0j[-1].SetDirectory(0)
        frac_1j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_1jet"))
        frac_1j[-1].SetDirectory(0)
        frac_2j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_2jet"))
        frac_2j[-1].SetDirectory(0)
        fractionFile.Close()  


    histogram_iso_tau                       = [ROOT.TH1D(v["hist_name"]+region+"_pass","{} distribution passing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau                  = [ROOT.TH1D(v["hist_name"]+region+"_fail","{} distribution failing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted             = [ROOT.TH1D(v["hist_name"]+region+"_pred","{} distribution predicted in isolated tau-region (fitted FF + non-closure)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit","{} distribution predicted in isolated tau-region (fitted FF)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas","{} distribution predicted in isolated tau-region (measured FF)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_0jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_0jet","{} distribution passing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_0jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_0jet","{} distribution failing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_0jet","{} distribution predicted tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_0jet","{} distribution predicted in isolated tau-region (fitted FF) - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_0jet","{} distribution predicted in isolated tau-region (measured FF) - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_1jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_1jet","{} distribution passing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_1jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_1jet","{} distribution failing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_1jet","{} distribution predicted tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_1jet","{} distribution predicted in isolated tau-region (fitted FF) - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_1jet","{} distribution predicted in isolated tau-region (measured FF) - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_2jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_2jet","{} distribution passing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_2jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_2jet","{} distribution failing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_2jet","{} distribution predicted tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_2jet","{} distribution predicted in isolated tau-region (fitted FF) - 2 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_2jet","{} distribution predicted in isolated tau-region (measured FF) - 2 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    

    nEntries = tree.GetEntries()
    passing = 0
    failing = 0
    for i in range(0, nEntries) : 
        tree.GetEntry(i)

        if ( eval(DR_cuts.replace(" * ", " and ")) ) : # passes DR selection criteria

            
            if ( eval(cuts["-TauIsoPass-"]) ) : # passes tau isolation requirement
                FillHistos(tree=tree, histograms=[histogram_iso_tau], variables=Variable, weight=[tree.weight_sf])
                passing += 1
                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_geq2-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_2jet], variables=Variable, weight=[tree.weight_sf])

            elif ( eval(cuts["-TauIsoFail-"])  ) : # fails tau isolation requirement
                
                # retrieve FF value
                raw_FF_value = 0
                raw_FF_value_measured = 0

                non_closure_corr = Tgraph_nonclosure.Eval(tree.lep_pt)
                frac = []
                if ( tree.njets==0 ) :
                    raw_FF_value = Tgraph_FF_Wjets_0jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_0jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_0j
                elif (tree.njets==1) :
                    raw_FF_value = Tgraph_FF_Wjets_1jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_1jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_1j
                elif (tree.njets>=2)  :
                    raw_FF_value = Tgraph_FF_Wjets_2jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_2jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_2j

                FillHistos(tree=tree, histograms=[histogram_anti_iso_tau], variables=Variable, weight=[tree.weight_sf])
                FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted,histogram_iso_tau_predicted_rawFFfitted,histogram_iso_tau_predicted_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                failing += 1
                

                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_0jet,histogram_iso_tau_predicted_0jet_rawFFfitted,histogram_iso_tau_predicted_0jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                elif ( eval(cuts["-NJET_1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_1jet,histogram_iso_tau_predicted_1jet_rawFFfitted,histogram_iso_tau_predicted_1jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                elif ( eval(cuts["-NJET_geq2-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_2jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_2jet,histogram_iso_tau_predicted_2jet_rawFFfitted,histogram_iso_tau_predicted_2jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                    
                
                if (tree.weight_sf * raw_FF_value < 0) :
                    print "problematic weight: {}".format(tree.weight_sf * raw_FF_value)
                    
                    

        if (i%50000 == 0) :
            print "{:8.1f} % processed".format(i/float(nEntries)*100.)  
            if (i > 10 and debug==True) :
                print "early stopping for debugging purpose"
                break

    for iv, v in enumerate(Variable) :
        output = ROOT.TFile("{0}/{1}/{2}/{3}_pred_FFdata.root".format(region,year,channel,v["hist_name"]),"RECREATE") 
        
        histogram_iso_tau[iv].Write()
        histogram_iso_tau_0jet[iv].Write()
        histogram_iso_tau_1jet[iv].Write()
        histogram_iso_tau_2jet[iv].Write()
        
        histogram_anti_iso_tau[iv].Write()
        histogram_anti_iso_tau_0jet[iv].Write()
        histogram_anti_iso_tau_1jet[iv].Write()
        histogram_anti_iso_tau_2jet[iv].Write()
    
        histogram_iso_tau_predicted[iv].Write()
        histogram_iso_tau_predicted_0jet[iv].Write()
        histogram_iso_tau_predicted_1jet[iv].Write()
        histogram_iso_tau_predicted_2jet[iv].Write()

        histogram_iso_tau_predicted_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_0jet_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_1jet_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_2jet_rawFFfitted[iv].Write()

        histogram_iso_tau_predicted_rawFF[iv].Write()
        histogram_iso_tau_predicted_0jet_rawFF[iv].Write()
        histogram_iso_tau_predicted_1jet_rawFF[iv].Write()
        histogram_iso_tau_predicted_2jet_rawFF[iv].Write()
    

        output.Close()


    print("# events passing tau ID: {}").format(passing)
    print("# events failing tau ID: {}").format(failing)

    print "done"
    preselection_file.Close()
    FF_Wjets.Close()
    FFhistFile.Close()
    NonClosureCorr.Close()

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
        for b in range(h.GetNbinsX()) :
            if (h.GetBinContent(b+1) < 0) :
                h.SetBinContent(b+1,1)
                h.SetBinError(b+1,1)
                
        h.Write()
    output.Close()   
    return 1

def CreateFractions(channel, year, var, region,ListOfFiles=["data","QCD","EMB","DY_J","DY_L","VV_J","VV_L","TT_J","TT_L"],TTbar=False) :
    for i, proc in enumerate(ListOfFiles) :
        # print "file: {}".format("{0}/{1}/{2}/{3}{4}.root".format(region,year,channel,var["hist_name"],"_{}".format(proc)))
        _file = ROOT.TFile("{0}/{1}/{2}/{3}{4}.root".format(region,year,channel,var["hist_name"],"_{}".format(proc))) 
        if (i==0) :
            histogram_iso_tau      = _file.Get( var["hist_name"]+region+"_pass").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass")
            histogram_iso_tau_0jet = _file.Get( var["hist_name"]+region+"_pass_0jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_0jet")
            histogram_iso_tau_1jet = _file.Get( var["hist_name"]+region+"_pass_1jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_1jet")
            histogram_iso_tau_2jet = _file.Get( var["hist_name"]+region+"_pass_2jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_2jet")
            
            histogram_anti_iso_tau      = _file.Get( var["hist_name"]+region+"_fail").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail")
            histogram_anti_iso_tau_0jet = _file.Get( var["hist_name"]+region+"_fail_0jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_0jet")
            histogram_anti_iso_tau_1jet = _file.Get( var["hist_name"]+region+"_fail_1jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_1jet")
            histogram_anti_iso_tau_2jet = _file.Get( var["hist_name"]+region+"_fail_2jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_2jet")
            
            tot      = _file.Get( var["hist_name"]+region+"_fail").Clone()
            tot_0jet = _file.Get( var["hist_name"]+region+"_fail_0jet").Clone()
            tot_1jet = _file.Get( var["hist_name"]+region+"_fail_1jet").Clone()
            tot_2jet = _file.Get( var["hist_name"]+region+"_fail_2jet").Clone()

            

            for h in [histogram_anti_iso_tau, histogram_anti_iso_tau_0jet, histogram_anti_iso_tau_1jet, histogram_anti_iso_tau_2jet, histogram_iso_tau, histogram_iso_tau_0jet, histogram_iso_tau_1jet, histogram_iso_tau_2jet, tot, tot_0jet, tot_1jet, tot_2jet] :
                h.SetDirectory(0)
        else :
            histogram_iso_tau.Add(_file.Get( var["hist_name"]+region+"_pass").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass"),-1)
            histogram_iso_tau_0jet.Add(_file.Get( var["hist_name"]+region+"_pass_0jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_0jet"),-1)
            histogram_iso_tau_1jet.Add(_file.Get( var["hist_name"]+region+"_pass_1jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_1jet"),-1)
            histogram_iso_tau_2jet.Add(_file.Get( var["hist_name"]+region+"_pass_2jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_2jet"),-1)
        
            histogram_anti_iso_tau.Add(_file.Get( var["hist_name"]+region+"_fail").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail"),-1)
            histogram_anti_iso_tau_0jet.Add(_file.Get( var["hist_name"]+region+"_fail_0jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_0jet"),-1)
            histogram_anti_iso_tau_1jet.Add(_file.Get( var["hist_name"]+region+"_fail_1jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_1jet"),-1)
            histogram_anti_iso_tau_2jet.Add(_file.Get( var["hist_name"]+region+"_fail_2jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_2jet"),-1)

            if (TTbar==True and i==2) :
                histogram_iso_tau.Add(_file.Get( var["hist_name"]+region+"_pass").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass"),2)
                histogram_iso_tau_0jet.Add(_file.Get( var["hist_name"]+region+"_pass_0jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_0jet"),2)
                histogram_iso_tau_1jet.Add(_file.Get( var["hist_name"]+region+"_pass_1jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_1jet"),2)
                histogram_iso_tau_2jet.Add(_file.Get( var["hist_name"]+region+"_pass_2jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_pass_2jet"),2)
            
                histogram_anti_iso_tau.Add(_file.Get( var["hist_name"]+region+"_fail").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail"),2)
                histogram_anti_iso_tau_0jet.Add(_file.Get( var["hist_name"]+region+"_fail_0jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_0jet"),2)
                histogram_anti_iso_tau_1jet.Add(_file.Get( var["hist_name"]+region+"_fail_1jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_1jet"),2)
                histogram_anti_iso_tau_2jet.Add(_file.Get( var["hist_name"]+region+"_fail_2jet").Clone(var["hist_name"]+region+"_WjetsExpFromData_fail_2jet"),2)



        _file.Close()
    
    
    
    output = ROOT.TFile("{0}/{1}/{2}/{3}{4}.root".format(region,year,channel,var["hist_name"],"_{}".format("frac")),"RECREATE") 
    for h in [histogram_anti_iso_tau, histogram_anti_iso_tau_0jet, histogram_anti_iso_tau_1jet, histogram_anti_iso_tau_2jet, histogram_iso_tau, histogram_iso_tau_0jet, histogram_iso_tau_1jet, histogram_iso_tau_2jet] :
        h.Write()

    # save fake factors
    histogram_iso_tau_0jet.Divide(histogram_anti_iso_tau_0jet)
    histogram_iso_tau_1jet.Divide(histogram_anti_iso_tau_1jet)
    histogram_iso_tau_2jet.Divide(histogram_anti_iso_tau_2jet)

    histogram_iso_tau_0jet.SetName(var["hist_name"]+region+"_FF_0jet")
    histogram_iso_tau_1jet.SetName(var["hist_name"]+region+"_FF_1jet")
    histogram_iso_tau_2jet.SetName(var["hist_name"]+region+"_FF_2jet")


    histogram_iso_tau_0jet.Write()
    histogram_iso_tau_1jet.Write()
    histogram_iso_tau_2jet.Write()
    



    h_frac_tot = histogram_anti_iso_tau.Clone(var["hist_name"]+region+"_ARfraction")
    h_frac_tot.Divide(tot)
    h_frac_tot_0jet = histogram_anti_iso_tau_0jet.Clone(var["hist_name"]+region+"_ARfraction_0jet")
    h_frac_tot_0jet.Divide(tot_0jet)
    h_frac_tot_1jet = histogram_anti_iso_tau_1jet.Clone(var["hist_name"]+region+"_ARfraction_1jet")
    h_frac_tot_1jet.Divide(tot_1jet)
    h_frac_tot_2jet = histogram_anti_iso_tau_2jet.Clone(var["hist_name"]+region+"_ARfraction_2jet")
    h_frac_tot_2jet.Divide(tot_2jet)
    
    for h in [h_frac_tot, h_frac_tot_0jet, h_frac_tot_1jet, h_frac_tot_2jet] :
        h.SetTitle("Fraction")
        h.Write()

    
    # pathRawFF="/home/jandrej/DeepTauFFproduction/2018_v15/CMSSW_8_0_25/src/ViennaTool/fakefactor/data_mt/FF_corr_Wjets_MCsum_noGen_fitted.root"
    # pathRawFF_raw="/home/jandrej/DeepTauFFproduction/2018_v15/CMSSW_8_0_25/src/ViennaTool/fakefactor/data_mt/FF_corr_Wjets_MCsum_noGen.root"

    # FF_Wjets = ROOT.TFile(pathRawFF) 
    # Tgraph_FF_Wjets_0jet = FF_Wjets.Get("dm0_njet0")
    # Tgraph_FF_Wjets_1jet = FF_Wjets.Get("dm0_njet1")
    # Tgraph_FF_Wjets_2jet = FF_Wjets.Get("dm0_njet2")

    # ff = ROOT.TFile(pathRawFF_raw)
    # hh = ff.Get("c_t")
    # output.cd()
    # hh.Write()
    # Tgraph_FF_Wjets_0jet.Write()
    # Tgraph_FF_Wjets_1jet.Write()
    # Tgraph_FF_Wjets_2jet.Write()

    
    output.Close()  
    # FF_Wjets.Close()
    # ff.Close()
    
    return 1

def DR_creationQCD(path, pathRawFF, pathClosCorr, channel, year, name, Variable, cuts, region, DR_cuts, debug=False) :
    preselection_file = ROOT.TFile(path)
    tree = preselection_file.Get("Events") 
    pathFractions="{0}/{1}/{2}".format(region,year,channel)
    extension = "_{}".format(name)

    FF_Wjets = ROOT.TFile(pathRawFF) 
    Tgraph_FF_Wjets_0jet = FF_Wjets.Get("dm0_njet0")
    Tgraph_FF_Wjets_1jet = FF_Wjets.Get("dm0_njet1")
    Tgraph_FF_Wjets_2jet = FF_Wjets.Get("dm0_njet2")
    

    FFhistFile = ROOT.TFile("{0}/h_tau_pt_FFbinningQCD_frac.root".format(pathFractions))
    Thist_FF_Wjets_0jet = FFhistFile.Get("h_tau_pt_FFbinningQCDDR_QCD_FF_0jet")
    Thist_FF_Wjets_1jet = FFhistFile.Get("h_tau_pt_FFbinningQCDDR_QCD_FF_1jet")
    Thist_FF_Wjets_2jet = FFhistFile.Get("h_tau_pt_FFbinningQCDDR_QCD_FF_2jet")

    NonClosureCorr = ROOT.TFile(pathClosCorr)
    Tgraph_nonclosure = NonClosureCorr.Get("nonclosure_QCD")

    frac_0j = []
    frac_1j = []
    frac_2j = []
    for v in Variable :
        fractionFile = ROOT.TFile("{0}/{1}_frac.root".format(pathFractions,v["hist_name"]))
        frac_0j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_0jet"))
        frac_0j[-1].SetDirectory(0)
        frac_1j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_1jet"))
        frac_1j[-1].SetDirectory(0)
        frac_2j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_2jet"))
        frac_2j[-1].SetDirectory(0)
        fractionFile.Close()  


    histogram_iso_tau                       = [ROOT.TH1D(v["hist_name"]+region+"_pass","{} distribution passing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau                  = [ROOT.TH1D(v["hist_name"]+region+"_fail","{} distribution failing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted             = [ROOT.TH1D(v["hist_name"]+region+"_pred","{} distribution predicted in isolated tau-region (fitted FF + non-closure)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit","{} distribution predicted in isolated tau-region (fitted FF)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas","{} distribution predicted in isolated tau-region (measured FF)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_0jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_0jet","{} distribution passing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_0jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_0jet","{} distribution failing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_0jet","{} distribution predicted tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_0jet","{} distribution predicted in isolated tau-region (fitted FF) - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_0jet","{} distribution predicted in isolated tau-region (measured FF) - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_1jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_1jet","{} distribution passing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_1jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_1jet","{} distribution failing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_1jet","{} distribution predicted tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_1jet","{} distribution predicted in isolated tau-region (fitted FF) - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_1jet","{} distribution predicted in isolated tau-region (measured FF) - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_2jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_2jet","{} distribution passing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_2jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_2jet","{} distribution failing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_2jet","{} distribution predicted tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_2jet","{} distribution predicted in isolated tau-region (fitted FF) - 2 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_2jet","{} distribution predicted in isolated tau-region (measured FF) - 2 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    

    nEntries = tree.GetEntries()
    passing = 0
    failing = 0
    for i in range(0, nEntries) : 
        tree.GetEntry(i)

        if ( eval(DR_cuts.replace(" * ", " and ")) ) : # passes DR selection criteria

            
            if ( eval(cuts["-TauIsoPass-"]) ) : # passes tau isolation requirement
                FillHistos(tree=tree, histograms=[histogram_iso_tau], variables=Variable, weight=[tree.weight_sf])
                passing += 1
                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_geq2-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_2jet], variables=Variable, weight=[tree.weight_sf])

            elif ( eval(cuts["-TauIsoFail-"])  ) : # fails tau isolation requirement
                
                # retrieve FF value
                raw_FF_value = 0
                raw_FF_value_measured = 0

                # non_closure_corr = Tgraph_nonclosure.Eval(tree.alltau_mvis[tree.tau_iso_ind]) # QCD closure is mvis dependent!
                non_closure_corr = Tgraph_nonclosure.Eval(tree.lep_pt) # QCD closure is new also in lepPt dependent!
                frac = []
                if ( tree.njets==0 ) :
                    raw_FF_value = Tgraph_FF_Wjets_0jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_0jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_0j
                elif (tree.njets==1) :
                    raw_FF_value = Tgraph_FF_Wjets_1jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_1jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_1j
                elif (tree.njets>=2)  :
                    raw_FF_value = Tgraph_FF_Wjets_2jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_2jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_2j

                FillHistos(tree=tree, histograms=[histogram_anti_iso_tau], variables=Variable, weight=[tree.weight_sf])
                FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted,histogram_iso_tau_predicted_rawFFfitted,histogram_iso_tau_predicted_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                failing += 1
                

                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_0jet,histogram_iso_tau_predicted_0jet_rawFFfitted,histogram_iso_tau_predicted_0jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                elif ( eval(cuts["-NJET_1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_1jet,histogram_iso_tau_predicted_1jet_rawFFfitted,histogram_iso_tau_predicted_1jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                elif ( eval(cuts["-NJET_geq2-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_2jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_2jet,histogram_iso_tau_predicted_2jet_rawFFfitted,histogram_iso_tau_predicted_2jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                    
                
                if (tree.weight_sf * raw_FF_value < 0) :
                    print "problematic weight: {}".format(tree.weight_sf * raw_FF_value)
                    
                    

        if (i%50000 == 0) :
            print "{:8.1f} % processed".format(i/float(nEntries)*100.)  
            if (i > 10 and debug==True) :
                print "Early stopping for debugging purpose"
                break

    for iv, v in enumerate(Variable) :
        output = ROOT.TFile("{0}/{1}/{2}/{3}_pred_FFdata.root".format(region,year,channel,v["hist_name"]),"RECREATE") 
        
        histogram_iso_tau[iv].Write()
        histogram_iso_tau_0jet[iv].Write()
        histogram_iso_tau_1jet[iv].Write()
        histogram_iso_tau_2jet[iv].Write()
        
        histogram_anti_iso_tau[iv].Write()
        histogram_anti_iso_tau_0jet[iv].Write()
        histogram_anti_iso_tau_1jet[iv].Write()
        histogram_anti_iso_tau_2jet[iv].Write()
    
        histogram_iso_tau_predicted[iv].Write()
        histogram_iso_tau_predicted_0jet[iv].Write()
        histogram_iso_tau_predicted_1jet[iv].Write()
        histogram_iso_tau_predicted_2jet[iv].Write()

        histogram_iso_tau_predicted_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_0jet_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_1jet_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_2jet_rawFFfitted[iv].Write()

        histogram_iso_tau_predicted_rawFF[iv].Write()
        histogram_iso_tau_predicted_0jet_rawFF[iv].Write()
        histogram_iso_tau_predicted_1jet_rawFF[iv].Write()
        histogram_iso_tau_predicted_2jet_rawFF[iv].Write()
    

        output.Close()


    print("# events passing tau ID: {}").format(passing)
    print("# events failing tau ID: {}").format(failing)

    print "done"
    preselection_file.Close()
    FF_Wjets.Close()
    FFhistFile.Close()
    NonClosureCorr.Close()

def DR_creationQCDttchan(path, pathRawFF, pathClosCorr, pathPtClosCorr, channel, year, name, Variable, cuts, region, DR_cuts, debug=False) :
    preselection_file = ROOT.TFile(path)
    tree = preselection_file.Get("Events") 
    pathFractions="{0}/{1}/{2}".format(region,year,channel)
    extension = "_{}".format(name)

    FF_Wjets = ROOT.TFile(pathRawFF) 
    Tgraph_FF_Wjets_0jet = FF_Wjets.Get("dm0_njet0")
    Tgraph_FF_Wjets_1jet = FF_Wjets.Get("dm0_njet1")
    Tgraph_FF_Wjets_2jet = FF_Wjets.Get("dm0_njet2")
    
    FFhistFile = ROOT.TFile("{0}/h_tau_pt_FFbinningQCD_frac.root".format(pathFractions))
    Thist_FF_Wjets_0jet = FFhistFile.Get("h_tau_pt_FFbinningQCD{}_FF_0jet".format(region))
    Thist_FF_Wjets_1jet = FFhistFile.Get("h_tau_pt_FFbinningQCD{}_FF_1jet".format(region))
    Thist_FF_Wjets_2jet = FFhistFile.Get("h_tau_pt_FFbinningQCD{}_FF_2jet".format(region))

    NonClosureCorr = ROOT.TFile(pathClosCorr)
    Tgraph_nonclosure = NonClosureCorr.Get("nonclosure_QCD")

    NonClosureCorrPt = ROOT.TFile(pathPtClosCorr)
    Tgraph_nonclosurePt = NonClosureCorrPt.Get("nonclosure_QCD")

    frac_0j = []
    frac_1j = []
    frac_2j = []
    for v in Variable :
        fractionFile = ROOT.TFile("{0}/{1}_frac.root".format(pathFractions,v["hist_name"]))
        frac_0j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_0jet"))
        frac_0j[-1].SetDirectory(0)
        frac_1j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_1jet"))
        frac_1j[-1].SetDirectory(0)
        frac_2j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_2jet"))
        frac_2j[-1].SetDirectory(0)
        fractionFile.Close()  


    histogram_iso_tau                       = [ROOT.TH1D(v["hist_name"]+region+"_pass","{} distribution passing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau                  = [ROOT.TH1D(v["hist_name"]+region+"_fail","{} distribution failing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted             = [ROOT.TH1D(v["hist_name"]+region+"_pred","{} distribution predicted in isolated tau-region (fitted FF + non-closure + pt_2closure)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1           = [ROOT.TH1D(v["hist_name"]+region+"_pred_1","{} distribution predicted in isolated tau-region (fitted FF + non-closure)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit","{} distribution predicted in isolated tau-region (fitted FF)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas","{} distribution predicted in isolated tau-region (measured FF)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_0jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_0jet","{} distribution passing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_0jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_0jet","{} distribution failing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_0jet","{} distribution predicted tau isolation criteria, both closures - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet_1           = [ROOT.TH1D(v["hist_name"]+region+"_pred_0jet_1","{} distribution predicted tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_0jet","{} distribution predicted in isolated tau-region (fitted FF) - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_0jet","{} distribution predicted in isolated tau-region (measured FF) - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_1jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_1jet","{} distribution passing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_1jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_1jet","{} distribution failing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_1jet","{} distribution predicted tau isolation criteria, both closures - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet_1           = [ROOT.TH1D(v["hist_name"]+region+"_pred_1jet_1","{} distribution predicted tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_1jet","{} distribution predicted in isolated tau-region (fitted FF) - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_1jet","{} distribution predicted in isolated tau-region (measured FF) - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 

    histogram_iso_tau_2jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_2jet","{} distribution passing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_2jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_2jet","{} distribution failing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_2jet","{} distribution predicted tau isolation criteria, both closures - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet_1           = [ROOT.TH1D(v["hist_name"]+region+"_pred_2jet_1","{} distribution predicted tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_2jet","{} distribution predicted in isolated tau-region (fitted FF) - 2 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet_rawFF       = [ROOT.TH1D(v["hist_name"]+region+"_predFFmeas_2jet","{} distribution predicted in isolated tau-region (measured FF) - 2 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    

    nEntries = tree.GetEntries()
    passing = 0
    failing = 0
    for i in range(0, nEntries) : 
        tree.GetEntry(i)

        if ( eval(DR_cuts.replace(" * ", " and ")) ) : # passes DR selection criteria

            
            if ( eval(cuts["-TauIsoPass-"]) ) : # passes tau isolation requirement
                FillHistos(tree=tree, histograms=[histogram_iso_tau], variables=Variable, weight=[tree.weight_sf])
                passing += 1
                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_geq2-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_2jet], variables=Variable, weight=[tree.weight_sf])

            elif ( eval(cuts["-TauIsoFail-"])  ) : # fails tau isolation requirement
                
                # retrieve FF value
                raw_FF_value = 0
                raw_FF_value_measured = 0

                non_closure_corr = Tgraph_nonclosure.Eval(tree.alltau_mvis[tree.tau_iso_ind]) # QCD closure is mvis dependent!
                #non_closure_corr = Tgraph_nonclosure.Eval(tree.lep_pt) # QCD closure is new also in lepPt dependent!
                
                non_closure_corrPt = Tgraph_nonclosurePt.Eval(tree.lep_pt) # QCD tau pt closure of other tau leg
                
                
                frac = []
                if ( tree.njets==0 ) :
                    raw_FF_value = Tgraph_FF_Wjets_0jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_0jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_0j
                elif (tree.njets==1) :
                    raw_FF_value = Tgraph_FF_Wjets_1jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_1jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_1j
                elif (tree.njets>=2)  :
                    raw_FF_value = Tgraph_FF_Wjets_2jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    raw_FF_value_measured = GetFFfromHistogram(histogram=Thist_FF_Wjets_2jet,xvalue=tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_2j

                FillHistos(tree=tree, histograms=[histogram_anti_iso_tau], variables=Variable, weight=[tree.weight_sf])
                FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted,histogram_iso_tau_predicted_1, histogram_iso_tau_predicted_rawFFfitted,histogram_iso_tau_predicted_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr * non_closure_corrPt),(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                failing += 1
                

                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_0jet,histogram_iso_tau_predicted_0jet_1,histogram_iso_tau_predicted_0jet_rawFFfitted,histogram_iso_tau_predicted_0jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr * non_closure_corrPt),(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                elif ( eval(cuts["-NJET_1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_1jet,histogram_iso_tau_predicted_1jet_1,histogram_iso_tau_predicted_1jet_rawFFfitted,histogram_iso_tau_predicted_1jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr * non_closure_corrPt),(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                elif ( eval(cuts["-NJET_geq2-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_2jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_2jet,histogram_iso_tau_predicted_2jet_1,histogram_iso_tau_predicted_2jet_rawFFfitted,histogram_iso_tau_predicted_2jet_rawFF], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr * non_closure_corrPt),(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value),(tree.weight_sf * raw_FF_value_measured)],fractions=frac)
                    
                
                if (tree.weight_sf * raw_FF_value < 0) :
                    print "problematic weight: {}".format(tree.weight_sf * raw_FF_value)
                    
                    

        if (i%50000 == 0) :
            print "{:8.1f} % processed".format(i/float(nEntries)*100.)  
            if (i > 10 and debug==True) :
                print "Early stopping for debugging purpose"
                break

    for iv, v in enumerate(Variable) :
        output = ROOT.TFile("{0}/{1}/{2}/{3}_pred_FFdata.root".format(region,year,channel,v["hist_name"]),"RECREATE") 
        
        histogram_iso_tau[iv].Write()
        histogram_iso_tau_0jet[iv].Write()
        histogram_iso_tau_1jet[iv].Write()
        histogram_iso_tau_2jet[iv].Write()
        
        histogram_anti_iso_tau[iv].Write()
        histogram_anti_iso_tau_0jet[iv].Write()
        histogram_anti_iso_tau_1jet[iv].Write()
        histogram_anti_iso_tau_2jet[iv].Write()
    
        histogram_iso_tau_predicted[iv].Write()
        histogram_iso_tau_predicted_0jet[iv].Write()
        histogram_iso_tau_predicted_1jet[iv].Write()
        histogram_iso_tau_predicted_2jet[iv].Write()

        histogram_iso_tau_predicted_1[iv].Write()
        histogram_iso_tau_predicted_0jet_1[iv].Write()
        histogram_iso_tau_predicted_1jet_1[iv].Write()
        histogram_iso_tau_predicted_2jet_1[iv].Write()

        histogram_iso_tau_predicted_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_0jet_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_1jet_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_2jet_rawFFfitted[iv].Write()

        histogram_iso_tau_predicted_rawFF[iv].Write()
        histogram_iso_tau_predicted_0jet_rawFF[iv].Write()
        histogram_iso_tau_predicted_1jet_rawFF[iv].Write()
        histogram_iso_tau_predicted_2jet_rawFF[iv].Write()
    

        output.Close()


    print("# events passing tau ID: {}").format(passing)
    print("# events failing tau ID: {}").format(failing)

    print "done"
    preselection_file.Close()
    FF_Wjets.Close()
    FFhistFile.Close()
    NonClosureCorr.Close()

def DR_creationTTbar(path, pathRawFF, pathClosCorr, channel, year, name, Variable, cuts, region, DR_cuts, debug=False) :
    preselection_file = ROOT.TFile(path)
    tree = preselection_file.Get("Events") 
    pathFractions="{0}/{1}/{2}".format(region,year,channel)
    extension = "_{}".format(name)

    FF_Wjets = ROOT.TFile(pathRawFF) 
    Tgraph_FF_Wjets_01jet = FF_Wjets.Get("dm0_njet0")
    Tgraph_FF_Wjets_2jet = FF_Wjets.Get("dm0_njet1")
    
    NonClosureCorr = ROOT.TFile(pathClosCorr)
    Tgraph_nonclosure = NonClosureCorr.Get("nonclosure_TT_MC")

    frac_0j = []
    frac_1j = []
    frac_2j = []
    for v in Variable :
        print "{0}/{1}_frac.root".format(pathFractions,v["hist_name"])
        fractionFile = ROOT.TFile("{0}/{1}_frac.root".format(pathFractions,v["hist_name"]))
        frac_0j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_0jet"))
        frac_0j[-1].SetDirectory(0)
        frac_1j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_1jet"))
        frac_1j[-1].SetDirectory(0)
        frac_2j.append(fractionFile.Get(v["hist_name"]+region+"_ARfraction_2jet"))
        frac_2j[-1].SetDirectory(0)
        fractionFile.Close()  


    histogram_iso_tau                       = [ROOT.TH1D(v["hist_name"]+region+"_pass","{} distribution passing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau                  = [ROOT.TH1D(v["hist_name"]+region+"_fail","{} distribution failing tau isolation criteria".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted             = [ROOT.TH1D(v["hist_name"]+region+"_pred","{} distribution predicted in isolated tau-region (fitted FF + non-closure)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit","{} distribution predicted in isolated tau-region (fitted FF)".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    
    histogram_iso_tau_0jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_0jet","{} distribution passing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_0jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_0jet","{} distribution failing tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_0jet","{} distribution predicted tau isolation criteria - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_0jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_0jet","{} distribution predicted in isolated tau-region (fitted FF) - 0 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    
    histogram_iso_tau_1jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_1jet","{} distribution passing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_1jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_1jet","{} distribution failing tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_1jet","{} distribution predicted tau isolation criteria - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_1jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_1jet","{} distribution predicted in isolated tau-region (fitted FF) - 1 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    
    histogram_iso_tau_2jet                       = [ROOT.TH1D(v["hist_name"]+region+"_pass_2jet","{} distribution passing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_anti_iso_tau_2jet                  = [ROOT.TH1D(v["hist_name"]+region+"_fail_2jet","{} distribution failing tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet             = [ROOT.TH1D(v["hist_name"]+region+"_pred_2jet","{} distribution predicted tau isolation criteria - 2 jet or more".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    histogram_iso_tau_predicted_2jet_rawFFfitted = [ROOT.TH1D(v["hist_name"]+region+"_predFFfit_2jet","{} distribution predicted in isolated tau-region (fitted FF) - 2 jet".format(region),len(v["binning"])-1,v["binning"]) for v in Variable] 
    

    nEntries = tree.GetEntries()
    passing = 0
    failing = 0
    for i in range(0, nEntries) : 
        tree.GetEntry(i)

        if ( eval(DR_cuts.replace(" * ", " and ")) ) : # passes DR selection criteria

            
            if ( eval(cuts["-TauIsoPass-"]) ) : # passes tau isolation requirement
                FillHistos(tree=tree, histograms=[histogram_iso_tau], variables=Variable, weight=[tree.weight_sf])
                passing += 1
                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])
                elif ( eval(cuts["-NJET_geq2-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_iso_tau_2jet], variables=Variable, weight=[tree.weight_sf])

            elif ( eval(cuts["-TauIsoFail-"])  ) : # fails tau isolation requirement
                
                # retrieve FF value
                raw_FF_value = 0
                
                non_closure_corr = Tgraph_nonclosure.Eval(tree.alltau_mvis[tree.tau_iso_ind]) # TTbar closure is mvis dependent!
                frac = []
                if ( tree.njets==0 ) :
                    raw_FF_value = Tgraph_FF_Wjets_01jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_0j
                elif (tree.njets==1) :
                    raw_FF_value = Tgraph_FF_Wjets_01jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_1j
                elif (tree.njets>=2)  :
                    raw_FF_value = Tgraph_FF_Wjets_2jet.Eval(tree.alltau_pt[tree.tau_iso_ind])
                    frac=frac_2j

                FillHistos(tree=tree, histograms=[histogram_anti_iso_tau], variables=Variable, weight=[tree.weight_sf])
                FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted,histogram_iso_tau_predicted_rawFFfitted], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value)],fractions=frac)
                failing += 1
                

                if ( eval(cuts["-NJET_0-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_0jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_0jet,histogram_iso_tau_predicted_0jet_rawFFfitted], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value)],fractions=frac)
                elif ( eval(cuts["-NJET_1-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_1jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_1jet,histogram_iso_tau_predicted_1jet_rawFFfitted], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value)],fractions=frac)
                elif ( eval(cuts["-NJET_geq2-"]) ) :
                    FillHistos(tree=tree, histograms=[histogram_anti_iso_tau_2jet], variables=Variable, weight=[tree.weight_sf])
                    FillHistosPredicted(tree=tree, histograms=[histogram_iso_tau_predicted_2jet,histogram_iso_tau_predicted_2jet_rawFFfitted], variables=Variable, weight=[(tree.weight_sf * raw_FF_value * non_closure_corr),(tree.weight_sf * raw_FF_value)],fractions=frac)
                    
                
                if (tree.weight_sf * raw_FF_value < 0) :
                    print "problematic weight: {}".format(tree.weight_sf * raw_FF_value)
                    
                    

        if (i%50000 == 0) :
            print "{:8.1f} % processed".format(i/float(nEntries)*100.)  
            if (i > 10 and debug==True) :
                print "Early stopping for debugging purpose"
                break

    for iv, v in enumerate(Variable) :
        output = ROOT.TFile("{0}/{1}/{2}/{3}_pred_FFdata.root".format(region,year,channel,v["hist_name"]),"RECREATE") 
        
        histogram_iso_tau[iv].Write()
        histogram_iso_tau_0jet[iv].Write()
        histogram_iso_tau_1jet[iv].Write()
        histogram_iso_tau_2jet[iv].Write()
        
        histogram_anti_iso_tau[iv].Write()
        histogram_anti_iso_tau_0jet[iv].Write()
        histogram_anti_iso_tau_1jet[iv].Write()
        histogram_anti_iso_tau_2jet[iv].Write()
    
        histogram_iso_tau_predicted[iv].Write()
        histogram_iso_tau_predicted_0jet[iv].Write()
        histogram_iso_tau_predicted_1jet[iv].Write()
        histogram_iso_tau_predicted_2jet[iv].Write()

        histogram_iso_tau_predicted_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_0jet_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_1jet_rawFFfitted[iv].Write()
        histogram_iso_tau_predicted_2jet_rawFFfitted[iv].Write()

    

        output.Close()


    print("# events passing tau ID: {}").format(passing)
    print("# events failing tau ID: {}").format(failing)

    print "done"
    preselection_file.Close()
    FF_Wjets.Close()
    NonClosureCorr.Close()
