#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Izaak Neutelings (January 2021)
# scp ineuteli@lxplus.cern.ch:/afs/cern.ch/user/j/jaandrej/public/forIzaak/LQ_FF/v2/2017/et/fakeFactors.root ./
# /work/ineuteli/analysis/CMSSW_10_3_3/src/HTTutilities/Jet2TauFakes/data/SM2017_DeepTauIDv2p1/medium/vloose/et
import os, re
from math import sqrt
from array import array
from ROOT import gROOT, gSystem, gDirectory, TFile
import atexit
def closeFakeFactor():
  from ROOT import closeFakeFactor as _closeFakeFactor
  _closeFakeFactor()

basedir = "/home/jandrej/DeepTauFFproduction/LQ_FF/FF_derivation/AutomaticSubmission"


histf = "m_vis"
pts     = [
  55.,70.,100.
]
dm      = 1.
dRs     = [0.5,3.5]
dR      = 0.5
njets   = 0
mviss   = [
  400.,500.,
  650, 1000., #1500.
]
pt_lep  = 55.
mt      = 50.
iso_lep = 0.1
uncerts = [
  ###"qcd_syst", "qcd_dm0_njet0_stat", "qcd_dm0_njet1_stat", #"qcd_frac",
  ###"w_syst",   "w_dm0_njet0_stat",   "w_dm0_njet1_stat",   #"w_frac", 
  ###"tt_syst",  "tt_dm0_njet0_stat",  "tt_dm0_njet1_stat",  #"tt_frac",
  # ZERO IMPACT: "qcd_dr0_njet0_stat", "qcd_dr1_njet0_stat", "qcd_dr1_njet1_stat",
  #              "tt_dr1_njet0_stat", "tt_dr1_njet1_stat", "tt_syst",
  #              "w_dr0_njet0_stat",  "w_dr1_njet0_stat",
  "qcd_syst", "w_syst", "tt_syst",
  "qcd_stat", "w_stat", "tt_stat",
                              "tt_dr0_njet0_morphed_stat", 
  "w_dr0_njet1_morphed_stat", "tt_dr0_njet1_morphed_stat", "qcd_dr0_njet1_morphed_stat",
  "w_dr0_njet2_morphed_stat",                              "qcd_dr0_njet2_morphed_stat",
  "w_dr1_njet1_morphed_stat",
  "w_dr1_njet2_morphed_stat",
  "w_dr0_njet0_morphed_stat",
  "w_dr1_njet0_morphed_stat",
  #"qcd_stat", "w_stat", "tt_stat",
  "qcd_mvis", #"qcd_mc", # small
  "w_lepPt", "w_mc", "w_mc_lepPt", "w_mt", #"w_mvis",
  "corr_w_lepPt", "corr_w_mt",
  "frac_w",
]


def jetFakeFactorPY():
    print ">>> jetFakeFactorPY"
    def closeFakeFactorPY():
      tool1.Delete()
      tool2.Delete()
      file1.Close()
      file2.Close()
    atexit.register(closeFakeFactorPY) # close FF tool upon exit to prevent verbose error
    # gSystem.Load(basedir+"/lib/slc7_amd64_gcc700/libHTTutilitiesJet2TauFakes.so")
    # fname1  = basedir+"/src/HTTutilities/Jet2TauFakes/data/SM2017_DeepTauIDv2p1/medium/vloose/et/fakeFactors.root"
    # fname2  = basedir+"/src/HTTutilities/Jet2TauFakes/data/SM2017_DeepTauIDv2p1_0j/medium/vloose/et/fakeFactors.root"
    # #fname2  = basedir+"/src/HTTutilities/Jet2TauFakes/data/SM2017_DeepTauIDv2p1_0j/medium/vloose/et/fakeFactors_WdR2.root"
    # fname1  = fname2
    fname1  = basedir+"/FF_v3p0_old/2016/et/fakeFactors.root" # fixed bug ff_w_mt no cap off >800 GeV
    fname2  = basedir+"/FF_v3p1/2016/et/fakeFactors.root" # fixed bug ff_w_mt with cap off >800 GeV
    print ">>> fname1:",fname1
    print ">>> fname2:",fname2
    file1   = TFile.Open(fname1)
    file2   = TFile.Open(fname2)
    tool1   = file1.Get("ff_comb")
    tool2   = file2.Get("ff_comb")
    innames = tool1.inputs() # this returns a ROOT.vector<string> object
    print ', '.join(innames)
    sys = ""
    fracs    = { # QCD W        TT
       150.: (0.136377,0.847364,0.0162588),
       200.: (0.205866,0.775952,0.0181818),
       250.: (0.205866,0.775952,0.0181818),
       300.: (0.330198,0.648978,0.0208233),
       400.: (0.188841,0.790956,0.0202033),
       500.: (0.188841,0.790956,0.0202033),
      1000.: (0,       0.973353,0.0266473),
      1500.: (0,       0.973353,0.0266473),
    }
    
    
    # COMPARE SYSTEMATICS
    pt, dR, njets, mvis, pt_lep, mt, iso_lep = 60., 2.5, 0, 80., 50., 50., 0.1
    sysnames1 = [s.replace("_up","") for s in tool1.systematics() if "_down" not in s]
    sysnames2 = [s.replace("_up","") for s in tool2.systematics() if "_down" not in s]
    #sysnames1 = [s for s in sysnames1 if "mvis" in s]
    #sysnames2 = [s for s in sysnames2 if "mvis" in s]
    #print ', '.join(sysnames1)
    #print ', '.join(sysnames2)
    for frac in ['w','qcd','tt']:
      print ">>>\n>>> %s, pt=%.1f, dR=%.2f, njets=%d, mvis=%.1f, pt_lep=%.1f, mt=%.1f, iso_lep=%.2f"%(frac,pt,dR,njets,mvis,pt_lep,mt,iso_lep)
      #print ', '.join(s for s in sysnames1 if frac+'_' in s or '_'+frac in s)
      print ">>> %8s %24s %36s"%("ffold","ffnew","uncertainty")
      for uncert in uncerts:
        if frac+'_' not in uncert and '_'+frac not in uncert: continue
        unc     = "ff_"+uncert
        inputs  = [pt,dR,njets,mvis,pt_lep,mt,iso_lep,0,1,0,0,0,0,0]
        ff1     = tool1.value(len(inputs),array('d',inputs),sys) # nominal fake factor
        ff2     = tool2.value(len(inputs),array('d',inputs),sys) # nominal fake factor
        ff1_up  = tool1.value(len(inputs),array('d',inputs),unc+"_up")
        ff1_dn  = tool1.value(len(inputs),array('d',inputs),unc+"_down")
        ff2_up  = tool2.value(len(inputs),array('d',inputs),unc+"_up")
        ff2_dn  = tool2.value(len(inputs),array('d',inputs),unc+"_down")
        dff_q   = 100.0*(ff2/ff1-1)
        unc1_up = ff1_up/ff1-1. if ff1 and ff1_up else 0
        unc1_dn = ff1_dn/ff1-1. if ff1 and ff1_dn else 0
        unc2_up = ff2_up/ff2-1. if ff2 and ff2_up else 0
        unc2_dn = ff2_dn/ff2-1. if ff2 and ff2_dn else 0
        #print ff1,ff1_up,ff1_dn,ff2,ff2_up,ff2_dn
        print ">>> %8.4f %+6.4f %+6.4f %8.4f %+6.4f %+6.4f (%+4.1f%%) %s"%(
            ff1,unc1_up,unc1_dn,ff2,unc2_up,unc2_dn,dff_q,uncert)
    


jetFakeFactorPY()
