import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from tds import tds


if __name__ == "__main__":

    insert_noise = False

    time_step = 0.001
    fs = 1/time_step
    time = np.arange(0, 5, time_step)

    freqs = np.array([12, 53, 150, 314, 498])
    phases = np.pi*np.array([0.5, 0.25, 1, 0, 3/4])
    gains = np.array([0.8, 0.7, 0.9, 1, 0.4])

    clean_signal = np.zeros(len(time))

    for freq, phase, gain in zip(freqs, phases, gains):
        clean_signal += gain*np.cos(2*np.pi*freq*time + phase)

    noise = np.random.normal(loc=0, scale=2.5*np.std(clean_signal), size=(len(time,)))

    signal = clean_signal + noise*insert_noise

    frequency_array, amplitude, phase = tds(
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
        x=frequency_array,
        y=amplitude,
    ), row=1, col=1)

    fig.append_trace(go.Scatter(
        x=frequency_array,
        y=phase,
    ), row=2, col=1)

    fig.show()