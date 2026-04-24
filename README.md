# easy-spectrum-compare
This is a light application for visualizing and comparing spectra under different experimental conditions.

A Streamlit app for browsing, filtering, and plotting spectra with metadata-driven selection.  
The app is designed for datasets where each spectrum is stored as a `.npy` file and each file is described by a row in a metadata CSV.

## Features

- Load metadata and spectrum directories from the UI
- Filter spectra by metadata attributes
- Select multiple spectra from filtered results
- Overlay multiple spectra in one Plotly figure
- Customize line labels and colors
- Switch to log scale
- Adjust x-axis plotting range
- Plot spectral differences relative to a selected reference
- Cache metadata and spectrum loading for faster reruns

## Repository structure

```text
.
├── app.py
├── README.md
├── requirements.txt
└── data/
    ├── metadata.csv
    └── spectra_npy/
        ├── sample_001.npy
        ├── sample_002.npy
        └── ...
```

## Data format

The app expects two data sources:

### 1. Metadata CSV
A CSV file containing one row per spectrum.

Example columns:

- `File_name`
- `Date`
- `Damage`
- `RPM`
- `Set_wind_speed`
- `Work_as_turbine`

### 2. Spectrum files
Each spectrum is stored as a `.npy` file.

The file name must match the value in `File_name` from the metadata table.

Example:

- Metadata row: `File_name = sample_001`
- Spectrum file: `sample_001.npy`

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit pandas numpy plotly
```

## Run the app

```bash
python -m streamlit run app.py
```

Then open the local URL shown in the terminal.

## Usage

1. Start the app.
2. Enter the metadata CSV path and the `.npy` spectra folder path.
3. Click **Load data**.
4. Use the sidebar to filter spectra by metadata.
5. Select records to plot.
6. Edit labels and line colors in the plotting section.
7. Adjust plot style, scales, and x-range as needed.

## Notes

- All `.npy` files should have a consistent format and compatible x-axis definition.
- Log-scale plotting requires positive x and y values.
- Cached loading is used to improve responsiveness during reruns.

## Future improvements

- Export selected plots as images
- Save and reload plot presets
- Add normalization and smoothing options
- Support CSV/Parquet spectrum formats in addition to `.npy`

## License

Choose a license for this project, for example MIT.

## Author

MUYAO LI
