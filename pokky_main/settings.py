"""
Django settings for pokky_main project.
Updated for Render Deployment.
"""
from pathlib import Path
import os
import dj_database_url  # Render Database ke liye
from decouple import config # .env file read karne ke liye

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
# SECRET_KEY Render ke environment variable se aayega, warna default use karega
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key-check-env')

# DEBUG: Render par False hona chahiye, Local par True
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*'] # Sabhi domains allow karein (Render/Hostinger ke liye)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store', # AAPKA T-SHIRT APP
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- NEW: CSS dikhane ke liye zaroori
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pokky_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # TEMPLATES FOLDER LINK
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

WSGI_APPLICATION = 'pokky_main.wsgi.application'

# --- DATABASE CONFIGURATION (SMART SWITCH) ---
# Agar Render par hai to 'DATABASE_URL' milega, warna local SQLite use karega.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES (CSS, JS, IMAGES) ---
STATIC_URL = 'static/'

# Render ke liye Static Root set karna zaroori hai (Jahan collectstatic file jama karega)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Local development ke liye folders
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Production Storage (WhiteNoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files (Product Images ke liye)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# --- RENDER SPECIFIC SETTINGS ---
# Isse Login/Order form me 'CSRF Failed' ka error nahi aayega
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',  # Render ke sabhi domains ko trust karega
    'https://pokky-store.onrender.com' # Aapka specific URL (Baad me change kar sakte hain)
]