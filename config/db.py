import  os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# mysqlclient

# MYSQL = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'otegDEV',
#         'USER': 'oteg-dev',
#         'PASSWORD': 'OTEG2023*Purpura.',
#         'HOST': 'sectur-gto.c31dkeyomhn9.us-east-2.rds.amazonaws.com',
#         'PORT': '3306',
#         'OPTIONS': {
#             'sql_mode': 'traditional',
#         }
#     }
# }


MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
