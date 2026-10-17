import pandas as pd
import numpy as np
from schwab_api.client import SchwabClient

class MidasSwingTrader:
    def __init__(self):
        self.client = SchwabClient()

    def get_market_data(self, symbol, period_type='year', frequency_type='daily'):
        """
        Fetch historical data and convert to DataFrame.
        """
        try:
            # period=1 year, daily frequency
            data = self.client.get_price_history(
                symbol, 
                period_type=period_type, 
                period=1, 
                frequency_type=frequency_type, 
                frequency=1
            )
            
            if not data or 'candles' not in data:
                print(f"No candle data for {symbol}")
                return None
                
            candles = data['candles']
            df = pd.DataFrame(candles)
            # Schwab returns timestamp in milliseconds
            df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
            df.set_index('datetime', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def calculate_indicators(self, df):
        """
        Add technical indicators to the DataFrame.
        """
        # SMA
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        
        # RSI (14)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        # Prevent division by zero
        rs = gain / loss.replace(0, np.finfo(float).eps) 
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands (20, 2)
        df['BB_Mid'] = df['SMA_20']
        df['BB_Std'] = df['close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Mid'] + (df['BB_Std'] * 2)
        df['BB_Lower'] = df['BB_Mid'] - (df['BB_Std'] * 2)
        
        return df

    def generate_chart_html(self, df, symbol, signal="NEUTRAL", reason=""):
        """
        Generates an interactive HTML chart using Plotly CDN.
        """
        # Prepare data strings for JS
        dates = [d.strftime('%Y-%m-%d') for d in df.index]
        
        # Helper to treat Series as list, handling NaNs if possible (JS handles null)
        def to_js_arr(series):
            return str(series.fillna('null').tolist())

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Midas Analysis: {symbol}</title>
            <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
            <style>
                body {{ font-family: sans-serif; background: #111; color: #eee; }}
                .container {{ width: 95%; margin: 0 auto; }}
                .header {{ padding: 20px; border-bottom: 1px solid #333; }}
                .signal {{ font-size: 24px; font-weight: bold; color: { '#00ff00' if 'BUY' in signal else '#ff0000' if 'SELL' in signal else '#ffff00' }; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Midas Swing Analysis: {symbol}</h1>
                    <div class="signal">SIGNAL: {signal}</div>
                    <p>Reason: {reason}</p>
                </div>
                <div id="chart" style="width:100%;height:800px;"></div>
            </div>
            <script>
                var dates = {dates};
                var open = {to_js_arr(df['open'])};
                var high = {to_js_arr(df['high'])};
                var low = {to_js_arr(df['low'])};
                var close = {to_js_arr(df['close'])};
                
                var sma20 = {to_js_arr(df['SMA_20'])};
                var sma50 = {to_js_arr(df['SMA_50'])};
                var bb_upper = {to_js_arr(df['BB_Upper'])};
                var bb_lower = {to_js_arr(df['BB_Lower'])};
                
                var rsi = {to_js_arr(df['RSI'])};

                var trace1 = {{
                    x: dates, 
                    close: close, 
                    decreasing: {{line: {{color: '#ff4d4d'}}}}, 
                    high: high, 
                    increasing: {{line: {{color: '#00cc66'}}}}, 
                    line: {{color: 'rgba(31,119,180,1)'}}, 
                    low: low, 
                    open: open, 
                    type: 'candlestick', 
                    xaxis: 'x', 
                    yaxis: 'y',
                    name: 'Price'
                }};

                var traceSMA20 = {{
                    x: dates, y: sma20, type: 'scatter', mode: 'lines',
                    line: {{color: '#ffff00', width: 1}}, name: 'SMA 20'
                }};
                
                var traceSMA50 = {{
                    x: dates, y: sma50, type: 'scatter', mode: 'lines',
                    line: {{color: '#ff00ff', width: 1}}, name: 'SMA 50'
                }};
                
                var traceBBU = {{
                    x: dates, y: bb_upper, type: 'scatter', mode: 'lines',
                    line: {{color: 'rgba(200,200,200,0.3)', width: 0}}, showlegend: false, hoverinfo: 'none'
                }};
                
                var traceBBL = {{
                    x: dates, y: bb_lower, type: 'scatter', mode: 'lines',
                    fill: 'tonexty', fillcolor: 'rgba(200,200,200,0.1)',
                    line: {{color: 'rgba(200,200,200,0.3)', width: 0}}, name: 'Bollinger Bands'
                }};

                var traceRSI = {{
                    x: dates, y: rsi, type: 'scatter', mode: 'lines',
                    line: {{color: '#00bfff', width: 1}}, name: 'RSI',
                    yaxis: 'y2'
                }};
                
                var layout = {{
                    dragmode: 'zoom', 
                    margin: {{r: 10, t: 25, b: 40, l: 60}}, 
                    showlegend: true, 
                    xaxis: {{
                        autorange: true, 
                        domain: [0, 1], 
                        range: [dates[0], dates[dates.length-1]], 
                        rangeslider: {{visible: false}}, 
                        title: 'Date', 
                        type: 'date'
                    }}, 
                    yaxis: {{
                        autorange: true, 
                        domain: [0.3, 1], 
                        type: 'linear',
                        gridcolor: '#333'
                    }},
                    yaxis2: {{
                        domain: [0, 0.2], 
                        anchor: 'x', 
                        title: 'RSI',
                        range: [0, 100],
                        gridcolor: '#333'
                    }},
                    plot_bgcolor: '#111',
                    paper_bgcolor: '#111',
                    font: {{ color: '#ccc' }},
                    shapes: [
                        {{ type: 'line', x0: dates[0], x1: dates[dates.length-1], y0: 70, y1: 70, yref: 'y2', line: {{color: 'red', width: 1, dash: 'dot'}} }},
                        {{ type: 'line', x0: dates[0], x1: dates[dates.length-1], y0: 30, y1: 30, yref: 'y2', line: {{color: 'green', width: 1, dash: 'dot'}} }}
                    ]
                }};

                Plotly.newPlot('chart', [trace1, traceSMA20, traceSMA50, traceBBU, traceBBL, traceRSI], layout);
            </script>
        </body>
        </html>
        """
        
        filename = f"charts/chart_{symbol}.html"
        try:
            with open(filename, "w", encoding='utf-8') as f:
                f.write(html_content)
            return filename
        except Exception as e:
            print(f"Failed to generate chart for {symbol}: {e}")
            return None

    def analyze_ticker(self, symbol):
        """
        Analyze a ticker for potential swing setups.
        """
        print(f"Analyzing {symbol}...")
        df = self.get_market_data(symbol)
        if df is None or len(df) < 50:
            return {
                "symbol": symbol,
                "signal": "ERROR",
                "reason": "Insufficient Data"
            }

        df = self.calculate_indicators(df)
        
        latest = df.iloc[-1]
        
        signal = "NEUTRAL"
        reason = ""
        
        # Trend Check
        trend_up = latest['SMA_20'] > latest['SMA_50']
        
        # Mean Reversion: RSI thresholds
        rsi = latest['RSI']
        
        if rsi < 30:
            signal = "BUY_CALL" # Oversold
            reason = f"RSI Oversold ({rsi:.2f})"
        elif rsi > 70:
            signal = "BUY_PUT" # Overbought
            reason = f"RSI Overbought ({rsi:.2f})"
            
        # Refine with Trend
        if signal == "BUY_CALL" and trend_up:
            reason += " + Uptrend Support"
        elif signal == "BUY_PUT" and not trend_up:
            reason += " + Downtrend Resistance"
            
        # Generate Chart
        chart_path = self.generate_chart_html(df, symbol, signal, reason)
            
        return {
            "symbol": symbol,
            "signal": signal,
            "reason": reason,
            "price": latest['close'],
            "RSI": rsi,
            "SMA_20": latest['SMA_20'],
            "chart": chart_path
        }

if __name__ == "__main__":
    bot = MidasSwingTrader()
    # Test on SPY
    try:
        result = bot.analyze_ticker("SPY")
        print(result)
    except Exception as e:
        print(f"Test failed: {e}")
