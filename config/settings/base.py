import os
from pathlib import Path

from decouple import config
import braintree

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = []

# Application definition
LOCAL_APPS = [
    'ecommerce.shop.apps.ShopConfig',
    'ecommerce.cart.apps.CartConfig',
    'ecommerce.orders.apps.OrdersConfig',
    'ecommerce.payment.apps.PaymentConfig',
    'ecommerce.coupons.apps.CouponsConfig',
    'ecommerce.common.apps.CommonConfig',
]
    
THIRD_PARTY_APPS = [
    'ckeditor',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    *LOCAL_APPS,
    # Third-Party apps
    *THIRD_PARTY_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates/')

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
                'ecommerce.cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'djangoecommerce',
        'USER': 'postgres',
        'PASSWORD': '12345678',
        'PORT': 5432,
        'HOST': 'localhost',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKeditor config
CKEDITOR_UPLOAD_PATH = 'media/uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}

# Cart session id
CART_SESSION_ID = 'cart'

# E-mail config
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Braintree settings
# A quiuck fix. It will be replaced with another payment systen.
BRAINTREE_MERCHANT_ID = config('MERCHANT_ID', default=1) # Merchant ID
BRAINTREE_PUBLIC_KEY = config('PUBLIC_KEY', default='1') # Public Key
BRAINTREE_PRIVATE_KEY = config('PRIVATE_KEY', default='1') # Private key

BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)
