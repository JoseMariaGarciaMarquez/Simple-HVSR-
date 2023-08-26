# HVSR-SG

HVSR-SG is a Python script that offers a user-friendly graphical user interface (GUI) for analyzing seismic data using the Horizontal-to-Vertical Spectral Ratio (HVSR) method. HVSR is a widely-used technique in seismology to investigate the amplification of ground motion across various frequencies.

## Features

1. **Seismic Data Plotting:** Visualize the three seismic data components (Z, N, E) on a single plot.
2. **HVSR Calculation:** Calculate the HVSR by providing paths to Z, N, and E seismic data files. The script performs linear detrending and computes the Fourier Transform using the Welch method.
3. **HVSR Plotting:** Plot the calculated HVSR on a logarithmic scale, along with individual spectral ratios of N and E components. Peak HVSR frequency is identified and marked on the plot.
4. **Results Saving:** Save the HVSR plot as an image file and the analysis results as a text file.

## Usage

1. Launch the script and use the file browse buttons to input paths to Z, N, and E seismic data files.
2. Select window size and a windowing function for Fourier Transform calculations.
3. Click "Calculate HVSR" to perform the analysis, generating the HVSR plot and results.
4. Use "Visualize data" to plot three seismic data components without HVSR calculation.
5. Save HVSR plot as an image and analysis results as a text file.

## Requirements

- Python 3.8 or higher
- Required libraries: ObsPy, NumPy, Matplotlib, PySimpleGUI, SciPy

## Contribution

Contributions to the project are welcome. For issues or suggestions, open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](link-to-license-file).

## Cite

- **Author:** José María
- **Title:** HVSR
- **Website:** [https://github.com/JoseMariaGarciaMarquez](https://github.com/JoseMariaGarciaMarquez) [[josemaria.me](https://www.josemaria.me)]
- **Version:** 3.0
- **Date:** June, 2023
- **E-Mail:** josemariagarcimarquez2.72@gmail.com


![Captura de Pantalla 2023-08-16 a la(s) 11 37 02](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/6f3d8218-bc8f-4cd7-9c6e-3baacf9ae5ac)

