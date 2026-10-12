import json
from pathlib import Path

FARES_PATH = Path(__file__).parent / "config" / "fares.json"

def load_fares(path: Path = FARES_PATH) -> tuple[float, float]:
    """Lee las tarifas del JSON y devuelve (tarifa parado, tarifa en movimiento)"""

    with open(path, encoding="utf-8") as file:
        data = json.load(file)
        
    return data["stopped_rate"], data["moving_rate"]