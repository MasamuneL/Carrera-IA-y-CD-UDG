lab.cugdl.udg.mx# EasyInvestbot v0.1 - Automated Trading Bot

An intelligent trading bot that uses machine learning to predict stock price movements and execute automated trading strategies on AAPL and MSFT stocks.

## Features

- **Machine Learning Predictions**: Uses RandomForest classifier to predict stock price movements
- **Real Market Data**: Downloads and processes real-time stock data using Yahoo Finance
- **Aggressive Trading Strategy**: Implements buy/sell strategies with profit-taking mechanisms
- **Portfolio Management**: Manages a $5000 portfolio split equally between symbols
- **Visualization**: Real-time plotting of trading operations vs actual price movements
- **Risk Management**: Built-in profit-taking and loss prevention mechanisms

## Trading Strategy

- **Buy Signals**: When model predicts UP OR price dips OR every 10th interval
- **Sell Signals**: When 0.5% profit is reached OR negative prediction + 0.2% profit
- **Portfolio**: $5000 split equally between AAPL and MSFT

## Installation

1. Clone the repository:
```bash
git clone https://lab.cugdl.udg.mx
/yourusername/EasyInvestbot_v0.1.git
cd EasyInvestbot_v0.1
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the trading bot:
```bash
python botfinanzas_v0.1.py
```

The bot will:
1. Download historical data for model training
2. Download recent intraday data for trading simulation
3. Train the machine learning model
4. Execute trading simulation
5. Display results and trading chart

## Configuration

Edit the configuration section in `botfinanzas_v0.1.py`:

```python
# Stock symbols to trade
acciones = ["AAPL", "MSFT"]

# Trading thresholds
PORCENTAJE_COMPRA = 0.998   # Buy threshold
PORCENTAJE_VENTA = 1.002    # Sell threshold
```

## Requirements

- Python 3.8+
- yfinance
- pandas
- matplotlib
- scikit-learn
- numpy

## Disclaimer

This bot is for educational and research purposes only. Trading stocks involves risk, and past performance does not guarantee future results. Always do your own research and consider consulting with a financial advisor before making investment decisions.

## License

MIT License - see LICENSE file for details.

## Author

Alan Solano, Martin Carrizalez, Oswaldo Rojas, Vicente Coronado, Alvaro Navarro & AI Assistant
