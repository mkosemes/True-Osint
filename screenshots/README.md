# Captures reelles pour le rapport

Le script `generate_infosec_report.py` utilise uniquement les captures reelles deposees ici.
Si une capture manque, la generation du PDF est arretee.

## Nommage attendu

Une image par instruction, avec le numero remplace `.` par `_` :

- `1_1.png` pour l'instruction **1.1**
- `1_2.jpg` pour l'instruction **1.2**
- `2_16.png` pour l'instruction **2.16**
- `7_2.jpg` pour l'instruction **7.2**

Extensions supportees : `.png`, `.jpg`, `.jpeg`, `.webp`

## Commande de generation

Depuis la racine du projet :

```bash
python3 generate_infosec_report.py
```

Le PDF est genere ici :

`./Rapport_Projet_Infosec_DVWA_Simule.pdf`

## Option chemin personnalise

```bash
INFOSEC_SCREENSHOTS_DIR="/chemin/vers/mes_captures" \
INFOSEC_REPORT_PDF_PATH="/chemin/rapport.pdf" \
python3 generate_infosec_report.py
```
