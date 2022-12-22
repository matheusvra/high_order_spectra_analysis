import numpy as np
import matplotlib.pyplot as plt
import time
import progressbar
from high_order_spectra_analysis.time_domain_spectrum.tds import tds
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# import gc


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
    phi = np.arange(0, 2*np.pi, phistep)

    spectrum = np.zeros(len(frequency_array))
    bispectrum = np.zeros(len(frequency_array))
    phase_spectrum = np.zeros(len(frequency_array))
    phase_bispectrum = np.zeros(len(frequency_array))


    S2 = np.power(signal, 2)

    bar = progressbar.ProgressBar(max_value=2*len(frequency_array)*len(phi))
    counter_step = 2*len(phi)

    # f2 = mean(signal*(cos(pi*f*t + phi))^2))))
    f1 = np.vectorize(
        lambda phi, f, time, signal: np.mean(np.power(np.cos(np.pi*f*time * phi), 2) * signal),
        excluded = ['f', 'time', 'signal']
    )

    # f2 = mean(signal*(cos(2pi*f*t + phi))^2))))
    f2 = np.vectorize(
        lambda phi, f, time, S2: np.mean(np.cos(2*np.pi*f*time + phi) * S2),
        excluded=['f', 'time', 'S2']
    )

    counter = 0
    for i in range(len(frequency_array)):
        
        evaluated_f1 = f1(
            phi=phi,
            f=frequency_array[i],
            time=time,
            signal=signal
        )

        maximum_amplitude = np.max(evaluated_f1)
        index_max = np.argwhere(evaluated_f1 == maximum_amplitude).reshape(-1)[0]
        # del evaluated_f1
        # gc.collect()
        spectrum[i] = maximum_amplitude
        phase_spectrum[i] = phi[index_max]

        evaluated_f2 = f2(
            phi=phi,
            f=frequency_array[i],
            time=time,
            S2=S2
        )

        maximum_amplitude = np.max(evaluated_f2)
        index_max = np.argwhere(evaluated_f2 == maximum_amplitude).reshape(-1)[0]
        # del evaluated_f2
        # gc.collect()
        bispectrum[i] = maximum_amplitude*spectrum[i]
        phase_bispectrum[i] = phi[index_max]

        counter += counter_step
        bar.update(counter)

    return frequency_array, spectrum, phase_spectrum, bispectrum, phase_bispectrum


if __name__ == "__main__":
    time_step = 0.001
    fs = 1/time_step
    time = np.arange(0, 5, time_step)

    freqs = np.array([12, 53, 150, 314, 498])
    phases = np.pi*np.array([0.5, 0.25, 1, 0, 3/4])
    gains = np.array([0.8, 0.7, 0.9, 1, 0.4])

    clean_signal = np.zeros(len(time))

    for freq, phase, gain in zip(freqs, phases, gains):
        clean_signal += gain*np.cos(2*np.pi*freq*time + phase)


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
        y=bispectrum,
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
        x=frequency_array,
        y=phase_bispectrum,
    ), row=3, col=1)

    fig.show()
