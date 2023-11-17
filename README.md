# Simple-HVSR(中村)

Simple-HVSR(中村) is a Python script that offers a user-friendly graphical user interface (GUI) for analyzing seismic data using the Horizontal-to-Vertical Spectral Ratio (HVSR) method. HVSR is a widely-used technique in seismology to investigate the amplification of ground motion across various frequencies.

## Features

1. **Seismic Data Plotting:** Visualize the three seismic data components (Z, N, E) on a single plot.![Captura de Pantalla 2023-11-11 a la(s) 19 15 22](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/9c179d11-3db0-4192-b1ab-8e05e469d746)
2. **HVSR Calculation:** Calculate the HVSR by providing paths to Z, N, and E seismic data files. The script performs linear detrending and computes the Fourier Transform using the Welch method.
3. **HVSR Plotting:** Plot the calculated HVSR on a logarithmic scale, along with individual spectral ratios of N and E components. Peak HVSR frequency is identified and marked on the plot.![ejemplo_a](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/0e1358d6-192d-4eac-82ff-978d31d78f89)

4. **Results Saving:** Save the HVSR plot as an image file and the analysis results as a text file.![res](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/56861742-b751-455f-95df-854581e526fc)


## Usage

1. Launch the script and use the file browse buttons to input paths to Z, N, and E seismic data files.![ventana2](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/32747eb0-1edb-49ef-991d-20c25b3c41df)

2. Select window size and a windowing function for Fourier Transform calculations.![ventana](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/e207aced-d725-47b5-b442-2d27b739c80c)

3. Click "Calculate HVSR" to perform the analysis, generating the HVSR plot and results.<img width="1278" alt="terminal5" src="https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/e8da8629-5f60-4cdc-bf9f-3ab2bf2a86de">

4. Use "Visualize data" to plot three seismic data components without HVSR calculation.
5. Save HVSR plot as an image and analysis results as a text file.

## Requirements

- Python 3.8 or higher
- Required libraries: ObsPy, NumPy, Matplotlib, tkinter, SciPy

## Contribution

Contributions to the project are welcome. For issues or suggestions, open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](link-to-license-file).

## Cite

- **Author:** José María
- **Title:** Simple-HVSR(中村)
- **Website:** [josemaria.me](https://www.josemaria.me)
- **Version:** 4.0
- **Date:** June, 2023
- **E-Mail:** josemariagarcimarquez2.72@gmail.com

