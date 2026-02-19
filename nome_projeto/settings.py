from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-diaamz&_726*n0750gef!7#gj39lhud5efz3hzv9bvv*22r*58'

MEDIA_ROOT = BASE_DIR / 'media'   # pasta física
MEDIA_URL = '/media/'             # endereço web

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api_s',
    'rest_framework',
    'django_filters',
    'widget_tweaks',
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

ROOT_URLCONF = 'nome_projeto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nome_projeto.wsgi.application'




DATABASES = {
      'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'KeaBase',       
        'USER': 'postgres',     
        'PASSWORD': '051273', 
        'HOST': 'localhost',      
        'PORT': '5433',          
    }
}




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


# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'nome_projeto' / 'static',
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# MEDIDAS DE SEGURANÇA - As que estiverem comentadas, ative quando for para produção

# 1. Desligar debug
# DEBUG = False

# 2. Hosts permitidos
# ALLOWED_HOSTS = ['seusite.com', 'www.seusite.com']  # coloque seu domínio ou IP

# 3. Cookies seguros
# SESSION_COOKIE_SECURE = True      # envia apenas via HTTPS
# CSRF_COOKIE_SECURE = True         # envia apenas via HTTPS
# SESSION_COOKIE_HTTPONLY = True    # impede acesso via JS
# CSRF_COOKIE_HTTPONLY = False      # deve ser False para funcionar com forms

# 4. Proteções contra ataques de navegador
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

# 5. Redirecionar todas as requisições HTTP para HTTPS
# SECURE_SSL_REDIRECT = True

# 6. HSTS (HTTP Strict Transport Security)
# SECURE_HSTS_SECONDS = 3600       # ajuste para produção
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# 7. CSRF e sessões
# CSRF_TRUSTED_ORIGINS = ['https://seusite.com']  # domínios de confiança