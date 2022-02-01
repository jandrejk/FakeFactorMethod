#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import argparse
from copy import deepcopy

import logging
logger = logging.getLogger("")

import ROOT


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        "Plot categories using HarryPlotter from shapes produced by shape-producer module."
    )
    parser.add_argument("--comparison", action="store_true", help="Plot Embedded - MC comparison. --emb has to be set.")

    parser.add_argument("--emb", action="store_true", help="Embedded prefix")
    parser.add_argument("--ff", action="store_true", help="Use fake-factors")
    parser.add_argument(
        "-v",
        "--variables",
        nargs="+",
        type=str,
        required=True,
        help="Variable on x-axis")
    parser.add_argument(
        "--categories",
        nargs="+",
        type=str,
        required=False, default=None,
        help="Categories")
    parser.add_argument("--era", type=str, default="2016", help="Era")
    parser.add_argument(
        "--lumi", type=float, default=None, help="Integrated Luminosity")
    parser.add_argument("--mass", type=str, default="125", help="Mass")
    parser.add_argument(
        "--additional-arguments",
        type=str,
        default="",
        help="Additional higgsplot.py arguments")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="plots",
        help="Output directory for plots")
    parser.add_argument(
        "--y-log",
        action="store_true",
        default=False,
        help="Use logarithmic y-axis")
    parser.add_argument(
        "--plot-qcd",
        action="store_true",
        default=False,
        help="Plot data-MC as QCD")
    parser.add_argument(
        "-c",
        "--channels", nargs="+", type=str, required=True, help="Channel")
    parser.add_argument(
        "--analysis", type=str, default="smhtt", help="Analysis")
    parser.add_argument(
        "--shapes",
        type=str,
        default=None,
        help="ROOT files with shapes of processes")
    parser.add_argument(
        "--x-label", type=str, default=None, help="Label on x-axis")
    parser.add_argument("--chi2", action="store_true", help="Print chi2 value")
    parser.add_argument(
        "--num-processes",
        type=int,
        default=24,
        help="Number of processes used for plotting")
    parser.add_argument("--filename-prefix", type=str, default="", help="filename prefix")
    parser.add_argument("--www", action="store_true", help="webplotting")
    parser.add_argument("--www-dir", type=str, default=None,
        help='Directory structure where the plots will be uploaded. {date} expressions will be replaced by date.')
    parser.add_argument("--www-no-overwrite", action='store_true', default=False, help="Don't overwrite remote file. [Default: %(default)s]")
    parser.add_argument("--no-overwrite", "--keep-both", "--keep", "-k", action='store_true', default=False, help="Don't overwrite output file. [Default: %(default)s]")
    parser.add_argument("--log-level", default="debug", help="log level. [Default: %(default)s]")
    parser.add_argument("--redo-cache", action="store_true",
                        help="Do not use inputs from cached trees, but overwrite them. [Default: False for absolute paths, True for relative paths]")

    return parser.parse_args()


def setup_logging(output_file, level=logging.DEBUG):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


config_template = {
    "colors": ["#B7B7B7", "#000000"],
    "filename": "",
    "files": [None],
    "labels": ["", ""],
    "legend": [0.46, 0.55, 0.88, 0.86],
    "legend_cols": 2,
    "legend_markers": ["ELP", "ELP"],
    "stacks": [],#["ratio_bkg", "ratio_data"],
    "markers": ["E2", "P"],
    "formats": ["pdf"],#, "png"],
    "title": "",
    "cms": True,
    "extra_text": "Work in progress",
    "energies": [13],
    "nicks_blacklist": ["noplot"],
    "analysis_modules": ["Ratio"],
    "ratio_result_nicks": ["ratio_Bkg", "ratio_Data"],
    "y_subplot_lims": [0.988, 1.012],
    "y_label": "N_{evts}",
    "y_subplot_label": "#scale[0.8]{Ratio}",
    "subplot_lines": [0.9, 1.0, 1.1],
    "x_title_offset" : 0.90,
}

logvars = []


def main(args):
    do_qcd = args.plot_qcd
    bkg_processes_names = ["w"]
    bkg_processes = ["Wjets"]
    
   
    channels = args.channels
    channel = channels[0]
    era = args.era
    if args.lumi is None:
        if "2016" in era:
            lumi = 35.9
        elif "2017" in era:
            lumi = 41.5
        elif "2018" in era:
            lumi = 59.7
    else:
        lumi=args.lumi
    output_dir = args.output_dir
    y_log = args.y_log
    variables = args.variables
    
    variables = args.variables#["mvis","mt","muiso","pt","lepPt"]
    
    if args.www:
        config_template['www'] = ''
    if args.www_dir:
        config_template['www_dir'] = args.www_dir
    if args.www_no_overwrite:
        config_template['www_no_overwrite'] = True
        config_template['no_overwrite'] = True
    if args.no_overwrite:
        config_template['no_overwrite'] = True
    if args.redo_cache:
        config_template['redo_cache'] = True

    if args.filename_prefix != '':
        args.filename_prefix = args.filename_prefix if args.filename_prefix[0] == '_' else '_' + args.filename_prefix
    
    configs = []

    if (channel != "tt") :
    
        uncertainties = [  
            [
            "jetFakes_CMS_ff_w_lowdR_njet0_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_w_lowdR_njet1_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_w_lowdR_njet2_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_w_highdR_njet0_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_w_highdR_njet1_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_w_highdR_njet2_morphed_stat_{}_{}".format(channel,era),
            ],
            [
            "jetFakes_CMS_ff_qcd_njet0_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_njet1_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_njet2_morphed_stat_{}_{}".format(channel,era),
            ],
            [
            "jetFakes_CMS_ff_tt_njet0_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_tt_njet1_morphed_stat_{}_{}".format(channel,era),
            ],
            [
            "jetFakes_CMS_ff_w_lepPt_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_mvis_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_tt_morphed_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_w_mt_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_muiso_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_mvis_osss_{}_{}".format(channel,era),
            ],
            [
            "jetFakes_CMS_ff_corr_w_lepPt_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_corr_qcd_mvis_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_corr_tt_syst_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_corr_w_mt_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_corr_qcd_muiso_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_corr_qcd_mvis_osss_{}_{}".format(channel,era),
            ],
            [
            "jetFakes_CMS_ff_jetbinned_stat_0jet_norm_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_jetbinned_stat_1jet_norm_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_jetbinned_stat_2jet_norm_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_syst_norm_{}_{}".format(channel,era)
            ],
            [
            "jetFakes_CMS_ff_frac_w_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_mc_{}_{}".format(channel,era),    
            "jetFakes_CMS_ff_w_mc_{}_{}".format(channel,era),   
            "jetFakes_CMS_ff_MCsubAR_norm_{}_{}".format(channel,era), 
            ],

        ]
        
        FF_names = [
            [
            "#DeltaR^{(l,#tau_{h})}< 3, N_{jets}= 0",
            "#DeltaR^{(l,#tau_{h})}< 3, N_{jets}= 1",
            "#DeltaR^{(l,#tau_{h})}< 3, N_{jets}#geq 2",
            "#DeltaR^{(l,#tau_{h})}#geq 3, N_{jets}= 0",
            "#DeltaR^{(l,#tau_{h})}#geq 3, N_{jets}= 1",
            "#DeltaR^{(l,#tau_{h})}#geq 3, N_{jets}#geq 2",
            ],
            ["N_{jets}= 0",
            "N_{jets}= 1",
            "N_{jets}#geq 2",
            ],
            ["N_{jets}= 0",
            "N_{jets}#geq 1",
            ],
            [
            "C^{(W+jets)}",
            "C^{(QCD)}",
            "C^{(t#bar{t})}",
            "B^{(W+jets)}",
            "B^{(QCD)}",
            "B^{(QCD)}_{SS#rightarrowOS}",
            ],
            [
            "C^{(W+jets)}",
            "C^{(QCD)}",
            "C^{(t#bar{t})}",
            "B^{(W+jets)}",
            "B^{(QCD)}",
            "B^{(QCD)}_{SS#rightarrowOS}",
            ],
            [
                "N_{jets}= 0 (raw F_{F})",
                "N_{jets}= 1 (raw F_{F})",
                "N_{jets}#geq 2 (raw F_{F})",
                "N_{jets}#geq 0 (corr)"
            ],
            [
                "fractions",
                "MC sub F_{F}^{(QCD)}",
                "MC sub F_{F}^{(W+jets)}",
                "sub in AR"
            ],
        ]

        colors = [
            ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#a65628"],
            ["#e41a1c","#377eb8","#4daf4a"],
            ["#e41a1c","#377eb8"],
            ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#a65628"],
            ["#e41a1c","#377eb8","#4daf4a","#984ea3","#ff7f00","#a65628"],
            ["#e41a1c","#377eb8","#4daf4a","#984ea3"],
            ["#e41a1c","#377eb8","#4daf4a","#984ea3"],
        ]

        extra_title = [
            "raw F_{F}^{(W+jets)} (stat.)",
            "raw F_{F}^{(QCD)} (stat.)",
            "raw F_{F}^{(t#bar{t})} (stat.)",
            "corr. (stat.)",
            "corr. (syst.)",
            "norm. (stat.)",
            "other unc."
        ]

        ouput_name = [
            "morphed_raw_FF_W",
            "morphed_raw_FF_QCD",
            "morphed_raw_FF_tt",
            "corr_stat",
            "corr_syst",
            "norm_stat",
            "others_uncs",    
        ]

        lim = [
        [0.988, 1.012],
        [0.988, 1.012],
        [0.988, 1.012],
        [0.97, 1.03],
        [0.85, 1.15],
        [0.9, 1.1],
        [0.97, 1.03],
    ]
   
    else :

        uncertainties = [  
            [
            "jetFakes_CMS_ff_qcd_njet0_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_njet1_morphed_stat_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_njet2_morphed_stat_{}_{}".format(channel,era),
            ],
            [
            "jetFakes_CMS_ff_qcd_mvis_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_tau2_pt_0jet_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_tau2_pt_1jet_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_qcd_mvis_osss_{}_{}".format(channel,era),
            ],
            [
            "jetFakes_CMS_ff_corr_qcd_mvis_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_corr_qcd_tau2_pt_0jet_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_corr_qcd_tau2_pt_1jet_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_corr_qcd_mvis_osss_{}_{}".format(channel,era),
            ],
            [
            "jetFakes_CMS_ff_jetbinned_stat_0jet_norm_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_jetbinned_stat_1jet_norm_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_jetbinned_stat_2jet_norm_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_syst_norm_{}_{}".format(channel,era)
            ],
            [
            "jetFakes_CMS_ff_w_syst_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_tt_syst_{}_{}".format(channel,era),    
            "jetFakes_CMS_ff_qcd_mc_{}_{}".format(channel,era),
            "jetFakes_CMS_ff_MCsubAR_norm_{}_{}".format(channel,era),    
            ],

        ]
        
        FF_names = [
            [
                "N_{jets}= 0",
                "N_{jets}= 1",
                "N_{jets}#geq 2",
            ],
            [
                "C^{(QCD)}(m_{vis})",
                "C^{(QCD)}(p_{T}^{(#tau^{(2)})}) N_{jets}= 0",
                "C^{(QCD)}(p_{T}^{(#tau^{(2)})}) N_{jets}#geq 1",
                "B^{(QCD)}_{SS#rightarrowOS}",
            ],
            [
                "C^{(QCD)}(m_{vis})",
                "C^{(QCD)}(p_{T}^{(#tau^{(2)})}) N_{jets}= 0",
                "C^{(QCD)}(p_{T}^{(#tau^{(2)})}) N_{jets}#geq 1",
                "B^{(QCD)}_{SS#rightarrowOS}",
            ],
            [
                "N_{jets}= 0 (raw F_{F})",
                "N_{jets}= 1 (raw F_{F})",
                "N_{jets}#geq 2 (raw F_{F})",
                "N_{jets}#geq 0 (corr)"
            ],
            [
                "extra unc. W/Z+jets",
                "extra unc. t#bar{t}",
                "MC sub F_{F}^{(QCD)}",
                "sub in AR"
            ],
        ]

        colors = [
            ["#e41a1c","#377eb8","#4daf4a"],
            ["#e41a1c","#377eb8","#4daf4a","#984ea3"],
            ["#e41a1c","#377eb8","#4daf4a","#984ea3"],
            ["#e41a1c","#377eb8","#4daf4a","#984ea3"],
            ["#e41a1c","#377eb8","#4daf4a","#984ea3"],
        ]

        extra_title = [
            "raw F_{F}^{(QCD)} (stat.)",
            "corr. (stat.)",
            "corr. (syst.)",
            "norm. (stat.)",
            "other unc."
        ]

        ouput_name = [
            "morphed_raw_FF",
            "corr_stat",
            "corr_syst",
            "norm_stat",
            "others_uncs",    
        ]

        lim = [
        [0.988, 1.012],
        [0.988, 1.012],
        [0.92, 1.08],
        [0.92, 1.08],
        [0.975, 1.025],
    ]
    

    for y_log in [False]:
        for variable in variables:
                for unc, uncertainty in enumerate(uncertainties) :

                    config = deepcopy(config_template)
                    path = "/home/jandrej/systematics_plots/"
                    
                    config["files"] = [["{}/fakes_{}_{}.root".format(path,channel,era)] * 2, [["{}/fakes_{}_{}.root".format(path,channel,era)] * 2*len(uncertainty)]]
                    
                    # print(config["files"])
                    # print(len(uncertainty))
                
                    
                    config["lumis"] = [lumi]
                    config["year"] = era.strip("Run")
                    config["output_dir"] = output_dir+"/"+channel
                    config["y_log"] = True if ((variable in logvars) or y_log) else False
                    config["y_rel_lims"] = [5, 500] if (variable in logvars or y_log) else [0.9, 1.5]
                    
                    config["markers"]        = ["LINE"] + ["E2"] + ["LINE"] * 2*len(uncertainty) + ["E2"] + ["LINE"]*2*len(uncertainty)# +["L"]  + ["E2"] + ["L"]*2
                    config["legend_markers"] = ["L"]    + ["F"]  + ["L"] * 2*len(uncertainty)                     + ["E2"] + ["L"]*2*len(uncertainty)#+ ["L"] + ["E2"] + ["P"]*2
                    
                    config["labels"] = ["nominal value"] + ["stat. uncertainty"] + [qu for qu in FF_names[unc]] + [""]*len(uncertainty) + ["special name"]*(1+2*len(uncertainty)) #[uncertainty]*5 #+ [uncertainty]*2 # + config["labels"]
                    
                    config["colors"] =   ["#000000"] + ["#B7B7B7"] + colors[unc]*2 + ["#B7B7B7"] + colors[unc]*2
                    config["nicks"] = ["nominal"] + ["stat"] + ["up{}".format(l) for l in range(len(uncertainty))]  + ["down{}".format(l) for l in range(len(uncertainty))]
                    
                    config["x_expressions"] = [
                        "jetFakes",
                        "jetFakes"] + ["{}Up".format(u) for u in uncertainty] + ["{}Down".format(u)for u in uncertainty] 
                    
                    # _file = ROOT.TFile(config["files"][0][0])
                    # for c in config["x_expressions"] :
                    #     h = _file.Get(c)
                    #     print("{} integral: {}".format(c,h.Integral(-1,1)))
                    # print(config["labels"])
                    # print(config["colors"])
                    # print(config["nicks"])
                    # print(config["x_expressions"])

                    # config["stacks"] = ["up"] + ["down"] + ["nominal","ratio_A","ratio_B","ratio_C"]
                    config["ratio_denominator_nicks"] = ["nominal"]*(1+2*len(uncertainty))
                    config["ratio_numerator_nicks"] = ["nominal"] + ["up{}".format(l) for l in range(len(uncertainty))]  + ["down{}".format(l) for l in range(len(uncertainty))]
                    config["ratio_result_nicks"] = ["stat_ratio"] + ["bkg_ratio_up{}".format(l) for l in range(len(uncertainty))] + ["bkg_ratio_down{}".format(l) for l in range(len(uncertainty))]
                    
                    
                    config["filename"] = "_".join(
                            [channel, era, variable,ouput_name[unc]]) + args.filename_prefix
                    
                    if y_log:
                        config["filename"] += "_log" 
                    if variable == "NN" :
                        config["x_label"] = "NN output"
                    
                    
                    config["y_subplot_lims"] = lim[unc]                            
                    channel_dict = {}
                    channel_dict["mt"] = "#mu#tau_{h}"
                    channel_dict["et"] = "e#tau_{h}"
                    channel_dict["tt"] = "#tau_{h}#tau_{h}"
                    
                    # config["title"] = "{0}  {1}".format(channel_dict[channel],extra_title[unc])#"_".join(["channel", channel])
                    config["title"] = "{0}, ".format(channel_dict[channel]) + "jet #rightarrow #tau_{h} class" #"_".join(["channel", channel])
                    config["extra_text"] = "#splitline{{{a}}}{{{b}}}".format(a=config["extra_text"],b=extra_title[unc])
                    
                    configs.append(config)

    higgsplot.HiggsPlotter(
        list_of_config_dicts=configs,
        list_of_args_strings=[args.additional_arguments],
        n_processes=args.num_processes)


if __name__ == "__main__":
    args = parse_arguments()
    if args.log_level == 'debug':
        ll = logging.DEBUG
    else:
        ll = logging.INFO
    setup_logging("plot_nominal.log", ll)
    main(args)
