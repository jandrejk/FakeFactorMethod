from Cuts import cuts
Regions = [
    {
        "name"      : "DR_Wjets",
        "selection" : " * ".join([cuts["-OS-"],cuts["-2L-"],cuts["-3L-"],cuts["-LepIso-"],cuts["-MT_DR-"],cuts["-Bpt_1-"]])
    },
    {
        "name"      : "DR_Wjets_SS",
        "selection" : " * ".join([cuts["-SS-"],cuts["-2L-"],cuts["-3L-"],cuts["-LepIso-"],cuts["-MT_DR-"],cuts["-Bpt_1-"]])
    },
    {
        "name"      : "DR_QCD",
        "selection" : " * ".join([cuts["-SS-"],cuts["-2L-"],cuts["-3L-"],cuts["-LepIso-"], cuts["-MT_DRQCD-"],cuts["-LepIsoQCD-"]])
    },
    {
        "name"      : "DR_TTbar",
        "selection" : " * ".join([cuts["-NisoLep_geq1-"],cuts["-NJET_g1-"],cuts["-3Lfail-"],cuts["-Bjet_1-"],cuts["-dRlep-"],cuts["-dRotherlep-"]])
    },
    {
        "name"      : "DR_QCD_tt",
        "selection" : " * ".join([cuts["-SS-"],cuts["-2L-"],cuts["-3L-"],cuts["-LepIso_ttchan-"]])
    },
    # (lep_iso > 9.000000) * (lep_q*alltau_q[0]>0.0) * (passesDLVeto > 0.5) * (passes3LVeto > 0.5)

]