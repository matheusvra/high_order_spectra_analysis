import numpy as np

def time_domain_spectrum(signal: np.ndarray, frequency_sampling: float) -> tuple[np.ndarray, np.ndarray]:
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
    time = np.linspace(0, time_end, len(signal))

    fmax = np.floor(frequency_sampling/2)-1 # Nyquist Frequency
    phase_len = np.floor(len(signal)*1/frequency_sampling)
    fmin = 1/phase_len #frequencia minima de teste - pelo menos um periodo no tempo;

    fstep = 0.1
    phistep = 0.01*np.pi

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
