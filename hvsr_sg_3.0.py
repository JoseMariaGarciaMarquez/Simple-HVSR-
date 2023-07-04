import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from scipy.fft import fft, fftshift, ifft, ifftshift
from scipy import signal
from obspy import read

def plotear(z, n, e):
    """
    Plot the seismic data components Z, N, E.
    """
    st = read(z)
    st += read(n)
    st += read(e)

    st.plot()

def calculate_hvsr(z, n, e, ventana, ventaneo):
    """
    Calculate the Horizontal-to-Vertical Spectral Ratio (HVSR) for seismic data.
    """
    st = read(z)
    st += read(n)
    st += read(e)

    # Linear detrend the data
    st.detrend('linear')
    z = st[0]
    n = st[1]
    e = st[2]

    # Calculate Fourier Transform with signal.welch
    fz, Pz = signal.welch(z, fs=z.stats.sampling_rate, window=ventaneo, nperseg=ventana, scaling='density')
    fn, Pn = signal.welch(n, fs=n.stats.sampling_rate, window=ventaneo, nperseg=ventana, scaling='density')
    fe, Pe = signal.welch(e, fs=e.stats.sampling_rate, window=ventaneo, nperseg=ventana, scaling='density')

    # Calculate HVSR
    Hn = Pn / Pz
    He = Pe / Pz
    f = (fn + fe) / 2
    H = (Hn + He) / 2

    pos = np.argmax(H)
    frecuencia_sitio = f[pos]
    periodo_sitio = 1 / frecuencia_sitio

    # Plot the HVSR
    title = sg.popup_get_text('Título de la gráfica')
    fig, ax = plt.subplots(figsize=(3, 2), dpi=300)
    ax.axvline(frecuencia_sitio, c='lightgrey', linewidth=10)
    ax.plot(fn, Hn)
    ax.plot(fe, He)
    ax.plot(f, H)
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('HVSR')
    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid()

    # Save the figure
    nombre = sg.popup_get_text('Nombre del archivo')
    plt.savefig('{}.png'.format(nombre), bbox_inches='tight')

    # Save the results to a text file
    with open('resultados_{}.txt'.format(nombre), 'w') as file:
        file.write('---------------------------------------🥑RESULTADOS🥑---------------------------------------\n'
                   'Datos:\n{}\n{}\n{}\n'
                   '-------------------------------------------------------------------------------------------------\n'
                   'Con un ventaneo que asegura {} muestras\n'
                   'Y eltipo de ventana usada de {}\n'
                   'La frecuencia del sitio es {}[Hz]\n'
                   'El periodo del sitio es {}[m]\n'
                   '-------------------------------------------------------------------------------------------------\n'
                   .format(z.stats, n.stats, e.stats, ventana, ventaneo, frecuencia_sitio, periodo_sitio))

    plt.show()

def main_window():
    window_options = ['boxcar', 'triang', 'blackman', 'hamming', 'hann']
    ventana_size = [1024, 2048, 4096, 8202]

    # Define the layout
    layout = [
        [sg.Text('Componente Z'), sg.Input(key='-SACZ-'), sg.FileBrowse()],
        [sg.Text('Componente N'), sg.Input(key='-SACN-'), sg.FileBrowse()],
        [sg.Text('Componente E'), sg.Input(key='-SACE-'), sg.FileBrowse()],
        [sg.Text('Muestreo'), sg.Combo(ventana_size, key='-VENTANA-')],
        [sg.Text('Ventaneo'), sg.Combo(window_options, key='-WINDOW-')],
        [sg.Button('Calculate HVSR'), sg.Button('Visualize data')],
        [sg.Button("Exit")],
    ]

    window = sg.Window('HVSR', layout)

    # While the window is open
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

        if event == 'Calculate HVSR':
            calculate_hvsr(values['-SACZ-'], values['-SACN-'], values['-SACE-'], values['-VENTANA-'], values['-WINDOW-'])

        if event == 'Visualize data':
            plotear(values['-SACZ-'], values['-SACN-'], values['-SACE-'])

    window.close()

if __name__ == '__main__':
    main_window()
