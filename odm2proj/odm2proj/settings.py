"""
Django settings for odm2proj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@m%tdt80#zobogsf@iz27^6_^bmn1&&+hy2e*o&w-6nbdrp#i1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'odm2rest',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    #'VIEW_DESCRIPTION_FUNCTION': 'rest_framework_swagger.views.get_restructuredtext',
    #'DEFAULT_PARSER_CLASSES': (
    #    'rest_framework.parsers.JSONParser',
    #    'rest_framework.parsers.YAMLParser',
    #    'rest_framework.parsers.XMLParser',
    #),
    #'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'odm2rest.negotiation.IgnoreClientContentNegotiation',
    # specifying the renderers
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
        'rest_framework_yaml.renderers.YAMLRenderer',
        #'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    #'PAGINATE_BY': 10,                 # Default to 10
    #'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    #'MAX_PAGINATE_BY': 100             # Maximum limit allowed when using `?page_size=xxx`.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

ROOT_URLCONF = 'odm2proj.urls'

WSGI_APPLICATION = 'odm2proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
    "permission_denied_handler": None, # If user has no permisssion, raise 403 error
    "info": {
        # Configure some Swagger UI variables, for details see:
        # https://github.com/swagger-api/swagger-spec/blob/master/versions/1.2.md#513-info-object
        'title': 'ODM2 REST APIs',
        'contact': 'cyoun@sdsc.edu',
        #'description': 'This is the docementation server to test services. Since Swagger UI does not have any control over what is sent in the HTTP Accept header, REST framework can take ?accept=application/json style URL parameters, which allow the Accept header to be overridden.',
        'description': 'This is the docementation server to test services.',
        #'license': 'Apache 2.0',
        #'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        #'termsOfServiceUrl': 'http://helloreverb.com/terms/',
    },

    "produces": [
        "application/json",
        "text/csv"
        ],
    "consumes": [
        "application/json",
        "text/csv"
        ],

}
