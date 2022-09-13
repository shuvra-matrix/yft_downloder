from django.shortcuts import render, redirect
import os
from random import randint
import re
import requests
import geoip2.database
from .models import User_details
import os
from pathlib import Path
import urllib.request


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
            link = link.replace('https://www.youtube.com/watch?v=', '')
            link = link.replace('https://www.youtube.com/shorts/', '')
            link = link.replace('https://youtu.be/', '')
            link = link.replace('https://youtube.com/shorts/', '')
            link = link.split('?')[0]
            link = link.split('&')[0]

            url = "https://yt-api.p.rapidapi.com/dl"

            querystring = {"id": link}
            headers = {
                "X-RapidAPI-Key": "53db47703bmsh43337a6ff98140ep1d9019jsnfa4b3f6ce92b",
                "X-RapidAPI-Host": "yt-api.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            obj = response.json()

            title = obj['title']
            length = int(obj['lengthSeconds'])
            mins = int(length/60)
            sec = length - (60*mins)
            length = f'{mins}:{sec} Minutes'
            thumb = obj['thumbnail'][3]['url']
            url1 = None
            q1 = None
            size1 = None
            url2 = None
            q2 = None
            size2 = None
            try:
                url1 = obj['formats'][1]['url']
                q1 = obj['formats'][1]['qualityLabel']
                file = urllib.request.urlopen(
                    url1)
                size1 = round((file.length)/1000000)
            except:
                pass
            try:
                url2 = obj['formats'][2]['url']
                q2 = obj['formats'][2]['qualityLabel']
                file = urllib.request.urlopen(
                    url2)
                size2 = round((file.length)/1000000)
            except:
                pass
            

        except:
            mess = 'Server Error'
            my_dict = {
                'grddient': 'grddient',
                'color': 'ytclass',
                'mess': mess
            }

            return render(request, 'ydown.html', context=my_dict)

        my_dict = {
            'color': 'ytdown',
            'title': title,
            'length': length,
            'thumb': thumb,
            'url1': url1,
            'q1': q1,
            'size1': size1,
            'url2': url2,
            'q2': q2,
            'size2': size2,
          
        }
        ip = request.session.get('ip')
        address = request.session.get('address')
        insert_ip = User_details.objects.create(
            ip_add=ip, location=address, download_link=link, download_type='Youtube Videos')

        return render(request, 'ytdownload.html', context=my_dict)
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
            link = link.replace('https://www.youtube.com/watch?v=', '')
            link = link.replace('https://www.youtube.com/shorts/', '')
            link = link.replace('https://youtu.be/', '')
            link = link.replace('https://youtube.com/shorts/', '')
            link = link.split('?')[0]
            link = link.split('&')[0]

            url = "https://yt-api.p.rapidapi.com/dl"

            querystring = {"id": link}
            headers = {
                "X-RapidAPI-Key": "53db47703bmsh43337a6ff98140ep1d9019jsnfa4b3f6ce92b",
                "X-RapidAPI-Host": "yt-api.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            obj = response.json()

            title = obj['title']
            length = int(obj['lengthSeconds'])
            mins = int(length/60)
            sec = length - (60*mins)
            length = f'{mins}:{sec} Minutes'
            thumb = obj['thumbnail'][3]['url']
            urls = None
            size = None
            try:
                urls = obj['adaptiveFormats'][len(
                    obj['adaptiveFormats'])-1]['url']
                file = urllib.request.urlopen(
                    urls)
                size = round((file.length)/1000000)
            except:
                pass
            print(urls)
            mydict = {
                'color': 'ytmdowns',
                'title': title,
                'urls': urls,
                'thumb': thumb,
                'length': length,
                'size': size,
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
                        hd_size = round((file.length)/1000000)

                except:
                    pass

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
