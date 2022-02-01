import ROOT as R


year = 2018
channel = "tt"
_file = R.TFile("htt_input_{}.root".format(year))
dir = _file.GetDirectory("htt_{}_21_{}".format(channel,year))
dir.cd()

output = R.TFile("fakes_{}_{}.root".format(channel,year),"recreate")

norm_lnN = {
    #first entry stat norm from corrections: https://github.com/KIT-CMS/SMRun2Legacy/blob/master/src/HttSystematics_SMRun2.cc#L1492
    # second entry norm from MC sub in AR: https://github.com/KIT-CMS/SMRun2Legacy/blob/master/src/HttSystematics_SMRun2.cc#L1639 
     
    "et" : [1.066,1.023],
    "mt" : [1.047,1.024],
    "tt" : [1.041,1.02],
}

for l in dir.GetListOfKeys() :
    name = l.GetName()
    if "jetFakes" in name :
        # print(name)
        h = dir.Get(name)
        h.Write()
        if name == "jetFakes" :
            h1up   = h.Clone("jetFakes_CMS_ff_syst_norm_{}_{}Up".format(channel,year))
            h1down = h.Clone("jetFakes_CMS_ff_syst_norm_{}_{}Down".format(channel,year))
            
            # h1up.Divide(h1up) # get unity
            h1up.Scale(norm_lnN[channel][0])
            # h1down.Divide(h1down) # get unity
            h1down.Scale(1./norm_lnN[channel][0])

            h2up   = h.Clone("jetFakes_CMS_ff_MCsubAR_norm_{}_{}Up".format(channel,year))
            h2down = h.Clone("jetFakes_CMS_ff_MCsubAR_norm_{}_{}Down".format(channel,year))
            
            # h2up.Divide(h2up) # get unity
            h2up.Scale(norm_lnN[channel][1])
            # h2down.Divide(h2down) # get unity
            h2down.Scale(1./norm_lnN[channel][1])

            h1up.Write()
            h1down.Write()
            h2up.Write()
            h2down.Write()


            # for q in range(h1up.GetNbinsX()) :
            #     print h1up.GetBinContent(q+1)

            print "heureka"
            # exit(0)

_file.Close()
output.Close()