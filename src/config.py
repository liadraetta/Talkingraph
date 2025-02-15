from pydantic_settings import BaseSettings, SettingsConfigDict
import os 

current_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_path, "..", "config.yml")# capire se funziona così!!!

class Settings(BaseSettings):
    SPARQL_ENDPOINT: str 
    name: str 

model_config = SettingsConfigDict( yml_file="") 

settings = Settings()