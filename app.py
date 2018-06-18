from flask import Flask, render_template, request, redirect
from plot_stock_data import plot_stock_data

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.error('Calling index method')
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/plot', methods=['POST'])
def plot():
    app.logger.info('Calling plot method')
    form = request.form
    ticker = form['ticker']
    features = form.getlist('features')

    if features:
        do_open = 'open' in features
        do_close= 'close' in features
        do_high = 'high' in features
        do_low= 'low' in features
        options= (do_open, do_close, do_high, do_low)
        return plot_stock_data(ticker, options)
    else:
        ##TODO: Error page, JS form validation, ticker name mapping.

        return "Error page"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
