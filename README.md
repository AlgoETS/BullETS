# BullETS

BullETS is a Python library designed to help with the development of algorithmic trading strategies.

## Upcoming features

- Retrieve stock data
- Investment portfolio management
- Backtesting framework

## Installation

This section will assume you have **Python** installed, if not, you can download & install it from [here](https://www.python.org/downloads/).

### Development mode

This section covers the installation process if you wish to **contribute** to the library. We recommend using a [virtual environment](https://docs.python.org/3/library/venv.html) to keep BullETS and its dependencies from interfering with your system installs.

1. Clone the repo and go the library's root directory
``` shell
# Clone this repository
git clone https://github.com/AlgoETS/BullETS

# Move to the BullETS directory
cd BullETS
```
2. Initialize and run the virtual environment (Windows)
```shell
# Initializing a virtual environment in the ./venv directory
py -3 -m venv venv

# Activating the virtual environment
venv\Scripts\activate.bat
```

2. Initialize and run the virtual environment (Mac OS & Linux)
```shell
# Initializing a virtual environment in the ./venv directory
python3 -m venv bot-env

# Activating the virtual environment (Mac OS & Linux)
source bot-env/bin/activate
```

3. Install BullETS in editable mode (while the virtual environment is activated)
```shell
# Run this command from the project's root directory
pip install -e .
```

