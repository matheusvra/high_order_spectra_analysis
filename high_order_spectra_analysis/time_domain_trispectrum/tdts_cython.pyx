import numpy as np

# "cimport" is used to import special compile-time information
# about the numpy module (this is stored in a file numpy.pxd which is
# currently part of the Cython distribution).
cimport numpy as np

from numpy.math cimport INFINITY

# It's necessary to call "import_array" if you use any part of the
# numpy PyArray_* API. From Cython 3, accessing attributes like
# ".shape" on a typed Numpy array use this API. Therefore we recommend
# always calling "import_array" whenever you "cimport numpy"
np.import_array()

def tdts(
    np.ndarray signal, 
    float frequency_sampling, 
    np.ndarray frequency_array,
    float phase_step,
):
    """Time domain trispectrum

    Args:
        signal (np.ndarray): Signal which the trispectrum will be calculated.
        frequency_sampling (float): Frequency sampling of the signal.
        frequency_array (np.ndarray | None, optional): Frequency array (in case of already available, if nots, it is calculated). Defaults to None.
        phase_step (float, optional): Phase step to scan. Defaults to 0.001.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]: frequency array, amplitude array, phase array
    """

    cdef np.uint32_t N = signal.shape[0]
    cdef np.float32_t time_sampling = 1/frequency_sampling
    cdef np.float32_t max_time = N*time_sampling
    cdef np.ndarray time = np.linspace(0, max_time, N, dtype="float32_t")
    cdef np.ndarray phi_array = np.arange(0, 2*np.pi, phase_step, dtype="float32_t")
    cdef np.ndarray bispectrum = np.zeros(N, dtype="float32_t")
    cdef np.ndarray phase_bispectrum = np.zeros(N, dtype="float32_t")
    cdef np.ndarray spectrum = np.zeros(N, dtype="float32_t")
    cdef np.ndarray phase_spectrum = np.zeros(N, dtype="float32_t")
    cdef np.ndarray trispectrum = np.zeros(N, dtype="float32_t")
    cdef np.ndarray phase_trispectrum = np.zeros(N, dtype="float32_t")
    cdef np.ndarray squared_signal = np.power(signal, 2, dtype="float32_t")
    cdef np.ndarray cubed_signal = np.power(signal, 3, dtype="float32_t")
    cdef np.float32_t max_amplitude_spectrum = -INFINITY
    cdef np.float32_t max_amplitude_bispectrum = -INFINITY
    cdef np.float32_t max_amplitude_trispectrum = -INFINITY
    cdef np.float32_t max_phi_spectrum = -1
    cdef np.float32_t max_phi_bispectrum = -1
    cdef np.float32_t max_phi_trispectrum = -1
    cdef np.float32_t phi = 0
    cdef np.ndarray P = np.zeros(N, dtype="float32_t") 
    cdef np.ndarray SP =  np.zeros(N, dtype="float32_t")  
    cdef np.float32_t evaluated_spectrum = np.zeros(N, dtype="float32_t")
    cdef np.ndarray S2P = np.zeros(N, dtype="float32_t")
    cdef np.float32_t evaluated_bispectrum = np.zeros(N, dtype="float32_t")
    cdef np.ndarray S3P = np.zeros(N, dtype="float32_t")
    cdef np.ndarray evaluated_trispectrum = np.zeros(N, dtype="float32_t")
    cdef np.float32_t freq = 0

    phase_length = phi_array.shape[0]

    for i in range(N):

        freq = frequency_array[i]

        max_amplitude_spectrum = -INFINITY
        max_amplitude_bispectrum = -INFINITY
        max_amplitude_trispectrum = -INFINITY
        max_phi_spectrum = -1
        max_phi_bispectrum = -1
        max_phi_trispectrum = -1

        for j in range(phase_length):
        
            phi = phi_array[j]

            P = np.cos(2*np.pi*freq*time + phi, dtype="float32_t")

            # Spectrum
    
            # x = SP
            SP =  np.multiply(signal, P, dtype="float32_t")
            # evaluated_x = mean(SP^2)
            evaluated_spectrum = np.mean(SP, dtype="float32_t")

            if evaluated_spectrum > max_amplitude_spectrum:
                max_amplitude_spectrum = evaluated_spectrum
                max_phi_spectrum = phi 

            # Bispectrum
            # x = S^2P
            S2P = np.multiply(squared_signal, P, dtype="float32_t")
            # evaluated_x = mean(S^2P)
            evaluated_bispectrum = np.mean(S2P, dtype="float32_t")

            if evaluated_bispectrum > max_amplitude_bispectrum:
                max_amplitude_bispectrum = evaluated_bispectrum
                max_phi_bispectrum = phi


            # Trispectrum
            # x = S^3P
            S3P = np.multiply(cubed_signal, P, dtype="float32_t")
            # evaluated_x = mean(S^3P)
            evaluated_trispectrum = np.mean(S3P, dtype="float32_t")

            if evaluated_trispectrum > max_amplitude_trispectrum:
                max_amplitude_trispectrum = evaluated_trispectrum
                max_phi_trispectrum = phi

        spectrum[i] = max_amplitude_spectrum
        phase_spectrum[i] = max_phi_spectrum
        bispectrum[i] = max_amplitude_bispectrum*max_amplitude_spectrum
        phase_bispectrum[i] = max_phi_bispectrum
        trispectrum[i] = max_amplitude_trispectrum*max_amplitude_spectrum*max_amplitude_bispectrum
        phase_trispectrum[i] = max_phi_trispectrum

    return frequency_array, spectrum, phase_spectrum, bispectrum, phase_bispectrum, trispectrum, phase_trispectrum



