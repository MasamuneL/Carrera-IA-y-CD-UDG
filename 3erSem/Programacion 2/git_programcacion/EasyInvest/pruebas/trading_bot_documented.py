"""
Automated Trading Bot with Machine Learning Predictions

This bot uses RandomForest classifier to predict stock price movements and executes
aggressive buy/sell strategies on AAPL and MSFT stocks using real market data.

Features:
- Downloads 1-year historical data for model training
- Uses 5-day intraday data (30-minute intervals) for trading simulation
- Implements aggressive buying strategy with profit-taking
- Visualizes trading operations vs actual price movements

Trading Strategy:
- Buy: When model predicts UP OR price dips OR every 10th interval
- Sell: When 0.5% profit is reached OR negative prediction + 0.2% profit
- Portfolio: $5000 split equally between symbols

Author: AI Assistant
Date: September 2025
"""

import yfinance as yf          # Stock data download
import pandas as pd            # Data manipulation
import matplotlib.pyplot as plt # Plotting
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from sklearn.ensemble import RandomForestClassifier  # ML model
import numpy as np

# =============================================================================
# CONFIGURATION SECTION
# =============================================================================

# Stock symbols to trade
acciones = ["AAPL", "MSFT"]

# Portfolio initialization - $5000 split equally between stocks
portafolio = {
    "efectivo": {symbol: 5000.0 / len(acciones) for symbol in acciones},  # Cash per symbol
    "acciones": {symbol: 0 for symbol in acciones},                       # Shares owned
    "precios_compra": {symbol: None for symbol in acciones}               # Purchase prices (unused)
}

# Trading thresholds - adjusted for more frequent trading
PORCENTAJE_COMPRA = 0.998   # Buy when 0.2% below reference price
PORCENTAJE_VENTA = 1.002    # Sell when 0.2% above reference price

# Tracking variables for performance analysis
total_acciones_compradas = {symbol: 0.0 for symbol in acciones}  # Total shares bought
acciones_vendidas = {symbol: 0.0 for symbol in acciones}         # Total shares sold

# =============================================================================
# DATA DOWNLOAD AND PREPROCESSING
# =============================================================================

# Download historical data for model training (1 year, daily intervals)
print("Downloading historical data for model training...")
datos_historico = {symbol: yf.download(symbol, period="1y", interval="1d") for symbol in acciones}

# Download recent intraday data for trading simulation (5 days, 30-minute intervals)
print("Downloading intraday data for trading simulation...")
datos_ultimo_dia = {symbol: yf.download(symbol, period="5d", interval="30m") for symbol in acciones}

# Normalize dataframes - fix MultiIndex columns and timezone issues
for dct in (datos_historico, datos_ultimo_dia):
    for sym, df in dct.items():
        # Fix MultiIndex columns (yfinance returns MultiIndex with Price/Ticker levels)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)  # Use level 0 (Price names)
        
        # Remove timezone information from datetime index for consistency
        if isinstance(df.index, pd.DatetimeIndex):
            try:
                df.index = df.index.tz_convert(None)
            except Exception:
                df.index = df.index.tz_localize(None)
        dct[sym] = df

# Initialize portfolio tracking history
historial_portafolio = []

# =============================================================================
# MAIN TRADING LOOP - Process each stock symbol
# =============================================================================

for symbol in acciones:
    print(f"\n--- Processing {symbol} ---")
    
    # =============================================================================
    # STEP 1: Validate and prepare historical data for ML model training
    # =============================================================================
    
    # Get historical data for this symbol
    df_historico = datos_historico.get(symbol, pd.DataFrame()).copy()
    if df_historico.empty:
        print(f"[WARN] No historical data for {symbol}, skipping.")
        continue
    
    if 'Close' not in df_historico.columns:
        print(f"[WARN] No 'Close' column for {symbol}, skipping.")
        continue

    # =============================================================================
    # STEP 2: Feature Engineering for Machine Learning Model
    # =============================================================================
    
    # Generate features for prediction model
    df_feat = df_historico.copy()
    df_feat['return'] = df_feat['Close'].pct_change()           # Daily return percentage
    df_feat['ma_3'] = df_feat['Close'].rolling(3).mean()       # 3-day moving average
    df_feat['vol_3'] = df_feat['Close'].rolling(3).std()       # 3-day volatility (std dev)
    df_feat['target'] = (df_feat['Close'].shift(-1) > df_feat['Close']).astype(int)  # 1=price will rise, 0=fall
    df_feat = df_feat.dropna()  # Remove rows with NaN values

    # Check if we have enough data for training
    if len(df_feat) < 10:
        print(f"[WARN] Insufficient data to train model for {symbol}")
        continue

    # =============================================================================
    # STEP 3: Train RandomForest Model for Price Direction Prediction
    # =============================================================================
    
    # Prepare training data
    X_train = df_feat[['return','ma_3','vol_3']]  # Features: return, moving avg, volatility
    y_train = df_feat['target']                   # Target: 1=up, 0=down

    # Train RandomForest classifier
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)
    print(f"Model trained for {symbol} with {len(X_train)} samples")

    # =============================================================================
    # STEP 4: Prepare Intraday Data for Trading Simulation
    # =============================================================================
    
    # Get intraday data for this symbol
    df_ultimo = datos_ultimo_dia.get(symbol, pd.DataFrame()).copy()
    if df_ultimo.empty:
        print(f"[WARN] No intraday data for {symbol}")
        continue

    if 'Close' not in df_ultimo.columns:
        print(f"[WARN] No 'Close' column in intraday data for {symbol}")
        continue

    # Convert close prices to numeric and clean data
    close_series = pd.to_numeric(df_ultimo['Close'].squeeze(), errors='coerce').dropna()
    if close_series.empty:
        print(f"[WARN] No valid close prices for {symbol}")
        continue
    
    fechas = close_series.index  # Timestamps for each price point

    # =============================================================================
    # STEP 5: Execute Trading Strategy on Intraday Data
    # =============================================================================
    
    print(f"Starting trading simulation for {symbol} with {len(close_series)} price points")
    
    # Iterate through each 30-minute interval
    for i, precio_actual in enumerate(close_series.values):
        
        # Calculate reference price (moving average of last 3 periods)
        if i >= 3:
            precio_referencia = float(close_series.iloc[i-3:i].mean())
            ma_3 = close_series.values[i-3:i].mean()
            vol_3 = close_series.values[i-3:i].std()
            ret = (precio_actual - close_series.values[i-1])/close_series.values[i-1]
        else:
            # For first few periods, use current price as reference
            precio_referencia = float(precio_actual)
            ma_3 = close_series.values[:i+1].mean()
            vol_3 = close_series.values[:i+1].std() if i > 0 else 0.01
            ret = 0

        # Skip if we have invalid data
        if np.isnan([ret, ma_3, vol_3]).any():
            continue

        # =============================================================================
        # STEP 6: Make ML Prediction for Current Price Point
        # =============================================================================
        
        # Prepare features for prediction
        X_pred = pd.DataFrame({'return':[ret],'ma_3':[ma_3],'vol_3':[vol_3]})
        pred = clf.predict(X_pred)[0]  # 1=price will go up, 0=price will go down

        # =============================================================================
        # STEP 7: Execute Buy/Sell Decisions Based on Strategy
        # =============================================================================
        
        # AGGRESSIVE BUYING STRATEGY:
        # Buy when: model predicts UP OR price is within 0.1% of reference OR every 10th interval
        if (portafolio['efectivo'][symbol] > 10 and 
            (pred == 1 or precio_actual <= precio_referencia * 1.001 or i % 10 == 0)):
            
            # Calculate how many shares we can buy with available cash
            cantidad = portafolio['efectivo'][symbol] / float(precio_actual)
            if cantidad > 0:
                # Execute buy order
                portafolio['acciones'][symbol] += cantidad
                portafolio['efectivo'][symbol] = 0.0
                total_acciones_compradas[symbol] += cantidad
                print(f"{symbol}: BUY {cantidad:.2f} shares at ${float(precio_actual):.2f}")

        # PROFIT-TAKING SELLING STRATEGY:
        # Sell when: 0.5% profit is reached OR negative prediction + 0.2% profit
        elif (portafolio['acciones'][symbol] > 0 and 
              (precio_actual >= precio_referencia * 1.005 or  # 0.5% profit
               (pred == 0 and precio_actual >= precio_referencia * 1.002))):  # Negative prediction + 0.2% profit
            
            # Execute sell order
            cantidad_inicial = portafolio['acciones'][symbol]
            ganancia = cantidad_inicial * float(precio_actual)
            acciones_vendidas[symbol] += cantidad_inicial
            portafolio['efectivo'][symbol] = float(ganancia)
            portafolio['acciones'][symbol] = 0.0
            print(f"{symbol}: SELL {cantidad_inicial:.2f} shares at ${float(precio_actual):.2f}")

        # =============================================================================
        # STEP 8: Record Portfolio State for Analysis
        # =============================================================================
        
        # Track portfolio value at each time point
        historial_portafolio.append({
            "fecha": fechas[i],
            "symbol": symbol,
            "acciones": float(portafolio['acciones'][symbol]),
            "efectivo": float(portafolio['efectivo'][symbol]),
            "valor_total": float(portafolio['acciones'][symbol])*float(precio_actual) + float(portafolio['efectivo'][symbol])
        })

# =============================================================================
# PERFORMANCE ANALYSIS AND RESULTS
# =============================================================================

print("\n" + "="*60)
print("FINAL TRADING SESSION RESULTS")
print("="*60)

total_inicial = 5000.0  # Starting portfolio value
total_final = 0.0       # Final portfolio value

# Calculate final portfolio value for each symbol
for sym in acciones:
    df_ultimo = datos_ultimo_dia.get(sym, pd.DataFrame()).copy()
    
    # Handle missing data gracefully
    if df_ultimo.empty or 'Close' not in df_ultimo.columns:
        efectivo_final = float(portafolio['efectivo'][sym])
        total_final += efectivo_final
        print(f"{sym}: Cash=${efectivo_final:.2f}, Shares=0.00, Stock Value=$0.00, Total=${efectivo_final:.2f}")
        continue

    # Get final stock price
    close_numeric = pd.to_numeric(df_ultimo['Close'].squeeze(), errors='coerce').dropna()
    if close_numeric.empty:
        efectivo_final = float(portafolio['efectivo'][sym])
        total_final += efectivo_final
        print(f"{sym}: Cash=${efectivo_final:.2f}, Shares=0.00, Stock Value=$0.00, Total=${efectivo_final:.2f}")
        continue

    # Calculate final values
    ultimo_precio = float(close_numeric.iloc[-1])           # Last stock price
    valor_acciones = float(portafolio['acciones'][sym]) * ultimo_precio  # Value of shares held
    efectivo_final = float(portafolio['efectivo'][sym])     # Cash remaining
    total_final += valor_acciones + efectivo_final

    print(f"{sym}: Cash=${efectivo_final:.2f}, Shares={float(portafolio['acciones'][sym]):.2f}, "
          f"Stock Value=${valor_acciones:.2f}, Total=${valor_acciones + efectivo_final:.2f}")

# Calculate and display performance metrics
ganancia = total_final - total_inicial
porcentaje_ganancia = (ganancia / total_inicial) * 100

print(f"\nPERFORMANCE SUMMARY:")
print(f"Initial Portfolio Value: ${total_inicial:.2f}")
print(f"Final Portfolio Value:   ${total_final:.2f}")
print(f"Net Profit/Loss:         ${ganancia:.2f} ({porcentaje_ganancia:+.2f}%)")

# Display trading activity summary
print(f"\nTRADING ACTIVITY SUMMARY:")
for sym in acciones:
    net_shares = total_acciones_compradas[sym] - acciones_vendidas[sym]
    print(f"{sym}: Bought {total_acciones_compradas[sym]:.2f} shares, "
          f"Sold {acciones_vendidas[sym]:.2f} shares, Net Position: {net_shares:.2f} shares")

# =============================================================================
# VISUALIZATION - Plot Trading Operations vs Price Movements
# =============================================================================

print(f"\nGenerating trading visualization...")

plt.figure(figsize=(15, 8))
hist_df_all = pd.DataFrame(historial_portafolio)

for symbol in acciones:
    # Get price data for plotting
    df = datos_ultimo_dia.get(symbol, pd.DataFrame()).copy()
    if df.empty or 'Close' not in df.columns:
        continue

    # Fix datetime index issues and filter to recent data
    df = df.reset_index()
    df.columns = ['Datetime'] + list(df.columns[1:])
    df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
    df = df.dropna(subset=['Datetime', 'Close'])
    df = df.set_index('Datetime')
    
    # Take only last 240 points (5 days * 48 30-minute intervals)
    df = df.sort_index().tail(240)
    
    if df.empty:
        continue

    # Get time range from actual data
    start_time = df.index.min()
    end_time = df.index.max()
    
    # Filter portfolio history for this symbol and time range
    hist_df = hist_df_all[hist_df_all['symbol'] == symbol].copy()
    hist_df['fecha'] = pd.to_datetime(hist_df['fecha'])
    hist_df = hist_df[(hist_df['fecha'] >= start_time) & (hist_df['fecha'] <= end_time)]
    hist_df = hist_df.sort_values('fecha')
    
    # Identify buy and sell operations
    hist_df['acciones_diff'] = hist_df['acciones'].diff().fillna(0)
    hist_df['efectivo_diff'] = hist_df['efectivo'].diff().fillna(0)

    # Separate buy and sell operations
    compras_df = hist_df[(hist_df['acciones_diff'] > 0) & (hist_df['efectivo_diff'] < 0)]  # Bought shares
    ventas_df = hist_df[(hist_df['acciones_diff'] < 0) & (hist_df['efectivo_diff'] > 0)]   # Sold shares

    # Plot price line
    plt.plot(df.index, df['Close'], label=f'{symbol} Price', alpha=0.8, linewidth=2)

    # Plot buy signals (green triangles pointing up)
    buy_label_added = False
    for _, row in compras_df.iterrows():
        buy_time = row['fecha']
        closest_idx = df.index.get_indexer([buy_time], method='nearest')[0]
        if closest_idx >= 0:
            price = df['Close'].iloc[closest_idx]
            label = f'{symbol} Buy' if not buy_label_added else ""
            plt.scatter(buy_time, price, marker='^', color='green', s=100, zorder=5, label=label)
            buy_label_added = True
    
    # Plot sell signals (red triangles pointing down)
    sell_label_added = False
    for _, row in ventas_df.iterrows():
        sell_time = row['fecha']
        closest_idx = df.index.get_indexer([sell_time], method='nearest')[0]
        if closest_idx >= 0:
            price = df['Close'].iloc[closest_idx]
            label = f'{symbol} Sell' if not sell_label_added else ""
            plt.scatter(sell_time, price, marker='v', color='red', s=100, zorder=5, label=label)
            sell_label_added = True

# Format the plot
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H:%M"))
plt.gcf().autofmt_xdate()
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
plt.title("Trading Bot Operations vs Actual Stock Prices (Last 5 Days)", fontsize=16, fontweight='bold')
plt.xlabel("Date and Time", fontsize=12)
plt.ylabel("Stock Price ($)", fontsize=12)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()

print("Displaying trading chart...")
plt.show()

print(f"\nTrading simulation completed successfully!")
