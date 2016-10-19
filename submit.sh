#!/bin/bash
./install.py --carddir Cards/Scalar_MonoJ_NLO_Mphi_Mchi_gSM-1p0_gDM-1p0_13TeV-madgraph     --proc 805  --gq 1  --runcms runcmsgrid_LO.sh
exit
./install.py --carddir Cards/Axial_MonoZLL_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph     --proc 801
./install.py --carddir Cards/Axial_MonoPhoton_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph  --proc 801
./install.py --carddir Cards/Axial_MonoJ_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph       --proc 801
./install.py --carddir Cards/Axial_MonoZ_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph       --proc 801
./install.py --carddir Cards/Axial_MonoW_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph       --proc 801

./install.py --carddir Cards/Vector_MonoZLL_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph    --proc 800
./install.py --carddir Cards/Vector_MonoPhoton_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph --proc 800
./install.py --carddir Cards/Vector_MonoJ_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph      --proc 800
./install.py --carddir Cards/Vector_MonoZ_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph      --proc 800
./install.py --carddir Cards/Vector_MonoW_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph      --proc 800
#./install.py --carddir Cards/Axial_MonoTop_NLO_Mphi_Mchi_gSM-0p25_gDM-1p0_13TeV-madgraph     --proc 801 