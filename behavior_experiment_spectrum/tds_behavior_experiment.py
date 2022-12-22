import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from high_order_spectra_analysis.time_domain_spectrum.tds import tds


def load_data():
    BASE_PATH = "behavior_experiment_spectrum"
    data = pd.read_csv(f"{BASE_PATH}/data_matrix.csv", delimiter=',', encoding="utf8")
    events_index = pd.read_csv(f"{BASE_PATH}/events_index.csv", delimiter=',', encoding="utf8")
    events_index_data_array = np.full((len(data),), None)

    for start, end, event_idx in zip(events_index.start, events_index.end, np.arange(1, len(events_index))):
        events_index_data_array[start:end] = event_idx
        
    data = data.assign(events_index=events_index_data_array)
    events_index_timestamp = pd.read_csv(f"{BASE_PATH}/events_index_timestamp.csv", delimiter=',', encoding="utf8")
    events_behavior_TS_LFP_index = pd.read_csv(f"{BASE_PATH}/events_behavior_TS_LFPindex.csv", delimiter=',', encoding="utf8")

    # Inserting the events behavior data in the dataframe as a column

    events_behavior_TS_LFP_index_array = np.full((len(data),), None)

    for start, end, event_idx in zip(events_behavior_TS_LFP_index.start, events_behavior_TS_LFP_index.end, np.arange(1, len(events_behavior_TS_LFP_index))):
        events_behavior_TS_LFP_index_array[start:end] = event_idx
        
    data = data.assign(events_behavior_TS_LFP_index=events_behavior_TS_LFP_index_array)

    events_behavior_TS_LFPsec = pd.read_csv(f"{BASE_PATH}/events_behavior_TS_LFPsec.csv", delimiter=',', encoding="utf8")

    return data, events_index, events_index_timestamp, events_behavior_TS_LFP_index, events_behavior_TS_LFPsec

def select_event_window(
    df: pd.DataFrame, 
    event_number: int, 
    samples_before: int = 0, 
    samples_after: int = 0
) -> pd.DataFrame:
  """
  Method to extract the slice of the dataframe which contais the event, with some data before and after, 
  given number of samples to add to the begin and end, respectively.
  """
  
  window_index = np.argwhere(data.events_index.to_numpy() == event_number).flatten()
  begin_index = window_index[0] - samples_before
  end_index = window_index[-1] + samples_after
  return df[begin_index:end_index]


def decimate(data, desired_frequency_sampling):
    backup_data = data.copy()
    time = backup_data.Time.to_numpy()
    TimeSampling = round(np.mean(time[1:] - time[:-1]), 6)
    FrequencySampling = 1.0/TimeSampling
    print(f"The time sampling is {TimeSampling} seconds and the frequency is "
        f"{FrequencySampling/float(1000**(FrequencySampling<=1000))} {'k'*bool(FrequencySampling>=1000)}Hz")

    newTimeSampling = 1.0/desired_frequency_sampling
    decimation_rate = np.ceil(newTimeSampling/TimeSampling).astype(int)
    print(f"The data will be decimated by the rate 1:{decimation_rate}")

    data = data[::decimation_rate]

    TimeSampling = newTimeSampling
    
    FrequencySampling = 1.0/TimeSampling
    print(f"The new time sampling is {np.round(TimeSampling, 5)} s and the new frequency is "
    f"{FrequencySampling/float(1000**(FrequencySampling>=1000))} {'k'*bool(FrequencySampling>=1000)}Hz")
    
    return data, TimeSampling, FrequencySampling, backup_data

if __name__ == "__main__":

    data, events_index, events_index_timestamp, events_behavior_TS_LFP_index, events_behavior_TS_LFPsec = load_data()

    samples_before = 0
    samples_after = 0
    event_number = 1

    event_data = select_event_window(
        df=data,
        event_number=event_number,
        samples_before=samples_before,
        samples_after=samples_after
    )

    data, TimeSampling, FrequencySampling, backup_data = decimate(event_data, desired_frequency_sampling=200)

    time = event_data.Time.to_numpy()
    signal = event_data.Inferior_colliculus_2.to_numpy()

    
    frequency_array, amplitude, phase = tds(
        signal=signal,
        frequency_sampling=200,
        time=time,
        fmin=52,
        fmax=55,
        freq_step=0.01,
        phase_step=0.01
    )


    fig = make_subplots(rows=3, cols=1)

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

    fig.show()