import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import psutil
import numpy as np
from obspy import read
from scipy import signal
import matplotlib.pyplot as plt
from obspy.signal.invsim import corn_freq_2_paz

def browse_file(entry_var):
    """
    Browse files function
    """
    file_path = filedialog.askopenfilename(filetypes=[('SAC Files', '*.sac')])
    entry_var.set(file_path)


def plotear(z, n, e, ventana, ventaneo, overlap):


    ventana = int(ventana)
    overlap = int(overlap)

    # Cargar datos con ObsPy
    st_z = read(z)
    st_n = read(n)
    st_e = read(e)
    


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
    Calcula la relación espectral horizontal a vertical (HVSR) para datos sísmicos.
    
    Args:
        z (str): Ruta al archivo de datos de la componente Z.
        n (str): Ruta al archivo de datos de la componente N.
        e (str): Ruta al archivo de datos de la componente E.
        ventana (int): Número de muestras en la ventana.
        ventaneo (str): Tipo de ventana.
        overlap (float): Porcentaje de solapamiento.
        
    Returns:
        float: Frecuencia del sitio calculada.
    """
    ventana = int(ventana)
    overlap = int(overlap)


    # Cargar datos con ObsPy
    st_z = read(z)
    st_n = read(n)
    st_e = read(e)

    ventana_segs = ventana / st_z[0].stats.sampling_rate



    # Obtener arreglos NumPy de los datos sísmicos
    z = st_z[0].data
    n = st_n[0].data
    e = st_e[0].data

    # Overlapping calculation
    overlapping = (overlap / 100) * ventana

    # Linear detrend the data
    z = signal.detrend(z, type='linear')
    n = signal.detrend(n, type='linear')
    e = signal.detrend(e, type='linear')

    # Calculate Fourier Transform with signal.welch
    fz, Pz = signal.welch(z, fs=st_z[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')
    fn, Pn = signal.welch(n, fs=st_n[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')
    fe, Pe = signal.welch(e, fs=st_e[0].stats.sampling_rate, window=ventaneo, nperseg=ventana, noverlap=overlapping, scaling='spectrum')

    # Calculate HVSR
    Hn = Pn / Pz  # Lunedei and Albarello N
    He = Pe / Pz  # Lunedei and Albarello E
    HVSRPico = (np.sqrt(Pn * Pe)) / Pz  # Picozzi
    HVSRLuMa = np.sqrt((Pn + Pe) / Pz)  # Lunedei and Malischewsky
    Nakamura = (np.sqrt(Pn**2 + Pe**2)) / Pz  # Nakamura

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
    ax.plot(fn, Hn, label='Lunedei and Albarello N')
    ax.plot(fe, He, label='Lunedei and Albarello E')
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
                   .format(st_z[0].stats, st_n[0].stats, st_e[0].stats, ventana_segs, ventana, ventaneo, overlap,
                           frecuencia_sitio, periodo_sitio, vs, h))

    proceso_actual = psutil.Process()
    uso_de_memoria = proceso_actual.memory_info().rss
    uso_de_memoria_mb = uso_de_memoria / (1024 * 1024)
    print(f"Uso de memoria actual: {uso_de_memoria_mb:.2f} MB")

    plt.show()

    return frecuencia_sitio


def main_window():
    window_options = ['boxcar', 'triang', 'blackman', 'hamming', 'hann', 'bartlett', 'flattop', 'parzen', 'bohmann', 'blackmanharris', 'nuttall', 'barthan', 'cosine', 'exponential', 'tukey', 'taylor', 'lanczos']
    ventana_size = [1024, 2048, 4096, 8202]
    overlap_values = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

    window = tk.Tk()
    window.title('Simple-HVSR(中村)')

    # Define a Tkinter StringVar for each Entry
    sacz_var = tk.StringVar()
    sacn_var = tk.StringVar()
    sace_var = tk.StringVar()

    # Define the layout
    layout = [
        [tk.Label(text='Cargar componentes', font=('Helvetica', 14, 'bold'))],
        [tk.Label(text='Componente Z'), tk.Entry(textvariable=sacz_var), tk.Button(text='Browse', command=lambda: browse_file(sacz_var))],
        [tk.Label(text='Componente N'), tk.Entry(textvariable=sacn_var), tk.Button(text='Browse', command=lambda: browse_file(sacn_var))],
        [tk.Label(text='Componente E'), tk.Entry(textvariable=sace_var), tk.Button(text='Browse', command=lambda: browse_file(sace_var))],
        [tk.Label(text='Procesamiento',font=('Helvetica', 14, 'bold'))],
        [tk.Label(text='Muestreo'), ttk.Combobox(values=ventana_size)],
        [tk.Label(text='Ventaneo'), ttk.Combobox(values=window_options)],
        [tk.Label(text='Overlap by'), ttk.Combobox(values=overlap_values), tk.Label(text='%')],
        [tk.Button(text='Calculate HVSR', command=lambda: calculate_hvsr(sacz_var.get(), sacn_var.get(), sace_var.get(), ventana_combobox.get(), ventaneo_combobox.get(), overlap_combobox.get()))],
        [tk.Button(text='Visualize data', command=lambda: plotear(sacz_var.get(), sacn_var.get(), sace_var.get(), ventana_combobox.get(), ventaneo_combobox.get(), overlap_combobox.get()))],
        [tk.Button(text="Exit", command=lambda: exit())],
    ]

    # Populate the layout
    for row in layout:
        if row:
            for idx in range(len(row)):
                row[idx].grid(row=layout.index(row), column=idx, padx=5, pady=5)

    ventana_combobox = layout[5][1]
    ventaneo_combobox = layout[6][1]
    overlap_combobox = layout[7][1]

    # Run the main loop
    window.mainloop()

if __name__ == '__main__':
    main_window()
