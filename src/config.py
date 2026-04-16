import os

from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_psycopg(self):
        return \
            (f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}'
             f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    model_config = SettingsConfigDict(env_file=dotenv_path)


settings = Settings()
