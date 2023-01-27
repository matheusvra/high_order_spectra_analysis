import numpy as np
import progressbar


def tds(
    signal: np.ndarray, 
    frequency_sampling: float, 
    time: np.ndarray | None = None,
    fmin: float | None = None,
    fmax: float | None = None,
    freq_step: float = 1e-3,
    phase_step: float = 1e-3
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Time domain spectrum

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

    amplitude = np.zeros(len(frequency_array))
    phase = np.zeros(len(frequency_array))

    s_squared = np.power(signal, 2)
    mean_s_squared = np.mean(s_squared)
    

    bar = progressbar.ProgressBar(max_value=len(frequency_array)*len(phi))

    counter = 0
    step_counter = len(phi)

    def f(phi, f, time, signal, mean_s_squared): 
        x = signal + np.cos(2*np.pi*f*time + phi)
        x = np.power(x, 2)
        x = np.mean(x)
        x = x - mean_s_squared
        x = x - 0.5
        return x

    f_vectorized = np.vectorize(
        f,
        excluded=['f', 'time', 'signal', 'mean_s_squared']
    )

    for i in range(len(frequency_array)):
        f_evaluated = f_vectorized(
            phi=phi,
            f=frequency_array[i],
            time=time,
            signal=signal,
            mean_s_squared=mean_s_squared
        )
        counter += step_counter
        bar.update(counter)
            
        maximum_amplitude = np.max(f_evaluated)
        index_max = np.argwhere(f_evaluated == maximum_amplitude).reshape(-1)[0]
        amplitude[i] = maximum_amplitude
        phase[i] = phi[index_max]
        
    return frequency_array, amplitude, phase
