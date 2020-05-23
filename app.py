from flask import Flask, render_template, request, redirect, Response
from alpha_vantage.timeseries import TimeSeries
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
app.vars={}
#comment
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['selectedTicker'] = request.form['Ticker']
        return redirect('/about')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/about/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def isIn0320(ele):
    return ele[0][:7] == '2020-03'

def getPrices(stock):
    key = '1YTAHUNQQKTA62OJ'
    ts = TimeSeries(key)
    stockPrices, meta = ts.get_daily(symbol=stock)
    stockClose = [(key, float(value['4. close'])) for key, value in stockPrices.items()]
    prices = list(map(lambda x: x[1], sorted(list(filter(isIn0320, stockClose)), key = lambda x: x[0])))
    return prices

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    fig.suptitle('2020 March Prices ' + app.vars['selectedTicker'])
    ys = getPrices(app.vars['selectedTicker'])
    xs = range(len(ys))
    axis.plot(xs, ys)
    return fig

if __name__ == '__main__':
  app.run(port=33507)
