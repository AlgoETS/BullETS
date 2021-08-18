# BullETS

![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/AlgoETS/BullETS/Build/main?label=Checks%20%28main%29)

BullETS is a Python library designed to help with the development of algorithmic trading strategies.

## Upcoming features

- Retrieve stock data
- Trading portfolio management
- Backtesting framework

## Installation

This section will assume you have **Python** installed, if not, you can download & install it from [here](https://www.python.org/downloads/).

We strongly recommend using a [virtual environment](https://docs.python.org/3/library/venv.html) to keep BullETS and its dependencies from interfering with your system installs.

### Initializing and running a virtual environment 

Windows:
```shell
# Initializing a virtual environment in the ./venv directory
py -3 -m venv venv

# Activating the virtual environment
venv\Scripts\activate.bat
```

Mac OS & Linux:
```shell
# Initializing a virtual environment in the ./venv directory
python3 -m venv bot-env

# Activating the virtual environment (Mac OS & Linux)
source bot-env/bin/activate
```

### Using BullETS to develop a strategy

1. Register an account on the [FinancialModelingPrep website](https://financialmodelingprep.com/developer) and retrieve your API key

2. Create a new folder, initialize and activate a virtual environment inside (see above)

3. Install [BullETS](https://pypi.org/project/BullETS/) from PyPI
```shell
pip install BullETS
```

4. Code your own strategy

```python
from bullets.strategy import Strategy, Resolution
from bullets.runner import Runner
from bullets.data_source.data_source_fmp import FmpDataSource
from datetime import datetime

# Extend the default strategy from BullETS
class MyStrategy(Strategy):
   
   # You can access the `portfolio` and the `data_source` variables to retrieve information for your strategy
   # You are also free to add your own data sources here and use them

    # Redefine this function to perform a task when the strategy starts
    def on_start(self):
        pass

    # Redefine this function to perform a task on each resolution
    def on_resolution(self):
        self.portfolio.market_order("AAPL", 5)

    # Redefine this function to perform a task at the end of the strategy
    def on_finish(self):
        pass

        
# Initialize your new strategy
if __name__ == '__main__':
    resolution = Resolution.DAILY # Define your resolution (DAILY, HOURLY or MINUTE)
    start_time = datetime(2019, 3, 5) # Define your strategy start time
    end_time = datetime(2019, 4, 22) # Define your strategy end time
    data_source = FmpDataSource("Insert your key here", resolution) # Initialize the FMP data source with your API key and resolution
    strategy = MyStrategy(resolution=resolution,
                                start_time=start_time,
                                end_time=end_time,
                                starting_balance=5000,
                                data_source=data_source)
    
    runner = Runner(strategy) # Initialize the runner, which handles the execution of your strategy
    runner.start() # Start the runner and your strategy
```

This section only covers the basic features to develop a strategy. BullETS has other features, such as slippage, transaction fees, and many others. Stay updated for our upcoming detailed documentation that demonstrates how to use these features.

### Development mode

This section covers the installation process if you wish to **contribute** to the library.

1. Clone the repo and go to the library's root directory
``` shell
# Clone this repository
git clone https://github.com/AlgoETS/BullETS

# Move to the BullETS directory
cd BullETS
```
2. Initialize and run a virtual environment (see above)

3. Install BullETS in editable mode (while the virtual environment is activated)
```shell
pip install -e .
```

4. Setup environment variables 
   1. Make a copy of the `.env.sample` file and name it `.env`
   2. Replace the required values inside the `.env` file
