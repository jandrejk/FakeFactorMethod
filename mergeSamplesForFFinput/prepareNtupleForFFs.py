import ROOT
import os
import glob
import time
import sys
import argparse




def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


parser = argparse.ArgumentParser(description='Process inputs')
parser.add_argument('--tmp', action="store_true")
parser.add_argument('--year', type=str,required=True,choices=['2016','2017','2018'])
parser.add_argument('--channel', type=str,required=True,choices=['et','mt','tt'])

args = parser.parse_args()

CreateTmpFiles = args.tmp
start = time.time()

output_dir = "/ceph/jandrej/MSSM_Ntuple_FF_input"
year=args.year
channel=args.channel
full_path = "{}/{}/{}".format(output_dir,year,channel)
ensure_dir(full_path)

if CreateTmpFiles :
	tmp_path = "{}/{}/{}/tmp".format(output_dir,year,channel)
	ensure_dir(tmp_path)

	input_dir = "/ceph/htautau/Run2Legacy_MSSM/{}/ntuples".format(year)
	listOfIInputFiles = glob.glob("{}/*/*.root".format(input_dir))

	for f in listOfIInputFiles :
		tmpFileName = f.split("/")[-1]
		if "GluGlu" in tmpFileName or "HToWWM125" in tmpFileName or "SUSYGluGluTo" in tmpFileName or "VBFHTo" in tmpFileName or "HToTauTauM125" in tmpFileName or "ggZHHToTauTau" in tmpFileName or "ttHJetTo" in tmpFileName or "MuonEG" in tmpFileName :
			continue
		
		openFile = ROOT.TFile(f)
		outputfile = ROOT.TFile("{}/{}".format(tmp_path,tmpFileName),"recreate")

		for h in openFile.GetListOfKeys() :
			if "{}_nominal".format(channel) in h.GetName() :
				dir_name = h.GetName()
				ntuple = openFile.Get("{}/ntuple".format(dir_name))
				newTree = ntuple.CloneTree()
				outputfile.mkdir(dir_name)
				outputfile.cd(dir_name)
				newTree.Write()
					

		openFile.Close()

		


os.system("sh hadd_{0}.sh {1} {2}".format(year,output_dir,channel))

end = time.time()-start
print "Total time {} sec / {} min / {} h".format(end,end/60,end/3600)