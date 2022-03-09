# pycdo
This library abstracts many of the Cisco Defense Orchestrator APIs in an attempt to make them easy to consume in Python.

# Requirements
See requirements.txt for more information
- Python Version 3.8 or newer is strongly recommended. 
- This library was developed uner Python 3.9 

# Installation
The intent is to make this library availaible in pypi. While it is under development, one can install via git hub. 

## Create virtual environment
```
python3 -m venv cdo
source cdo/bin/activate
pip3 install --upgrade pip setuptools
```
## Clone pycdo repo
```
cd cdo
git clone https://github.com/aaronhackney/pycdo.git
```

## Install library dependencies
```
cd pycdo
pip install -r requirements.txt
```

## (OPTIONAL) Install for dev use
```
pip install wheel
python setup.py bdist_wheel
```
## Install the CDO Module from the source tree
```
pip install -e .
```

## Test that the library is working in this virtual env
```
$ python
Python 3.10.1 (v3.10.1:2cd268a3a9, Dec  6 2021, 14:28:59) [Clang 13.0.0 (clang-1300.0.29.3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pycdo
>>> dir(pycdo)
['CDOBaseClient', 'CDOChangeLogs', 'CDOClient', 'CDOConnectors', 'CDODevices', 'CDOMSSPClient', 'CDOObjects', 'CDOOnboard', 'CDOStateMachines', 'CDOTenants', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', '__version__', 'base', 'changelogs', 'connectors', 'devices', 'encrypt', 'errors', 'helpers', 'log', 'logging', 'model', 'mssp', 'objects', 'onboard', 'state_machine', 'tenants']
>>>
```
# How to use
The easist way to see how to use the API library is to look at the pytest tests in the tests directory. But the client requires a CDO token and CDO region
```
>>> from pycdo import CDOClient
>>> cdo_client = CDOClient("1234567890", "us")
>>>
```
# License
MIT License - See LICENSE.TXT for full text  