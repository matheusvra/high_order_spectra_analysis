
# Time Domain High Order Spectral Analysis


This document will present a tutorial on how to configure your environment for the 
first time, install dependencies, run the project main script, debugging and generation of the optimization results.

----

***Disclaimer***: This tutorial was made and tested on Ubuntu, if 
you are not using a Linux distribution, some steps may need to be different.


##  Important

This repository is meant to be used as package for steel shop optimization, meaning that the steps below are important to locally install and test, but ultimately, the configuration must be done in the mais 
project which will import and use the Science Base Steel Shop package, and some steps may be different.  

## Prerequisites

What things you need to have to be able to run:

* Python 3.11+
* Pip 3.11+

## Python 101

We do recommend
Learn Python awesome interactive tutorials

https://www.learnpython.org/

## Libs versioning

All used libs are versioned in the file 'pyproject.toml', on the root of the project folder, with the Poetry.

# IDE

The default IDE used in this projetc is vscode.

# Setup 

## Installing python 3.11+

This quick tutorial is going to show you how to install the latest
Python 3.11+ in Ubuntu.

* Open terminal via Ctrl+Alt+T or searching for “Terminal” from 
app launcher. 
When it opens, run commands:

### Install Python 3.11+ on Ubuntu 20.04|18.04 using Apt Repo

```shell
$ sudo apt install software-properties-common -y
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt install python3.11
```

Now you have at least one Python version installed, use ***python*** command for version 2.x (if still installed),
***python3*** for the main version used in the OS, and ***python3.11*** for version 3.11.x.

To verify if it worked type
```shell
python3.11 --version
```
your output should look like:

Python 3.11.7

## Installing pip

Pip is a package management system used to install and 
manage software packages written in Python. 
Many packages can be found in it.

It's recommended to install the latest version of pip3.10: 

Install the latest with:

```shell
$ curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
```

and test result:

```shell
$ python3.11 -m pip --version
```

and then test upgrade

```shell
$ python3.11 -m pip install --upgrade pip
```

## Installing Poetry

To install Poetry, the package used in this repository, just run the command after installation of Python3.11:

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
```

## Creating Virtual Environment

First, if you want, you can set the path of the virtual environment to be created to be in the project folder, running the command:

```bash
$ poetry config virtualenvs.in-project true
```

To create the environment, you can explicitly determine the python version used, if the version choosed matches the restriction in pyproject.toml. If you want Poetry to create automatically, skip the next command, but if you want to create the environment explicitly, for example, to use python3.11, run:

```bash
$ poetry env use python3.11
```

## Enabling Virtual Environment

To enable (or create, if not already created) the virtual environment, just run the command:

```bash
$ poetry shell
```

After creating the virtual environment, you need to install the dependencies. This can be done with the command:

```bash
$ poetry install
```

Now you're ready to run the project. If you are using the vscode, remember to set the interpreter to be the virtual environment created.

More information about the Poetry usage can be found [HERE](https://python-poetry.org/docs)

# Authors
 * **Matheus Anjos** - [matheusvra@hotmail.com](mailto:matheusvra@hotmail.com)