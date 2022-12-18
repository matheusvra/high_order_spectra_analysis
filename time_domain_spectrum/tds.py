import numpy as np
import matplotlib.pyplot as plt
import time
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
    
    fstep = 0.01 if freq_step is None else fmin
    phistep = 0.01*np.pi if phase_step is None else phase_step

    frequency_array = np.arange(fmin, fmax, fstep)
    phi = np.arange(0, 2*np.pi, phistep)

    amplitude = np.zeros(len(frequency_array))
    phase = np.zeros(len(frequency_array))
    aux = np.zeros(len(phi))

    S = np.power(signal, 2)

    D = 1

    bar = progressbar.ProgressBar(max_value=len(frequency_array)*len(phi))

    counter = 0
    for i in range(len(frequency_array)):
        for j in range(len(phi)):
            x = signal + D*np.cos(2*np.pi*(frequency_array[i]*time) + phi[j])
            aux[j] = np.mean(np.power(x, 2)) - np.mean(S) - 0.5;                
            counter +=1 
            if counter % 100 == 0:
                bar.update(counter)
            
        maximum_amplitude = np.max(aux)
        index_max = np.argwhere(aux == maximum_amplitude)[0][0]
        amplitude[i] = maximum_amplitude
        phase[i] = phi[index_max]
        
    return frequency_array, amplitude, phase


if __name__ == "__main__":
    time_step = 0.001
    fs = 1/time_step
    time = np.arange(0, 5, time_step)

    freqs = np.array([12, 53, 150, 314, 498])
    phases = np.pi*np.array([0.5, 0.25, 1, 0, 3/4])

    clean_signal = np.zeros(len(time))

    for freq, phase in zip(freqs, phases):
        clean_signal += np.cos(2*np.pi*freq*time + phase)

    noise = np.random.normal(loc=0, scale=2.5*np.std(clean_signal), size=(len(time,)))

    signal = clean_signal + noise

    frequency_array, amplitude, phase = tds(
        signal=signal,
        frequency_sampling=fs,
        time=None,
        fmin=None,
        fmax=None,
        freq_step=1,
        phase_step=1
    )

    plt.figure(num=1, figsize=(14,12))
    plt.plot(time, signal)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.savefig('time_domain_waveform3.png', format='png')
    plt.savefig('time_domain_waveform3.eps', format='eps')
    plt.show()

    plt.figure(num=2, figsize=(14,12))
    plt.subplot(211)
    plt.plot(frequency_array, amplitude)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Spectrum Amplitude")
    plt.subplot(212)
    plt.plot(frequency_array, phase)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Spectrum Phase")
    plt.yticks([0, np.pi, 2*np.pi], ["$0$", "$\\pi$", "$2\\pi$", ])
    plt.savefig('time_domain_spectrum3.png', format='png')
    plt.savefig('time_domain_spectrum3.eps', format='eps')
    plt.show()
