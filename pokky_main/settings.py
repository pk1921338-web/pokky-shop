from pathlib import Path
import os
import dj_database_url  # Database connection ke liye
from decouple import config # Environment variables padhne ke liye

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY SETTINGS ---
# SECRET_KEY Render ke environment variable se aayega, warna local default use karega
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key-check-env')

# DEBUG: Render par False hona chahiye (Environment variable se set hoga)
DEBUG = config('DEBUG', default=True, cast=bool)

# Allowed Hosts: Render aur sabhi domains ke liye allow kiya hai
ALLOWED_HOSTS = ['*']

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store', # AAPKA MAIN APP
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- CSS/Images ke liye ZAROORI (Render par)
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Templates folder ka path
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

# --- DATABASE CONFIGURATION (NEON DB / POSTGRESQL FIX) ---
# Ye sabse important part hai. Ye check karega:
# 1. Agar Render par DATABASE_URL hai (Neon DB), to use connect karega.
# 2. Agar Laptop par hai, to SQLite use karega.
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,  # <--- NEON DB ke liye ye ZAROORI hai
    )
}

# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata' # India ka time zone set kiya hai (Optional)
USE_I18N = True
USE_TZ = True

# --- STATIC FILES (CSS, JavaScript, Images) ---
STATIC_URL = 'static/'

# Render ke liye Static Root (Jahan file jama hongi)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Local development ke liye folder
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# WhiteNoise Storage (Compression ke liye taaki site fast chale)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- MEDIA FILES (Product Images) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- RENDER & SECURITY SETTINGS ---
# CSRF Error hatane ke liye
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com', # Render ke sabhi subdomains allow karega
    'https://pokky-shop.onrender.com',
]

# --- LIFETIME LOGIN SETTINGS ---
# User tab tak login rahega jab tak wo khud Logout nahi dabata
SESSION_COOKIE_AGE = 31536000 * 20  # 20 Saal (Seconds mein)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False # Browser band karne par bhi logout nahi hoga
SESSION_SAVE_EVERY_REQUEST = True # Har click par session renew hoga