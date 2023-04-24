import  os
# carga las variables de entorno desde el archivo .env
from dotenv import load_dotenv
from django.conf import settings

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

settings.DATABASES = DATABASES
# routers.py

class EcosistemaRouter:
    """
    A router to control all database operations on models in the
    ecosistema application.
    """
    app_label = 'ecosistema'

    def db_for_read(self, model, **hints):
        """
        Attempts to read ecosistema models go to ecosistema.
        """
        if model._meta.app_label == self.app_label:
            return self.app_label
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write ecosistema models go to ecosistema.
        """
        if model._meta.app_label == self.app_label:
            return self.app_label
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the ecosistema app is involved.
        """
        if obj1._meta.app_label == self.app_label or \
           obj2._meta.app_label == self.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the ecosistema app only appears in the 'ecosistema' database.
        """
        if app_label == self.app_label:
            return db == self.app_label
        return None



