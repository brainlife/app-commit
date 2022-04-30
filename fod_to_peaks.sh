#!/bin/bash

set -x

# config inputs
lmax2=`jq -r '.lmax2' config.json`
lmax4=`jq -r '.lmax4' config.json`
lmax6=`jq -r '.lmax6' config.json`
lmax8=`jq -r '.lmax8' config.json`
lmax10=`jq -r '.lmax10' config.json`
lmax12=`jq -r '.lmax12' config.json`
lmax14=`jq -r '.lmax14' config.json`
lmax=`jq -r '.lmax' config.json`
mask=`jq -r '.mask' config.json`
ncores=8

# set the fod to the proper lmax image
fod=$(eval "echo \$lmax${lmax}")

# generate peaks if not already there
[ ! -f peaks.nii.gz ] && sh2peaks ${fod} ./peaks.nii.gz -force -nthreads ${ncores} -quiet

# generate white matter binary mask from 5tt image
[ ! -f wm.nii.gz ] && mrconvert -coord 3 2 ${mask} wm_prob.nii.gz -force -nthreads ${ncores} && fslmaths wm_prob.nii.gz -bin ./wm.nii.gz
