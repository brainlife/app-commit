[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.622-blue.svg)](https://doi.org/10.25663/brainlife.app.622)

# Compute streamline weights using COMMIT

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
