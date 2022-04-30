#!/usr/bin/env python3

import os, sys
import amico
import commit
from commit import trk2dictionary
import json



def run_commit(track_path,wm_path,peaks_path,dwi_path,bvals_path,bvecs_path,dPar,dPerp,dIso,model,fiber_shift,peaks_use_affine,b0_thr,b0_min_signal,max_iters,lmax,min_seg_len,min_fiber_len,max_fiber_len,vf_THR,flip_peaks,blur_spacing,blur_core_extent,blur_gauss_extent,blur_gauss_min):

    commit.setup(lmax=lmax)

    trk2dictionary.run(
        filename_tractogram = track_path,
        filename_peaks = peaks_path,
        filename_mask = wm_path,
        path_out = './COMMIT',
        fiber_shift = fiber_shift,
        peaks_use_affine = peaks_use_affine,
        min_seg_len = min_seg_len,
        min_fiber_len = min_fiber_len,
        max_fiber_len = max_fiber_len,
        vf_THR = vf_THR,
        flip_peaks = flip_peaks,
        blur_spacing = blur_spacing,
        blur_core_extent = blur_core_extent,
        blur_gauss_extent = blur_gauss_extent,
        blur_gauss_min = blur_gauss_min
    )

    # generate scheme file
    amico.util.fsl2scheme(bvals_path,bvecs_path,'DWI.scheme')

    # load data
    mit = commit.Evaluation('.','.')
    mit.load_data(dwi_path,'DWI.scheme',b0_thr=b0_thr,b0_min_signal=b0_min_signal)

    # set forward model
    mit.set_model( model ) # StickZepplinBall
    d_par       = dPar           # Parallel diffusivity [mm^2/s] 1.7E-3
    d_perps_zep = [dPerp]        # Perpendicular diffusivity(s) [mm^2/s] [ 0.51E-3 ]
    d_isos      = [ float(f) for f in dIso.split(", ") ] # Isotropic diffusivity(s) [mm^2/s] [ 1.7E-3, 3.0E-3 ].had to code as string on bl input
    mit.model.set( d_par, d_perps_zep, d_isos )
    mit.generate_kernels( lmax=lmax, regenerate=True )
    mit.load_kernels()

    # load sparse dictionary
    mit.load_dictionary( 'COMMIT' )

    # bulid linear operator
    mit.set_threads(8)
    mit.build_operator(build_dir='tmp')

    # fit the model
    mit.fit(tol_fun=1e-3,max_iter=max_iters)

    # save results
    mit.save_results(stat_coef=stat_coef)

def main():

    # load config.json
    with open('config.json','r') as config_f:
        config = json.load(config_f)

    # make commit dir
    if not os.path.isdir('COMMIT'):
        os.mkdir('COMMIT')

    # make tmp dir for operator building
    if not os.path.isdir('tmp'):
        os.mkdir('tmp')

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
    fiber_shift = config['fiber_shift']
    peaks_use_affine = config['peaks_use_affine']
    b0_thr = config['b0_threshold'] # default 0
    b0_min_signal = config['b0_min_signal'] # default 0
    max_iters = config['max_iters'] # default 1000
    stat_coef = config['stat_coef'] # default 'sum'; options; sum, mean, median, min, max, all
    lmax = config['lmax']
    min_seg_len = config['min_seg_len'] # default 0.001
    min_fiber_len = config['min_fiber_len'] # default 0
    max_fiber_len = config['max_fiber_len'] # default 250
    vf_THR = config['vf_THR'] # default 0.1
    flip_peaks = config['flip_peaks'] # default false
    blur_spacing = config['blur_spacing'] # default 0.25
    blur_core_extent = config['blur_core_extent'] # default 0.0
    blur_gauss_extent = config['blur_gauss_extent'] # default 0
    blur_gauss_min = config['blur_gauss_min'] # default 0.1

    # run commit
    run_commit(track_path,wm_path,peaks_path,dwi_path,bvals_path,bvecs_path,dPar,dPerp,dIso,model,fiber_shift,peaks_use_affine,b0_thr,b0_min_signal,max_iters,lmax,min_seg_len,min_fiber_len,max_fiber_len,vf_THR,flip_peaks,blur_spacing,blur_core_extent,blur_gauss_extent,blur_gauss_min)

if __name__ == '__main__':
    main()
