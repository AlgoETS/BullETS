import plotly.graph_objects as go
import plotly.express as px

def candle_chart(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
    return fig

def cash_balance_chart(df):
    fig = px.line(df, x='timestamp', y="cash_balance", title='Cash Balance evolution')
    return fig
