# Captures reelles pour le rapport

Le script `generate_infosec_report.py` utilise uniquement les captures reelles.
Aucune image simulee n'est ajoutee.

## Source des captures

Le script lit les captures dans :

- `rapport_infosec_assets/Pictures/is1.png`
- `rapport_infosec_assets/Pictures/is2.png`
- etc.

La correspondance image -> instruction est manuelle dans
`generate_infosec_report.py` (variable `MANUAL_IMAGE_MAP`).

Si vous ajoutez/modifiez des captures, mettez a jour ce mapping.

## Commande de generation

Depuis la racine du projet :

```bash
python3 generate_infosec_report.py
```

Le PDF est genere ici :

`./Rapport_Projet_Infosec_DVWA_Simule.pdf`

## Option chemin personnalise

```bash
INFOSEC_REPORT_PDF_PATH="/chemin/rapport.pdf" \
python3 generate_infosec_report.py
```
