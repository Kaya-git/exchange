import os
from dataclasses import dataclass

import yadisk_async
from dotenv import load_dotenv
from fastapi_storages import FileSystemStorage
from sqlalchemy.engine import URL
load_dotenv()


@dataclass
class DataBaseConfig:
    """ Database connection variables """
    name: str = os.environ.get("DB_NAME")
    user: str = os.environ.get("DB_USER")
    passwd: str = os.environ.get("DB_PASS")
    port: str = os.environ.get("DB_PORT")
    host: str = os.environ.get("DB_HOST")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """ This function build a connection string """
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class RedisConfig:
    """ Redis connection variables"""

    db: str = int(os.environ.get("REDIS_DATABASE", 1))
    host: str = os.environ.get("REDIS_HOST")
    port: str = os.environ.get("REDIS_PORT")
    state_ttl: int = os.environ.get("REDIS_TTL_STATE", None)
    data_ttl: int = os.environ.get("REDIS_TTL_DATA", None)


@dataclass
class ParserConfiguration:
    """ Parser URL's """
    api_key = os.environ.get("BINANCE_API_KEY")
    secret_key_binance = os.environ.get("SECRET_KEY_BINANCE")


@dataclass
class ImageStorageConfiguration:
    "Yadisk Image"
    yadisk_token = os.environ.get("YADISKTOKEN")

    async def build_image_storage(self):
        image_storage = yadisk_async.YaDisk(token=self.yadisk_token)
        return image_storage


@dataclass
class Auth:
    "JWT secret"
    jwt_token = os.environ.get("SECRET_JWT")
    algorithm = os.environ.get("ALGORITHM")
    user_menager = os.environ.get("SECRET_USER_MENAGER")


@dataclass
class Google_reCaptcha:
    """Google reCapthca set up"""
    google_url = os.environ.get("Google_URL")
    gsk = os.environ.get("GSK")
    gpk = os.environ.get("GPK")


@dataclass
class Configuration:
    """ All in one's configuration class """
    secret_key = os.environ.get("SECRET_KEY")
    admin_auth = os.environ.get("ADMIN_AUTH")
    debug = bool(os.environ.get("DEBUG"))
    logging_level = int(os.environ.get("LOGGING_LEVEL"))
    image_admin_storage = FileSystemStorage(path='tmp')
    yandex_email = os.environ.get("EMAIL")
    yandex_email_pass = os.environ.get("EMAIL_PASSWORD")
    image_storage = ImageStorageConfiguration()
    google_recaptcha = Google_reCaptcha()
    parser = ParserConfiguration()
    redis = RedisConfig()
    db = DataBaseConfig()
    auth = Auth()


conf = Configuration()
