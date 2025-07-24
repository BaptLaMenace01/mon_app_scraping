from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

def lancer_enrichissement(fichier_path):
    # Configuration de Selenium
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver_path = "/opt/homebrew/bin/chromedriver"
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    output_path = fichier_path.replace(".csv", "_enrichi.csv")

    with open(fichier_path, newline='') as infile, open(output_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Email trouvé']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Simulation simple d’enrichissement
            siren = row.get("siren", "")
            email = f"contact+{siren}@exemple.com" if siren else "non trouvé"
            row["Email trouvé"] = email
            writer.writerow(row)
            time.sleep(0.5)

    driver.quit()
    return os.path.basename(output_path)

