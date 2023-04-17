import  os
# carga las variables de entorno desde el archivo .env
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# accede a las variables de entorno
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')

DB_NAME_FUENTES_INFO = os.getenv('DB_NAME_FUENTES_INFO')
DB_USER_FUENTES_INFO = os.getenv('DB_USER_FUENTES_INFO')
DB_PASSWORD_FUENTES_INFO = os.getenv('DB_PASSWORD_FUENTES_INFO')
DB_HOST_FUENTES_INFO = os.getenv('DB_HOST_FUENTES_INFO')



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '3306',
    },
    'ecosistema': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME_FUENTES_INFO,
        'USER': DB_USER_FUENTES_INFO,
        'PASSWORD': DB_PASSWORD_FUENTES_INFO,
        'HOST': DB_HOST_FUENTES_INFO,
        'PORT': '3306',
    },
}


# class MyRouter:
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'back':
#             return 'default'
#         return 'ecosistema'

#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'back':
#             return 'default'
#         return 'ecosistema'

#     def allow_relation(self, obj1, obj2, **hints):
#         if obj1._meta.app_label == 'back' or \
#            obj2._meta.app_label == 'back':
#            return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label == 'back':
#             return db == 'default'
#         return db == 'ecosistema'


