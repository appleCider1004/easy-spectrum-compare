# easy-spectrum-compare
This is a set of Streamlit apps for browsing, filtering, and plotting spectra for different types of measurements with metadata-driven selection.  
The apps are designed for datasets where each spectrum is stored as a `.npy` file and each file is described by a row in a metadata CSV.

## Features

- Load metadata directory from the UI
- Filter spectra by metadata attributes (e.g. experimental conditions)
- Select multiple spectra from filtered results
- Overlay multiple spectra in one figure for the purpose of comparison
- Customize line labels and colors
- Switch to log scale
- Adjust frequency range for plotting
- Plot spectral differences relative to a selected baseline spectrum

## Repository structure

```text
.
├── app.py
├── README.md
├── requirements.txt
└── data/
    ├──metadata1.csv
    ├──metadata2.csv
    └── spectra_npy_samples1/
        ├── sample_001.npy
        ├── sample_002.npy
        └── ...
    └── spectra_npy_samples2/
        ├── sample_001.npy
        ├── sample_002.npy
        └── ...
```

## Data format

The app expects two data sources:

### 1. Metadata CSV
A CSV file containing one row per spectrum.

Example columns:

- `File_name`: The corresponding data file names
- `Damage`: Data attribute
- `RPM`: Data attribute
- `Set_wind_speed`: Data attribute
- ...
- `Path`: The corresponding data file paths

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
2. Enter the metadata CSV path.
3. Click **Load data**.
4. Use the sidebar to filter spectra by metadata.
5. Select records to plot.
6. Edit labels and line colors in the plotting section.
7. Adjust plot style, scales, and x-range as needed.

## Notes

- All `.npy` files should have a consistent format and compatible x-axis definition.
- Log-scale plotting requires positive x and y values.

## Future improvements

- Export selected plots as images
- Save and reload plot presets
- Add normalization and smoothing options
- Support CSV/Parquet spectrum formats in addition to `.npy`

## License

Choose a license for this project, for example MIT.

## Author

Muyao Li
