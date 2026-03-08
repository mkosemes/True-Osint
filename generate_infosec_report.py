from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image as RLImage
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PDF = Path(os.getenv("INFOSEC_REPORT_PDF_PATH", BASE_DIR / "Rapport_Projet_Infosec_DVWA_Simule.pdf"))
PICTURES_DIR = BASE_DIR / "rapport_infosec_assets" / "Pictures"

SECTIONS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "1. Attaque XSS (Cross-Site Scripting) avec DVWA",
        [
            ("1.1", "Lancer la machine virtuelle Metasploitable2 et recuperer son adresse IP."),
            ("1.2", "Sur la machine hote, ouvrir Firefox et saisir l'adresse IP de Metasploitable2."),
            ("1.3", "Dans la liste des applications, choisir DVWA."),
            ("1.4", "Se connecter avec admin / password."),
            ("1.5", "Dans DVWA Security, positionner le niveau sur low."),
            ("1.6", "Ouvrir XSS Reflected, afficher le code source et injecter un script JavaScript d'alerte."),
            ("1.7", "Remettre DVWA Security sur medium."),
            ("1.8", "Revenir sur XSS Reflected et modifier l'attaque pour contourner la defense medium."),
            ("1.9", "Positionner DVWA Security sur high."),
            ("1.10", "Verifier dans XSS Reflected si une balise HTML ou script reste injectable au niveau high."),
            ("1.11", "Revenir au niveau low."),
            ("1.12", "Ouvrir XSS Stored, afficher le source et injecter un script JavaScript stocke."),
            ("1.13", "Se reconnecter en smithy/password et verifier l'effet de la XSS stored."),
            ("1.14", "Se reconnecter en admin."),
            ("1.15", "Passer DVWA Security sur medium."),
            ("1.16", "Adapter la charge XSS Stored pour contourner la defense medium."),
            ("1.17", "Passer DVWA Security sur high."),
            ("1.18", "Verifier si un script JavaScript est encore injectable en XSS Stored high."),
            ("1.19", "Revenir au niveau low."),
            ("1.20", "Ouvrir Command Execution et injecter une commande Linux en plus d'une IP."),
            ("1.21", "Passer DVWA Security sur medium."),
            ("1.22", "Modifier l'attaque Command Execution pour contourner la defense medium."),
            ("1.23", "Passer DVWA Security sur high."),
            ("1.24", "Verifier si autre chose qu'une IP valide peut etre saisie en high."),
            ("1.25", "Revenir au niveau low."),
            ("1.26", "Ouvrir File Inclusion et afficher /etc/passwd via le parametre page."),
        ],
    ),
    (
        "2. Attaque Cross-Site Request Forgery (CSRF)",
        [
            ("2.1", "Lancer Kali Linux et recuperer son adresse IP."),
            ("2.2", "Depuis la machine hote, se connecter a DVWA avec admin/password."),
            ("2.3", "Positionner le niveau de securite sur low."),
            ("2.4", "Ouvrir le menu CSRF."),
            ("2.5", "Observer le formulaire de changement de mot de passe utilisateur."),
            ("2.6", "Afficher le source pour identifier action, methode et parametres du formulaire."),
            ("2.7", "Construire l'URL permettant de changer le mot de passe en 1234."),
            ("2.8", "Injecter un commentaire XSS stored contenant une redirection vers l'URL CSRF."),
            ("2.9", "Verifier que le mot de passe admin est passe a 1234."),
            ("2.10", "Remettre le mot de passe admin a password."),
            ("2.11", "Se reconnecter en smithy/password."),
            ("2.12", "Positionner le niveau sur low."),
            ("2.13", "Verifier sur XSS Stored que le mot de passe smithy a ete change en 1234."),
            ("2.14", "Remettre le mot de passe smithy a password."),
            ("2.15", "Se reconnecter en admin."),
            ("2.16", "Reinitialiser la base de donnees DVWA."),
        ],
    ),
    (
        "3. Televersement (upload) de fichier",
        [
            ("3.1", "Ouvrir Firefox sur Kali Linux."),
            ("3.2", "Se connecter a DVWA avec admin."),
            ("3.3", "Positionner DVWA Security sur low."),
            ("3.4", "Ouvrir le menu Upload."),
            ("3.5", "Afficher le script de traitement via view source."),
            ("3.6", "Identifier le repertoire de stockage des fichiers televerses."),
            ("3.7", "Televerser /usr/share/webshells/php/php-backdoor.php."),
            ("3.8", "Acceder a l'URL de la backdoor televersee."),
            ("3.9", "Verifier les possibilites offertes par la backdoor."),
            ("3.10", "Passer le niveau de securite a medium."),
            ("3.11", "Retourner sur Upload."),
            ("3.12", "Afficher le code source du script de traitement medium."),
            ("3.13", "Identifier les types de fichiers acceptes."),
            ("3.14", "Intercepter avec Burp et modifier a la volee le type de fichier televerse."),
            ("3.15", "Editer php-reverse-shell.php et remplacer l'IP locale par l'IP Kali."),
            ("3.16", "Televerser php-reverse-shell.php."),
            ("3.17", "Lancer netcat en ecoute sur Kali: nc -l -v -p 1234."),
            ("3.18", "Executer le reverse shell via l'URL du script televerse."),
            ("3.19", "Verifier la connexion reverse shell et l'execution de commandes distantes."),
            ("3.20", "Expliquer pourquoi on parle de reverse shell."),
            ("3.21", "Positionner le niveau de securite sur high."),
            ("3.22", "Afficher le code source du traitement high."),
            ("3.23", "Identifier les fichiers encore acceptes en high."),
        ],
    ),
    (
        "4. Vol de cookies (et de sessions)",
        [
            ("4.1", "Sur Kali, demarrer Apache et MariaDB/MySQL."),
            ("4.2", "Creer la base maBD avec une table cookie."),
            ("4.3", "Creer un script PHP qui stocke un cookie recu en parametre."),
            ("4.4", "Creer un script PHP de visualisation des cookies voles."),
            ("4.5", "Ouvrir le navigateur sur Kali."),
            ("4.6", "Se connecter a DVWA avec admin."),
            ("4.7", "Poster un commentaire contenant une redirection vers le script voleur de cookies."),
            ("4.8", "Sur la machine hote, ouvrir le navigateur."),
            ("4.9", "Se connecter a DVWA avec smithy."),
            ("4.10", "Positionner le niveau sur low."),
            ("4.11", "Ouvrir XSS Stored pour declencher le vol."),
            ("4.12", "Recuperer le cookie PHPSESSID dans maBD sur Kali."),
            ("4.13", "Injecter ce cookie dans Burp pour usurper la session smithy."),
        ],
    ),
    (
        "5. Attaque par SQL Injection (SQLi) avec DVWA",
        [
            ("5.1", "Demonstrer les vulnerabilites SQLi presentes dans DVWA."),
            ("5.2", "Utiliser des techniques SQLi manuelles pour contourner des formulaires."),
            ("5.3", "Extraire des informations de la base de donnees."),
            ("5.4", "Identifier et exploiter des requetes faibles."),
            ("5.5", "Proposer des defenses: requetes preparees et sanitisation des entrees."),
        ],
    ),
    (
        "6. Mise en place de solutions de defense",
        [
            ("6.1", "Implementer un hachage robuste des mots de passe dans la base maBD."),
            ("6.2", "Implementer des mesures contre SQLi, XSS, CSRF et vol de cookies."),
        ],
    ),
    (
        "7. Securisation d'applications web (HTTPS)",
        [
            ("7.1", "Securiser Apache avec SSL (passage de HTTP vers HTTPS)."),
            ("7.2", "Configurer HTTPS avec certificats Let's Encrypt."),
        ],
    ),
]

# Mapping manuel valide visuellement (instruction -> captures correspondantes)
MANUAL_IMAGE_MAP: dict[str, list[str]] = {
    "1.1": ["is1.png"],
    "1.2": ["is2.png"],
    "1.5": ["is3.png"],
    "1.6": ["is5.png", "is6.png"],
    "1.8": ["is4.png"],
    "1.10": ["is7.png"],
    "1.12": ["is8.png"],
    "1.13": ["is9.png", "is10.png", "is11.png"],
    "1.20": ["is12.png", "is13.png", "is14.png"],
    "1.22": ["is15.png", "is16.png"],
    "1.24": ["is17.png"],
    "1.26": ["is18.png"],
    "2.6": ["is19.png"],
    "2.8": ["is20.png"],
    "3.2": ["is21.png"],
    "3.7": ["is22.png", "is24.png"],
    "3.8": ["is23.png"],
    "3.9": ["is25.png", "is26.png", "is27.png"],
    "3.13": ["is28.png"],
    "3.14": ["is29.png", "is30.png"],
    "3.15": ["is31.png"],
    "4.12": ["is32.png"],
    "5.1": ["is33.png"],
    "5.2": ["is34.png"],
    "5.3": ["is35.png", "is36.png"],
}


def resolve_mapped_images() -> dict[str, list[Path]]:
    resolved: dict[str, list[Path]] = {}
    missing: list[str] = []
    for step_id, file_names in MANUAL_IMAGE_MAP.items():
        step_images: list[Path] = []
        for name in file_names:
            p = PICTURES_DIR / name
            if p.exists():
                step_images.append(p)
            else:
                missing.append(str(p))
        if step_images:
            resolved[step_id] = step_images

    if missing:
        joined = "\n".join(f"- {m}" for m in missing)
        raise SystemExit(f"Fichiers manquants dans le mapping manuel:\n{joined}")

    return resolved


def build_pdf(mapped_images: dict[str, list[Path]]) -> tuple[int, int]:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontSize=24, leading=30, alignment=1))
    styles.add(ParagraphStyle(name="CoverSubtitle", parent=styles["Heading2"], fontSize=14, leading=20, alignment=1))
    styles.add(ParagraphStyle(name="CoverMeta", parent=styles["Normal"], fontSize=12, leading=18, alignment=1))
    styles.add(
        ParagraphStyle(
            name="CoverNameLabel",
            parent=styles["Normal"],
            fontSize=12,
            leading=18,
            alignment=1,
            spaceBefore=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverName",
            parent=styles["Heading3"],
            fontSize=14,
            leading=20,
            alignment=1,
            textColor=colors.HexColor("#0b3d91"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallInfo",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#444444"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="StepTitle",
            parent=styles["Heading4"],
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#0b3d91"),
            spaceBefore=6,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MissingShot",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#B00020"),
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=1.7 * cm,
        rightMargin=1.7 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.7 * cm,
        title="Rapport Projet Infosec DVWA",
        author="Assistant IA",
    )

    elements = []
    elements.append(Spacer(1, 4 * cm))
    elements.append(Paragraph("Rapport Projet Infosec", styles["CoverTitle"]))
    elements.append(Spacer(1, 14))
    elements.append(
        Paragraph(
            "Analyse de vulnérabilités et sécurisation d’applications web : "
            "Étude de cas pratique sur l'environnement DVWA",
            styles["CoverSubtitle"],
        )
    )
    elements.append(Spacer(1, 1.8 * cm))
    elements.append(Paragraph("<b>Examen:</b> Infosec", styles["CoverMeta"]))
    elements.append(Paragraph("<b>Niveau :</b> Licence 2 Big Data", styles["CoverMeta"]))
    elements.append(Paragraph("<b>Année :</b> 2025/2026", styles["CoverMeta"]))
    elements.append(Spacer(1, 1.2 * cm))
    elements.append(Paragraph("Présenté par :", styles["CoverNameLabel"]))
    elements.append(Paragraph("Mouhamadou Moustapha Souane", styles["CoverName"]))
    elements.append(Spacer(1, 1.0 * cm))
    elements.append(
        Paragraph(
            "Ce document utilise uniquement des captures reelles. "
            "La correspondance photo-instruction est effectuee manuellement.",
            styles["SmallInfo"],
        )
    )
    elements.append(PageBreak())

    used_images_count = 0
    missing_steps_count = 0

    for section_name, steps in SECTIONS:
        elements.append(Paragraph(section_name, styles["Heading2"]))
        elements.append(Spacer(1, 6))

        for step_id, step_text in steps:
            elements.append(Paragraph(f"Instruction {step_id}", styles["StepTitle"]))
            elements.append(Paragraph(step_text, styles["Normal"]))
            elements.append(Spacer(1, 4))

            images = mapped_images.get(step_id, [])
            if images:
                for image_path in images:
                    elements.append(RLImage(str(image_path), width=16.0 * cm, height=10.2 * cm))
                    elements.append(Spacer(1, 6))
                    used_images_count += 1
            else:
                elements.append(Paragraph("Capture reelle non fournie pour cette instruction.", styles["MissingShot"]))
                elements.append(Spacer(1, 6))
                missing_steps_count += 1

    doc.build(elements)
    return used_images_count, missing_steps_count


def main() -> None:
    if not PICTURES_DIR.exists():
        raise SystemExit(f"Dossier des captures introuvable: {PICTURES_DIR}")

    mapped_images = resolve_mapped_images()
    used_images_count, missing_steps_count = build_pdf(mapped_images)

    print(f"PDF genere: {OUTPUT_PDF}")
    print(f"Captures reelles utilisees: {used_images_count}")
    print("Captures simulees utilisees: 0")
    print(f"Instructions sans photo: {missing_steps_count}")


if __name__ == "__main__":
    main()
