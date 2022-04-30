#!/usr/bin/env python3

import amico
import commit
from commit import trk2dictionary
import json

def run_commit(track_path,wm_path,peaks_path,dwi_path,bvals_path,bvecs_paths,dPar,dPerp,dIso,model):

    # create dictionary
    trk2dictionary.run(
        filename_tractogram = track_path,
        filename_peaks = peaks_path,
        filename_mask = wm_path
        #fiber_shift = 0.5, # this param could be optional
        #peaks_use_a    ffine = True
    )

    # generate scheme file
    amico.util.fsl2scheme(bvals_path,bvecs_path,'DWI.scheme')

    # load data
    mit = commit.Evaluation('.','.')
    mit.load_data(dwi_path,'DWI.scheme')

    # set forward model
    mit.set_model( model ) # StickZepplinBall
    d_par       = dPar           # Parallel diffusivity [mm^2/s] 1.7E-3
    d_perps_zep = [dPerp]        # Perpendicular diffusivity(s) [mm^2/s] [ 0.51E-3 ]
    d_isos      = [ float(f) for f in dIso.split(", ") ] # Isotropic diffusivity(s) [mm^2/s] [ 1.7E-3, 3.0E-3 ].had to code as string on bl input
    mit.model.set( d_par, d_perps_zep, d_isos )
    mit.generate_kernels( regenerate=True )
    mit.load_kernels()

    # load sparse dictionary
    mit.load_dictionary( 'COMMIT' )

    # bulid linear operator
    mit.set_threads(8)
    mit.build_operator()

    # fit the model
    mit.fit(tol_fun=1e-3,max_iter=1000)

    # save results
    mit.save_results()

def main():

    # load config.json
    with open('config.json','r') as config_f:
        config = json.load(config_f)

    # grab appropriate variables and paths
    track_path = config['track']
    wm_path = 'wm.nii.gz'
    peaks_path = 'peaks.nii.gz'
    dwi_path = config['dwi']
    bvals_path = config['bvals']
    bvecs_path = config['bvecs']
    dPar = config['dPar']
    dPerp = config['dPerp']
    dIso = config['dIso']
    model = config['model']

    # run commit
    run_commit(track_path,wm_path,peaks_path,dwi_path,bvals_path,bvecs_paths,dPar,dPerp,dIso,model)
    
if __name__ == '__main__':
    main()
