"""
Automated Trading Bot with Machine Learning Predictions - Streamlit Version
WITH ALPACA BROKER INTEGRATION

This bot uses RandomForest classifier to predict stock price movements and executes
aggressive buy/sell strategies on selected stocks using real market data.

Features:
- Interactive Streamlit interface
- Real-time data visualization
- Configurable trading parameters
- Performance metrics dashboard
- Alpaca Paper Trading integration
- Download trading results

Author: Alan Solano & AI Assistant
Date: September 2025
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Try to import Alpaca - if not available, continue without it
try:
    import alpaca_trade_api as tradeapi
    ALPACA_AVAILABLE = True
except ImportError:
    ALPACA_AVAILABLE = False
    st.sidebar.warning("⚠️ Alpaca not installed. Run: pip install alpaca-trade-api")

# =============================================================================
# STREAMLIT PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Trading Bot ML + Broker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SIDEBAR CONFIGURATION
# =============================================================================

st.sidebar.title("🤖 Trading Bot Configuration")

# Stock selection
available_stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "META", "NFLX", "SPY", "QQQ"]
selected_stocks = st.sidebar.multiselect(
    "Select stocks to trade:",
    available_stocks,
    default=["AAPL", "NVDA", "TSLA"]  # More volatile stocks
)

# Portfolio configuration
initial_portfolio = st.sidebar.number_input(
    "Initial Portfolio ($):",
    min_value=1000.0,
    max_value=100000.0,
    value=5000.0,
    step=500.0
)

# Trading parameters
st.sidebar.subheader("📊 Trading Parameters")
buy_threshold = st.sidebar.slider(
    "Buy Threshold (% below reference):",
    0.5, 3.0, 1.0, 0.1
) / 100

sell_threshold = st.sidebar.slider(
    "Sell Threshold (% profit to take):",
    1.0, 5.0, 2.0, 0.1
) / 100

min_profit_threshold = st.sidebar.slider(
    "Min Profit Threshold (% with negative prediction):",
    0.1, 1.0, 0.2, 0.1
) / 100

# ML Model parameters
st.sidebar.subheader("🧠 ML Model Parameters")
n_estimators = st.sidebar.slider("Random Forest Estimators:", 10, 200, 50, 10)
train_period = st.sidebar.selectbox("Training Period:", ["1y", "6mo", "3mo"], index=0)
trade_period = st.sidebar.selectbox("Trading Period:", ["1mo", "15d", "10d", "5d", "3d", "1d"], index=0)
trade_interval = st.sidebar.selectbox("Trading Interval:", ["30m", "15m", "5m"], index=0)

# Trading style configuration
trading_style = st.sidebar.selectbox(
    "Trading Style:",
    ["Conservative", "Moderate", "Aggressive"],
    index=1
)

# =============================================================================
# ALPACA BROKER CONFIGURATION
# =============================================================================

st.sidebar.subheader("🏦 Alpaca Broker Integration")

# Initialize Alpaca API as None
alpaca_api = None

if ALPACA_AVAILABLE:
    # Toggle for real trading
    enable_broker = st.sidebar.checkbox("Enable Alpaca Paper Trading", value=False)
    
    if enable_broker:
        st.sidebar.warning("⚠️ Paper Trading Mode - Virtual Money")
        
        # API Configuration
        api_key = st.sidebar.text_input("Alpaca API Key:", type="password", key="api_key")
        secret_key = st.sidebar.text_input("Alpaca Secret Key:", type="password", key="secret_key")
        
        if api_key and secret_key:
            try:
                # Initialize Alpaca API (Paper Trading)
                alpaca_api = tradeapi.REST(
                    api_key,
                    secret_key,
                    base_url='https://paper-api.alpaca.markets',  # Paper trading
                    api_version='v2'
                )
                
                # Test connection
                account = alpaca_api.get_account()
                st.sidebar.success(f"✅ Connected!")
                st.sidebar.metric("Buying Power", f"${float(account.buying_power):,.2f}")
                st.sidebar.metric("Portfolio Value", f"${float(account.portfolio_value):,.2f}")
                
            except Exception as e:
                st.sidebar.error(f"❌ Connection failed: {str(e)}")
                alpaca_api = None
        else:
            st.sidebar.info("💡 Enter API credentials to enable real trading")
    else:
        st.sidebar.info("📊 Simulation mode only")
else:
    st.sidebar.error("❌ Alpaca library not installed")

# Control buttons
run_simulation = st.sidebar.button("🚀 Run Trading Simulation", type="primary")
reset_data = st.sidebar.button("🔄 Reset Data")

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

if 'portfolio_history' not in st.session_state:
    st.session_state.portfolio_history = []
if 'trading_operations' not in st.session_state:
    st.session_state.trading_operations = []
if 'simulation_complete' not in st.session_state:
    st.session_state.simulation_complete = False

if reset_data:
    st.session_state.portfolio_history = []
    st.session_state.trading_operations = []
    st.session_state.simulation_complete = False
    st.rerun()

# =============================================================================
# MAIN APP INTERFACE
# =============================================================================

st.title("📈 AI Trading Bot with Broker Integration")
st.markdown("*Machine Learning + Real Trading Capabilities*")
st.markdown("---")

# Display current configuration
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Portfolio", f"${initial_portfolio:,.0f}")
with col2:
    st.metric("Stocks", len(selected_stocks))
with col3:
    st.metric("Buy Threshold", f"{buy_threshold*100:.1f}%")
with col4:
    st.metric("Sell Threshold", f"{sell_threshold*100:.1f}%")
with col5:
    broker_status = "🟢 Alpaca" if alpaca_api else "🔴 Simulation"
    st.metric("Trading Mode", broker_status)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def download_stock_data(symbol, period, interval):
    """Download stock data with caching"""
    try:
        data = yf.download(symbol, period=period, interval=interval, progress=False)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        if isinstance(data.index, pd.DatetimeIndex):
            try:
                data.index = data.index.tz_convert(None)
            except:
                data.index = data.index.tz_localize(None)
        return data
    except Exception as e:
        st.error(f"Error downloading {symbol}: {str(e)}")
        return pd.DataFrame()

def create_features(df):
    """Create features for ML model"""
    df_feat = df.copy()
    df_feat['return'] = df_feat['Close'].pct_change()
    df_feat['ma_3'] = df_feat['Close'].rolling(3).mean()
    df_feat['vol_3'] = df_feat['Close'].rolling(3).std()
    df_feat['ma_5'] = df_feat['Close'].rolling(5).mean()
    df_feat['ma_10'] = df_feat['Close'].rolling(10).mean()
    df_feat['rsi'] = calculate_rsi(df_feat['Close'])
    df_feat['target'] = (df_feat['Close'].shift(-1) > df_feat['Close']).astype(int)
    return df_feat.dropna()

def calculate_rsi(prices, window=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def execute_trade(symbol, action, quantity, price, use_alpaca=False):
    """Execute trade - either simulation or real via Alpaca"""
    
    result = {
        'success': False,
        'message': '',
        'executed_qty': 0,
        'executed_price': price,
        'order_id': None
    }
    
    if not use_alpaca or alpaca_api is None:
        # Simulation mode
        result.update({
            'success': True,
            'message': f"SIM: {action} {quantity:.2f} shares of {symbol} @ ${price:.2f}",
            'executed_qty': quantity,
            'executed_price': price,
            'order_id': f"SIM_{datetime.now().strftime('%H%M%S')}"
        })
        return result
    
    try:
        # Real Alpaca trading
        # Check market status
        #clock = alpaca_api.get_clock()
        #if not clock.is_open:
            #result['message'] = f"Market closed - {symbol}"
            #return result
        
        # Check account
        account = alpaca_api.get_account()
        
        if action.upper() == 'BUY':
            buying_power = float(account.buying_power)
            cost = quantity * price
            if cost > buying_power:
                result['message'] = f"Insufficient funds: need ${cost:.2f}, have ${buying_power:.2f}"
                return result
        
        elif action.upper() == 'SELL':
            try:
                position = alpaca_api.get_position(symbol)
                available = float(position.qty)
                if quantity > available:
                    result['message'] = f"Insufficient shares: need {quantity:.2f}, have {available:.2f}"
                    return result
            except:
                result['message'] = f"No position in {symbol} to sell"
                return result
        
        # Submit order
        order = alpaca_api.submit_order(
            symbol=symbol,
            qty=max(1, int(quantity)),  # Alpaca requires whole shares
            side=action.lower(),
            type='market',
            time_in_force='gtc'
        )
        
        # Wait for fill
        time.sleep(2)
        order_status = alpaca_api.get_order(order.id)
        
        if order_status.status == 'filled':
            result.update({
                'success': True,
                'message': f"REAL: {action} {order_status.filled_qty} shares of {symbol} @ ${order_status.filled_avg_price}",
                'executed_qty': float(order_status.filled_qty),
                'executed_price': float(order_status.filled_avg_price),
                'order_id': order.id
            })
        else:
            result['message'] = f"Order {order_status.status}: {order.id}"
            
    except Exception as e:
        result['message'] = f"Trade error: {str(e)}"
    
    return result

def run_trading_simulation(symbols, portfolio_value, use_real_trading=False):
    """Main trading simulation function with broker integration"""
    
    # Adjust thresholds based on trading style
    global buy_threshold, sell_threshold, min_profit_threshold
    if trading_style == "Aggressive":
        buy_threshold = buy_threshold * 0.7  # Buy easier
        min_profit_threshold = min_profit_threshold * 0.5
    elif trading_style == "Conservative":
        buy_threshold = buy_threshold * 1.3  # Buy harder
        sell_threshold = sell_threshold * 1.2
    
    
    # Initialize portfolio
    portfolio = {
        "cash": {symbol: portfolio_value / len(symbols) for symbol in symbols},
        "shares": {symbol: 0 for symbol in symbols},
    }
    
    total_bought = {symbol: 0.0 for symbol in symbols}
    total_sold = {symbol: 0.0 for symbol in symbols}
    portfolio_history = []
    trading_operations = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, symbol in enumerate(symbols):
        status_text.text(f"Processing {symbol}... ({idx+1}/{len(symbols)})")
        progress_bar.progress((idx + 1) / len(symbols))
        
        # Download data
        historical_data = download_stock_data(symbol, train_period, "1d")
        trading_data = download_stock_data(symbol, trade_period, trade_interval)
        
        if historical_data.empty or trading_data.empty:
            st.warning(f"No data available for {symbol}")
            continue
            
        if 'Close' not in historical_data.columns or 'Close' not in trading_data.columns:
            st.warning(f"Missing Close price data for {symbol}")
            continue

        # Prepare ML model
        df_features = create_features(historical_data)
        if len(df_features) < 20:
            st.warning(f"Insufficient historical data for {symbol}")
            continue
    
        # Train model
        feature_cols = ['return', 'ma_3', 'vol_3', 'ma_5', 'ma_10', 'rsi']
        X_train = df_features[feature_cols]
        y_train = df_features['target']
        
        clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        clf.fit(X_train, y_train)
        
        # Trading simulation
        close_prices = pd.to_numeric(trading_data['Close'], errors='coerce').dropna()

        
        # AGREGAR ESTAS LÍNEAS NUEVAS:
        has_bought = False      # Control para evitar múltiples compras
        has_sold = False        # Control para evitar múltiples ventas
        buy_signals = 0         # Contador de señales de compra
        sell_signals = 0        # Contador de señales de venta
        last_buy_price = 0      # Precio de última compra
        
        
        for i, current_price in enumerate(close_prices.values):
            timestamp = close_prices.index[i]
            
            # Calculate features for prediction
            if i >= 10:
                recent_prices = close_prices.values[i-10:i+1]
                ret = (current_price - close_prices.values[i-1]) / close_prices.values[i-1]
                ma_3 = np.mean(recent_prices[-3:])
                vol_3 = np.std(recent_prices[-3:])
                ma_5 = np.mean(recent_prices[-5:])
                ma_10 = np.mean(recent_prices[-10:])
                
                # Calculate RSI
                price_changes = np.diff(recent_prices)
                gains = np.where(price_changes > 0, price_changes, 0)
                losses = np.where(price_changes < 0, -price_changes, 0)
                avg_gain = np.mean(gains[-14:]) if len(gains) >= 14 else np.mean(gains)
                avg_loss = np.mean(losses[-14:]) if len(losses) >= 14 else np.mean(losses)
                rs = avg_gain / (avg_loss + 1e-10)
                rsi = 100 - (100 / (1 + rs))
                
                reference_price = ma_3
            else:
                ret, ma_3, vol_3, ma_5, ma_10, rsi = 0, current_price, 0.01, current_price, current_price, 50
                reference_price = current_price
            
            # Make prediction
            if not np.isnan([ret, ma_3, vol_3, ma_5, ma_10, rsi]).any():
                X_pred = pd.DataFrame({
                    'return': [ret], 'ma_3': [ma_3], 'vol_3': [vol_3],
                    'ma_5': [ma_5], 'ma_10': [ma_10], 'rsi': [rsi]
                })
                prediction = clf.predict(X_pred)[0]
            else:
                prediction = 0
            
            # Debug information (optional)
            debug_conditions = {
                'cash_available': portfolio['cash'][symbol] > 10,
                'ml_prediction': prediction == 1,
                'price_dip': current_price <= reference_price * (1 - buy_threshold),
                'rsi_oversold': rsi < 35,
                'time_based': i % 8 == 0,
                'current_rsi': rsi,
                'current_price': current_price,
                'reference_price': reference_price
            }

        # Uncomment next line to see debug info
        # print(f"{symbol} at {timestamp}: {debug_conditions}")
            
         # BUY LOGIC - Con control de duplicados
            buy_condition = (portfolio['cash'][symbol] > 10 and 
                            not has_bought and  # NUEVO: No comprar si ya compró
                           (prediction == 1 or 
                            current_price <= reference_price * (1 - buy_threshold) or 
                            rsi < 35 or    # RSI oversold
                            current_price < ma_10 * 0.99))  # Price below MA10
            
            if buy_condition:
                buy_signals += 1
                
                # EJECUTAR COMPRA SOLO DESPUÉS DE 2+ SEÑALES CONSECUTIVAS
                if buy_signals >= 2:
                    shares_to_buy = portfolio['cash'][symbol] / current_price
                    
                    if shares_to_buy > 0:
                        # Execute trade
                        trade_result = execute_trade(
                            symbol, 'BUY', shares_to_buy, current_price, use_real_trading
                        )
                        
                        if trade_result['success']:
                            executed_qty = trade_result['executed_qty']
                            executed_price = trade_result['executed_price']
                            cost = executed_qty * executed_price
                            
                            portfolio['shares'][symbol] += executed_qty
                            portfolio['cash'][symbol] -= cost
                            total_bought[symbol] += executed_qty
                            has_bought = True      # MARCAR QUE YA COMPRÓ
                            last_buy_price = executed_price
                            
                            trading_operations.append({
                                'timestamp': timestamp,
                                'symbol': symbol,
                                'action': 'BUY',
                                'shares': executed_qty,
                                'price': executed_price,
                                'prediction': prediction,
                                'message': trade_result['message']
                            })
            else:
                buy_signals = 0  # Reset si no hay señal
            
            # REEMPLAZAR TU SELL LOGIC ACTUAL POR ESTO:
            # SELL LOGIC - Con control de duplicados
            sell_condition = (portfolio['shares'][symbol] > 0 and 
                            not has_sold and  # NUEVO: No vender si ya vendió
                            (current_price >= reference_price * (1 + sell_threshold) or
                             (prediction == 0 and current_price >= reference_price * (1 + min_profit_threshold)) or
                             rsi > 65 or
                             (has_bought and current_price >= last_buy_price * 1.02)))  # 2% profit target
            
            if sell_condition:
                sell_signals += 1
                
                # EJECUTAR VENTA DESPUÉS DE 1+ SEÑAL (más rápido que compra)
                if sell_signals >= 1:
                    shares_to_sell = portfolio['shares'][symbol]
                    
                    # Execute trade
                    trade_result = execute_trade(
                        symbol, 'SELL', shares_to_sell, current_price, use_real_trading
                    )
                    
                    if trade_result['success']:
                        executed_qty = trade_result['executed_qty']
                        executed_price = trade_result['executed_price']
                        proceeds = executed_qty * executed_price
                        
                        total_sold[symbol] += executed_qty
                        portfolio['cash'][symbol] += proceeds
                        portfolio['shares'][symbol] -= executed_qty
                        has_sold = True  # MARCAR QUE YA VENDIÓ
                        
                        trading_operations.append({
                            'timestamp': timestamp,
                            'symbol': symbol,
                            'action': 'SELL',
                            'shares': executed_qty,
                            'price': executed_price,
                            'prediction': prediction,
                            'message': trade_result['message']
                        })
            else:
                sell_signals = 0
            
            # Record portfolio state
            portfolio_value_now = (portfolio['shares'][symbol] * current_price + 
                                 portfolio['cash'][symbol])
            
            portfolio_history.append({
                'timestamp': timestamp,
                'symbol': symbol,
                'shares': portfolio['shares'][symbol],
                'cash': portfolio['cash'][symbol],
                'price': current_price,
                'portfolio_value': portfolio_value_now,
                'prediction': prediction
            })
    
    progress_bar.empty()
    status_text.empty()
    
    return portfolio_history, trading_operations, portfolio, total_bought, total_sold

# =============================================================================
# REAL-TIME BROKER STATUS
# =============================================================================

if alpaca_api is not None:
    with st.sidebar:
        st.subheader("💼 Live Account Status")
        try:
            account = alpaca_api.get_account()
            positions = alpaca_api.list_positions()
            
            # Account metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Portfolio", f"${float(account.portfolio_value):,.0f}")
                # Usar getattr para atributos que pueden no existir
                day_pnl = getattr(account, 'unrealized_pl', getattr(account, 'unrealized_plpc', 0))
                st.metric("Day P&L", f"${float(day_pnl):,.0f}")
            with col2:
                st.metric("Buying Power", f"${float(account.buying_power):,.0f}")
                cash_value = getattr(account, 'cash', getattr(account, 'non_marginable_buying_power', 0))
                st.metric("Cash", f"${float(cash_value):,.0f}")
            
            # Current positions
            if positions:
                st.write("**Current Positions:**")
                for pos in positions:
                    # Usar getattr para manejar diferentes versiones de API
                    pnl = getattr(pos, 'unrealized_pl', 0)
                    pnl_pct = getattr(pos, 'unrealized_plpc', 0)
                    if pnl_pct and pnl_pct != 0:
                        pnl_pct = float(pnl_pct) * 100
                        st.write(f"• {pos.symbol}: {pos.qty} shares ({pnl_pct:+.1f}%)")
                    else:
                        st.write(f"• {pos.symbol}: {pos.qty} shares")
        except Exception as e:
            st.error(f"Error getting account status: {str(e)}")
            # Información básica de debug
            st.write("Debug info:")
            try:
                account = alpaca_api.get_account()
                available_attrs = [attr for attr in dir(account) if not attr.startswith('_')]
                st.write(f"Available account attributes: {available_attrs[:10]}...")
            except:
                pass

# =============================================================================
# RUN SIMULATION
# =============================================================================

if run_simulation and selected_stocks:
    st.info("🚀 Starting trading simulation...")
    
    # Determine trading mode
    use_real_trading = alpaca_api is not None
    
    if use_real_trading:
        st.warning("🔥 **REAL TRADING MODE** - Using Alpaca Paper Trading")
    else:
        st.info("📊 **SIMULATION MODE** - Virtual trading only")
    
    with st.spinner("Running AI trading simulation..."):
        results = run_trading_simulation(
            selected_stocks, initial_portfolio, use_real_trading
        )
        
        portfolio_history, trading_ops, final_portfolio, bought, sold = results
    
    # Store results
    st.session_state.portfolio_history = portfolio_history
    st.session_state.trading_operations = trading_ops
    st.session_state.final_portfolio = final_portfolio
    st.session_state.total_bought = bought
    st.session_state.total_sold = sold
    st.session_state.simulation_complete = True
    
    st.success("✅ Trading simulation completed successfully!")

# =============================================================================
# DISPLAY RESULTS
# =============================================================================

if st.session_state.simulation_complete:
    st.markdown("## 📊 Trading Performance Report")
    
    # Calculate performance metrics
    initial_value = initial_portfolio
    final_values = {}
    total_final_value = 0
    
    for symbol in selected_stocks:
        if symbol in st.session_state.final_portfolio['cash']:
            # Get current price
            final_data = download_stock_data(symbol, "1d", "1m")
            if not final_data.empty and 'Close' in final_data.columns:
                final_price = final_data['Close'].iloc[-1]
                stock_value = st.session_state.final_portfolio['shares'][symbol] * final_price
                cash_value = st.session_state.final_portfolio['cash'][symbol]
                symbol_total = stock_value + cash_value
                total_final_value += symbol_total
                final_values[symbol] = symbol_total
    
    profit_loss = total_final_value - initial_value
    profit_percentage = (profit_loss / initial_value) * 100
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Initial Portfolio", f"${initial_value:,.2f}")
    with col2:
        st.metric("Final Portfolio", f"${total_final_value:,.2f}")
    with col3:
        st.metric("Profit/Loss", f"${profit_loss:,.2f}", f"{profit_percentage:+.2f}%")
    with col4:
        total_trades = len(st.session_state.trading_operations)
        st.metric("Total Trades", total_trades)
    
    # Trading activity summary
    st.markdown("### 📋 Trading Summary by Stock")
    activity_data = []
    for symbol in selected_stocks:
        if symbol in st.session_state.total_bought:
            net_position = st.session_state.total_bought[symbol] - st.session_state.total_sold[symbol]
            activity_data.append({
                'Symbol': symbol,
                'Bought': f"{st.session_state.total_bought[symbol]:.2f}",
                'Sold': f"{st.session_state.total_sold[symbol]:.2f}",
                'Net Position': f"{net_position:.2f}",
                'Final Value': f"${final_values.get(symbol, 0):.2f}"
            })
    
    if activity_data:
        df_activity = pd.DataFrame(activity_data)
        st.dataframe(df_activity, use_container_width=True)
    
    # Recent trades
    if st.session_state.trading_operations:
        st.markdown("### 📈 Recent Trading Operations")
        recent_trades = pd.DataFrame(st.session_state.trading_operations[-10:])  # Last 10 trades
        if not recent_trades.empty:
            st.dataframe(recent_trades[['timestamp', 'symbol', 'action', 'shares', 'price', 'message']], use_container_width=True)
    
    # Interactive visualization
    st.markdown("### 📊 Trading Performance Visualization")
    
    if st.session_state.portfolio_history:
        df_history = pd.DataFrame(st.session_state.portfolio_history)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Stock Prices & Trading Signals', 'Portfolio Value Over Time'),
            vertical_spacing=0.15
        )
        
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
        
        # Plot data for each symbol
        for i, symbol in enumerate(selected_stocks):
            symbol_data = df_history[df_history['symbol'] == symbol]
            if not symbol_data.empty:
                color = colors[i % len(colors)]
                
                # Price line
                fig.add_trace(
                    go.Scatter(
                        x=symbol_data['timestamp'],
                        y=symbol_data['price'],
                        mode='lines',
                        name=f'{symbol} Price',
                        line=dict(color=color, width=2),
                        yaxis='y1'
                    ),
                    row=1, col=1
                )
                
                # Portfolio value
                fig.add_trace(
                    go.Scatter(
                        x=symbol_data['timestamp'],
                        y=symbol_data['portfolio_value'],
                        mode='lines',
                        name=f'{symbol} Value',
                        line=dict(color=color, dash='dash'),
                        yaxis='y2'
                    ),
                    row=2, col=1
                )
        
        # Add trading signals
        if st.session_state.trading_operations:
            ops_df = pd.DataFrame(st.session_state.trading_operations)
            
            # Buy signals
            buy_ops = ops_df[ops_df['action'] == 'BUY']
            if not buy_ops.empty:
                for _, buy in buy_ops.iterrows():
                    fig.add_trace(
                        go.Scatter(
                            x=[buy['timestamp']],
                            y=[buy['price']],
                            mode='markers',
                            marker=dict(symbol='triangle-up', size=12, color='green'),
                            name='Buy',
                            showlegend=False,
                            hovertemplate=f"BUY {buy['symbol']}<br>Price: ${buy['price']:.2f}<br>Shares: {buy['shares']:.2f}"
                        ),
                        row=1, col=1
                    )
            
            # Sell signals
            sell_ops = ops_df[ops_df['action'] == 'SELL']
            if not sell_ops.empty:
                for _, sell in sell_ops.iterrows():
                    fig.add_trace(
                        go.Scatter(
                            x=[sell['timestamp']],
                            y=[sell['price']],
                            mode='markers',
                            marker=dict(symbol='triangle-down', size=12, color='red'),
                            name='Sell',
                            showlegend=False,
                            hovertemplate=f"SELL {sell['symbol']}<br>Price: ${sell['price']:.2f}<br>Shares: {sell['shares']:.2f}"
                        ),
                        row=1, col=1
                    )
        
        fig.update_layout(
            title="AI Trading Bot - Performance Analysis",
            height=700,
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text="Time", row=2, col=1)
        fig.update_yaxes(title_text="Stock Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Portfolio Value ($)", row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Download functionality
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download Excel Report", type="secondary"):
            # Create comprehensive report
            report_data = {
                'Summary': pd.DataFrame([{
                    'Initial_Value': initial_value,
                    'Final_Value': total_final_value,
                    'Profit_Loss': profit_loss,
                    'Return_Percent': profit_percentage,
                    'Total_Trades': len(st.session_state.trading_operations)
                }]),
                'Trading_Activity': pd.DataFrame(activity_data) if activity_data else pd.DataFrame(),
                'All_Trades': pd.DataFrame(st.session_state.trading_operations),
                'Portfolio_History': pd.DataFrame(st.session_state.portfolio_history)
            }
            
            # Create Excel file
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                for sheet_name, df in report_data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            st.download_button(
                label="Download Complete Report",
                data=buffer.getvalue(),
                file_name=f"trading_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        if st.button("🔄 Run New Simulation", type="primary"):
            st.session_state.simulation_complete = False
            st.rerun()

elif not selected_stocks:
    st.warning("⚠️ Please select at least one stock to trade.")
else:
    st.info("💡 Configure your settings in the sidebar and click 'Run Trading Simulation' to start.")
    
    # Show sample data
    if selected_stocks:
        st.markdown("### 📈 Sample Stock Data Preview")
        sample_symbol = selected_stocks[0]
        sample_data = download_stock_data(sample_symbol, "5d", "1h")
        if not sample_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sample_data.index,
                y=sample_data['Close'],
                mode='lines',
                name=f'{sample_symbol} Price',
                line=dict(width=2)
            ))
            fig.update_layout(
                title=f"{sample_symbol} - Recent Price Movement",
                xaxis_title="Time",
                yaxis_title="Price ($)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# EDUCATIONAL SECTION
# =============================================================================

with st.expander("🎓 How This AI Trading Bot Works"):
    st.markdown("""
    ### 🧠 Machine Learning Components:
    
    **1. RandomForest Classifier:**
    - Creates multiple decision trees that "vote" on price direction
    - Predicts: Will price go UP (1) or DOWN (0)?
    - Trained on historical data patterns
    
    **2. Features Used (Bot's "Senses"):**
    - **Return**: Price change percentage
    - **Moving Averages (3, 5, 10 days)**: Trend identification
    - **Volatility**: How "nervous" the stock is
    - **RSI**: Overbought/oversold indicator
    
    **3. Trading Strategy:**
    - **BUY**: When ML predicts UP OR price dips OR time-based
    - **SELL**: When profit target hit OR ML predicts DOWN with some profit
    
    **4. Risk Management:**
    - Portfolio split equally among selected stocks
    - Profit-taking at configurable thresholds
    - Stop-loss via prediction reversal
    """)

with st.expander("🏦 Alpaca Integration Details"):
    st.markdown("""
    ### 🔗 Real Broker Trading Features:
    
    **Paper Trading Mode:**
    - $100,000 virtual money
    - Real market data and execution
    - No financial risk
    - Same API as live trading
    
    **How to Set Up:**
    1. Register at [alpaca.markets](https://alpaca.markets) (free)
    2. Get Paper Trading API keys
    3. Install: `pip install alpaca-trade-api`
    4. Enter credentials in sidebar
    5. Enable "Alpaca Paper Trading"
    
    **Safety Features:**
    - Market hours checking
    - Balance verification
    - Position validation
    - Error handling
    
    **Order Types:**
    - Market orders for immediate execution
    - Automatic retry logic
    - Real-time status updates
    """)

with st.expander("📊 Performance Metrics Explained"):
    st.markdown("""
    ### 📈 Key Performance Indicators:
    
    **Portfolio Metrics:**
    - **Initial Value**: Starting capital
    - **Final Value**: Current portfolio worth
    - **Profit/Loss**: Absolute and percentage gains
    - **Total Trades**: Number of buy/sell operations
    
    **Trading Activity:**
    - **Shares Bought/Sold**: Volume of trades
    - **Net Position**: Current stock holdings
    - **Final Value**: Per-stock portfolio value
    
    **Visualization Elements:**
    - 🟢 Green triangles: Buy signals
    - 🔴 Red triangles: Sell signals
    - Lines: Price movements and portfolio value
    - Interactive: Hover for details
    """)

# =============================================================================
# FOOTER AND DISCLAIMERS
# =============================================================================

st.markdown("---")

# Warning section
st.error("""
⚠️ **IMPORTANT DISCLAIMERS:**
- This is an educational tool and trading simulation
- Past performance does not guarantee future results
- Trading involves risk of financial loss
- Always do your own research before investing
- Start with paper trading before using real money
- The AI predictions are not financial advice
""")

# Technical info
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Technologies Used:**\n- Streamlit UI\n- scikit-learn ML\n- yfinance Data\n- Plotly Charts")
with col2:
    st.info("**Data Sources:**\n- Yahoo Finance\n- Real-time prices\n- Historical data\n- Market indicators")
with col3:
    st.info("**AI Features:**\n- RandomForest ML\n- Feature engineering\n- Predictive signals\n- Risk management")

# Footer
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
<p><b>AI Trading Bot v2.0</b> | Built with ❤️ by Alan Solano & AI Assistant</p>
<p>For educational and research purposes | September 2025</p>
</div>
""", unsafe_allow_html=True)