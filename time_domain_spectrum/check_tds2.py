import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from tds import tds
from scipy.signal import hilbert


if __name__ == "__main__":

    insert_noise = False

    frequency_sample = 1e4
    time_step = 1/frequency_sample
    time = np.arange(0, 0.1, time_step)

    freq = 53.71
    carrier_freq = 1e3

    clean_signal = (1 - np.cos(2*np.pi*freq*time))*np.cos(2*np.pi*carrier_freq*time)

    noise = np.random.normal(loc=0, scale=2.5*np.std(clean_signal), size=(len(time,)))

    signal = clean_signal + noise*insert_noise

    analytic_signal = hilbert(signal)
    signal_envelope = np.abs(analytic_signal)

    frequency_array_modulating, amplitude_modulating, phase_modulating = tds(
        signal=signal_envelope,
        frequency_sampling=frequency_sample,
        time=None,
        fmin=45,
        fmax=65,
        freq_step=0.01,
        phase_step=0.01
    )

    frequency_array, amplitude, phase = tds(
        signal=signal,
        frequency_sampling=frequency_sample,
        time=None,
        fmin=900,
        fmax=1100,
        freq_step=0.1,
        phase_step=0.01
    )

    fig = make_subplots(rows=3, cols=2)

    fig.append_trace(go.Scatter(
        x=time,
        y=signal,
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=frequency_array,
        y=amplitude,
    ), row=2, col=1)

    fig.append_trace(go.Scatter(
        x=frequency_array,
        y=phase,
    ), row=3, col=1)

    fig.append_trace(go.Scatter(
        x=time,
        y=signal_envelope,
    ), row=1, col=2)

    fig.append_trace(go.Scatter(
        x=frequency_array_modulating,
        y=amplitude_modulating,
    ), row=2, col=2)

    fig.append_trace(go.Scatter(
        x=frequency_array_modulating,
        y=phase_modulating,
    ), row=3, col=2)

    fig.show()