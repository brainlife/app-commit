#!/bin/bash

mri_vol2vol --mov ./wm.nii.gz --targ ./peaks.nii.gz --regheader --interp nearest --o ./wm.nii.gz
