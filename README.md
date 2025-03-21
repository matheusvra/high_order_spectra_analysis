# Time Domain High Order Spectral Analysis

This repository provides tools for performing **Time Domain High Order Spectral Analysis (TD-HOSA)**, a technique used to analyze non-linear and non-Gaussian signals by extending traditional spectral analysis beyond second-order statistics. This method is particularly useful in applications where standard Fourier-based techniques fall short, such as detecting system nonlinearities, identifying transient behaviors, and reducing Gaussian noise interference.

## What is Time Domain High Order Spectral Analysis?

Traditional spectral analysis, such as Fourier or wavelet transforms, primarily focuses on second-order statistics (power spectra), which assume that the underlying process is linear and Gaussian. However, many real-world signals exhibit nonlinearity and non-Gaussian properties. **High Order Spectral Analysis (HOSA)** extends the analysis to higher-order statistics (such as bispectrum and trispectrum), which help reveal phase relationships and suppress Gaussian noise components.

**Time Domain HOSA**, as opposed to frequency domain methods, directly analyzes signals in the time domain, allowing for a more detailed characterization of transient and nonlinear features.

### Applications of TD-HOSA

- **Industrial Process Monitoring:** Detecting anomalies and faults in mechanical and electrical systems.
- **Biomedical Signal Processing:** Analysis of EEG and ECG signals to detect abnormal brain and heart activities.
- **Structural Health Monitoring:** Identifying nonlinear vibrations in materials and infrastructures.
- **Seismic Signal Analysis:** Understanding nonlinear interactions in geophysical data.
- **Communication Systems:** Enhancing signal processing in non-Gaussian noise environments.

## Repository Context

This repository was designed to be used as a package for processing neural signals, meaning that the tools and analysis techniques implemented here aimed to identify complex signal patterns in neural electrophysiological data.&#x20;

## Setup Guide

### Prerequisites

To run this repository, ensure you have the following installed:

- Python 3.11+
- Pip 3.11+

### Python 101

For those new to Python, we recommend the following interactive tutorials:

[Learn Python - Interactive Tutorials](https://www.learnpython.org/)

### Library Versioning

All library dependencies are managed and versioned in the `pyproject.toml` file using **Poetry**.

## IDE

The recommended IDE for this project is **VS Code**.

## Installation and Setup

### Installing Python 3.11+

To install Python 3.11+ on Ubuntu, follow these steps:

```shell
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11
```

Verify the installation:

```shell
python3.11 --version
```

### Installing Pip

Install the latest version of pip for Python 3.11:

```shell
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
```

Verify installation:

```shell
python3.11 -m pip --version
```

Upgrade pip:

```shell
python3.11 -m pip install --upgrade pip
```

### Installing Poetry

Poetry is used for package and dependency management. Install it with:

```bash
curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3
```

### Creating a Virtual Environment

To create a virtual environment within the project directory:

```bash
poetry config virtualenvs.in-project true
```

Explicitly create the environment using Python 3.11:

```bash
poetry env use python3.11
```

### Activating the Virtual Environment

To activate (or create) the virtual environment:

```bash
poetry shell
```

### Installing Dependencies

Once inside the virtual environment, install dependencies with:

```bash
poetry install
```

If using **VS Code**, set the interpreter to the newly created virtual environment.

More details about Poetry can be found [HERE](https://python-poetry.org/docs).

# Authors

- **Matheus Anjos** - [matheusvra@hotmail.com](mailto\:matheusvra@hotmail.com) - [https://github.com/matheusvra](https://github.com/matheusvra)
