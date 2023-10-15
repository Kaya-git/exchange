import os
from dotenv import load_dotenv
from dataclasses import dataclass
from sqlalchemy.engine import URL
import yadisk_async
from fastapi_storages import FileSystemStorage
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
        print(f" Яндекс диск права: {await image_storage.check_token()}")
        return image_storage


@dataclass
class Auth:
    "JWT secret"
    jwt_token = os.environ.get("SECRET_JWT")
    user_menager = os.environ.get("SECRET_USER_MENAGER")


@dataclass
class Configuration:
    """ All in one's configuration class """
    secret_key = os.environ.get("SECRET_KEY")
    admin_auth = os.environ.get("ADMIN_AUTH")
    debug = bool(os.environ.get("DEBUG"))
    logging_level = int(os.environ.get("LOGGING_LEVEL"))
    image_admin_storage = FileSystemStorage(path='src\static\currency_icons')

    image_storage = ImageStorageConfiguration()
    parser = ParserConfiguration()
    redis = RedisConfig()
    db = DataBaseConfig()
    auth = Auth()


conf = Configuration()
