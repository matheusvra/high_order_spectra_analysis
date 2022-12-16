import numpy as np
import matplotlib.pyplot as plt


def tds(
    signal: np.ndarray, 
    frequency_sampling: float, 
    time: np.ndarray | None = None,
    fmin: float | None = None,
    fmax: float | None = None,
    freq_step: float | None = None,
    phase_step: float | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    %TDS Time Domain Spectrum
    L,f = TDS(s,fs,t,flag)
    s = signal
    fs = sampling frequency
    t = time vector
    flagplot = 1, a figure is created
    """
    time_sampling = 1/frequency_sampling
    time_end = len(signal)/time_sampling
    if time is None:
        time = np.linspace(0, time_end, len(signal))

    fmax = np.floor(frequency_sampling/2)-1 if fmax is None else fmax # Nyquist Frequency
    phase_len = np.floor(len(signal)*1/frequency_sampling)
    fmin = 1/phase_len if fmin is None else fmin #frequencia minima de teste - pelo menos um periodo no tempo;

    fstep = 0.1 if freq_step is None else fmin
    phistep = 0.01*np.pi if phase_step is None else phase_step

    frequency_array = np.arange(fmin, fmax, fstep)
    phi = np.arange(0, 2*np.pi, phistep)

    amplitude = np.zeros(len(frequency_array))
    phase = np.zeros(len(frequency_array))
    aux = np.zeros((1,len(phi)))

    S = np.power(signal, 2)
    D = 1

    for i in range(len(frequency_array)):
        for j in range(len(phi)):
            x = signal + D*np.cos(2*np.pi*(frequency_array[i]*time) + phi[j])
            aux[j] = np.mean(np.power(x, 2)) - np.mean(S) - 0.5;                
            
        maximum_amplitude = np.max(aux)
        index_max = np.argwhere(aux == maximum_amplitude)[0][0]
        amplitude[i] = maximum_amplitude
        phase[i] = phi(index_max)
        
    return frequency_array, amplitude, phase


if __name__ == "__main__":
    time_step = 0.1
    fs = 1/time_step
    time = np.arange(0, 5, time_step)
    f1 = 12
    phi1 = np.pi*0.5
    f2 = 19
    phi2 = np.pi*0.5
    f3 = 21
    phi3 = np.pi*0.5
    signal = np.cos(2*np.pi*f1*time + phi1) + np.cos(2*np.pi*f2*time + phi2) + np.cos(2*np.pi*f3*time + phi3)
    plt.figure(figsize=(14,12))
    plt.plot(time, signal)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()

    frequency_array, amplitude, phase = tds(
        signal=signal,
        frequency_sampling=fs,
        time=time,
        fmin=10,
        fmax=25,
        freq_step=1,
        phase_step=0.1
    )

    plt.figure(figsize=(14,12))
    plt.subplot(211)
    plt.plot(frequency_array, amplitude)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Spectrum Amplitude")
    plt.subplot(212)
    plt.plot(frequency_array, phase)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Spectrum Phase")
    plt.show()
