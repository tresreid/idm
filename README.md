# MadGraph5_aMCatNLO_Grid

Packages for generating gridpacks.

## Installation

Log into lxplus machine, clone a copy of the package in a clean directory

```
git clone -b cmslpc-branch git@github.com:SiewYan/MadGraph5_aMCatNLO_Grid.git
```

## Produce gridpack

To produce gridpack, do

```
./install.py --carddir Cards/psdcalar_darkphoton_13TeV-madgraph --proc 702 --dm 10 --med 50
```

Examples are show (here)[https://github.com/SiewYan/MadGraph5_aMCatNLO_Grid/blob/cmslpc-branch/run.sh#L16]
The output folder is assigned (here)[https://github.com/SiewYan/MadGraph5_aMCatNLO_Grid/blob/cmslpc-branch/install.py#L412]


