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
    print('---------------My Files----------------', url)
    for f in filelist:
        print('---------------------Search File ------------------- >', f)
        if f == urls:
            os.remove(f)
            print('-------------Delete File----------')
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
    if request.session.has_key('ip'):
        pass
    else:
        return redirect('/')

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
    if request.session.has_key('ip'):
        pass
    else:
        return redirect('/')

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

    if request.session.has_key('ip'):
        pass
    else:
        return redirect('/')

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
            try:
                url = "https://aiov-download-youtube-videos.p.rapidapi.com/GetVideoDetails"

                querystring = {
                    "URL": PRODUCT_URL}

                headers = {
                    "X-RapidAPI-Key": "53db47703bmsh43337a6ff98140ep1d9019jsnfa4b3f6ce92b",
                    "X-RapidAPI-Host": "aiov-download-youtube-videos.p.rapidapi.com"
                }

                response = requests.request(
                    "GET", url, headers=headers, params=querystring)

                a = response.json()

                duration = a['duration_string']
                thumb = a['thumbnail']
                title = a['title']
                sd_link = None
                sd_size = None
                hd_link = None
                hd_size = None
                try:
                    sd_link = a['formats'][2]['url']
                    file = urllib.request.urlopen(
                        sd_link)
                    sd_size = round((file.length)/1000000)

                except:
                    pass
                try:
                    hd = a['formats'][3]['format_id']
                    if hd == 'hd':
                        hd_link = a['formats'][3]['url']

                        file = urllib.request.urlopen(
                            hd_link)
                        size = round((file.length)/1000000)
                        if size < 100:
                            hd_size = size
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

                my_dict = {
                    'color': 'fb_body',

                    'sd_url': sd_link,
                    'sd_size': sd_size,
                    'hd_link': hd_link,
                    'hd_size': hd_size,
                    'title': title,
                    'thumb': thumb,
                    'duration': duration,
                }
                ip = request.session.get('ip')
                address = request.session.get('address')
                insert_ip = User_details.objects.create(
                    ip_add=ip, location=address, download_link=PRODUCT_URL, download_type='Facebook Videos')

                return render(request, 'fbselect.html', context=my_dict)
            except:
                mess = 'Server Error'
                my_dict = {
                    'grddient': 'grddient',
                    'color': 'fb_body',
                    'mess': mess
                }

                return render(request, 'fbsearch.html', context=my_dict)

            return render(request, 'fbsearch.html', context=my_dict)

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
    if request.session.has_key('ip'):
        pass
    else:
        return redirect('/')

    if request.method == 'POST':
        link = request.POST.get('link')
        x = re.match(
            r'^(https:|)[/][/]twitter.com', link)
        if x == None:
            mess = 'Please Enter Valid Twitter Link'
            my_dict = {
                'grddient': 'grddient',
                'color': 'fb_body',
                'mess': mess
            }
            return render(request, 'twisearch.html', context=my_dict)

        url = "https://twitter65.p.rapidapi.com/api/twitter/links"

        payload = {
            "url": link}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "53db47703bmsh43337a6ff98140ep1d9019jsnfa4b3f6ce92b",
            "X-RapidAPI-Host": "twitter65.p.rapidapi.com"
        }

        try:

            response = requests.request(
                "POST", url, json=payload, headers=headers)
            obj = response.json()[0]
            thumb = obj['pictureUrl']
            print(thumb)
            title = obj['meta']['title']
            urls_2 = None
            quality_2 = None
            urls_3 = None
            quality_3 = None
            size_2 = None
            size_3 = None
            try:
                urls_1 = obj['urls'][0]['url']
                quality_1 = obj['urls'][0]['quality']
                file = urllib.request.urlopen(
                    urls_1)
                size_1 = round((file.length)/1000000)
            except:
                pass
            try:
                urls_2 = obj['urls'][1]['url']
                quality_2 = obj['urls'][1]['quality']
                file = urllib.request.urlopen(
                    urls_2)
                size_2 = round((file.length)/1000000)
            except:
                pass
            try:
                urls_3 = obj['urls'][2]['url']
                quality_3 = obj['urls'][2]['quality']
                file = urllib.request.urlopen(
                    urls_3)
                size_3 = round((file.length)/1000000)
            except:
                pass
            my_dict = {
                'color': 'twi_body',
                'title': title,
                'thumb': thumb,
                'url1': urls_1,
                'quality1': quality_1,
                'url2': urls_2,
                'quality2': quality_2,
                'url3': urls_3,
                'quality3': quality_3,
                'size1': size_1,
                'size2': size_2,
                'size3': size_3,


            }
            ip = request.session.get('ip')
            address = request.session.get('address')
            insert_ip = User_details.objects.create(
                ip_add=ip, location=address, download_link=link, download_type='Twitter Videos')
            return render(request, 'twitterselect.html', context=my_dict)
        except:
            mess = 'Server Error'
            my_dict = {
                'grddient': 'grddient',
                'color': 'twi_body',
                'mess': mess
            }

            return render(request, 'twisearch.html', context=my_dict)

    my_dict = {
        'color': 'twi_body'
    }
    return render(request, 'twisearch.html', context=my_dict)


def twitterdown(request):
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
                'color': 'twi_body',
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
                'color': 'twi_body',
                'mess': mess
            }

            return render(request, 'twisearch.html', context=my_dict)

    return redirect('/')


def admins(request):
    if request.session.has_key('ip'):
        pass
    else:
        return redirect('/')

    user_detais = User_details.objects.all()
    my_dict = {
        'color': 'bodyclass',
        'user': user_detais,
    }
    return render(request, 'admins.html', context=my_dict)
