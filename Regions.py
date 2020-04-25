from Cuts import cuts
Regions = [
    {
        "name"      : "DR_Wjets",
        "selection" : " * ".join([cuts["-OS-"],cuts["-2L-"],cuts["-3L-"],cuts["-LepIso-"],cuts["-MT_DR-"],cuts["-Bpt_1-"]])
    },
    {
        "name"      : "DR_Wjets_SS",
        "selection" : " * ".join([cuts["-SS-"],cuts["-2L-"],cuts["-3L-"],cuts["-LepIso-"],cuts["-MT_DR-"],cuts["-Bpt_1-"]])
    }
]