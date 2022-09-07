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
import requests
import geoip2.database
from .models import User_details
import os
from pathlib import Path
import urllib.request


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
            print("hi")
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
                'grddient': 'grddient',
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
                'grddient': 'grddient',
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
                'grddient': 'grddient',
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
                'grddient': 'grddient',
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
                'grddient': 'grddient',
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
                    'grddient': 'grddient',
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
                'grddient': 'grddient',
                'color': 'yt_body',
                'mess': mess
            }

            return render(request, 'ytmusic.html', context=my_dict)

        return render(request, 'ytmdownload.html', context=mydict)
    return redirect('/ytmusic')


def fbsearch(request):
    PRODUCT_URL = ''
    my_dict = {
        'color': 'fb_body',


    }

    if request.method == 'POST':
        PRODUCT_URL = request.POST.get('link')
        x = re.match(
            r'^(https:|)[/][/]www.([^/]+[.])*facebook.com', PRODUCT_URL)
        y = re.match(r'^(https:|)[/][/]www.([^/]+[.])*fb.watch', PRODUCT_URL)
        z = re.match(r'^(https:|)[/][/]*fb.watch', PRODUCT_URL)
        w = re.match(
            r'^(https:|)[/][/]m.([^/]+[.])*facebook.com', PRODUCT_URL)

        if x == None and y == None and z == None and w == None:
            mess = 'Please Enter Valid Facebook Link'
            my_dict = {
                'grddient': 'grddient',
                'color': 'fb_body',
                'mess': mess
            }

        else:
            # try:
            url = "https://fb-dl.p.rapidapi.com/"

            querystring = {
                "url": PRODUCT_URL}

            headers = {
                "X-RapidAPI-Key": "a1408669c6msh81873aaa94d74b0p1575dfjsn0bf62c16c6fa",
                "X-RapidAPI-Host": "fb-dl.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            a = response.text.split(',')
            sd_link = a[0].replace('{"sd":', "")
            sd_link = sd_link.replace('"', "")
            hd_link = None
            hd_size = None
            # try:
            file = urllib.request.urlopen(
                sd_link)
            sd_size = round((file.length)/1000000)

            # except:
            #     pass
            try:
                hd_link = a[1].replace('"hd":', "")
                hd_link = hd_link.replace('"', "")

                file = urllib.request.urlopen(
                    hd_link)
                hd_size = round((file.length)/1000000)
            except:
                pass

            if sd_size > 100 and hd_size > 100:
                mess = 'File Size Is Too Large'
                my_dict = {
                    'grddient': 'grddient',
                    'color': 'fb_body',
                    'mess': mess
                }

                return render(request, 'fbsearch.html', context=my_dict)

            thumb = a[-1].replace('"thumbnail":', "")

            thumb = thumb.replace('}', "")
            thumb = thumb.replace('"', "")

            title = a[2].replace('"title":', "")
            title = title.replace('"', "")

            my_dict = {
                'color': 'fb_body',

                'sd_url': sd_link,
                'sd_size': sd_size,
                'hd_link': hd_link,
                'hd_size': hd_size,
                'title': title,
                'thumb': thumb,
            }
            ip = request.session.get('ip')
            address = request.session.get('address')
            insert_ip = User_details.objects.create(
                ip_add=ip, location=address, download_link=PRODUCT_URL, download_type='Facebook Videos')

            return render(request, 'fbselect.html', context=my_dict)
            # except:
            #     mess = 'Server Error'
            #     my_dict = {
            #         'grddient': 'grddient',
            #         'color': 'fb_body',
            #         'mess': mess
            #     }

            #     return render(request, 'fbsearch.html', context=my_dict)

            # return render(request, 'fbsearch.html', context=my_dict)

    return render(request, 'fbsearch.html', context=my_dict)


def fbdown(request):
    link = ''
    if request.method == 'POST':
        BASE_DIR = Path(__file__).resolve().parent.parent
        SAVE_PATH = os.path.join(BASE_DIR, 'media')
        title = request.POST.get('title')
        thumb = request.POST.get('thumb')
        size = request.POST.get('size')
        link = request.POST.get('link')
        try:
            filename = wget.download(link, SAVE_PATH)
            newfilename = filename.replace('./media/', '')
            rand = randint(1, 8909)
            fileid = f'video{rand}'
            url = cloud_upload(filename, fileid)
            my_dict = {
                'color': 'fb_body',
                'url': url,
                'title': title,
                'thumb': thumb,
                'size': size,
            }
            return render(request, 'fbdown.html', context=my_dict)
        except:
            mess = 'Server Error'
            my_dict = {
                'grddient': 'grddient',
                'color': 'fb_body',
                'mess': mess
            }

            return render(request, 'fbsearch.html', context=my_dict)

    return redirect('/fbsearch')


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
