from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Stock
from django import forms
import yfinance as yf
import datetime
# Create your views here.

now = datetime.datetime.now()
currenthour = now.hour
systemHour = 0
percent_change = []
last_prices = []

def stockUpdater():
    global systemHour
    global currenthour
    global percent_change
    global last_prices
    if systemHour != currenthour:
        print(systemHour)
        systemHour = currenthour
        stocks = Stock.objects.all()
        for stock in stocks:
            ticker = yf.Ticker(str(stock.stockCode))
            fastInfo = ticker.fast_info
            percent_change.append(round(fastInfo.last_price/fastInfo.previous_close * 100 - 100, 3))
            last_prices.append(str(round(fastInfo.last_price, 3)))

def index(request):
    #stocks = Stock.objects.all()
    #percent_change = []
    #last_prices = []
    #for stock in stocks:
        #ticker = yf.Ticker(str(stock.stockCode))
        #fastInfo = ticker.fast_info
        #percent_change.append(round(fastInfo.last_price/fastInfo.previous_close * 100 - 100, 3))
        #last_prices.append(str(round(fastInfo.last_price, 3)))
    global percent_change
    global last_prices
    stockUpdater()
    return render(request, "stocks/index.html", {
        "stocks": Stock.objects.all(),
        "percent_change": percent_change,
        "last_prices": last_prices
    })

def add(request):
    if request.method == 'POST':
        data = request.POST
        stock = Stock(stockCode = data.get("stockCode"), companyName = data.get("companyName"))
        stock.save()
        return HttpResponseRedirect(reverse("index", args=()))
    else:
        return render(request, 'stocks/add.html')

def stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    ticker = yf.Ticker(str(stock.stockCode))
    fastInfo = ticker.fast_info
    return render(request, "stocks/stock.html", {
        "stock": stock,
        "open": str(fastInfo.open),
        "dayhigh": str(fastInfo.day_high),
        "daylow": str(fastInfo.day_low),
        "lastprice": str(fastInfo.last_price),
        "share": str(fastInfo.shares),
        "currency": str(fastInfo.currency),
        "percent_change": str(round(fastInfo.last_price/fastInfo.previous_close * 100 - 100, 3))
    })
