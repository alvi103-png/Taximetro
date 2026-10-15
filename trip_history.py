import csv
from datetime import datetime
from pathlib import Path

HISTORY_DIR = Path(__file__).parent / "data"
HISTORY_FILE = HISTORY_DIR / "trips_history.csv"

FIELDS = ["date", "duration_seconds", "total_eur"]


def save_trip(duration: float, total: float, path: Path = HISTORY_FILE) -> None:
    """Añade una carrera terminada al final del histórico"""
    path.parent.mkdir(exist_ok=True)

    is_new_file = not path.exists()

    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if is_new_file:
            writer.writerow(FIELDS)
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            round(duration, 1),
            round(total, 2),
        ])


def load_today_trips(path: Path = HISTORY_FILE) -> list[dict]:
    """Devuelve las carreras guardadas hoy"""
    if not path.exists():
        return []

    today = datetime.now().date().isoformat()

    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader if row["date"].startswith(today)]