# app.py
from flask import Flask
import WSB_Trends as wsb
import json


app = Flask(__name__)
# defining a route
@app.route("/") # decorator
def home(): # route handler function
    # returning a response
    return "Hello World!"


@app.route('/getTopWSBStocks')
def getTopWSBStocks():
    data = wsb.getTopWSBStocks()
    return data

app.run(debug=True)