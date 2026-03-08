# Captures reelles pour le rapport

Le script `generate_infosec_report.py` utilise uniquement les captures reelles.
Aucune image simulee n'est ajoutee.

## Nommage attendu

### Mode A (recommande) : nommage par instruction

Une image par instruction, avec le numero remplace `.` par `_` (dans `screenshots/`) :

- `1_1.png` pour l'instruction **1.1**
- `1_2.jpg` pour l'instruction **1.2**
- `2_16.png` pour l'instruction **2.16**
- `7_2.jpg` pour l'instruction **7.2**

Extensions supportees : `.png`, `.jpg`, `.jpeg`, `.webp`

### Mode B : captures sequentielles (vos fichiers `is1.png`, `is2.png`, ...)

Le script accepte aussi les captures dans :

- `rapport_infosec_assets/Pictures/is1.png`
- `rapport_infosec_assets/Pictures/is2.png`
- etc.

Dans ce mode, les images sont affectees aux instructions dans l'ordre du projet.
S'il n'y a pas assez de captures, le PDF est genere uniquement avec les etapes couvertes.

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
