import psutil
import numpy as np
from obspy import read
from scipy import signal
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from obspy.signal.invsim import corn_freq_2_paz


def plotear(z, n, e):
    """
    Plot the seismic data components Z, N, E.
    """
    paz_sts2 = {
    'poles': [-62.382 +135.39j, -62.382 - 135.39j, -350.00 + 0j,
               -75.000 - 0j, -23.560e-3 + 23.560e-3j, -23.560e-3 + 23.560e-3j],
    'zeros': [0 + 0j, 0 + 0j],
    'gain': 60077000.0,
    'sensitivity': 5.858e+8}
    paz_1hz = corn_freq_2_paz(1.0, damp=0.707) 
    paz_1hz['sensitivity'] = 1.0

    
    # Cargar datos con ObsPy
    st_z = obspy.read(z)
    st_n = obspy.read(n)
    st_e = obspy.read(e)
    
    st_z = st_z.simulate(paz_remove = paz_sts2, paz_simulate = paz_1hz)
    st_n = st_n.simulate(paz_remove = paz_sts2, paz_simulate = paz_1hz)
    st_e = st_e.simulate(paz_remove = paz_sts2, paz_simulate = paz_1hz)

    # Obtener arreglos NumPy de los datos sísmicos
    z = st_z[0].data
    n = st_n[0].data
    e = st_e[0].data

    # Overlapping calculation
    overlapping = (overlap/100) * ventana

    # Linear detrend the data
    z = signal.detrend(z, type='linear')
    n = signal.detrend(n, type='linear')
    e = signal.detrend(e, type='linear')


    # Calculate Fourier Transform with signal.welch
    fz, Pz = signal.welch(z, fs=st_z[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')
    fn, Pn = signal.welch(n, fs=st_n[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')
    fe, Pe = signal.welch(e, fs=st_e[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')
    
    fig, ax = plt.subplots(3, 2, figsize=(15, 10), dpi=200)
    ax[0, 0].plot(st_z[0].times("matplotlib"), z)
    ax[0, 1].plot(fz, Pz)
    ax[0, 1].set_xscale('log')
    
    ax[1, 0].plot(st_n[0].times("matplotlib"), n)
    ax[1, 1].plot(fn, Pn)
    ax[1, 1].set_xscale('log')
    
    ax[2, 0].plot(st_e[0].times("matplotlib"), e)
    ax[2, 1].plot(fe, Pe)
    ax[2, 1].set_xscale('log')
    
    plt.show()

def calculate_hvsr(z, n, e, ventana, ventaneo, overlap):
    """
    Calculate the Horizontal-to-Vertical Spectral Ratio (HVSR) for seismic data.
    Args:
        z (str): Path to the Z component data file.
        n (str): Path to the N component data file.
        e (str): Path to the E component data file.
        ventana (int): Number of samples in the window.
        ventaneo (str): Type of window.
        overlap (float): Overlapping percentage.
    """
    paz_sts2 = {
    'poles': [-62.382 +135.39j, -62.382 - 135.39j, -350.00 + 0j,
               -75.000 - 0j, -23.560e-3 + 23.560e-3j, -23.560e-3 + 23.560e-3j],
    'zeros': [0 + 0j, 0 + 0j],
    'gain': 60077000.0,
    'sensitivity': 5.858e+8}
    paz_1hz = corn_freq_2_paz(1.0, damp=0.707) 
    paz_1hz['sensitivity'] = 1.0

    # Cargar datos con ObsPy
    st_z = read(z)
    st_n = read(n)
    st_e = read(e)

    ventana_segs = ventana / st_z[0].stats.sampling_rate

    st_z = st_z.simulate(paz_remove = paz_sts2, paz_simulate = paz_1hz)
    st_n = st_n.simulate(paz_remove = paz_sts2, paz_simulate = paz_1hz)
    st_e = st_e.simulate(paz_remove = paz_sts2, paz_simulate = paz_1hz)

    # Obtener arreglos NumPy de los datos sísmicos
    z = st_z[0].data
    n = st_n[0].data
    e = st_e[0].data

    # Overlapping calculation
    overlapping = (overlap/100) * ventana

    # Linear detrend the data
    z = signal.detrend(z, type='linear')
    n = signal.detrend(n, type='linear')
    e = signal.detrend(e, type='linear')

    # Calculate Fourier Transform with signal.welch
    fz, Pz = signal.welch(z, fs=st_z[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')
    fn, Pn = signal.welch(n, fs=st_n[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')
    fe, Pe = signal.welch(e, fs=st_e[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')

    # Calculate HVSR
    Hn = Pn / Pz
    He = Pe / Pz
    HVSRPico = (np.sqrt(Pn * Pe)) / Pz
    HVSRLuMa = np.sqrt((Pn + Pe) / Pz)
    Nakamura = (np.sqrt(Pn**2 + Pe**2)) / Pz

    f = (fn + fe) / 2

    # Filtrar frecuencias mayores a 0.3 Hz
    mask = f >= 0.3
    f_filtered = f[mask]


    HVSRPico_filtered = HVSRPico[mask]
    HVSRLuMa_filtered = HVSRLuMa[mask]
    Nakamura_filtered = Nakamura[mask]

    # Calcular la frecuencia y el periodo del sitio
    pos = np.argmax(Nakamura_filtered)
    frecuencia_sitio = f_filtered[pos]
    periodo_sitio = 1 / frecuencia_sitio

    vs = 1 / (2 * frecuencia_sitio)
    h = vs / (4 * frecuencia_sitio)

    # Plot the HVSR
    title = input('Título de la gráfica\n')
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    ax.axvline(frecuencia_sitio, c='lightgrey', linewidth=10)
    ax.plot(fn, Hn, label = 'Lunedei and Albarello N')
    ax.plot(fe, He, label = 'Lunedei and Albarello E')
    ax.plot(f_filtered, HVSRPico_filtered, label='Picozzi')
    ax.plot(f_filtered, HVSRLuMa_filtered, label='Lunedei and Malischewsky')
    ax.plot(f_filtered, Nakamura_filtered, label='Nakamura')
    ax.axvline(frecuencia_sitio, c='black', linestyle='--', label='Frecuencia del sitio')
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('HVSR')
    ax.set_title(title)
    ax.set_xscale('log')
    ax.set_xlim(0.3, 40)
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Save the figure
    nombre = input('Nombre del archivo\n')
    plt.savefig('{}.png'.format(nombre), bbox_inches='tight')

    # Save the results to a text file
    with open('resultados_{}.txt'.format(nombre), 'w') as file:
     file.write('------------------------------------------🥑RESULTADOS🥑------------------------------------------\n'
                       'Datos:\n{}\n{}\n{}\n'
                       '-------------------------------------------------------------------------------------------------\n'
                       'Con un ventaneo de {}s que asegura {} muestras\n'
                       'Y el tipo de ventana usada de {}\n'
                       'Con un solapamiento del {}%\n'
                       'La frecuencia del sitio es {}[Hz]\n'
                       'El periodo del sitio es {}[m]\n'
                       'El cálculo de la velocidad de corte es {}[m/s]\n'
                       'El espesor de la capa de sedimento es de {}[m]\n'
                       '-------------------------------------------------------------------------------------------------\n'
                       .format(st_z[0].stats, st_n[0].stats, st_e[0].stats, ventana_segs,ventana, ventaneo, overlap, frecuencia_sitio,periodo_sitio, vs, h))

    proceso_actual = psutil.Process()
    uso_de_memoria = proceso_actual.memory_info().rss 
    uso_de_memoria_mb = uso_de_memoria / (1024 * 1024)
    print(f"Uso de memoria actual: {uso_de_memoria_mb:.2f} MB")

    plt.show()

    return frecuencia_sitio

def main_window():
    window_options = ['boxcar', 'triang', 'blackman', 'hamming', 'hann', 'bartlett', 'flattop', 'parzen', 'bohmann', 'blackmanharris', 'nuttall', 'barthan', 'cosine', 'exponential', 'tukey', 'taylor', 'lanczos']
    ventana_size = [1024, 2048, 4096, 8202]
    overlap = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    # Define the layout
    layout = [
        [sg.Text('---------------------------------------------------Cargar componentes---------------------------------------------------')],
        [sg.Text('Componente Z'), sg.Input(key='-SACZ-'), sg.FileBrowse()],
        [sg.Text('Componente N'), sg.Input(key='-SACN-'), sg.FileBrowse()],
        [sg.Text('Componente E'), sg.Input(key='-SACE-'), sg.FileBrowse()],
        [sg.Text('-----------------------------------------------------Procesamiento-----------------------------------------------------')],
        [sg.Text('Muestreo'), sg.Combo(ventana_size, key='-VENTANA-'),sg.Text('Ventaneo'), sg.Combo(window_options, key='-WINDOW-'), sg.Text('Overlap by'), sg.Combo(overlap, key='OLAP'), sg.Text('%')],
        [sg.Text('---------------------------------------------------------------------------------------------------------------------------------')],
        [sg.Button('Calculate HVSR'), sg.Button('Visualize data')],
        [sg.Button("Exit")],
    ]

    window = sg.Window('Simple-HVSR(中村)', layout)

    # While the window is open
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

        if event == 'Calculate HVSR':
            calculate_hvsr(values['-SACZ-'], values['-SACN-'], values['-SACE-'], values['-VENTANA-'], values['-WINDOW-'], values['OLAP'])

        if event == 'Visualize data':
            plotear(values['-SACZ-'], values['-SACN-'], values['-SACE-'])

    window.close()

if __name__ == '__main__':
    main_window()
