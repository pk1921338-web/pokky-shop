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

# --- CUSTOM AUTHENTICATION (Login with Email/Phone) ---
AUTHENTICATION_BACKENDS = [
    'store.backends.EmailPhoneBackend',  # Hamara naya code pehle chalega
    'django.contrib.auth.backends.ModelBackend', # Default wala backup ke liye
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

# --- DATABASE CONFIGURATION (Smart Fix) ---
# Ye check karega ki kya hum Render par hain?
if 'DATABASE_URL' in os.environ:
    # RENDER / NEON DB (PostgreSQL) - Yahan SSL zaroori hai
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    # LOCAL LAPTOP (SQLite) - Yahan SSL nahi chahiye
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
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

# --- LIFETIME LOGIN SETTINGS ---
# User tab tak login rahega jab tak wo khud Logout nahi dabata
SESSION_COOKIE_AGE = 31536000 * 20  # 20 Saal (Seconds mein)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False # Browser band karne par bhi logout nahi hoga
SESSION_SAVE_EVERY_REQUEST = True # Har click par session renew hoga

# --- SECURITY & RENDER SETTINGS ---

# 1. Isme 'https://' hona zaroori hai
CSRF_TRUSTED_ORIGINS = [
    'https://pokky-shop.onrender.com',  # Aapki exact site URL
    'https://*.onrender.com',           # Render ke liye wildcard
]

# 2. Render Proxy Fix (Ye line bahut zaroori hai)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 3. Cookie Settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True