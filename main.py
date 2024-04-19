from wsgiref import simple_server
from flask import Flask, request, render_template
import pickle
import json
import numpy as np
app = Flask(__name__)

def get_predict_profit(x1,x2,x3,x4,x5,x6,x7,x8):
    with open('models/profit_prediction_model_HP.sav', 'rb') as f:
        model = pickle.load(f)

    with open("models/columns.json", "r") as f:
        data_columns = json.load(f)['data_columns']

    x = np.zeros(len(data_columns))
    x[0] = x1
    x[1] = x2
    x[2] = x3
    x[3] = x4
    x[4] = x5
    x[5] = x6
    x[6] = x7
    x[7] = x8

    return round(model.predict([x])[0], 2)


@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        current_assets = float(request.form['Current assets'])
        cost_of_goods_sold = float(request.form["Cost of goods sold"])
        depreciation = float(request.form["Depreciation and amortization"])
        inventory = float(request.form["Inventory"])
        total_receivables = float(request.form["Total Receivables"])
        total_assets = float(request.form["Total assets"])
        total_long_term_debt = float(request.form["Total Long-term debt"])
        total_operating_expenses = float(request.form["Total Operating Expenses"])
        #output= "Success"
        output = get_predict_profit(current_assets, cost_of_goods_sold, depreciation, inventory,total_receivables, total_assets, total_long_term_debt, total_operating_expenses)
        return render_template('index.html',show_hidden=True, prediction_text='Company Profit must be $ {}'.format(output))

if __name__ == "__main__":
    #app.run(debug=True)
    host = '0.0.0.0'
    port = 5000
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()
