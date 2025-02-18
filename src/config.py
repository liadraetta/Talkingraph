import yaml
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os

# modelli per la configurazione annidata
class NamespaceConfig(BaseModel):
    left: dict[str, str]
    right: dict[str, str]

class PrefixConfig(BaseModel):
    urw: str

class AppConfig(BaseSettings):
    name: str
    endpoint: str
    namespace: NamespaceConfig
    prefix: PrefixConfig

# definisco il percorso del file di configurazione
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(BASE_DIR, "config.yml")

# funzione per caricare e trasformare i dati YML in un oggetto Pydantic
def load_yaml_config(filepath: str = CONFIG_PATH ) -> AppConfig:
    config_path = Path(filepath)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {filepath}")

    with config_path.open("r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)

    return AppConfig(**yaml_data["app"])  #converto il dizionario in un oggetto Pydantic

# creo l'istanza globale di configurazione
config = load_yaml_config()
