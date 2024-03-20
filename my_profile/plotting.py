import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def create_btc_usd_chart():
    # Fetch data at 5-minute intervals
    data = yf.download(tickers='BTC-USD', interval='5m', period='1mo')

    # Calculate the logarithmic returns from the closing prices
    data['Log_Return'] = np.log(data['Close'] / data['Close'].shift(1))

    # Calculate daily log return and daily volatility
    daily_log_return = data['Log_Return'].resample('D').sum()
    daily_volatility = data['Log_Return'].pow(2).resample(
        'D').sum()  # Daily volatility as the sum of squared log returns
    normalized_log_return = daily_log_return / np.sqrt(daily_volatility)

    # Create a subplot with 6 rows and 1 column, sharing y-axes for all plots
    fig = make_subplots(rows=6, cols=1, shared_yaxes=True, vertical_spacing=0.08, subplot_titles=(
    'BTC-USD Price', 'Trading Volume', 'Logarithmic Returns', 'Daily Log Return', 'Daily Volatility',
    'Normalized Daily Log Return'))

    # Candlestick chart for the BTC-USD prices
    price_chart = go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'],
                                 close=data['Close'], increasing_line_color='#00CC96', decreasing_line_color='#FF4136')
    fig.add_trace(price_chart, row=1, col=1)

    # Bar chart for trading volume
    volume_chart = go.Scatter(x=data.index, y=data['Volume'], mode='lines', name='Volume', line=dict(color='white'))
    fig.add_trace(volume_chart, row=2, col=1)

    # Line chart for logarithmic returns
    log_return_chart = go.Scatter(x=data.index, y=data['Log_Return'], mode='lines', name='Log Return',
                                  line=dict(color='#d62728'))
    fig.add_trace(log_return_chart, row=3, col=1)

    # Line chart for daily log return
    daily_log_return_chart = go.Scatter(x=daily_log_return.index, y=daily_log_return, mode='lines',
                                        name='Daily Log Return', line=dict(color='#2ca02c'))
    fig.add_trace(daily_log_return_chart, row=4, col=1)

    # Line chart for daily volatility
    daily_volatility_chart = go.Scatter(x=daily_volatility.index, y=daily_volatility, mode='lines',
                                        name='Daily Volatility', line=dict(color='#ff7f0e'))
    fig.add_trace(daily_volatility_chart, row=5, col=1)

    # Line chart for normalized log return
    normalized_log_return_chart = go.Scatter(x=normalized_log_return.index, y=normalized_log_return, mode='lines',
                                             name='Normalized Daily Log Return', line=dict(color='#9467bd'))
    fig.add_trace(normalized_log_return_chart, row=6, col=1)


    # Update the layout for a dark background
    fig.update_layout(template="plotly_dark", height=1200, title='BTC-USD Analysis', title_x=0.5)
    fig.update_yaxes(title_text='Price (USD)', row=1, col=1)
    fig.update_yaxes(title_text='Volume', row=2, col=1)# , type='log')
    fig.update_yaxes(title_text='Log Return', row=3, col=1)
    fig.update_yaxes(title_text='Daily Log Return', row=4, col=1)
    fig.update_yaxes(title_text='Daily Volatility', row=5, col=1)
    fig.update_yaxes(title_text='Normalized Daily Log Return', row=6, col=1)


    for i, y_data in enumerate([data['Close'], data['Volume'], data['Log_Return'], daily_log_return, daily_volatility,
                                normalized_log_return], start=1):
        y_min = y_data.min()
        y_max = y_data.max()
        margin = 0.1
        y_range = y_max - y_min
        y_lower_limit = y_min - margin * y_range
        y_upper_limit = y_max + margin * y_range
        fig.update_yaxes(range=[y_lower_limit, y_upper_limit], row=i, col=1)

    # Hide the rangeslider
    fig.update_layout(xaxis_rangeslider_visible=False)

    # Add x-axis title beneath each subplot
    for i, title in enumerate(('BTC-USD Price', 'Trading Volume', 'Logarithmic Returns', 'Daily Log Return',
                               'Daily Volatility', 'Normalized Daily Log Return'), start=1):
        fig.update_xaxes(title_text='Time', row=i, col=1)

    # Create a shared x-axis object
    shared_xaxis = dict(anchor="y", domain=[0, 1], matches='x')

    # Assign the shared x-axis to all subplots
    for i in range(1, 7):
        fig.update_xaxes(shared_xaxis, row=i, col=1)

    # Set x-axis range for all subplots
    x_range = [data.index.min(), data.index.max()]
    for i in range(1, 7):
        fig.update_xaxes(range=x_range, row=i, col=1)

    # Add annotations for date and time underneath each subplot
    for i, title in enumerate(('BTC-USD Price', 'Trading Volume', 'Logarithmic Returns', 'Daily Log Return',
                               'Daily Volatility', 'Normalized Daily Log Return'), start=1):
        fig.add_annotation(x=0.5, y=-0.1, xref="paper", yref="paper",
                           xanchor="center", yanchor="top",
                           text="Time: {} - {}".format(data.index[0], data.index[-1]),
                           showarrow=False,
                           font=dict(size=10),
                           row=i, col=1)

    return fig

# Test the function
if __name__ == "__main__":
    fig = create_btc_usd_chart()
    fig.show()
