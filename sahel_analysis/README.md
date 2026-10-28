# Sahel analysis: data and code for Figures 2 and 3

Grid-cell data, figure source data and the statistical analysis for

> Tong, X. et al. *Satellite mapping reveals complex patterns of intensively used croplands in the
> Western Sahel*. Nature Food (submitted).

The unit of analysis is a 1 × 1 km grid cell. The data cover 117,006 cells in Mali, Niger and Senegal,
grouped into 284 blocks of 0.5° for clustered errors and spatial cross-validation.

```
analysis_fig3.py                 Statistical analysis behind Fig. 3 (and the archetype shares in Fig. 2c)
data/analysis_table.csv          Full grid-cell table read by analysis_fig3.py
source_data/SourceData_Fig2.csv  Source data for Fig. 2
source_data/SourceData_Fig3.csv  Source data for Fig. 3
requirements.txt                 Python packages
```

## Running the analysis

```bash
cd sahel_analysis
pip install -r requirements.txt
python analysis_fig3.py
```

The script runs in about 30 seconds on a multi-core CPU and prints:

- the design effect of clustering on 0.5° blocks
- the controls on cultivated fraction (Fig. 3a): standardised coefficients with 95% CIs and unique R²
- spatial block cross-validation of linear and gradient-boosting models
- contrasts between cultivated-fraction classes 5 and 1 (Fig. 3e)
- the cultivated fraction × tree cover interaction on productivity
- archetype shares per country with block-bootstrap 95% CIs (Fig. 2c)
- a block permutation test of differences in archetype composition between countries

Random seeds are fixed, so repeated runs give the same numbers.

## Methods in brief

- Regressions are OLS with country fixed effects and a quadratic surface in longitude and latitude.
  Standard errors are clustered on 0.5° blocks.
- Right-skewed variables (productivity, tree cover, soil quality) are log-transformed for the class contrasts.
  Population uses log(1 + x) because 22 cells have zero population.
- Cultivated-fraction classes 1–5 are five equal-width intervals of the cultivated fraction.
- Each archetype code has three letters, each `h` (high) or `l` (low). In order they give cultivated
  fraction, productivity and tree cover. For example, `hlh` = high cultivated fraction, low productivity,
  high tree cover. The intensive archetypes (`hh*`) combine high cultivated fraction with high productivity.

## Source data

### `SourceData_Fig2.csv`

| Column | Description |
| --- | --- |
| `longitude`, `latitude` | Cell centre (WGS84) |
| `country` | Mali, Niger or Senegal |
| `cultivated_fraction` | Cultivated fraction, 1 km sliding window, min–max normalised (0–1) |
| `productivity_norm` | Productivity, min–max normalised (0–1) |
| `tree_cover_norm` | Tree cover of cropped fields, min–max normalised (0–1) |
| `archetype` | Three-letter archetype code (see above) |

### `SourceData_Fig3.csv`

| Column | Description |
| --- | --- |
| `longitude`, `latitude` | Cell centre (WGS84) |
| `country` | Mali, Niger or Senegal |
| `block_0p5deg` | ID of the 0.5° block used for clustering |
| `cultivated_fraction` | Cultivated fraction, normalised (0–1) |
| `cf_class` | Cultivated-fraction class, 1 (lowest) to 5 (highest) |
| `productivity_400mm` | Productivity normalised to 400 mm rainfall |
| `tree_cover_pct` | Tree cover of cropped fields (%) |
| `soil_quality_index` | Soil quality index |
| `rainfall_mm` | Mean annual rainfall, CHIRPS 1982–2020 (mm) |
| `population_per_cell` | Population per 1 km cell, WorldPop 2019 |
| `elevation_m` | Mean elevation (m) |

## `data/analysis_table.csv`

Columns starting with `n` are the min–max normalised (0–1) versions of the corresponding raw variables.

| Column | Description |
| --- | --- |
| `lon`, `lat` | Cell centre (WGS84) |
| `arch` | Archetype code |
| `nci` | Cultivated fraction, 1 km sliding window, normalised |
| `nndvi` | Productivity, normalised |
| `nwc30` | Tree cover of cropped fields, normalised |
| `nrf`, `ndem`, `nsqi`, `npop` | Rainfall, elevation, soil quality and population, normalised |
| `rf_mean` | Mean annual rainfall, CHIRPS 1982–2020 (mm) |
| `sqi` | Soil quality index |
| `soc_norm`, `ph_norm` | Normalised soil organic carbon and soil pH |
| `pop_sum` | Population per cell, WorldPop 2019 |
| `dem_mean` | Mean elevation (m) |
| `cwc302_mea` | Tree cover of cropped fields (%) |
| `nm1_cali` | Productivity normalised to 400 mm rainfall |
| `c_perc`, `f_perc`, `perc` | Fraction of the cell mapped as cropped, fallow, and their sum |
| `ADMIN` | Country |
| `block` | ID of the 0.5° block |

Empty cells are missing values.

## Data sources

The cropped and fallow maps come from the U-Net models in this repository; see
[the maps on Zenodo](https://doi.org/10.5281/zenodo.15261630). Rainfall: CHIRPS. Population: WorldPop 2019.
Imagery: Planet / NICFI Satellite Data Program.
