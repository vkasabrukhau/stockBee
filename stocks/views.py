from django.shortcuts import render
import yfinance as yf
from .models import Stock
# Create your views here.

def index(request):
    return render(request, "stocks/index.html", {
        "stocks": Stock.objects.all()
    })

def stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    ticker = yf.Ticker(str(stock.stockCode))
    print(stock.stockCode)
    fastInfo = ticker.fast_info
    print(fastInfo.open)
    print(fastInfo.day_high)
    print(fastInfo.day_low)
    return render(request, "stocks/stock.html", {
        "stock": stock,
        "open": str(fastInfo.open),
        "dayhigh": str(fastInfo.day_high),
        "daylow": str(fastInfo.day_low),
    })
