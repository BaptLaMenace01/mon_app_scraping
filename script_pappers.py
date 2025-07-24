import csv

# Chemin vers ton fichier d’entrée
fichier_path = "conquete.csv"

# Crée un nouveau fichier enrichi
output_path = fichier_path.replace(".csv", "_enrichi.csv")

with open(fichier_path, newline='') as infile, open(output_path, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Email trouvé']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        siren = row.get("siren", "")
        email = f"contact+{siren}@exemple.com" if siren else "non trouvé"
        row["Email trouvé"] = email
        writer.writerow(row)

print(f"✅ Fichier enrichi généré : {output_path}")

