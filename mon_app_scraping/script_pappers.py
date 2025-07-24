import requests
import csv
import os
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm

API_KEY = "3d96bd10804182e3f44fa76e98527ee4e38f7539833546a0"

def lancer_collecte_pappers(dossier_sortie, codes_postaux, max_age_annees=1, max_total=10):
    """
    Paramètres :
    - dossier_sortie : chemin du dossier où enregistrer le fichier
    - codes_postaux : liste de codes postaux à interroger
    - max_age_annees : âge max des entreprises (ex : 1 = entreprises de moins d'un an)
    - max_total : nombre maximal d'entreprises à collecter
    """

    # Date de création minimale = aujourd'hui - max_age_annees
    date_limite = datetime.today() - timedelta(days=365 * max_age_annees)
    fichier_csv = os.path.join(dossier_sortie, "fichier_conquete.csv")
    entreprises = []

    for code_postal in tqdm(codes_postaux, desc="Scraping Pappers"):
        if len(entreprises) >= max_total:
            break

        url = f"https://api.pappers.fr/v2/recherche"
        params = {
            "api_token": API_KEY,
            "code_postal": code_postal,
            "date_creation_min": date_limite.strftime("%Y-%m-%d"),
            "par_page": min(20, max_total - len(entreprises))
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()
            for e in data.get("entreprises", []):
                entreprises.append({
                    "siren": e.get("siren"),
                    "nom": e.get("nom_entreprise"),
                    "code_postal": code_postal
                })
                if len(entreprises) >= max_total:
                    break
        except Exception as err:
            print(f"Erreur pour {code_postal} : {err}")

    if entreprises:
        df = pd.DataFrame(entreprises)
        df.to_csv(fichier_csv, index=False)
        return "fichier_conquete.csv"
    else:
        raise Exception("Aucune entreprise trouvée")
