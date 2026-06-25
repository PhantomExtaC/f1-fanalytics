import os
import requests
from urllib.parse import quote

OUTPUT_DIR = "public/images/drivers"

drivers = {
    "max_verstappen": "Max Verstappen",
    "lando_norris": "Lando Norris",
    "oscar_piastri": "Oscar Piastri",
    "charles_leclerc": "Charles Leclerc",
    "lewis_hamilton": "Lewis Hamilton",
    "george_russell": "George Russell",
    "kimi_antonelli": "Andrea Kimi Antonelli",
    "fernando_alonso": "Fernando Alonso",
    "lance_stroll": "Lance Stroll",
    "pierre_gasly": "Pierre Gasly",
    "franco_colapinto": "Franco Colapinto",
    "esteban_ocon": "Esteban Ocon",
    "oliver_bearman": "Oliver Bearman",
    "alex_albon": "Alexander Albon",
    "carlos_sainz": "Carlos Sainz Jr.",
    "liam_lawson": "Liam Lawson",
    "isack_hadjar": "Isack Hadjar",
    "nico_hulkenberg": "Nico Hülkenberg",
    "gabriel_bortoleto": "Gabriel Bortoleto",
    "yuki_tsunoda": "Yuki Tsunoda",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

API = "https://en.wikipedia.org/w/api.php"

for file_id, page in drivers.items():
    params = {
        "action": "query",
        "titles": page,
        "prop": "pageimages",
        "piprop": "original",
        "format": "json",
    }

    try:
        data = requests.get(API, params=params, timeout=30).json()
        pages = data["query"]["pages"]

        for _, value in pages.items():
            image_url = value.get("original", {}).get("source")

            if image_url:
                ext = image_url.split(".")[-1].split("?")[0]
                filename = os.path.join(
                    OUTPUT_DIR,
                    f"{file_id}.{ext}"
                )

                img = requests.get(image_url, timeout=30)

                with open(filename, "wb") as f:
                    f.write(img.content)

                print(f"Downloaded {filename}")
            else:
                print(f"No image found for {page}")

    except Exception as e:
        print(page, e)