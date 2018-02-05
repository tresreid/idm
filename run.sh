#bin/bash

#./install.py --carddir Cards/DarkHiggsDiJetsDMJets_axial_LO_MZprime_Mhs_Mchi-10_gSM-0p25_gDM-1p0_th_0p01_13TeV-madgraph --gq 0.25 --gdm 1.001

#BBbarDM
#./install.py --carddir Cards/BBbarDM_LO_MZprime_Mhs_Mchi_gSM-0p25_gDM-1p0_th_0p01_13TeV-madgraph --gq 0.25 --gdm 1.001 --hdm 50
#./install.py --carddir Cards/BBbarDM_LO_MZprime_Mhs_Mchi_gSM-0p25_gDM-1p0_th_0p01_13TeV-madgraph --gq 0.25 --gdm 1.001

#DijetDM, 50,100,300
#./install.py --carddir Cards/DiJetsDM_LO_MZprime_Mhs_Mchi_gSM-0p25_gDM-1p0_th_0p01_13TeV-madgraph --gq 0.25 --gdm 1.001 --hdm 150 --dm 10 --med 50
#./install.py --carddir Cards/DiJetsDM_LO_MZprime_Mhs_Mchi_gSM-0p25_gDM-1p0_th_0p01_13TeV-madgraph --gq 0.25 --gdm 1.001

#pseudoscalar dark photon
#./install.py --carddir Cards/psdcalar_darkphoton_13TeV-madgraph --proc 702 --dm 10 --med 50 
#iDM
./install.py --carddir Cards/iDM_darkphoton_13TeV-madgraph --proc 703 --dm 10 --med 500 --hdm 100
