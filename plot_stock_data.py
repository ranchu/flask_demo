from bokeh.plotting import figure, output_file, show
from flask import Flask, render_template, request
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
import pandas as pd

def plot_stock_data(ticker_symbol, options):
    do_cls, do_open, do_high, do_low = options
    
    print 'Plot stock data method'

    url= "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker_symbol+"&apikey=U4AV38IHD6RSSF9Q&datatype=csv" 
    
    ## Using pandas to process the data.
    stock_data = pd.read_csv(url)
    stock_data  = stock_data.sort_values(by='timestamp')  
    stock_data['timestamp'] = pd.to_datetime(stock_data.timestamp, errors='coerce')
    stock_data = stock_data.set_index('timestamp')  
     

    ## Plotting using Bokeh
    p = figure(title="Stock data", x_axis_label='Date', y_axis_label='Stock price')
    
    if do_open:
        print 'Plotting opening price'
        p.line(stock_data.index.values, stock_data.open.values, legend="Open", line_width=2, color='blue')
    if do_cls:
        print 'Plotting closing price'
        p.line(stock_data.index.values, stock_data.close.values, legend="Close", line_width=2, color='red')
    if do_high:
        print 'Plotting high price'
        p.line(stock_data.index.values, stock_data.high.values, legend="High", line_width=2, color='cyan')
    if do_low:
        print 'Plotting low price'
        p.line(stock_data.index.values, stock_data.low.values, legend="Low", line_width=2, color='black')

    p.xaxis[0].formatter = DatetimeTickFormatter()
    p.legend.location = "top_left"

    script, div = components(p)
    
    print 'Script = ', script
    print 'Div= ', div
    

    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # output to static HTML file
    output_file("lines.html")

    # create a new plot with a title and axis labels
    p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(x, y, legend="Temp.", line_width=2)

    # show the results
    show(p)

    return render_template("plot.html", script=script, div=div, company="")
    
