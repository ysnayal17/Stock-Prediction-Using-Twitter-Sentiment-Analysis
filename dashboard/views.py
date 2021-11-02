from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib import messages
import yfinance
import tweepy as tw
from tweepy import OAuthHandler
import datetime
from newsapi import NewsApiClient
import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler



# Create your views here.
def dashboard(request):
    if not request.user.is_anonymous:
        global static_prices
        if request.method == 'POST':
            ticker = request.POST['ticker']
            if ticker.upper() == 'NASDAQ:MSFT':
                getInfo = yfinance.Ticker('MSFT')
                price = [
                    getInfo.info['open'],
                    getInfo.info['currentPrice'],
                    getInfo.info['dayHigh'],
                    getInfo.info['dayLow']
                ]
                tweetObj = tweet('Microsft')
                newsObj = news('Microsoft')
                predClose = prediction()
                context = {
                    'prices': price,
                    'ticker': 'NASDAQ:MSFT',
                    'tweetObj': tweetObj,
                    'newsObj': newsObj,
                    'predClose': predClose
                }
                static_prices = context
                return render(request, 'dashboard/dashboard.html', context)
            if ticker.upper() == 'NASDAQ:GOOGL':
                getInfo = yfinance.Ticker('GOOGL')
                price = [
                    getInfo.info['open'],
                    getInfo.info['currentPrice'],
                    getInfo.info['dayHigh'],
                    getInfo.info['dayLow']
                ]
                tweetObj = tweet('Google')
                newsObj = news('Microsoft')
                context = {
                    'prices': price,
                    'ticker': 'NASDAQ:GOOGL',
                    'tweetObj': tweetObj,
                    'newsObj': newsObj
                }
                static_prices = context
                return render(request, 'dashboard/dashboard.html', context)
            else:
                return HttpResponse('Enter as per format')
        else:
            return render(request, 'dashboard/dashboard.html', static_prices)
    else:
        messages.error(request, 'You are not authenticated')
        return render(request, 'home/index1.html')

def tweet(query):
    # consumer_key = 'p1c4TOG04CIlYFGSbjRdBQr98'
    # consumer_secret = 'lf29kiY3mXdW0FLgvnFIaT0F9vjsNgeM49DbMseBCppsHzwQtm'
    # access_token = '1354062104139952130-goNdDKZ7Hn66cSXvO6jLaQce2mELAE'
    # access_token_secret = '51uilEwpSGQcZnAM7AwuIpxkzHPU9AIa2Geppigjl5R1U'
    # auth = tw.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tw.API(auth)

    # tweets = api.search_tweets(q = query, count = 2, lang='en')
    tweets = [
        {'created_at': 'Oct. 3, 2021, 3:23 a.m.', 'text': 'RT @IamRenganathan: Life is short get your name in the hall of fame Google, Apple, Microsft, Netflix, Amazon, and Facebook.'},
        {'created_at': 'Oct. 2, 2021, 7:43 p.m.', 'text': '@TMessi_1 @Porkchop_EXP @Cernovich So microsft flight sim is for kids? tell that to the pilots that use it to train.'}
    ]
    return tweets

def news(query):

    # top_headlines = newsapi.get_top_headlines(q='microsoft',
    #                                       sources='bbc-news,the-verge',
    #                                       # category='business',
    #                                       language='en',
    #                                       # country='us'
    #                                       )
    # news = top_headlines

    news = [{'articles': [{'author': 'Verge Staff',
                'content': 'Come on in, the windows are fine\r\nIf you buy something from a Verge link, Vox Media may earn a commission. See our ethics statement.\r\nMicrosofts next version of Windows, Windows 11, is coming October… [+17914 chars]',
                'description': 'Microsoft’s next version of Windows, Windows 11, is coming October 5th. Technically, a near-final version is already here, and we’ve spent considerable time with it on over a dozen different PCs.',
                'publishedAt': '2021-10-02T15:00:00Z',
                'source': {'id': 'the-verge', 'name': 'The Verge'},
                'title': 'Windows 11 seems okay',
                'url': 'https://www.theverge.com/22705148/windows-11-upgrade-beta-release-preview-impressions',
                'urlToImage': 'https://cdn.vox-cdn.com/thumbor/p_u0ZlnLrGczT6gT7lTppXCub3M=/0x178:2560x1518/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/22894952/twarren__windows11_sharper.jpg'}],
            'status': 'ok',
            'totalResults': 1},
            {'articles': [{'author': 'Verge Staff',
                'content': 'Come on in, the windows are fine\r\nIf you buy something from a Verge link, Vox Media may earn a commission. See our ethics statement.\r\nMicrosofts next version of Windows, Windows 11, is coming October… [+17914 chars]',
                'description': 'Microsoft’s next version of Windows, Windows 11, is coming October 5th. Technically, a near-final version is already here, and we’ve spent considerable time with it on over a dozen different PCs.',
                'publishedAt': '2021-10-02T15:00:00Z',
                'source': {'id': 'the-verge', 'name': 'The Verge'},
                'title': 'Windows 11 seems okay',
                'url': 'https://www.theverge.com/22705148/windows-11-upgrade-beta-release-preview-impressions',
                'urlToImage': 'https://cdn.vox-cdn.com/thumbor/p_u0ZlnLrGczT6gT7lTppXCub3M=/0x178:2560x1518/fit-in/1200x630/cdn.vox-cdn.com/uploads/chorus_asset/file/22894952/twarren__windows11_sharper.jpg'}],
            'status': 'ok',
            'totalResults': 1}]
    return news

def prediction():
    np.random.seed(17)
    model = load_model("dashboard/lstm_model/my_model.h5")
    stocks_data = pd.read_csv("dashboard/tweets/Microsoft.csv")
    # take last 60 days data as input and convert to numpy arrays - today's feature
    startFrom = len(stocks_data) - 60
    inputX = stocks_data.filter(['Adj Close'])[startFrom:].values
    scaler = MinMaxScaler(feature_range = (0,1))
    scaled_data = scaler.fit_transform(inputX)
    scaled_data = np.reshape(scaled_data.T, (scaled_data.T.shape[0], scaled_data.T.shape[1], 1))
    predClose = model.predict(scaled_data)
    predClose = scaler.inverse_transform(predClose)
    # predClose = [[289.81406]]
    # print(predClose)
    return predClose[0][0]

def retrain_model(request):
    # model = load_model("dashboard/lstm_model/my_model.h5")
    # stocks_data = pd.read_csv("dashboard/tweets/Microsoft.csv")
    # startFrom = len(stocks_data) - 60
    # # yesterday's feature
    # inputX_ystd = stocks_data.filter(['Adj Close'])[startFrom-1:len(stocks_data)-1].values
    # scaler = MinMaxScaler(feature_range = (0,1))
    # scaled_data_ystd = scaler.fit_transform(inputX_ystd)
    # scaled_data_ystd = np.reshape(scaled_data_ystd.T, (scaled_data_ystd.T.shape[0], scaled_data_ystd.T.shape[1], 1))
    # actual_today = scaler.fit_transform(stocks_data['Adj Close'].values.reshape(-1,1))[-1]
    # model.fit(scaled_data_ystd, actual_today)
    # model.save("dashboard/lstm_model/my_model.h5")
    # return HttpResponse('Retrained Successfully!')
    return redirect('dashboard')