from django.shortcuts import render, redirect
from pytube import YouTube
import os
import glob
from random import randint
import cloudinary
import cloudinary.uploader
import cloudinary.api
import re
import wget
from bs4 import BeautifulSoup
import requests
import lxml
import socket
import geoip2.database
from .models import User_details
import os
from pathlib import Path


def cloud_upload(dc, fileid):
    cloudinary.config(
        cloud_name="dqone7ala",
        api_key="412496529895946",
        api_secret="2siKsON-MfBmh9o0pIPVd31z-Ww",


    )

    upload_result = cloudinary.uploader.upload_large(
        dc,  resource_type="video", public_id=fileid)

    files = os.path.basename(dc)
    url = upload_result['url']
    dir = 'media'

    urls = f'media\\{files}'
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
        if f == urls:
            os.remove(f)
    return url


def index(request):
    ip = ''
    address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    request.session['ip'] = ip
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent

        FILE_DIR = os.path.join(BASE_DIR, 'GeoLite2-City.mmdb')
        reader = geoip2.database.Reader(FILE_DIR)
        response = reader.city(ip)
        country = response.country.name
        state = response.subdivisions.most_specific.name
        city = response.city.name
        pin = response.postal.code
        lat = response.location.latitude
        lon = response.location.longitude
        address = f'{city},{state},{country},{pin},{lat},{lon}'
        request.session['address'] = address
    except:
        pass
    my_dict = {
        'color': 'bodyclass',
    }
    return render(request, 'index.html', context=my_dict)


def ydown(request):
    my_dict = {
        'color': 'ytclass',
    }

    return render(request, 'ydown.html', context=my_dict)


def ytdownload(request):
    if request.method == 'POST':
        quality_list = []
        size_list = []
        link = request.POST.get('link')
        x = re.match(
            r'^(https:|)[/][/]www.([^/]+[.])*youtube.com', link)
        y = re.match(r'^(https:|)[/][/]([^/]+[.])*youtu.be', link)
        z = re.match(
            r'^(https:|)[/][/]([^/]+[.])*youtube.com', link)
        if y == None and x == None and z == None:
            mess = 'Please Enter Valid Youtube Link'
            my_dict = {
                'color': 'ytclass',
                'mess': mess
            }

            return render(request, 'ydown.html', context=my_dict)

        try:
            yt = YouTube(link)
            title = yt.title
            length = yt.length
            mins = int(length/60)
            sec = length - (60*mins)
            length = f'{mins}:{sec} Minutes'
            thumb = yt.thumbnail_url

        except:
            mess = 'Server Error'
            my_dict = {
                'color': 'ytclass',
                'mess': mess
            }

            return render(request, 'ydown.html', context=my_dict)

        try:

            s1 = round((yt.streams.get_by_resolution('360p').filesize)/1000000)
            if s1 < 100:
                size_list.append(s1)
                quality_list.append('360p')

        except:
            pass
        try:
            s2 = round((yt.streams.get_by_resolution('720p').filesize)/1000000)
            if s2 < 100:
                size_list.append(s2)
                quality_list.append('720p')
        except:
            pass

        if len(quality_list) == 0:
            mess = 'File Size Is Too Large'
            my_dict = {
                'color': 'ytclass',
                'mess': mess
            }

            return render(request, 'ydown.html', context=my_dict)

        my_dict = {
            'qlist': quality_list,
            'llist': link,
            'color': 'ytdown',
            'title': title,
            'length': length,
            'thumb': thumb,
            'size': size_list,
        }
        ip = request.session.get('ip')
        address = request.session.get('address')
        insert_ip = User_details.objects.create(
            ip_add=ip, location=address, download_link=link, download_type='Youtube Videos')

        return render(request, 'ytdownload.html', context=my_dict)
    return redirect('/')


def yvdown(request):
    if request.method == 'POST':
        SAVE_PATH = "./media"
        dc = None
        title = request.POST.get('title')
        link = request.POST.get('link')
        reg = request.POST.get('reg')

        thumb = request.POST.get('thumb')
        try:
            yt = YouTube(link)
            links = yt.streams.filter(res=reg, progressive=True).first()
            rand = randint(1, 8909)
            filename = f'video{rand}.mp4'
            fileid = f'video{rand}'
            dc = links.download(SAVE_PATH, filename=filename)

            url = cloud_upload(dc, fileid)

        except:
            mess = 'Server Error'
            my_dict = {
                'color': 'ytclass',
                'mess': mess
            }

            return render(request, 'ydown.html', context=my_dict)

        mydict = {

            'color': 'ytdowns',
            'title': title,
            'url': url,
            'thumb': thumb,
            'reg': reg,
        }
        return render(request, 'ytdownpage.html', context=mydict)
    return redirect('/')


def ytmusic(request):
    my_dict = {
        'color': 'yt_body',
    }
    return render(request, 'ytmusic.html', context=my_dict)


def ytmsearch(request):
    if request.method == 'POST':
        SAVE_PATH = "./media"
        dc = None
        link = request.POST.get('link')
        x = re.match(
            r'^(https:|)[/][/]www.([^/]+[.])*youtube.com', link)
        y = re.match(r'^(https:|)[/][/]([^/]+[.])*youtu.be', link)
        z = re.match(
            r'^(https:|)[/][/]([^/]+[.])*youtube.com', link)
        if y == None and x == None and z == None:
            mess = 'Please Enter Valid Youtube Link'
            my_dict = {
                'color': 'yt_body',
                'mess': mess
            }

            return render(request, 'ytmusic.html', context=my_dict)
        try:
            yt = YouTube(link)
            title = yt.title
            length = yt.length
            mins = int(length/60)
            sec = length - (60*mins)
            length = f'{mins}:{sec} Minutes'
            thumb = yt.thumbnail_url
            music_list = yt.streams.filter(
                only_audio=True, abr='128kbps').first()
            music_size = round((yt.streams.filter(
                only_audio=True, abr='128kbps').first().filesize)/1000000)
            if music_size > 100:
                mess = 'FILE SIZE IS TOO LARGE'
                my_dict = {
                    'color': 'yt_body',
                    'mess': mess
                }

                return render(request, 'ytmusic.html', context=my_dict)
            rand = randint(1, 8909)
            filename = f'audio{rand}.mp3'
            fileid = f'audio{rand}'
            dc = music_list.download(SAVE_PATH, filename=filename)
            url = cloud_upload(dc, filename)

            mydict = {
                'color': 'ytmdowns',
                'title': title,
                'url': url,
                'thumb': thumb,
                'size': music_size,
                'length': length,
            }
            ip = request.session.get('ip')
            address = request.session.get('address')
            insert_ip = User_details.objects.create(
                ip_add=ip, location=address, download_link=link, download_type='Youtube Music')
        except:
            mess = 'Server Error'
            my_dict = {
                'color': 'yt_body',
                'mess': mess
            }

            return render(request, 'ytmusic.html', context=my_dict)

        return render(request, 'ytmdownload.html', context=mydict)
    return redirect('/ytmusic')


def fbsearch(request):

    my_dict = {
        'color': 'fb_body',


    }

    if request.method == 'POST':
        SAVE_PATH = "./media"
        PRODUCT_URL = request.POST.get('link')
        x = re.match(
            r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', PRODUCT_URL)
        y = re.match(r'^(https:|)[/][/]www.([^/]+[.])*fb.watch', PRODUCT_URL)
        z = re.match(r'^(https:|)[/][/]*fb.watch', PRODUCT_URL)
        w = re.match(
            r'^(https:|)[/][/]m.([^/]+[.])*facebook.com', PRODUCT_URL)
        print(z)
        if x == None and y == None and z == None:
            mess = 'Please Enter Valid Facebook Link'
            my_dict = {
                'color': 'fb_body',
                'mess': mess
            }

        else:
            try:
                header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48",
                          'Accept-Language': "en-US,en;q=0.9"}
                req = requests.get(PRODUCT_URL)
                supe = BeautifulSoup(req.text, 'lxml')
                desc = supe.find(
                    'meta', property="og:video:url").attrs['content']

                filename = wget.download(desc, SAVE_PATH)

                newfilename = filename.replace('./media/', '')

                rand = randint(1, 8909)
                fileid = f'video{rand}'
                url = cloud_upload(filename, fileid)
                my_dict = {
                    'color': 'fb_body',

                    'url': url
                }
                ip = request.session.get('ip')
                address = request.session.get('address')
                insert_ip = User_details.objects.create(
                    ip_add=ip, location=address, download_link=PRODUCT_URL, download_type='Facebook Videos')

                return render(request, 'fbsearch.html', context=my_dict)
            except:
                mess = 'Server Error'
                my_dict = {
                    'color': 'fb_body',
                    'mess': mess
                }

                return render(request, 'fbsearch.html', context=my_dict)

            return render(request, 'fbsearch.html', context=my_dict)

    return render(request, 'fbsearch.html', context=my_dict)


def twisearch(request):
    my_dict = {
        'color': 'twi_body'
    }
    return render(request, 'twisearch.html', context=my_dict)


def admins(request):
    user_detais = User_details.objects.all()
    my_dict = {
        'color': 'bodyclass',
        'user': user_detais,
    }
    return render(request, 'admins.html', context=my_dict)
