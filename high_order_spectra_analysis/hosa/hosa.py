import numpy as np
from high_order_spectra_analysis.time_domain_spectrum.tds import tds
from high_order_spectra_analysis.time_domain_bispectrum.tdbs import tdbs
from high_order_spectra_analysis.time_domain_tetraspectrum.tdt4s import tdt4s
from high_order_spectra_analysis.time_domain_trispectrum.tdts import tdts

class Tdhosa:

    def __init__(
        self,
        frequency_sampling: float,
        frequency_array: np.ndarray | None = None,
        fmin: float | None = None,
        fmax: float | None = None,
        freq_step: float = 1e-3,
        phase_step: float = 1e-3,
        dtype: np.dtype = np.float64,
        enable_progress_bar: bool = True
    ):
        self.frequency_sampling = frequency_sampling
        self.frequency_array = frequency_array
        self.fmin = fmin
        self.fmax = fmax
        self.freq_step = freq_step
        self.phase_step = phase_step
        self.dtype = dtype
        self.enable_progress_bar = enable_progress_bar


    def run_tdspec(
        self, 
        signal: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]: 
        
        return tds(
            signal, 
            self.frequency_sampling, 
            frequency_array=self.frequency_array, 
            fmin=self.fmin, 
            fmax=self.fmax, 
            freq_step=self.freq_step, 
            phase_step=self.phase_step, 
            dtype=self.dtype, 
            enable_progress_bar=self.enable_progress_bar
        )
        
    
    def run_td2spec(
        self, 
        signal: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        
        return tdbs(
            signal, 
            self.frequency_sampling, 
            frequency_array=self.frequency_array, 
            fmin=self.fmin, 
            fmax=self.fmax, 
            freq_step=self.freq_step, 
            phase_step=self.phase_step, 
            dtype=self.dtype, 
            enable_progress_bar=self.enable_progress_bar
        )
        
    
    def run_td3spec(
        self, 
        signal: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        
        return tdts(
            signal, 
            self.frequency_sampling, 
            frequency_array=self.frequency_array, 
            fmin=self.fmin, 
            fmax=self.fmax, 
            freq_step=self.freq_step, 
            phase_step=self.phase_step, 
            dtype=self.dtype, 
            enable_progress_bar=self.enable_progress_bar
        )
        
    def run_td4spec(
        self, 
        signal: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 
        
        return tdt4s(
            signal, 
            self.frequency_sampling, 
            frequency_array=self.frequency_array, 
            fmin=self.fmin, 
            fmax=self.fmax, 
            freq_step=self.freq_step, 
            phase_step=self.phase_step, 
            dtype=self.dtype, 
            enable_progress_bar=self.enable_progress_bar
        )