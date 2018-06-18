from bokeh.plotting import figure, output_file, show
from flask import Flask, render_template, request
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
import pandas as pd

def plot_stock_data(ticker_symbol, options):
    do_cls, do_open, do_high, do_low = options
    

    url= "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker_symbol+"&apikey=U4AV38IHD6RSSF9Q&datatype=csv" 
    

    ## Using pandas to process the data.
    stock_data = pd.read_csv(url)
    stock_data  = stock_data.sort_values(by='timestamp')  
    stock_data['timestamp'] = pd.to_datetime(stock_data.timestamp, errors='coerce')
    stock_data = stock_data.set_index('timestamp')  
     
    ## The API returns data of last 100 days.
    stock_data = stock_data[:30]
    ## Plotting using Bokeh
    p = figure(#title="Stock data", 
            x_axis_label='Date', y_axis_label='Stock price', x_axis_type='datetime')
    
    if do_open:
        p.line(stock_data.index.values, stock_data.open.values, legend="Open", line_width=2, color='blue')
    if do_cls:
        p.line(stock_data.index.values, stock_data.close.values, legend="Close", line_width=2, color='red')
    if do_high:
        p.line(stock_data.index.values, stock_data.high.values, legend="High", line_width=2, color='cyan')
    if do_low:
        p.line(stock_data.index.values, stock_data.low.values, legend="Low", line_width=2, color='black')

    p.xaxis[0].formatter = DatetimeTickFormatter()
    p.legend.location = "top_left"

    script, div = components(p)
    
    return render_template("plot.html", script=script, div=div, company="")
    
