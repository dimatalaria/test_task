from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )
    bot_token: str
    admin_ids: frozenset[int] = frozenset({42, 3595399})

settings = Settings(bot_token="7566406026:AAEe_AiRPOTcX1AgAswFStb7tnjPqWk1d1g")