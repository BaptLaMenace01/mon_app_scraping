import pandas as pd
import time
import logging
import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def lancer_enrichissement(fichier_entree):
    # Options Chrome Headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

chemin_chromedriver = "/Users/baptistequaino/mon_app_scraping/chromedriver"
service = Service(executable_path=chemin_chromedriver)
 
    df = pd.read_csv(fichier_entree)
    resultats = []
    for _, row in df.iterrows():
        siren = row.get("siren")
        if not siren:
            continue

        try:
            url = f"https://annuaire-entreprises.data.gouv.fr/entreprise/{siren}"
            driver.get(url)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(1)

            try:
                nom_dirigeant = driver.find_element(By.XPATH, "//dt[text()='Dirigeant(s)']/following-sibling::dd").text
            except:
                nom_dirigeant = "Non trouvé"

            try:
                activite = driver.find_element(By.XPATH, "//dt[text()='Activité principale']/following-sibling::dd").text
            except:
                activite = "Non trouvée"

            try:
                adresse = driver.find_element(By.XPATH, "//dt[text()='Adresse']/following-sibling::dd").text
            except:
                adresse = "Non trouvée"

            resultats.append({
                "siren": siren,
                "nom": row.get("nom", ""),
                "code_postal": row.get("code_postal", ""),
                "nom_dirigeant": nom_dirigeant,
                "activite": activite,
                "adresse": adresse
            })

        except Exception as e:
            print(f"Erreur pour SIREN {siren} : {e}")
            continue

    driver.quit()

    # Enregistrement
    df_final = pd.DataFrame(resultats)
    fichier_sortie = f"enrichi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    chemin_sortie = os.path.join("static", fichier_sortie)
    df_final.to_csv(chemin_sortie, index=False)
    return fichier_sortie
