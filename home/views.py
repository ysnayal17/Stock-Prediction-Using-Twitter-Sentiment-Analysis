from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Create your views here.
def home(request):
    # DEVELOPER_KEY = 'AIzaSyA3Fg-1Qaz3Ula4M2FTBOFoEMrcxCPB-rI'
    # YOUTUBE_API_SERVICE_NAME = 'youtube'
    # YOUTUBE_API_VERSION = 'v3'

    # youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    # developerKey=DEVELOPER_KEY)

    # # Call the search.list method to retrieve results matching the specified
    # # query term.
    # search_response = youtube.search().list(
    # q="stocks OR share OR investing",
    # part='id,snippet',
    # maxResults=3
    # ).execute()
    search_response = {'etag': 'ttOuhZ4yS1vKTezOOaSKIfO6sMo',
        'items': [{'etag': 'kcty-H1rE-WiSCK6MIHehafGfvY',
        'id': {'kind': 'youtube#video', 'videoId': 'ZCFkWDdmXG8'},
        'kind': 'youtube#searchResult',
        'snippet': {'channelId': 'UCWOA1ZGywLbqmigxE4Qlvuw',
            'channelTitle': 'Netflix',
            'description': 'In partnership with Vox Media Studios and Vox, this enlightening explainer series will take viewers deep inside a wide range of culturally relevant topics, ...',
            'liveBroadcastContent': 'none',
            'publishTime': '2020-04-17T13:00:02Z',
            'publishedAt': '2020-04-17T13:00:02Z',
            'thumbnails': {'default': {'height': 90,
            'url': 'https://i.ytimg.com/vi/ZCFkWDdmXG8/default.jpg',
            'width': 120},
            'high': {'height': 360,
            'url': 'https://i.ytimg.com/vi/ZCFkWDdmXG8/hqdefault.jpg',
            'width': 480},
            'medium': {'height': 180,
            'url': 'https://i.ytimg.com/vi/ZCFkWDdmXG8/mqdefault.jpg',
            'width': 320}},
            'title': 'Explained | The Stock Market | FULL EPISODE | Netflix'}},
        {'etag': '47Hqk0ZiKd-AJ52YzulwYLHQMik',
        'id': {'kind': 'youtube#video', 'videoId': 'p7HKvqRI_Bo'},
        'kind': 'youtube#searchResult',
        'snippet': {'channelId': 'UCsooa4yRKGN_zEE8iknghZA',
            'channelTitle': 'TED-Ed',
            'description': 'Download a free audiobook version of "The Richest Man in Babylon" and support TED-Ed\'s nonprofit mission: https://www.audible.com/ted-ed Check out our full ...',
            'liveBroadcastContent': 'none',
            'publishTime': '2019-04-29T15:01:41Z',
            'publishedAt': '2019-04-29T15:01:41Z',
            'thumbnails': {'default': {'height': 90,
            'url': 'https://i.ytimg.com/vi/p7HKvqRI_Bo/default.jpg',
            'width': 120},
            'high': {'height': 360,
            'url': 'https://i.ytimg.com/vi/p7HKvqRI_Bo/hqdefault.jpg',
            'width': 480},
            'medium': {'height': 180,
            'url': 'https://i.ytimg.com/vi/p7HKvqRI_Bo/mqdefault.jpg',
            'width': 320}},
            'title': 'How does the stock market work? - Oliver Elfenbaum'}}],
        'kind': 'youtube#searchListResponse',
        'nextPageToken': 'CAIQAA',
        'pageInfo': {'resultsPerPage': 2, 'totalResults': 1000000},
        'regionCode': 'US'}
    # print(search_response)
    context = {
        "tutorials": search_response
    }                                 
    return render(request, 'home/index1.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return render(request, 'home/index1.html')
        else:
            messages.error(request, "Wrong Credentials")
            return render(request, 'home/Login1.html')
    else: 
        return render(request, 'home/Login1.html')

def logout_user(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
        user.first_name = fname
        user.last_name = lname
        user.save()
        login(request, user)
        print('User created successfully!')
        messages.success(request, 'Successfully registered')
        return render(request, 'home/index1.html')

def dashboard(request):
    return HttpResponse('DashBoard')

