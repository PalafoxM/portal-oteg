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
    Enrutador para controlar todas las operaciones de base de datos en los modelos de la
    aplicación 'ecosistema'.
    """
    app_label = 'ecosistema'

    def db_for_read(self, model, **hints):
        """
        Intentos de lectura de modelos de la aplicación 'ecosistema' se dirigen a la base de datos 'ecosistema'.
        """
        if model._meta.app_label == self.app_label:
            return self.app_label
        return None

    def db_for_write(self, model, **hints):
        """
        Intentos de escritura de modelos de la aplicación 'ecosistema' se dirigen a la base de datos 'ecosistema'.
        """
        if model._meta.app_label == self.app_label:
            return self.app_label
        return None

    def db_for_delete(self, model, **hints):
        """
        Intentos de eliminación de modelos de la aplicación 'ecosistema' se dirigen a la base de datos 'ecosistema'.
        """
        if model._meta.app_label == self.app_label:
            return self.app_label
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relaciones si está involucrado un modelo de la aplicación 'ecosistema'.
        """
        if obj1._meta.app_label == self.app_label or obj2._meta.app_label == self.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Asegura que la aplicación 'ecosistema' aparezca solo en la base de datos 'ecosistema'.
        """
        if app_label == self.app_label:
            return db == self.app_label
        return None




