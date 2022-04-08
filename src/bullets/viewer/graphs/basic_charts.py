import plotly.graph_objects as go
import plotly.express as px

def candle_chart(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
    return fig

def summary_graph(df):
    fig = px.line(df, x='timestamp', y=df.columns[[6,10,13,14]], title='Summary Graph')
    #fig.append_trace(px.Line(df,x='timestamp'))
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    return fig



