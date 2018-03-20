
from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import requests
import weather
import sys
# import cv2
# import matplotlib.pyplot as plt
from PIL import Image
import numpy as np  # dealing with arrays
import tqdm
from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask import make_response
from flask_cors import CORS
#import ui
# Flask app should start in global layout
app = Flask(__name__)
CORS(app)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


@app.route('/webhook1', methods=['POST'])
def webhook1():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = req.get("url")
    #res = openphoto(url1)
    return res


def processRequest(req):
    print("Request:")
    print(json.dumps(req, indent=4))
    if req.get("result").get("action") == "yahooWeatherForecast":
        res = weather.weather(req)
    elif req.get("result").get("action") == "commodityprice":
        data = req
        res = price(data)
    # elif req.get("result").get("action") == "sayfeatures":
    # 	res=feature()
    # elif req.get("result").get("action") == "getChemicalSymbol":
    #     data = req
    #     res = makeWebhookResultForGetChemicalSymbol(data)
    elif req.get("result").get("action") == "news":
        res = news.news()
    else:
        return {}
    return res


# def feature():
# 	speech="1.I can update you with the weather information of the required location to plan your next move.\n 2.I can update you with today's headlines of the agricultural domain. \n 3..I can tell you about the market price of a commodity you wish to sell. \n"
# 	return {
#         "speech": speech,
#         "displayText": speech,
#         # "data": data,
#         # "contextOut": [],
#         "source": "apiai-weather-webhook-sample"
#     }


def price(req):
    commodity = req.get("result").get("parameters").get("CommodityName")
    district = req.get("result").get("parameters").get("DistrictName")
    # commodity=commodity.upper()
    # district=district.upper()
    r = requests.get(
        "https://www.mandiguru.co.in/daily-bhav/rajasthan?date_from=&date_to=&mandi=" + district + "+%28F+%26+V%29&product=" + commodity + "+&search=Search")
    soup = BeautifulSoup(r.text, 'html.parser')
    tr = soup.find_all('tr')
    records = []
    for link in tr:
        td = link.find_all('td')
        if len(td) > 1:
            x = 0
            a = b = c = d = ""
            for t in td:
                if x == 4:
                    d = t.text[41:63]
                x = x + 1
            records.append((d))
    speech = "The price of " + commodity + " in district " + district + " is " + d + "."
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
