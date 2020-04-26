from array import *

Variable = [
    {
        "name": "tree.alltau_mvis[tree.tau_iso_ind]",
        "binning" : array('d',[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300]),
        "N_bins" : 30,
        "bin_min" : 0,
        "bin_max" : 300,
        "hist_name" : "h_mvis",
        "xlabel" : "m_{vis} [GeV]",

    },
    {
        "name": "tree.alltau_pt[tree.tau_iso_ind]",
        "binning" : array('d',[0,20,30,40,50,60,70,80,90,100,125,150,175,200]),
        "N_bins" : 25,
        "bin_min" : 20,
        "bin_max" : 100,
        "hist_name" : "h_tau_pt",
        "xlabel" : "p_{T}(#tau_{h}) [GeV]"

    },
    {
        "name": "tree.alltau_mt[tree.tau_iso_ind]",
        "binning" : array('d',[50,60,70,80,90,100,110,120,130,150,200]),
        "N_bins" : 30,
        "bin_min" : 0,
        "bin_max" : 150,
        "hist_name" : "h_mt",
        "xlabel" : "m_{T} [GeV]"

    },
    # {
    #     "name": "tree.alltau_mt2[tree.tau_iso_ind]",
    #     "binning" : array('d',[50,60,70,80,90,100,110,120,130,150,200]),
    #     "N_bins" : 30,
    #     "bin_min" : 0,
    #     "bin_max" : 150,
    #     "hist_name" : "h_mt2",
    #     "xlabel" : "#tau_{h} m_{T} [GeV]"

    # },
    {
        "name": "tree.alltau_decay[tree.tau_iso_ind]",
        "binning" : array('d',[-.5,.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5]),
        "N_bins" : 15,
        "bin_min" : 0,
        "bin_max" : 15,
        "hist_name" : "h_decaymode",
        "xlabel" : "#tau_{h} decay mode",
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
        "xlabel" : "m_{jj}",
    },
    {
        "name": "tree.lep_pt",
        "binning" : array('d',[0,20,30,40,50,60,70,80,90,100,125,150,175,200,300,500]),
        "hist_name" : "h_lep_pt",
        "xlabel" : "p_{T}(lepton) [GeV]"
    },
    {
        "name": "tree.ptvis",
        "binning" : array('d',[0,20,30,40,50,60,70,80,90,100,125,150,175,200,300,500]),
        "hist_name" : "h_ptvis",
        "xlabel" : "p_{T}(lepton) [GeV]"
    },
    # {
    #     "name": "tree.lep_eta",
    #     "binning" : array('d',[-2.5,-2.0,-1.5,-1.,-.5,0.,.5,1.,1.5,2.,2.5]),
    #     "hist_name" : "h_lep_eta",
    #     "xlabel" : "#eta (lepton) "
    # },
    {
        "name": "tree.alltau_dRToLep[tree.tau_iso_ind]",
        "binning" : array('d',[0.5,0.75,1.,1.25,1.5,1.75,2.,2.25,2.5,2.75,3.,3.25,3.5,3.75,4.,4.25,4.5,5.]),
        "hist_name" : "h_dRToLep",
        "xlabel" : "#Delta R (#tau_{h}, lepton) "
    },   
    # {
    #     "name": "tree.bpt_1",
    #     "binning" : array('d',[0,20,30,40,50,60,70,80,90,100,125,150,175,200,300,500]),
    #     "hist_name" : "h_bpt_1",
    #     "xlabel" : "leading b-jet p_{T}",
    # },
    # {
    #     "name": "tree.bpt_2",
    #     "binning" : array('d',[0,20,30,40,50,60,70,80,90,100,125,150,175,200,300,500]),
    #     "hist_name" : "h_bpt_2",
    #     "xlabel" : "subleading b-jet p_{T}",
    # },
    # {
    #     "name": "tree.nbtag",
    #     "binning" : array('d',[-.5,.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,15]),
    #     "hist_name" : "h_nbtag",
    #     "xlabel" : "N_{b tagged jets}",
    # }, 
    # {
    #     "name": "tree.jdeta",
    #     "binning" : array('d',[0,0.5,1.,1.5,2.,2.5,3.,3.5,4.,4.5,5.,6.,8.]),
    #     "hist_name" : "h_jdeta",
    #     "xlabel" : "#Delta #eta_{jj}",
    # },
    # {
    #     "name": "tree.met",
    #     "binning" : array('d',[10,20,30,40,50,60,70,80,90,100,150]),
    #     "hist_name" : "h_met",
    #     "xlabel" : "MET",
    # }, 
    # {
    #     "name": "tree.lep_phi",
    #     "binning" : array('d',[-3.5,-3.,-2.5,-2.0,-1.5,-1.,-.5,0.,.5,1.,1.5,2.,2.5,3.,3.5]),
    #     "hist_name" : "h_lep_phi",
    #     "xlabel" : "#phi (lepton) "
    # },
    # {
    #     "name": "tree.alltau_phi[tree.tau_iso_ind]",
    #     "binning" : array('d',[-3.5,-3.,-2.5,-2.0,-1.5,-1.,-.5,0.,.5,1.,1.5,2.,2.5,3.,3.5]),
    #     "hist_name" : "h_phi",
    #     "xlabel" : "#phi (#tau_{h}) "
    # },
]