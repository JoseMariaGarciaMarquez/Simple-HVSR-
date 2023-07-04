# HVSR-SG
This Python script provides a graphical user interface (GUI) for analyzing seismic data using the HVSR method. HVSR is a technique used in seismology to study the amplification of ground motion at different frequencies.

The script utilizes the following libraries and tools:
- ObsPy: A Python library for processing and analyzing seismological data.
- NumPy: A library for numerical computing in Python.
- Matplotlib: A plotting library for creating visualizations.
- PySimpleGUI: A simple yet powerful GUI framework for Python.
- SciPy: A library for scientific and technical computing in Python.

Features:
1. Plotting Seismic Data: The script allows users to visualize the three components (Z, N, E) of seismic data in a single plot.
2. HVSR Calculation: Users can calculate the HVSR by providing the paths to the Z, N, and E seismic data files. The script performs linear detrending and calculates the Fourier Transform using the Welch method.
3. HVSR Plotting: The calculated HVSR is plotted on a logarithmic scale, along with the individual spectral ratios of the N and E components. The script identifies the peak HVSR frequency and marks it on the plot.
4. Saving Results: Users can save the HVSR plot as an image file and the analysis results as a text file.

Usage:
1. Run the script and provide the paths to the Z, N, and E seismic data files using the file browse buttons.
2. Select the desired window size and windowing function for the Fourier Transform calculation.
3. Click "Calculate HVSR" to perform the analysis and generate the HVSR plot and results.
4. Click "Visualize data" to plot the three seismic data components without performing the HVSR calculation.
5. The HVSR plot can be saved as an image file, and the analysis results are saved as a text file.

Note: This script requires Python 3.8 or higher and the installation of the required libraries.

Contributing:
Contributions to the project are welcome. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

License:
This project is licensed under the [MIT License](link-to-license-file).

Please, cite me:

Author: José María
Title: HVSR
Website: https://github.com/JoseMariaGarciaMarquez
Version: 3.0
Date: June, 2023
E-Mail: josemariagarcimarquez2.72@gmail.com
Location: Benito Juárez, CDMX, México

![Captura de Pantalla 2023-07-03 a la(s) 22 52 39](https://github.com/JoseMariaGarciaMarquez/HVSR-SG/assets/30852961/2d8e3171-066d-42aa-a05c-162c61caefa4)
