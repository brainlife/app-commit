[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.622-blue.svg)](https://doi.org/10.25663/brainlife.app.622)

# Compute streamline weights using COMMIT

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

**Filters a whole-brain tractogram with COMMIT, fitting streamline weights to the DWI signal with a microstructure model, and outputs streamline weights, fit errors and compartment maps.**

Derives peaks from the CSD (sh2peaks) unless peaks are given, builds a white-matter mask from the 5TT image, builds the COMMIT dictionary from the tractogram and fits the chosen forward model (default Stick-Zeppelin-Ball) to the DWI with AMICO/COMMIT. Use it to assess or prune streamlines by their contribution to the measured signal. Tractogram, DWI, CSD and mask must share the same space.

Run it on brainlife.io: [https://doi.org/10.25663/brainlife.app.622](https://doi.org/10.25663/brainlife.app.622)

| Input | Datatype | Required | Description |
|---|---|---|---|
| `track` | `neuro/track/tck` | yes | Whole-brain tractogram (.tck) to evaluate. |
| `dwi` | `neuro/dwi` | yes | Diffusion-weighted image with bvals and bvecs used for the fit. |
| `csd` | `neuro/csd` | yes | CSD FODs; the lmax selected by the lmax parameter is converted to peaks. |
| `mask` | `neuro/mask` (5tt_masks) | yes | 5-tissue-type image; its white-matter volume is binarised as the COMMIT mask. |
| `peaks` | `neuro/peaks` | no | Optional precomputed peaks; used instead of deriving peaks from the CSD. |

| Output | Datatype | Description |
|---|---|---|
| `streamline_weights` | `neuro/streamline-weights` | Per-streamline COMMIT weights (weights.csv). |
| `raw` | `raw` | COMMIT dictionary files and fitted model pickles. |
| `errors` | `raw` | COMMIT fit error maps (RMSE, NRMSE). |
| `noddi-commit` | `neuro/noddi` | Note: this is not the same as a normal noddi dataset. compartment_IC from COMMIT => ndi.nii.gz compartment_EC from COMMIT => odi.nii.gz compartment_ISO from COMMIT => isovf.nii.gz This is temporary until we develop a datatype to capture these outputs |
| `tdi` | `raw` | temporary until we figure out a datatype for tract density images |
| `peaks` | `neuro/peaks` | Peaks image used for the fit. |

| Parameter | Type | Default | Description |
|---|---|---|---|
| `dPar` | number | `0.0017` | parallel diffusivity value |
| `dPerp` | number | `0.00051` | perpendicular diffusivity value |
| `dIso` | string | `0.0017, 0.003` | isotropic diffusivity values |
| `model` | enum | `StickZeppelinBall` | The model to use Options: `StickZeppelinBall`, `CylinderZeppelinBall`, `VolumeFraction`. |
| `lmax` | number | `8` | the spherical harmonic order (lmax) to generate peaks from to use in model fitting |
| `fiber_shift` | number | `0` | COMMIT trk2dictionary fiber_shift: shift applied to streamline coordinates. |
| `peaks_use_affine` | boolean | `false` | Whether trk2dictionary applies the peaks image affine to peak directions. |
| `b0_threshold` | number | `0` | b-value threshold below which volumes are treated as b0 when loading the DWI. |
| `b0_min_signal` | number | `0` | Minimum b0 signal for a voxel to be fitted. |
| `max_iters` | number | `1000` | Maximum number of iterations of the COMMIT fit. |
| `stat_coef` | enum | `sum` | Statistic used by COMMIT save_results to summarise each streamline's coefficients (stat_coeffs). Options: `sum`, `mean`, `median`, `min`, `max`, `all`. |
| `min_seg_len` | number | `0.001` | Minimum streamline segment length kept in the dictionary. |
| `min_fiber_len` | number | `0` | Minimum streamline length kept in the dictionary. |
| `max_fiber_len` | number | `250` | Maximum streamline length kept in the dictionary. |
| `vf_THR` | number | `0.1` | Volume-fraction threshold used when building the dictionary from peaks. |
| `blur_spacing` | number | `0.25` | COMMIT trk2dictionary blur_spacing. |
| `blur_core_extent` | number | `0` | COMMIT trk2dictionary blur_core_extent. |
| `blur_gauss_extent` | number | `0` | COMMIT trk2dictionary blur_gauss_extent. |
| `blur_gauss_min` | number | `0.1` | COMMIT trk2dictionary blur_gauss_min. |
| `flip_peaks` | string | `false false false` | Three space-separated true/false flags to flip the peaks along x, y and z. |

Runtime: container `brainlife/mrtrix3:3.0_RC3`; 8 CPUs; 40 GB memory; 3 h walltime; needs `FREESURFER_LICENSE`.

Please cite:
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)
- Daducci A, Dal Palu A, Lemkaddem A, Thiran JP. COMMIT: Convex optimization modeling for microstructure informed tractography. IEEE Trans Med Imaging 34(1):246-257 (2015). [doi:10.1109/TMI.2014.2352414](https://doi.org/10.1109/TMI.2014.2352414)

<!-- brainlife-app:end -->

This app will compute streamline weights using COMMIT (Dadducci et al, 2018). This app takes in as input a track/tck wholebrain tractogram, a neuro/dwi, a neuro/csd, and a neuro/mask: 5tt datatypes as input and outputs a strealine-weights datatype containing the streamline weights from COMMIT and multiple raw directories (temporarily) to capture the rest of the COMMIT outputs, and a "noddi" datatype containing intra-compartmental (ndi), extra-compartmental (odi), and isotropic (isovf) components of the signal.

### Authors

- Brad Caron (bacaron@utexas.edu)

### Contributors

- Soichi Hayashi (shayashi@iu.edu)

### Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your publications and code reusing this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)

### Citations

We kindly ask that you cite the following articles when publishing papers and code using this code.

1. Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). https://doi.org/10.1038/s41597-019-0073-y

2. Daducci A, Dal Palù A, Lemkaddem A, Thiran JP. COMMIT: Convex optimization modeling for microstructure informed tractography. IEEE Trans Med Imaging. 2015 Jan;34(1):246-57. doi: 10.1109/TMI.2014.2352414. Epub 2014 Aug 27. PMID: 25167548.

#### MIT Copyright (c) 2020 brainlife.io The University of Texas at Austin and Indiana University

## Running the App

### On Brainlife.io

You can submit this App online at [https://doi.org/10.25663/brainlife.app.622](https://doi.org/10.25663/brainlife.app.622) via the 'Execute' tab.

### Running Locally (on your machine)

1. git clone this repo

2. Inside the cloned directory, create `config.json` with something like the following content with paths to your input files.

```json
{
    "track": "/input/track/track.tck",
    "dwi":  "/input/dwi/dwi.nii.gz",
    "bvals":  "/input/dwi/dwi.bvals",
    "bvecs":  "/input/dwi/dwi.bvecs",
    "lmax2":  "/input/csd/lmax2.nii.gz",
    "lmax4":  "/input/csd/lmax4.nii.gz",
    "lmax6":  "/input/csd/lmax6.nii.gz",
    "lmax8":  "/input/csd/lmax8.nii.gz",
    "lmax10":  "/input/csd/lmax10.nii.gz",
    "lmax12":  "/input/csd/lmax12.nii.gz",
    "lmax14":  "/input/csd/lmax14.nii.gz",
    "mask": "/input/5tt/mask.nii.gz",
    "dPar": 0.0017,
    "dPerp": 0.00051,
    "dIso": "0.0017, 0.003",
    "model": "StickZeppelinBall",
    "lmax": 8,
    "fiber_shift": 0,
    "peaks_use_affine": false,
    "b0_threshold": 0,
    "b0_min_signal": 0,
    "max_iters": 1000,
    "stat_coef": "sum",
    "min_seg_len": 0.001,
    "min_fiber_len": 0,
    "max_fiber_len": 250,
    "vf_THR": 0.1,
    "blur_spacing": 0.25,
    "blur_core_extent": 0,
    "blur_gauss_extent": 0,
    "blur_gauss_min": 0.1,
    "flip_peaks": "false false false",
    "peaks":  "/input/peaks/peaks.nii.gz"
}
```

### Sample Datasets

You can download sample datasets from Brainlife using [Brainlife CLI](https://github.com/brain-life/cli).

```
npm install -g brainlife
bl login
mkdir input
bl dataset download
```

3. Launch the App by executing 'main'

```bash
./main
```

## Output

The main output of this App is a streamline-weights datatype, multiple raw datatypes for the dictionaries, errors, and tract-density images, and a "noddi" datatype containing the compartment-based signal measurements.

#### Product.json

The secondary output of this app is `product.json`. This file allows web interfaces, DB and API calls on the results of the processing.

### Dependencies

This App only requires [singularity](https://www.sylabs.io/singularity/) to run. If you don't have singularity, you will need to install following dependencies.

- python3: https://www.python.org/downloads/
- Amico: https://github.com/daducci/AMICO
- Commit: https://github.com/daducci/COMMIT
- MRTrix3: https://numpy.org/

#### MIT Copyright (c) 2020 brainlife.io The University of Texas at Austin and Indiana University
