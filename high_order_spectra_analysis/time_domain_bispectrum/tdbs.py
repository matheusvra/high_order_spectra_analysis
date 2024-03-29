import numpy as np
import progressbar


def tdbs(
    signal: np.ndarray, 
    frequency_sampling: float, 
    time: np.ndarray | None = None,
    frequency_array: np.ndarray | None = None,
    fmin: float | None = None,
    fmax: float | None = None,
    freq_step: float = 1e-3,
    phase_step: float = 1e-3,
    dtype: np.dtype = np.float64,
    enable_progress_bar: bool = True
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Time domain bispectrum

    Args:
        signal (np.ndarray): Signal which the bispectrum will be calculated.
        frequency_sampling (float): Frequency sampling of the signal.
        time (np.ndarray | None, optional): Time array (in case of already available, if nots, it is calculated). Defaults to None.
        frequency_array (np.ndarray | None, optional): Frequency array (in case of already available, if nots, it is calculated). Defaults to None.
        fmin (float | None, optional): minimum frequency to generate spectrum. Defaults to None, but the minimum used in this case is of one period.
        fmax (float | None, optional): maximum frequency to generate spectrum. Defaults, but the maximum used in this case is the Nyquist frequency.
        freq_step (float, optional): Frequency step to scan. Defaults to 0.001.
        phase_step (float, optional): Phase step to scan. Defaults to 0.001.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]: frequency array, amplitude array, phase array
    """

    time_sampling = 1/frequency_sampling
    time_end = len(signal)*time_sampling

    if time is None:
        time = np.arange(0, time_end, time_sampling)[0:len(signal)].astype(dtype)

    fmax = np.floor(frequency_sampling/2)-1 if fmax is None else fmax # Nyquist Frequency
    phase_len = np.floor(len(signal)*1/frequency_sampling)
    fmin = 1/phase_len if fmin is None else fmin # Minimun test frequency at least one period 
    
    fstep = 0.01 if freq_step is None else freq_step
    phistep = 0.01*2*np.pi if phase_step is None else phase_step

    frequency_array = np.arange(fmin, fmax, fstep).astype(dtype) if frequency_array is None else frequency_array
    phi_array = np.arange(0, 2*np.pi, phistep).astype(dtype)

    bispectrum = np.zeros(len(frequency_array)).astype(dtype)
    phase_bispectrum = np.zeros(len(frequency_array)).astype(dtype)
    spectrum = np.zeros(len(frequency_array)).astype(dtype)
    phase_spectrum = np.zeros(len(frequency_array)).astype(dtype)
    x = np.zeros(len(frequency_array)).astype(dtype)

    if enable_progress_bar:
        bar = progressbar.ProgressBar(max_value=len(frequency_array)*len(phi_array))
        counter_step = len(phi_array)

        counter = 0

    for i, freq in enumerate(frequency_array):

        max_amplitude_spectrum: dtype = dtype('-inf')
        max_amplitude_bispectrum: dtype = dtype('-inf')
        max_phi_spectrum: dtype = dtype(-1.0)
        max_phi_bispectrum: dtype = dtype(-1.0)

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

        if enable_progress_bar:
            bar.update(counter)
            counter += counter_step

    return frequency_array, spectrum, phase_spectrum, bispectrum, phase_bispectrum
