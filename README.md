# Simple-HVSR(中村)

Simple-HVSR(中村) is a Python script that offers a user-friendly graphical user interface (GUI) for analyzing seismic data using the Horizontal-to-Vertical Spectral Ratio (HVSR) method. HVSR is a widely-used technique in seismology to investigate the amplification of ground motion across various frequencies.

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
- **Website:** [josemaria.me](https://www.josemaria.me)
- **Version:** 3.7.2
- **Date:** June, 2023
- **E-Mail:** josemariagarcimarquez2.72@gmail.com

![interfaz1](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/6326f85c-169b-4bc2-9bac-6d86117f7a74)
![interfaz2](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/bd875391-b051-45f6-8123-6802df2338e2)
![terminal4](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/20e52907-06b2-4c70-8c78-9899b0f6416f)
![ejemplo_b](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/f752a08d-0a84-4f2e-b1c9-cdf4f189c3b8)
![resultados](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/4831544f-3c56-40fd-a3d2-65ce4798790f)
