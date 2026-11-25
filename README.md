<h1 align="center">Compute streamline weights using COMMIT</h1>

<p align="center">
  Per-streamline weights, fit-error maps and compartment maps from a whole-brain tractogram and its diffusion data, with COMMIT.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.622"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.622-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

## 🧠 At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Filters a whole-brain tractogram with COMMIT, fitting streamline weights to the DWI signal with a microstructure model, and outputs streamline weights, fit errors and compartment maps.**

Derives peaks from the CSD (sh2peaks) unless peaks are given, builds a white-matter mask from the 5TT image, builds the COMMIT dictionary from the tractogram and fits the chosen forward model (default Stick-Zeppelin-Ball) to the DWI with AMICO/COMMIT. Use it to assess or prune streamlines by their contribution to the measured signal. Tractogram, DWI, CSD and mask must share the same space.

| | |
|---|---|
| 📥 **Inputs** | `neuro/track/tck` · `neuro/dwi` · `neuro/csd` · `neuro/mask` · `neuro/peaks` (optional) |
| 📤 **Outputs** | `neuro/streamline-weights` · `raw` ×3 · `neuro/noddi` · `neuro/peaks` |
| 🐳 **Container** | `brainlife/mrtrix3:3.0_RC3` |
| ⚙️ **Resources** | 8 CPUs · 40 GB memory · 3 h walltime |
| 🔑 **Requires** | `FREESURFER_LICENSE` |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.622](https://doi.org/10.25663/brainlife.app.622) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `track` | `neuro/track/tck` | yes | Whole-brain tractogram (.tck) to evaluate. |
| `dwi` | `neuro/dwi` | yes | Diffusion-weighted image with bvals and bvecs used for the fit. |
| `csd` | `neuro/csd` | yes | CSD FODs; the lmax selected by the lmax parameter is converted to peaks. |
| `mask` | `neuro/mask` (5tt_masks) | yes | 5-tissue-type image; its white-matter volume is binarised as the COMMIT mask. |
| `peaks` | `neuro/peaks` | no | Optional precomputed peaks; used instead of deriving peaks from the CSD. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `streamline_weights` | `neuro/streamline-weights` | Per-streamline COMMIT weights (weights.csv). |
| `raw` | `raw` | COMMIT dictionary files and fitted model pickles. |
| `errors` | `raw` | COMMIT fit error maps (RMSE, NRMSE). |
| `noddi-commit` | `neuro/noddi` | Note: this is not the same as a normal noddi dataset. compartment_IC from COMMIT => ndi.nii.gz compartment_EC from COMMIT => odi.nii.gz compartment_ISO from COMMIT => isovf.nii.gz This is temporary until we develop a datatype to capture these outputs |
| `tdi` | `raw` | temporary until we figure out a datatype for tract density images |
| `peaks` | `neuro/peaks` | Peaks image used for the fit. |

<details>
<summary><b>⚙️ Parameters</b> (20)</summary>

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

</details>

<!-- brainlife-app:end -->

## 🚀 Running the App

### ☁️ On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.622](https://doi.org/10.25663/brainlife.app.622), choose a whole-brain tractogram (`neuro/track/tck`), a `neuro/dwi`, a `neuro/csd` and a 5-tissue-type `neuro/mask` (and, optionally, precomputed `neuro/peaks`) from your project, set the options and press **Execute**. All inputs must be in the same space. The App archives a `neuro/streamline-weights` dataset, a `neuro/noddi` dataset with the COMMIT compartment maps, the peaks used for the fit, and three `raw` datasets (dictionaries, fit errors and the tract density image).

### 💻 Locally

You need [Singularity/Apptainer](https://apptainer.org/), [`jq`](https://jqlang.github.io/jq/) and a [FreeSurfer license](https://surfer.nmr.mgh.harvard.edu/registration.html) (FreeSurfer 6.0.0 reslices the white-matter mask onto the peaks grid). The App pulls the `brainlife/mrtrix3`, `brainlife/freesurfer:6.0.0` and `brainlife/commit:1.6.1` containers.

1. Clone this repository and check out the App branch: `git checkout v1.0`.
2. Create `config.json` with the paths to your inputs and the options you want:

   ```json
   {
       "track": "/input/track/track.tck",
       "dwi": "/input/dwi/dwi.nii.gz",
       "bvals": "/input/dwi/dwi.bvals",
       "bvecs": "/input/dwi/dwi.bvecs",
       "lmax2": "/input/csd/lmax2.nii.gz",
       "lmax4": "/input/csd/lmax4.nii.gz",
       "lmax6": "/input/csd/lmax6.nii.gz",
       "lmax8": "/input/csd/lmax8.nii.gz",
       "lmax10": "/input/csd/lmax10.nii.gz",
       "lmax12": "/input/csd/lmax12.nii.gz",
       "lmax14": "/input/csd/lmax14.nii.gz",
       "mask": "/input/5tt/mask.nii.gz",
       "peaks": "/input/peaks/peaks.nii.gz",
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
       "flip_peaks": "false false false"
   }
   ```

   `peaks` is optional: when the file does not exist, peaks are derived from the CSD image of order `lmax` with MRtrix3 `sh2peaks`. `model` is one of `StickZeppelinBall`, `CylinderZeppelinBall` or `VolumeFraction`.

3. Export your license and run the App:

   ```bash
   export FREESURFER_LICENSE="$(cat ~/freesurfer/license.txt)"
   ./main
   ```

### 🧪 Sample data

Download sample datasets from brainlife.io with the [brainlife CLI](https://github.com/brainlife/cli):

```bash
npm install -g brainlife
bl login
mkdir input
bl dataset download <dataset-id>
```

## 📦 Outputs

```text
streamline_weights/weights.csv   COMMIT weight of each streamline
noddi-commit/                    COMMIT compartment maps, named as a noddi dataset:
    ndi.nii.gz                     intra-axonal compartment (compartment_IC)
    odi.nii.gz                     extra-axonal compartment (compartment_EC)
    isovf.nii.gz                   isotropic compartment (compartment_ISO)
errors/                          fit error maps (fit_*: RMSE, NRMSE)
raw/                             COMMIT dictionaries (*.dict) and fitted model pickles
tdi/tdi.nii.gz                   tract density image from the dictionary
peaks/peaks.nii.gz               peaks image used for the fit
```

The `noddi-commit` dataset is not a NODDI fit; it reuses the `neuro/noddi` datatype until a dedicated datatype exists, and `tdi` and the other `raw` outputs are likewise temporary.

## 🩺 Troubleshooting

- **`Please set FREESURFER_LICENSE in .bashrc`**: export your FreeSurfer license text in the `FREESURFER_LICENSE` environment variable before running `./main`.
- **Inputs in different spaces**: the tractogram, DWI, CSD and 5TT mask must share the same space; the white-matter mask is resliced onto the peaks grid by header only.

## 📚 Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Daducci A, Dal Palù A, Lemkaddem A, Thiran JP. COMMIT: Convex optimization modeling for microstructure informed tractography. *IEEE Trans Med Imaging* 34(1):246–257 (2015). [doi:10.1109/TMI.2014.2352414](https://doi.org/10.1109/TMI.2014.2352414)
- Compute streamline weights using COMMIT. brainlife.io App. [doi:10.25663/brainlife.app.622](https://doi.org/10.25663/brainlife.app.622)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)
- Fischl. FreeSurfer. *NeuroImage* 62:774-781 (2012). [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021)
- Tournier et al. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. *NeuroImage* 202:116137 (2019). [doi:10.1016/j.neuroimage.2019.116137](https://doi.org/10.1016/j.neuroimage.2019.116137)
- Daducci et al. Accelerated Microstructure Imaging via Convex Optimization (AMICO) from diffusion MRI data. *NeuroImage* 105:32-44 (2015). [doi:10.1016/j.neuroimage.2014.10.026](https://doi.org/10.1016/j.neuroimage.2014.10.026)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)

## 👥 Authors

- Brad Caron
- Franco Pestilli (project director)

**Contributors:** Soichi Hayashi

## 💰 Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## ⚖️ License

[MIT](LICENSE). COMMIT, AMICO, MRtrix3 and FreeSurfer are distributed under their own licenses.
