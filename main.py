import json
import os
import zipfile
import sys

import easygui
import requests

msg = "Quelle version souhaitez vous installer ? (aucune modification ne seras possible plus tard)"
title = "Server updater"

choices = ["latest", "recommended"]

# Récupération du choix de version s'il existe, sinon demande à l'utilisateur
if os.path.exists("version_choice.txt"):
    with open("version_choice.txt", "r") as f:
        version_choice = f.read().strip()
else:
    version_choice = reply = easygui.buttonbox(msg, title, choices=choices)
    with open("version_choice.txt", "w") as f:
        f.write(version_choice)
# Récupération des données de la dernière version
url = "https://changelogs-live.fivem.net/api/changelog/versions/win32/server"
response = requests.get(url)
if response.status_code == 200:
    data = json.loads(response.content)
    # Choix de la version à télécharger
    if version_choice == "latest":
        download_url_key = "latest_download"
        version_key = "latest"
    elif version_choice == "recommended":
        download_url_key = "recommended_download"
        version_key = "recommended"
    else:
        print("Choix invalide.")
        sys.exit("Choix invalide.")
    download_url = data[download_url_key]
    version = data[version_key]
    print(f"Version téléchargée : {version}")
    # Vérification de la version déjà extraite
    if os.path.exists("arthefact/version.txt"):
        with open("arthefact/version.txt", "r") as f:
            extracted_version = f.read().strip()
        print(f"Version extraite : {extracted_version}")
        if extracted_version == version:
            print("La version téléchargée est la même que celle déjà extraite.")
            sys.exit("La version téléchargée est la même que celle déjà extraite.")
        else:
            print("Suppression de l'ancienne version extraite.")
            for root, dirs, files in os.walk("arthefact/", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
    else:
        os.makedirs("arthefact")
    # Téléchargement du fichier correspondant
    response = requests.get(download_url)
    if response.status_code == 200:
        with open("fichier_telecharge.zip", "wb") as f:
            f.write(response.content)
        print("Le fichier a été téléchargé avec succès.")
        # Extraction du fichier téléchargé dans le dossier "arthefact"
        with zipfile.ZipFile("fichier_telecharge.zip", 'r') as zip_ref:
            zip_ref.extractall("arthefact")
        print("Le fichier a été extrait avec succès dans le dossier 'arthefact'.")
        # Écriture de la version extraite dans un fichier texte
        with open("arthefact/version.txt", "w") as f:
            f.write(version)
        print("La version extraite a été enregistrée.")
        # Suppression du fichier téléchargé
        os.remove("fichier_telecharge.zip")
        print("Le fichier téléchargé a été supprimé.")
    else:
        print("Erreur lors du téléchargement du fichier.")
else:
    print("Erreur lors de la récupération des données.")

sys.exit("Programme fini")