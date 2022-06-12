import dj_database_url
import os
from pathlib import Path

'''
#version:3.1.1
from environs import Env
env=Env()
env.read_env() # read .env file, if it exists
'''


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = '#3v6h1vd4g0@2$2%1yr*r_7udp75+%lzl7dn+qhm)@*78w*td+'

DEBUG = True

ALLOWED_HOSTS = ['dimensional-illusions.herokuapp.com','ec2-13-126-12-146.ap-south-1.compute.amazonaws.com','dimensionalillusions.com','www.dimensionalillusions.com' ,'127.0.0.1',]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CUSTOM  APPS
    'Ehub.apps.EhubConfig',
    'Eblog.apps.EblogConfig',

    # 'Edashboard.apps.EdashboardConfig',
    'Mvfx.apps.MvfxConfig',
    'Msfx.apps.MsfxConfig',
    'Mgraphics.apps.MgraphicsConfig',
    'Mweb.apps.MwebConfig',

    'mptt',
    'ckeditor',
    'taggit',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Dimensionalillusions.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), ],
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


WSGI_APPLICATION = 'Dimensionalillusions.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dimensionalillusions',  
        'USER': 'postgres',    
        'PASSWORD': 'ProgrammerSam123',  
        'HOST': 'database-1.csolgo685quk.ap-south-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}



'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DimensionalIllusionV1',  
        'USER': 'postgres',    
        'PASSWORD': 'ProgrammerGodRobo123',  
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

'''


'''
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)
'''


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_L10N = True
USE_TZ = False


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# meaning- static url is /static/ which is a relative path and appears in url section .we dont need to mention statiic path in codes(links)
STATIC_URL = '/staticfiles/'

# MUST FOR LOADIN STATIC FILES
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# WHITENOISE CONFIGURATION FOR SERVING STATIC FILES ONLY.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# FOR SAVING IMAGES INTO THE 'static/images'
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles/mediafiles')
MEDIA_URL = '/mediafiles/'


# SMTP CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# THIS IS YOUR LOGIN INFO FOR GMAIL ADDRESS
EMAIL_HOST_USER = 'dimensionalassistanceteam37@gmail.com'
EMAIL_HOST_PASSWORD = '123@gmailcom'
