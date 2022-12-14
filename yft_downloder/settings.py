"""
Django settings for yft_downloder project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!@assc!vx+b81aypnm!60r+7dylfa2fh=#d!!5)8p3r((2k5j('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ytf_app',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'yft_downloder.urls'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'yft_downloder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = STATIC_DIR
# STATICFILES_DIRS = [STATIC_DIR]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PWA_CONFIG = {
    # ...
    "name": "YTF Downloder",
    "short_name": "YTF Downloder",
    "theme_color": "#c12c11",
    "background_color": "#f85032",
    "display": "standalone",
    "orientation": "portrait",
    "scope": "/",
    "start_url": "/",
    "lang": "en",
    "dir": "ltr",
    "icons": [
        {
            "src": "/static/images/72x72.png",
            "type": "image/png",
            "sizes": "72x72"
        },
        {
            "src": "/static/images/96x96.png",
            "type": "image/png",
            "sizes": "96x96"
        },
        {
            "src": "/static/images/128x128.png",
            "type": "image/png",
            "sizes": "128x128"
        },
        {
            "src": "/static/images/144x144.png",
            "type": "image/png",
            "sizes": "144x144"
        },
        {
            "src": "/static/images/152x152.png",
            "type": "image/png",
            "sizes": "152x152"
        },
        {
            "src": "/static/images/192x192.png",
            "type": "image/png",
            "sizes": "192x192"
        },
        {
            "src": "/static/images/384x384.png",
            "type": "image/png",
            "sizes": "384x384"
        },
        {
            "src": "/static/images/512x512.png",
            "type": "image/png",
            "sizes": "512x512"
        }
    ],
    "description": "Download Videos and Music From Youtube, Facebook, Twitter",
    "version": "2",
    "manifest_version": "0.2",
    "permissions": [
        "notifications",
        "webRequest"
    ],
    "author": "Shuvra Chakrabarty"
    # ...
}


PWA_APP_DIR = 'ltr'

PWA_APP_LANG = 'en-US'

PWA_APP = """if ("serviceWorker" in navigator) {
	window.addEventListener("load", () => {
		navigator.serviceWorker
		.register("/sw.js")
		.then(res => console.log("service worker registered!"))
		.catch(err => console.log("Your browser support service worker but service worker not registered.", err));
	});
} else {
	console.log(`Your browser Dosn't Support serviceWorker, so you can'n install PWA.`);
};"""

PWA_SW = """const manifest = self.__WB_MANIFEST;
if (manifest) {
  // do nothing
}

// https://web.dev/offline-fallback-page/
const CACHE_NAME = 'offline-html';
const FALLBACK_HTML_URL = '/offline/';
self.addEventListener('install',  (event) => {
  event.waitUntil(
    // Setting {cache: 'reload'} in the new request will ensure that the
    // response isn't fulfilled from the HTTP cache; i.e., it will be from
    // the network.
    caches.open(CACHE_NAME)
      .then((cache) => cache.add(
        new Request(FALLBACK_HTML_URL, { cache: "reload" })
      ))
  );

  // Force the waiting service worker to become the active service worker.
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  // Tell the active service worker to take control of the page immediately.
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
      .catch(() => {
        return caches.match(FALLBACK_HTML_URL);
      })
  );
}); """
