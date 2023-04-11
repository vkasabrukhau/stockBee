from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Stock, ExtendedUser
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

@login_required
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

def signin(request):
    if(request == "POST"):
        authenticate()
    return render(request, "stocks/signin.html")
    
def signup(request):
    if(request.method == 'POST'):
        firstName = request.POST['firstname']
        lastName = request.POST['lastname']
        age = request.POST['age']
        finances = request.POST['finances']
        username = request.POST['username']
        password = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if(password == password2):
            if(User.objects.filter(email=email).exists()):
                messages.info(request, "Email already taken")
                return redirect(request, 'signup')
            elif(User.objects.filter(username=username).exists()):
                messages.info(request, "Username already taken")
                return redirect('signup')
            else:
                user = User.objects.create_user(username = username, email = email, password = password)
                extendedUser = ExtendedUser.objects.create(user = user, age = age, startingFinance = finances)
                extendedUser.save()
                user.save()
                user.first_name = firstName
                user.last_name = lastName
                user.date_joined = now
                user.save()
                user_login = authenticate(username = username, password = password)
                login(request, user_login)
                return redirect('index')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, "stocks/signup.html")

@login_required
def profile(request):
    u = request.user
    extendeduser = u.extendeduser
    return render(request, "stocks/profile.html", {
        "firstname": u.username,
        "lastname": u.last_name,
        "username": u.username,
        "email": u.email,
        "age": extendeduser.age,        
        "startingfinances": extendeduser.startingFinance,
    })