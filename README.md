# pycdo
This library abstracts many of the Cisco Defense Orchestrator APIs in an attempt to make them easy to consume in Python.

# Requirements
See requirements.txt for more information
- Python Version 3.8 or newer is recommended. 
- This library was developed uner Python 3.9 

# Installation
The intent is to eventually make this library availaible in pypi. While it is under development, one can install via git hub. 

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

## Install library dependencies and the pycdo module
```
cd pycdo
pip install -r requirements.txt
python3 setup.py install
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
The easist way to see how to use the API library is to look at the pytest tests in the tests directory. But the client requires a CDO token and CDO region [defenseorchestrator.com, "apj.cdo.cisco.com" "defenseorchestrator.eu"]
```
>>> from pycdo import CDOClient
>>> cdo_client = CDOClient("1234567890", "defenseorchestrator.com")
>>>
```

# Test Cases
The test cases require a number of environment variables to be avaialbe. Here is a sample:
```
CDO_REGION = "defenseorchestrator.com"
CDO_TOKEN = "yourcdotokengoeshere"
SEARCH_TENANT = "youtenantname"
ASA_USER = "yourasausername"
ASA_PASS = "yourpassword"
ASA_IP = "10.10.10.10"
ASA_NAME = "pytest-asav-1"
ASA_PORT = "8443"
CONNECTOR_NAME = "yourconnectorname"
TEST_ASA_NAME = "yourasanameincdo"
```
# License
MIT License - See LICENSE.TXT for full text  