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
    
    # Validar histórico
    df_historico = datos_historico.get(symbol, pd.DataFrame()).copy()
    if df_historico.empty:
        print(f"[WARN] Histórico vacío para {symbol}, se omite.")
        continue
    
    if 'Close' not in df_historico.columns:
        print(f"[WARN] Histórico sin 'Close' para {symbol}, se omite.")
        continue

    # Generar features para predicción
    df_feat = df_historico.copy()
    df_feat['return'] = df_feat['Close'].pct_change()
    df_feat['ma_3'] = df_feat['Close'].rolling(3).mean()
    df_feat['vol_3'] = df_feat['Close'].rolling(3).std()
    df_feat['target'] = (df_feat['Close'].shift(-1) > df_feat['Close']).astype(int)
    df_feat = df_feat.dropna()

    if len(df_feat) < 10:
        print(f"[WARN] Insuficientes datos para entrenar {symbol}")
        continue

    X_train = df_feat[['return','ma_3','vol_3']]
    y_train = df_feat['target']

    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X_train, y_train)

    # Datos intradía
    df_ultimo = datos_ultimo_dia.get(symbol, pd.DataFrame()).copy()
    if df_ultimo.empty:
        print(f"[WARN] Datos intradía vacíos para {symbol}")
        continue

    if 'Close' not in df_ultimo.columns:
        print(f"[WARN] Datos intradía sin 'Close' para {symbol}")
        continue

    close_series = pd.to_numeric(df_ultimo['Close'].squeeze(), errors='coerce').dropna()
    if close_series.empty:
        continue
    
    fechas = close_series.index

    for i, precio_actual in enumerate(close_series.values):
        # Fixed: Use simple moving average as reference
        if i >= 3:
            precio_referencia = float(close_series.iloc[i-3:i].mean())
            ma_3 = close_series.values[i-3:i].mean()
            vol_3 = close_series.values[i-3:i].std()
            ret = (precio_actual - close_series.values[i-1])/close_series.values[i-1]
        else:
            precio_referencia = float(precio_actual)
            ma_3 = close_series.values[:i+1].mean()
            vol_3 = close_series.values[:i+1].std() if i > 0 else 0.01
            ret = 0

        # Fixed: Check for NaN values
        if np.isnan([ret, ma_3, vol_3]).any():
            continue

        X_pred = pd.DataFrame({'return':[ret],'ma_3':[ma_3],'vol_3':[vol_3]})
        pred = clf.predict(X_pred)[0]

        # Very aggressive: Buy on any slight dip or positive prediction
        if (portafolio['efectivo'][symbol] > 10 and 
            (pred == 1 or precio_actual <= precio_referencia * 1.001 or i % 10 == 0)):  # Buy every 10th interval too
            
            cantidad = portafolio['efectivo'][symbol] / float(precio_actual)
            if cantidad > 0:
                portafolio['acciones'][symbol] += cantidad
                portafolio['efectivo'][symbol] = 0.0
                total_acciones_compradas[symbol] += cantidad
                print(f"{symbol}: Comprando {cantidad:.2f} acciones a {float(precio_actual):.2f}")

        # Sell on profit margin OR strong negative signal
        elif (portafolio['acciones'][symbol] > 0 and 
              (precio_actual >= precio_referencia * 1.005 or  # Sell on 0.5% profit
               (pred == 0 and precio_actual >= precio_referencia * 1.002))):  # OR negative prediction + small profit
            
            cantidad_inicial = portafolio['acciones'][symbol]
            ganancia = cantidad_inicial * float(precio_actual)
            acciones_vendidas[symbol] += cantidad_inicial
            portafolio['efectivo'][symbol] = float(ganancia)
            portafolio['acciones'][symbol] = 0.0
            print(f"{symbol}: Vendiendo {cantidad_inicial:.2f} acciones a {float(precio_actual):.2f}")

        historial_portafolio.append({
            "fecha": fechas[i],
            "symbol": symbol,
            "acciones": float(portafolio['acciones'][symbol]),
            "efectivo": float(portafolio['efectivo'][symbol]),
            "valor_total": float(portafolio['acciones'][symbol])*float(precio_actual) + float(portafolio['efectivo'][symbol])
        })

# Resultados finales (same as original)
print("\nResultados finales de la sesión:")
total_inicial = 5000.0
total_final = 0.0

for sym in acciones:
    df_ultimo = datos_ultimo_dia.get(sym, pd.DataFrame()).copy()
    if df_ultimo.empty or 'Close' not in df_ultimo.columns:
        total_final += float(portafolio['efectivo'][sym])
        continue

    close_numeric = pd.to_numeric(df_ultimo['Close'].squeeze(), errors='coerce').dropna()
    if close_numeric.empty:
        total_final += float(portafolio['efectivo'][sym])
        continue

    ultimo_precio = float(close_numeric.iloc[-1])
    valor_acciones = float(portafolio['acciones'][sym]) * ultimo_precio
    efectivo_final = float(portafolio['efectivo'][sym])
    total_final += valor_acciones + efectivo_final

    print(f"{sym}: efectivo={efectivo_final:.2f}, acciones={float(portafolio['acciones'][sym]):.2f}, valor_acciones={valor_acciones:.2f}, total={valor_acciones + efectivo_final:.2f}")

ganancia = total_final - total_inicial
print(f"\nValor inicial: {total_inicial:.2f}")
print(f"Valor final: {total_final:.2f}")
print(f"Ganancia/Pérdida neta: {ganancia:.2f}")

# Acciones ganadas por sesión
print("\nAcciones ganadas por sesión (netas):")
for sym in acciones:
    ganancia_acciones_neta = total_acciones_compradas[sym] - acciones_vendidas[sym]
    print(f"{sym}: {ganancia_acciones_neta:.2f}")

# Graficar precios y compras del bot (últimos 5 días)
plt.figure(figsize=(12,6))
hist_df_all = pd.DataFrame(historial_portafolio)

for symbol in acciones:
    df = datos_ultimo_dia.get(symbol, pd.DataFrame()).copy()
    if df.empty or 'Close' not in df.columns:
        continue

    # Fix datetime index issues and filter to recent data only
    df = df.reset_index()
    df.columns = ['Datetime'] + list(df.columns[1:])
    df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
    df = df.dropna(subset=['Datetime', 'Close'])
    df = df.set_index('Datetime')
    
    # Sort and take only last 240 points (5 days * 48 intervals)
    df = df.sort_index().tail(240)
    
    if df.empty:
        continue

    # Get actual time range from filtered data
    start_time = df.index.min()
    end_time = df.index.max()
    
    # Filter portfolio history
    hist_df = hist_df_all[hist_df_all['symbol'] == symbol].copy()
    hist_df['fecha'] = pd.to_datetime(hist_df['fecha'])
    hist_df = hist_df[(hist_df['fecha'] >= start_time) & (hist_df['fecha'] <= end_time)]
    hist_df = hist_df.sort_values('fecha')
    hist_df['acciones_diff'] = hist_df['acciones'].diff().fillna(0)
    hist_df['efectivo_diff'] = hist_df['efectivo'].diff().fillna(0)

    # Compras y ventas
    compras_df = hist_df[(hist_df['acciones_diff'] > 0) & (hist_df['efectivo_diff'] < 0)]
    ventas_df = hist_df[(hist_df['acciones_diff'] < 0) & (hist_df['efectivo_diff'] > 0)]

    # Plot price line
    plt.plot(df.index, df['Close'], label=f'{symbol} Precio', alpha=0.7)

    # Plot buy/sell markers
    for _, row in compras_df.iterrows():
        plt.scatter(row['fecha'], row['valor_total']/row['acciones'] if row['acciones'] > 0 else 0, 
                   marker='^', color='green', s=100, zorder=5)
    
    for _, row in ventas_df.iterrows():
        plt.scatter(row['fecha'], row['efectivo']/abs(hist_df.loc[hist_df.index[hist_df.index.get_loc(row.name)-1], 'acciones']) if abs(hist_df.loc[hist_df.index[hist_df.index.get_loc(row.name)-1], 'acciones']) > 0 else 0,
                   marker='v', color='red', s=100, zorder=5)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H:%M"))
plt.gcf().autofmt_xdate()
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
plt.title("Operaciones del bot (últimos 5 días)")
plt.xlabel("Fecha y hora")
plt.ylabel("Precio")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
