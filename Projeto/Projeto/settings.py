"""
Django settings for Projeto project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3vxq2c8_&+l!@t%b$g4yea4$e&8gp(bkd#shmj%e!ihm21dk-4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

PASSWORD_RESET_TIMEOUT = 300

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap4',
    'SAFERapp',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'SAFERapp.CustomUser'

LOGIN_URL = '/'

MEDIA_URL = '/media/'  # URL base para acessar os arquivos de mídia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Diretório onde os arquivos de mídia serão salvos

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

]

ROOT_URLCONF = 'Projeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Aqui, o Django procura na pasta templates
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

WSGI_APPLICATION = 'Projeto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# SQlite DB
#DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': BASE_DIR / 'db.sqlite3',
#      }
#  }

# ## Mysql DB
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': os.getenv('DB_NAME', 'safer_db'),
#        'USER': os.getenv('DB_USER', 'safer_user'),
#        'PASSWORD': os.getenv('DB_PASSWORD', 'safer_pass'),
#        'HOST': os.getenv('DB_HOST', 'db'),  # Nome do serviço do MySQL no docker-compose
#        'PORT': os.getenv('DB_PORT', '3306'),
#    }
# }
## MS SQL DB
DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'safer-db',
            'USER': 'safer-admin@safer-server',
            'PASSWORD': '$af&r2o25',
            'HOST': 'safer-server.database.windows.net',

            'OPTIONS': {
                'driver': 'ODBC Driver 18 for SQL Server',
            },
        },
    }
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# configuração de email

# backend no caso de só imprimir email no console sem enviar
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Backend padrão (com console)
#EMAIL_HOST = 'smtp.example.com'  # Servidor SMTP

# No caso de querer salvar o conteúdo em arquivo
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = '/tmp/emails'  # Certifique-se de que este diretório existe


#EMAIL_PORT = 587  # Porta do servidor SMTP
#EMAIL_USE_TLS = True  # Habilitar TLS (ou use EMAIL_USE_SSL para SSL)
#EMAIL_HOST_USER = 'seu-email@example.com'  # Usuário do email
#EMAIL_HOST_PASSWORD = 'sua-senha'  # Senha do email
#DEFAULT_FROM_EMAIL = 'seu-email@example.com'  # Email padrão para envio
