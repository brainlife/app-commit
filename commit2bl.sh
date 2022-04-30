#!/bin/bash

model=`jq -r '.model' config.json`
commit_dir="./COMMIT"
results_dir=${commit_dir}/Results_${model}

[ ! -d raw ] && mkdir -p raw && cp -R ${commit_dir}/*.dict ./raw/ && cp ${results_dir}/*.pickle ./raw/

[ ! -d noddi-commit ] && mkdir -p noddi-commit && cp ${results_dir}/compartment_EC.nii.gz ./noddi-commit/odi.nii.gz && cp ${results_dir}/compartment_IC.nii.gz ./noddi-commit/ndi.nii.gz && cp ${results_dir}/compartment_ISO.nii.gz ./noddi-commit/isovf.nii.gz

[ ! -d errors ] && mkdir -p errors && cp ${results_dir}/fit_* ./errors/

[ ! -d streamline_weights ] && mkdir -p streamline_weights && cp ${results_dir}/streamline_weights.txt ./streamlines_weights/weights.csv

[ ! -d tdi ] && mkdir -p tdi && cp ${commit_dir}/dictionary_tdi.nii.gz ./tdi/tdi.nii.gz
