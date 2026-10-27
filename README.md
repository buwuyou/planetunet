# PlanetUNet: mapping cropped and fallowed fields in the Sahel

Code and trained models used to map **cropped** and **fallowed** fields across the Sahel from
PlanetScope / NICFI 4.8 m monthly mosaics (June–November 2019) with U-Net semantic segmentation.
The study also uses a previously published U-Net framework for detecting individual trees (see
[Tree detection](#tree-detection)).

## Outputs

The resulting maps are available on Zenodo:

> Tong, X. (2025). *Sahel mappings for cropped and fallowed fields* (v1) [Dataset]. Zenodo.
> https://doi.org/10.5281/zenodo.15261630

| File | Content |
| --- | --- |
| `c2019.tif` | Cropped-field map, 2019 |
| `f2019.tif` | Fallowed-field map, 2019 |
| `validation_info.gpkg` | Reference and prediction for 1,472 validation points |
| `good_practice_validation.zip` | Validation material |

## Repository structure

```
planetunet-crop/      U-Net for cropped fields (input: blue, green, red, NIR, NDVI)
planetunet-fallow/    U-Net for fallowed fields (input: blue, green, red, NIR, NDVI + crop prediction)
environment.yml       Conda environment
```

Both model folders have the same layout:

| Notebook | Purpose |
| --- | --- |
| `1-Preprocessing_new.ipynb` | Extract training areas, labels and boundary weights from the imagery and annotation shapefiles |
| `2-UNetTraining_new.ipynb` | Train the U-Net (Tversky loss, AdaDelta, 512×512 patches) |
| `3-RasterAnalysis_new.ipynb` | Run the trained model over the mosaic tiles |
| `4-MergeCropPrediction.ipynb` (fallow only) | Stack the crop prediction onto the imagery as an extra input band for the fallow model |
| `Auxiliary-1-UNetEvaluation.ipynb` | Evaluate a trained model |
| `Auxiliary-2-SplitRasterToAnalyse.ipynb` | Split large rasters into tiles for prediction |
| `config/` | Paths and parameters for each notebook (`Preprocessing.py`, `UNetTraining.py`, `RasterAnalysis.py`) |
| `core/` | U-Net architecture, losses, optimizers, patch generators and helpers |

### Workflow

1. **Crop model** (`planetunet-crop`): preprocess, train, and predict cropped fields on the 2019 mosaics.
2. **Merge** (`planetunet-fallow/4-MergeCropPrediction.ipynb`): add the crop prediction as a sixth band to each image tile.
3. **Fallow model** (`planetunet-fallow`): preprocess, train, and predict fallowed fields on the six-band tiles.

The paths in `config/*.py` and in some notebook cells point to the original data storage. Edit them
to match your environment before running.

## Trained models

The trained weights are too large for git (about 360 MB each), so they are attached to the
[v1.0 release](https://github.com/buwuyou/planetunet/releases/tag/v1.0):

| Model | File | MD5 |
| --- | --- | --- |
| Crop | `crop_20211010-1531_AdaDelta_weightmap_tversky_01234_512.h5` | `0864ebfc30e95c675b2529473d01e1e9` |
| Fallow | `fallow_20210419-1602_AdaDelta_weightmap_tversky_012345_512.h5` | `91aba01af725def5befffa4ea5d7d0b6` |

Put each file in the matching `planetunet-<crop|fallow>/saved_models/UNet/` folder. The filename gives the
training timestamp, optimizer, loss, input bands (`01234` = blue, green, red, NIR, NDVI; `012345` adds the
crop prediction) and patch size.

## Installation

```bash
conda env create --file environment.yml
conda activate planetunet
jupyter lab
```

The study used GDAL v3.1.2, rasterio v1.2, TensorFlow v2.5 and geopandas v0.9.

### Hardware

Training and prediction ran on a single NVIDIA GeForce RTX 3090 GPU with 24 GB of memory. The batch sizes in
`config/UNetTraining.py` (8) and `config/RasterAnalysis.py` (200) are set for that card. Lower them for
GPUs with less memory. The RTX 3090 needs CUDA 11, which TensorFlow 2.5 supports.

## Tree detection

Tree detection used the published PlanetUNet tree framework, which this repository does not duplicate:

- **U-Net tree detection framework:** https://doi.org/10.5281/zenodo.3978185.
  Contact: A. Kariryaa (ak@di.ku.dk, ankit.ky@gmail.com) or F. Reiner (flr@ign.ku.dk).
- **Preparation of imagery from PlanetScope raw scenes:** https://doi.org/10.5281/zenodo.7764360.
  Contact: F. Reiner (flr@ign.ku.dk).
- Associated publication: Reiner, F. et al. (2023). More than one quarter of Africa's tree cover is
  found outside areas previously classified as forest. *Nature Communications* 14, 2258.
  https://www.nature.com/articles/s41467-023-37880-4

Those pipelines use GDAL v3.1.2, rasterio v1.2, TensorFlow v2.5, geopandas v0.9 and the Planet Python API v1.4.7.

## Acknowledgements

The `core/` modules and notebook structure are adapted from the U-Net framework by Ankit Kariryaa,
with later contributions from Sizhuo Li and Florian Reiner
(https://doi.org/10.5281/zenodo.3978185). Imagery: Planet / NICFI Satellite Data Program.

## License

Code: [MIT](LICENSE). Maps on Zenodo: CC-BY-4.0.
