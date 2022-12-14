from django.shortcuts import render, redirect, HttpResponse
import os
from random import randint
import re
import requests
import geoip2.database
from .models import User_details
import os
from pathlib import Path
import urllib.request


def short_link(link):
    link = link.replace('https://www.youtube.com/watch?v=', '')
    link = link.replace('https://www.youtube.com/shorts/', '')
    link = link.replace('https://youtu.be/', '')
    link = link.replace('https://youtube.com/shorts/', '')
    link = link.split('?')[0]
    link = link.split('&')[0]
    return link


def create_db(request, links, type):
    ip = request.session.get('ip')
    address = request.session.get('address')
    insert_ip = User_details.objects.create(
        ip_add=ip, location=address, download_link=links, download_type=type)


def warning_message(request, mess, to, bg):
    my_dict = {
        'grddient': 'grddient',
        'color': bg,
        'mess': mess,
    }
    return render(request, to, context=my_dict)


def get_size(urls):
    file = urllib.request.urlopen(
        urls)
    size = round((file.length)/1000000)
    return size


def validate_yt_link(link):
    x = re.match(
        r'^(https:|)[/][/]www.([^/]+[.])*youtube.com', link)
    y = re.match(r'^(https:|)[/][/]([^/]+[.])*youtu.be', link)
    z = re.match(
        r'^(https:|)[/][/]([^/]+[.])*youtube.com', link)

    return (x, y, z)


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
        x, y, z = validate_yt_link(link)
        if y == None and x == None and z == None:
            return warning_message(request, mess='Please Enter Valid Youtube Link', to='ydown.html', bg='ytclass')

        try:
            link = short_link(link)
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
            thumb = obj['thumbnail'][-1]['url']
            url1 = q1 = size1 = url2 = q2 = size2 = None
            try:
                url1 = obj['formats'][1]['url']
                q1 = obj['formats'][1]['qualityLabel']
                size1 = get_size(url1)
            except:
                pass
            try:
                url2 = obj['formats'][2]['url']
                q2 = obj['formats'][2]['qualityLabel']
                size2 = get_size(url2)
            except:
                pass

        except:
            return warning_message(request, mess='Server Error', to='ydown.html', bg='ytclass')

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
        create_db(request, links=link, type='Youtube Videos')

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
        x, y, z = validate_yt_link(link)
        if y == None and x == None and z == None:
            return warning_message(request, mess='Please Enter Valid Youtube Link', to='ytmusic.html', bg='yt_body')

        try:
            link = short_link(link)

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
            urls = size = None
            try:
                urls = obj['adaptiveFormats'][len(
                    obj['adaptiveFormats'])-1]['url']
                size = get_size(urls)
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
            create_db(request, links=link, type='Youtube Music')
        except:
            return warning_message(request, mess='Server Error', to='ytmusic.html', bg='yt_body')

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
            return warning_message(request, mess='Please Enter Valid Facebook Link', to='fbsearch.html', bg='fb_body')

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
                sd_link = sd_size = hd_link = hd_size = None
                try:
                    sd_link = a['formats'][2]['url']
                    sd_size = get_size(sd_link)
                except:
                    pass
                try:
                    hd = a['formats'][3]['format_id']
                    if hd == 'hd':
                        hd_link = a['formats'][3]['url']
                        hd_size = get_size(hd_link)
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

                create_db(request, links=PRODUCT_URL, type='Facebook Videos')

                return render(request, 'fbselect.html', context=my_dict)
            except:
                return warning_message(request, mess='Server Error', to='fbsearch.html', bg='fb_body')

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
            return warning_message(request, mess='Please Enter Valid Twitter Link', to='twisearch.html', bg='twi_body')

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
            title = obj['meta']['title']
            urls_2 = quality_2 = urls_3 = quality_3 = size_2 = size_3 = None
            try:
                urls_1 = obj['urls'][0]['url']
                quality_1 = obj['urls'][0]['quality']
                size_1 = get_size(urls_1)
            except:
                pass
            try:
                urls_2 = obj['urls'][1]['url']
                quality_2 = obj['urls'][1]['quality']
                size_2 = get_size(urls_2)

            except:
                pass
            try:
                urls_3 = obj['urls'][2]['url']
                quality_3 = obj['urls'][2]['quality']
                size_3 = get_size(urls_3)

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
            create_db(request, links=link, type='Twitter Videos')
            return render(request, 'twitterselect.html', context=my_dict)
        except:
            return warning_message(request, mess='Server Error', to='twisearch.html', bg='twi_body')

    my_dict = {
        'color': 'twi_body'
    }
    return render(request, 'twisearch.html', context=my_dict)


def insta_search(request):
    if request.session.has_key('ip'):
        pass
    else:
        return redirect('/')

    if request.method == 'POST':
        link = request.POST.get('link')
        x = re.match(
            r'^(https:|)[/][/]www.([^/]+[.])*instagram.com', link)
        if x == None:
            return warning_message(request, mess='Please Enter Valid Instagram Link', to='instasearch.html', bg='insta_body')

        try:
            import requests

            url = "https://instagram-story-downloader-media-downloader.p.rapidapi.com/index"

            querystring = {
                "url": link}

            headers = {
                "X-RapidAPI-Key": "53db47703bmsh43337a6ff98140ep1d9019jsnfa4b3f6ce92b",
                "X-RapidAPI-Host": "instagram-story-downloader-media-downloader.p.rapidapi.com"
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)

            obj = response.json()

            media_link = obj['media']

            my_dict = {
                'color': 'insta_down',
                'link': media_link,
            }
            create_db(request, links=link, type='Instagram Videos')
            return render(request, 'instasearch.html', context=my_dict)

        except:
            return warning_message(request, mess='Server Error', to='instasearch.html', bg='insta_body')

    my_dict = {
        'color': 'insta_body',
    }
    return render(request, 'instasearch.html', context=my_dict)


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
