from array import *

Variable = [
    {
        "name"       : "tree.alltau_pt[tree.tau_iso_ind]",
        "binning"    : array('d',[23,25,30.,34,39,48,60,95,110,500]),
        "binning_mt" : array('d',[23,25,30.,34,39,48,60,95,110,500]),
        "binning_et" : array('d',[23.,26.,30.,34.,39.,50,60,75,90,115,500]),
        "hist_name"  : "h_tau_pt_FFbinningWjets",
        "xlabel"     : "p_{T}(#tau_{h}) [GeV]"
    },
    {
        "name"       : "tree.alltau_pt[tree.tau_iso_ind]",
        "binning"    : array('d',[23,26,29,32.5,36,42,65,500]),
        "binning_mt" : array('d',[23,26,29,32.5,36,42,65,500]),
        "binning_et" : array('d',[23,28,33,40,50,500]),
        "binning_tt" : array('d',[40.,42.5,45.,50.,55,60,65,105,500]),
        "hist_name"  : "h_tau_pt_FFbinningQCD",
        "xlabel"     : "p_{T}(#tau_{h}) [GeV]"
    },
    {
        "name"       : "tree.alltau_pt[tree.tau_iso_ind]",
        "binning"    : array('d',[23,26,29.,32.,35.,38.,41.,45,52,70,90,115,175,500]),
        "binning_mt" : array('d',[23,26,29.,32.,35.,38.,41.,45,52,70,90,115,175,500]),
        "binning_et" : array('d',[23.,25.,28.,30.,32.,34,37.,40,45,70,100,160,500]),
        "hist_name"  : "h_tau_pt_FFbinningTTbar",
        "xlabel"     : "p_{T}(#tau_{h}) [GeV]"
    },
    {
        "name"       : "tree.alltau_pt[tree.tau_iso_ind]",
        "binning"    : array('d',[30,40,50,60,70,80,90,100,150,200]),
        "hist_name"  : "h_tau_pt_coarseTTbar",
        "xlabel"     : "p_{T}(#tau_{h}) [GeV]"
    },
    {
        "name": "tree.alltau_pt[tree.tau_iso_ind]",
        "binning" : array('d',[23,24.5,26,27.5,29,31,32.5,33,36,38,40,42,46,50,55,60,65,100,200,500]),
        "hist_name" : "h_tau_ptQCDFine",
        "xlabel" : "p_{T}(#tau_{h}) [GeV]"
    },
    {
        "name": "tree.alltau_pt[tree.tau_iso_ind]",
        "binning" : array('d',[23,25,27,30,32,34,36,39,44,48,54,60,70,80,95,110,125,150,175,200,300,500]),
        "hist_name" : "h_tau_ptWjetsFine",
        "xlabel" : "p_{T}(#tau_{h}) [GeV]"
    },
    {
        "name": "tree.alltau_mvis[tree.tau_iso_ind]",
        "binning" : array('d',[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300]),
        "hist_name" : "h_mvis",
        "xlabel" : "m_{vis} [GeV]",
    },
    {
        "name": "tree.alltau_mvis[tree.tau_iso_ind]",
        "binning" : array('d',[0,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,200,250,450]),
        "hist_name" : "h_mvisFFbinning",
        "xlabel" : "m_{vis} [GeV]",
    },
    {
        "name": "tree.alltau_mt[tree.tau_iso_ind]",
        "binning" : array('d',[0,10,20,30,40,50,60,70,80,90,100,110,120,130,150,200]),
        "hist_name" : "h_mt",
        "xlabel" : "m_{T} [GeV]"
    },
    {
        "name": "tree.alltau_decay[tree.tau_iso_ind]",
        "binning" : array('d',[-.5,.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5]),
        "hist_name" : "h_decaymode",
        "xlabel" : "#tau_{h} decay mode",
    },
    {
        "name": "tree.njets",
        "binning" : array('d',[-.5,.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,15]),
        "hist_name" : "h_njets",
        "xlabel" : "N_{jets}",
    },
    {
        "name": "tree.mjj",
        "binning" : array('d',[0,100,200,300,400,500,650,800,1000,1500]),
        "hist_name" : "h_mjj",
        "xlabel" : "m_{jj} [GeV]",
    },
    {
        "name": "tree.lep_pt",
        "binning" : array('d',[25,30,40,50,60,70,80,90,100,120,200]),
        "hist_name" : "h_lep_pt",
        "xlabel" : "p_{T}(lepton) [GeV]"    
    },
    {
        "name": "tree.lep_pt",
        "binning" : array('d',[25,28,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,250]),
        "hist_name" : "h_lep_ptFFbinning",
        "xlabel" : "p_{T}(lepton) [GeV]"
    },
    {
        "name": "tree.alltau_dRToLep[tree.tau_iso_ind]",
        "binning" : array('d',[0.5,0.75,1.,1.25,1.5,1.75,2.,2.25,2.5,2.75,3.,3.25,3.5,3.75,4.,4.25,4.5,5.]),
        "hist_name" : "h_dRToLep",
        "xlabel" : "#Delta R (#tau_{h}, lepton) "
    },   



    # {
    #     "name": "tree.alltau_eta[tree.tau_iso_ind]",
    #     "binning" : array('d',[-2.5,-2.0,-1.5,-1.,-.5,0.,.5,1.,1.5,2.,2.5]),
    #     "N_bins" : 30,
    #     "bin_min" : -2.5,
    #     "bin_max" : 2.5,
    #     "hist_name" : "h_eta",
    #     "xlabel" : "#eta(#tau_{h})",
    # },
    # {
    #     "name": "tree.lep_eta",
    #     "binning" : array('d',[-2.5,-2.0,-1.5,-1.,-.5,0.,.5,1.,1.5,2.,2.5]),
    #     "hist_name" : "h_lep_eta",
    #     "xlabel" : "#eta(lepton)"
    # },
    # {
    #     "name": "tree.lep_phi",
    #     "binning" : array('d',[-3.5,-3.,-2.5,-2.0,-1.5,-1.,-.5,0.,.5,1.,1.5,2.,2.5,3.,3.5]),
    #     "hist_name" : "h_lep_phi",
    #     "xlabel" : "#phi(lepton)"
    # },
    # {
    #     "name": "tree.alltau_phi[tree.tau_iso_ind]",
    #     "binning" : array('d',[-3.5,-3.,-2.5,-2.0,-1.5,-1.,-.5,0.,.5,1.,1.5,2.,2.5,3.,3.5]),
    #     "hist_name" : "h_phi",
    #     "xlabel" : "#phi(#tau_{h})"
    # },
]