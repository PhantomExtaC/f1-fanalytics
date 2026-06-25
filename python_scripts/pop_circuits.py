import csv
import json
import re
from pathlib import Path


def make_id(name: str) -> str:
    """
    Convert a circuit name into a stable identifier.
    Example:
        "Brands Hatch" -> "brands_hatch"
        "Circuit de Spa-Francorchamps" -> "circuit_de_spa_francorchamps"
    """
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


INPUT_CSV = Path("all_f1_circuits.csv")
OUTPUT_JSON = Path("public/data/tracks.json")

tracks = []

with INPUT_CSV.open("r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        circuit_name = row["Circuit"].strip()
        track_id = make_id(circuit_name)

        track = {
            "id": track_id,
            "name": circuit_name,
            "city": row["City"].strip(),
            "country": row["Country"].strip(),
            "lengthKm": float(row["Track Length (km)"]),
            "turns": int(row["Turns"]),
            "direction": row["Direction"].strip(),
            "circuitType": row["Circuit Type"].strip(),
            "firstGrandPrix": row["First Grand Prix"].strip(),
            "lastGrandPrix": row["Last Grand Prix"].strip(),
            "racesHeld": int(row["Races"]),
            "lapRecord": {
                "time": row["Best Lap Timing"].strip(),
                "driver": row["Best Lap Driver"].strip(),
                "year": int(row["Best Lap Year"]),
                "milliseconds": float(row["Best Lap Time"]),
            },
            # Placeholder image path
            "layoutImage": f"/images/tracks/{track_id}.png",
            "active": True,
        }

        tracks.append(track)

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_JSON.open("w", encoding="utf-8") as f:
    json.dump(tracks, f, indent=2, ensure_ascii=False)

print(f"Wrote {len(tracks)} tracks to {OUTPUT_JSON}")