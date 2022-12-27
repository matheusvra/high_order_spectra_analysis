import numpy as np
import matplotlib.pyplot as plt
import time
import progressbar
from high_order_spectra_analysis.time_domain_spectrum.tds import tds
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def tdbs(
    signal: np.ndarray, 
    frequency_sampling: float, 
    time: np.ndarray | None = None,
    fmin: float | None = None,
    fmax: float | None = None,
    freq_step: float = 1e-3,
    phase_step: float = 1e-3
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Time domain bispectrum

    Args:
        signal (np.ndarray): Signal which the spectrum will be calculated.
        frequency_sampling (float): Frequency sampling of the signal.
        time (np.ndarray | None, optional): Time array (in case of already available, if nots, it is calculated). Defaults to None.
        fmin (float | None, optional): minimum frequency to generate spectrum. Defaults to None, but the minimum used in this case is of one period.
        fmax (float | None, optional): maximum frequency to generate spectrum. Defaults, but the maximum used in this case is the Nyquist frequency.
        freq_step (float, optional): Frequency step to scan. Defaults to 0.001.
        phase_step (float, optional): Phase step to scan. Defaults to 0.001.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: frequency array, amplitude array, phase array
    """

    time_sampling = 1/frequency_sampling
    time_end = len(signal)*time_sampling

    if time is None:
        time = np.arange(0, time_end, time_sampling)[0:len(signal)]

    fmax = np.floor(frequency_sampling/2)-1 if fmax is None else fmax # Nyquist Frequency
    phase_len = np.floor(len(signal)*1/frequency_sampling)
    fmin = 1/phase_len if fmin is None else fmin # Minimun test frequency at least one period 
    
    fstep = 0.01 if freq_step is None else freq_step
    phistep = 0.01*2*np.pi if phase_step is None else phase_step

    frequency_array = np.arange(fmin, fmax, fstep)
    phi_array = np.arange(0, 2*np.pi, phistep)

    bispectrum = np.zeros(len(frequency_array))
    phase_bispectrum = np.zeros(len(frequency_array))
    spectrum = np.zeros(len(frequency_array))
    phase_spectrum = np.zeros(len(frequency_array))
    x = np.zeros(len(frequency_array))

    bar = progressbar.ProgressBar(max_value=len(frequency_array)*len(phi_array))
    counter_step = len(phi_array)

    counter = 0

    for i, freq in enumerate(frequency_array):

        max_amplitude_spectrum: float = float('-inf')
        max_amplitude_bispectrum: float = float('-inf')
        max_phi_spectrum: float = -1.0
        max_phi_bispectrum: float = -1.0

        for phi in phi_array:
        
            # x = P^2 for \Omega = \omega/2
            x = np.cos(np.pi*freq*time + phi)**2
            # x = SP^2
            x = signal * x
            # evaluated_x = mean(SP^2)
            evaluated_spectrum = np.mean(x)

            update_max: bool = evaluated_spectrum > max_amplitude_spectrum
            max_amplitude_spectrum = evaluated_spectrum if update_max else max_amplitude_spectrum
            max_phi_spectrum = phi if update_max else max_phi_spectrum

            # x = S^2
            x = np.power(signal, 2)
            # x = S^2P
            x = x * np.cos(2*np.pi*freq*time + phi)
            # evaluated_x = mean(S^2P)
            evaluated_bispectrum = np.mean(x)

            update_max: bool = evaluated_bispectrum > max_amplitude_bispectrum

            max_amplitude_bispectrum = evaluated_bispectrum if update_max else max_amplitude_bispectrum
            max_phi_bispectrum = phi if update_max else max_phi_bispectrum


        bispectrum[i] = max_amplitude_bispectrum*max_amplitude_spectrum
        phase_bispectrum[i] = max_phi_bispectrum
        spectrum[i] = max_amplitude_spectrum
        phase_spectrum[i] = max_phi_spectrum

        bar.update(counter)
        counter += counter_step

    return frequency_array, spectrum, phase_spectrum, bispectrum, phase_bispectrum


if __name__ == "__main__":
    time_step = 0.003
    fs = 1/time_step
    time = np.arange(0, 5, time_step)

    freqs = np.array([31, 40, 69])
    w1, w3 = tuple(2*np.pi*np.array(freqs[::2]))
    phases = np.pi*np.array([0.53, 1.14, 0.09])
    phi1, phi3 = phases[0], phases[2]
    gains = np.array([1.14, 0.92, 1.13])

    clean_signal = np.zeros(len(time))

    for freq, phase, gain in zip(freqs, phases, gains):
        clean_signal += gain*np.cos(2*np.pi*freq*time + phase) + np.cos((w1 + w3)*time + (phi1 + phi3))


    signal = clean_signal 

    frequency_array, spectrum, phase_spectrum, bispectrum, phase_bispectrum = tdbs(
        signal=signal,
        frequency_sampling=fs,
        time=None,
        fmin=None,
        fmax=None,
        freq_step=0.1,
        phase_step=0.1
    )

    fig = make_subplots(rows=3, cols=1)

    fig.append_trace(go.Scatter(
        x=time,
        y=signal,
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=frequency_array,
        y=spectrum,
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
        x=frequency_array,
        y=bispectrum,
    ), row=3, col=1)

    fig.show()
