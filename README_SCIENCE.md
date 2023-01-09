
# Science Base Steel Shop


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

* Python 3.10+
* Pip 3.10+
* VirtualEnvWrapper is recommended but not mandatory
* PyCharm IDE is ***highly recommended*** and will be approached in 
the next section

## Python 101

We do recommend
Learn Python awesome interactive tutorials

https://www.learnpython.org/

## Libs versioning

All used libs are versioned in the file 'pyproject.toml', on the root of the project folder, with the Poetry.

By using this setup, libs may be installed using the command (after repo configuration):

```shell
$ poetry install
```

Make sure that you are in the correct virtual environment when using
this command.

# IDE


The default IDE is pycharm community edition. Available at:
https://www.jetbrains.com/pycharm/

We do recommend installing it through the
[jetbrains toolbox](https://www.jetbrains.com/toolbox/) to keep it
up to date.

The professional edition is available for free if you are a student and
would like to have the extra features. Professionals must pay for the premium recourses available in the professional version.


## Tips

The IDE is quite powerful and provides a vast set of features to speed 
up and facilitate python development. Take your time to get to know this
amazing tool that is at your disposal.

Memorizing shortcuts is also very helpful, I recommend using a [cheat 
sheet](https://blog.jetbrains.com/pycharm/files/2010/07/PyCharm_Reference_Card.pdf) while you are a beginner in the tool.

Finally, the full action search (ctrl + shift + a) allows you to search 
for any IDE feature and is quite powerful, do not be afraid to 
experiment with it.

# Setup 

## Installing python 3.10+

This quick tutorial is going to show you how to install the latest
Python 3.10+ in Ubuntu.

* Open terminal via Ctrl+Alt+T or searching for “Terminal” from 
app launcher. 
When it opens, run commands:

### Install Python 3.10 on Ubuntu 20.04|18.04 using Apt Repo

```shell
$ sudo apt install software-properties-common -y
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt install python3.10
```
### Install Python 3.10 on Ubuntu 20.04|18.04 from Source
#### Installing dependencies
Depending on the method used to install Python, is recommended to install the dependencies first: 

```shell
$ sudo apt update
$ sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev
```

#### Installing Python 3.10
* Downloading the Python3.10 files installation compressed (Python 3.10.7 as example):
```shell
$ wget https://www.python.org/ftp/python/3.10.7/Python-3.10.7.tgz
```

* Extracting the files and opening the work directory:
```shell
$ tar -xf Python-3.10.*.tgz
$ cd Python-3.10.*/ 
```

* Configuring installation:
```shell
$ ./configure --enable-optimizations
```

* Building:
```shell
$ make -j $(nproc)
```

* Installing:
```shell
$ sudo make altinstall
```
Now you have at least one Python version installed, use ***python*** command for version 2.x (if still installed),
***python3*** for the main version used in the OS, and ***python3.10*** for version 3.10.x.

To verify if it worked type
```shell
python3.10 --version
```
your output should look like:

Python 3.10.7

## Installing pip

Pip is a package management system used to install and 
manage software packages written in Python. 
Many packages can be found in it.

It's recommended to install the latest version of pip3.10: 

Install the latest with:

```shell
$ curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```

and test result:

```shell
$ python3.10 -m pip --version
```

and then test upgrade

```shell
$ python3.10 -m pip install --upgrade pip
```

## Installing Poetry

To install Poetry, the package used in this repository, just run the command after installation of Python3.10 e pip:

```bash
$ python3.10 -m pip install poetry
```

## Installing virtualenv and virtualenvwrapper

(This section is optional, but highly recommended. [The folks over at RealPython may be able to convince you if 
you still have doubts.](https://realpython.com/blog/python/python-virtual-environments-a-primer/))

Using pip , we can install any package in the Python Package Index
quite easily including virtualenv and virtualenvwrapper. 


It’s standard practice in the 
Python community to be leveraging virtual environments of some sort, 
so I suggest you do the same:

```shell
$ sudo pip install virtualenv virtualenvwrapper
$ sudo rm -rf ~/.cache/pip get-pip.py
```


Once you have virtualenv and virtualenvwrapper installed,
update our ~/.bashrc (or ~/.zshrc) file to include the following 
lines at the bottom of the file:


```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh
```

After editing ~/.bashrc (or ~/.zshrc), reload the changes:

**bash**
```shell
$ source ~/.bashrc
```

**zsh**
```shell
$ source ~/.zshrc
```
 
The next step is to actually create the Python virtual
environment. For the command, ensure you set the --python 
flag to python 3.8 as this is our current default python version.

The name "science_base_steel_shop" is used as example, feel free to use a descriptive name, that helps to identify which project is using the environment. 

```
$ mkvirtualenv science_base_steel_shop --python=python3.10.7
```

If you ever reboot your system; log out and log back in; 
or open up a new terminal, you’ll need to use the workon  
command to re-access your ***science_base_steel_shop*** virtual environment. 
Example:

```
$ workon science_base_steel_shop
```

# Authors
 * **Matheus Anjos** - [matheus.anjos@enacom.com.br](mailto:matheus.anjos@enacom.com.br)