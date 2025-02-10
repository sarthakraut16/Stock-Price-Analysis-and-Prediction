import plotly.graph_objects as go
import dateutil 
import pandas_ta as pta
import datetime
import pandas as pd


def plotly_table(df):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df.columns),
            fill_color="#FFD700",   # Header background color
            font=dict(color="black", size=18),  # Header font color & size
            align="left",
            height=40
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=["#2E2E2E", "#333333"],  # Alternating row colors
            font=dict(color="white", size=18),  # Cell text color & size
            align="left",
            height=40
        )
    )])

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=250)  # Adjust margins
    return fig




from dateutil import relativedelta
import datetime

def filter_data(dataframe, num_period):
    if num_period == '1mo': 
        date = dataframe.index[-1] + relativedelta.relativedelta(months=-1) 
    elif num_period == '5d':
        date = dataframe.index[-1] + relativedelta.relativedelta(days=-5)
    elif num_period == '6mo': 
        date = dataframe.index[-1] + relativedelta.relativedelta(months=-6) 
    elif num_period == '1y': 
        date = dataframe.index[-1] + relativedelta.relativedelta(years=-1)
    elif num_period == '3y': 
        date = dataframe.index[-1] + relativedelta.relativedelta(years=-3)
    elif num_period == '5y':
        date = dataframe.index[-1] + relativedelta.relativedelta(years=-5) 
    else: 
        date = dataframe.index[0]  # Use the earliest date if period is not specified

    # Ensure 'Date' is in datetime format and filter based on the calculated date
    dataframe = dataframe.reset_index()
    dataframe['Date'] = pd.to_datetime(dataframe['Date'])
    
    # Return the filtered dataframe
    return dataframe[dataframe['Date'] > date]





def close_chart(dataframe, num_period =False):
    if num_period: 
        dataframe = filter_data(dataframe, num_period) 
    fig = go.Figure() 
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines',name='Open', line=dict(width=2,color='pink') ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines',name='Close', line=dict(width=2,color='yellow') ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines',name='High', line=dict(width=2,color='green') ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines',name='Low', line=dict(width=2,color='red') ))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout( 
        height=450,plot_bgcolor = 'black', paper_bgcolor = 'black',margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="bottom", 
        y=1.02, 
        xanchor="right",
        x=1
        )
    )
    return fig


def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe['Date'],
                        open = dataframe['Open'], high=dataframe['High'],
                        low = dataframe['Low'], close = dataframe['Close']))
    fig.update_layout( 
        height=450,plot_bgcolor = 'black', paper_bgcolor = 'black',margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="bottom", 
        y=1.02, 
        xanchor="right",
        x=1
        )
    )
    return fig



def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe.RSI,
                             name='RSI', marker_color="orange", line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe),
                             name='Overbrought', marker_color="red", line=dict(width=2, color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe), name='Oversold', marker_color="blue", line=dict(width=2, color='blue', dash='dash'))) 
    fig.update_layout( 
        height=300,plot_bgcolor = 'black', paper_bgcolor = 'black',margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="bottom", 
        y=1.02, 
        xanchor="right",
        x=1
        )
    )
    return fig



def movingaverage(dataframe, num_period):
    dataframe["SMA_50"] = pta.sma(dataframe['Close'], 50)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure() 
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines',name='Open', line=dict(width=2,color='pink') ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines',name='Close', line=dict(width=2,color='yellow') ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines',name='High', line=dict(width=2,color='green') ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines',name='Low', line=dict(width=2,color='red') ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],mode='lines',name='SMA 50', line=dict(width=2,color='purple')))
    fig.update_layout( 
        height=450,plot_bgcolor = 'black', paper_bgcolor = 'black',margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="bottom", 
        y=1.02, 
        xanchor="right",
        x=1
        )
    )
    fig.update_xaxes(rangeslider_visible=True)
    return fig



def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close']).iloc[:,0]
    macd_signal = pta.macd(dataframe['Close']).iloc[:,1] 
    macd_hist = pta.macd(dataframe['Close']).iloc[:,2] 
    dataframe['MACD'] = macd 
    dataframe['MACD Signal'] = macd_signal 
    dataframe = filter_data(dataframe, num_period) 
    fig = go.Figure()
    fig.add_trace(go.Scatter( x=dataframe['Date'], y=dataframe['MACD'], name = 'RSI',marker_color='orange', line = dict( width=2, color = 'orange'), )) 
    fig.add_trace(go.Scatter(
         x=dataframe['Date'], 
         y=dataframe ['MACD Signal'], name = 'Overbought', marker_color='red', line = dict( width=2, color = 'red'), 
        ))
    c = ['red' if cl <0 else "green" for cl in macd_hist] 
    fig.update_layout( 
        height=300,plot_bgcolor = 'black', paper_bgcolor = 'black',margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", yanchor="bottom", 
        y=1.02, 
        xanchor="right",
        x=1
        )
    )
    return fig



def Moving_average_forecast(df):
    fig = go.Figure()

    # Plot the historical closing prices
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='blue')))

    # Plot the forecasted closing prices
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Forecast', line=dict(color='red', dash='dash')))

    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0),
                      plot_bgcolor='white', paper_bgcolor='grey', legend=dict(x=0, y=1, traceorder='normal'))
    return fig
