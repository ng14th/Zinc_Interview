from .base_settings import BaseSettings
from typing import Optional, Dict


class DatabaseSettings(BaseSettings):

    # Django Database
    DJANGO_DB_MASTER_ENABLE: bool = True
    DJANGO_DB_MASTER_ENGINE: Optional[str] = None
    DJANGO_DB_MASTER_NAME: Optional[str] = None
    DJANGO_DB_MASTER_USERNAME: Optional[str] = None
    DJANGO_DB_MASTER_PASSWORD: Optional[str] = None
    DJANGO_DB_MASTER_HOST: Optional[str] = None
    DJANGO_DB_MASTER_PORT: Optional[str] = None

    DJANGO_DB_REPLICA_01_ENABLE: bool = False
    DJANGO_DB_REPLICA_01_ENGINE: Optional[str] = None
    DJANGO_DB_REPLICA_01_NAME: Optional[str] = None
    DJANGO_DB_REPLICA_01_USERNAME: Optional[str] = None
    DJANGO_DB_REPLICA_01_PASSWORD: Optional[str] = None
    DJANGO_DB_REPLICA_01_HOST: Optional[str] = None
    DJANGO_DB_REPLICA_01_PORT: Optional[str] = None

    def create_django_databases(self) -> Dict:
        dbs = {}
        for role in ('MASTER', 'REPLICA_01'):
            attr_enable = f'DJANGO_DB_{role}_ENABLE'
            if not getattr(self, attr_enable):
                continue
            attr_engine = f'DJANGO_DB_{role}_ENGINE'
            attr_name = f'DJANGO_DB_{role}_NAME'
            attr_username = f'DJANGO_DB_{role}_USERNAME'
            attr_password = f'DJANGO_DB_{role}_PASSWORD'
            attr_host = f'DJANGO_DB_{role}_HOST'
            attr_port = f'DJANGO_DB_{role}_PORT'

            dbs.update({
                'default' if role == 'MASTER' else role: {
                    'ENGINE': getattr(self, attr_engine),
                    'NAME': getattr(self, attr_name),
                    'USER': getattr(self, attr_username),
                    'PASSWORD': getattr(self, attr_password),
                    'HOST': getattr(self, attr_host),
                    'PORT': getattr(self, attr_port),
                    'ATOMIC_REQUESTS': True,
                    'CONN_MAX_AGE': 60,
                    'CONN_HEALTH_CHECKS': True
                }
            })
        # print('created databases:', dbs)
        return dbs
