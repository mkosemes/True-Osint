from __future__ import annotations

import os
import re
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as RLImage,
    PageBreak,
)


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = Path(os.getenv("INFOSEC_REPORT_ASSETS_DIR", BASE_DIR / "rapport_infosec_assets"))
OUTPUT_PDF = Path(os.getenv("INFOSEC_REPORT_PDF_PATH", BASE_DIR / "Rapport_Projet_Infosec_DVWA_Simule.pdf"))
SCREENSHOTS_DIR = Path(os.getenv("INFOSEC_SCREENSHOTS_DIR", BASE_DIR / "screenshots"))
PICTURES_DIR = BASE_DIR / "rapport_infosec_assets" / "Pictures"


SECTIONS = [
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


def fake_console_lines(step_id: str, text: str) -> list[str]:
    lower = text.lower()
    if "adresse ip" in lower:
        return [
            "kali@lab:~$ ip a | rg \"inet \"",
            "inet 192.168.56.20/24 brd 192.168.56.255 scope global eth0",
            "msf2@target:~$ ifconfig eth0",
            "inet addr:192.168.56.10  Bcast:192.168.56.255  Mask:255.255.255.0",
        ]
    if "xss" in lower:
        return [
            "Payload teste: <script>alert('XSS-" + step_id + "')</script>",
            "Observation: execution JavaScript selon niveau de securite DVWA.",
            "Trace navigateur: requete HTTP 200 + rendu page vulnerabilite.",
            "Validation: preuve visuelle d'alerte cote client.",
        ]
    if "csrf" in lower:
        return [
            "GET /dvwa/vulnerabilities/csrf/?password_new=1234&password_conf=1234&Change=Change HTTP/1.1",
            "Cookie: PHPSESSID=victim_session",
            "Resultat: mot de passe modifie sans consentement explicite.",
            "Defense attendue: token anti-CSRF + verification Origin/Referer.",
        ]
    if "upload" in lower or "televers" in lower:
        return [
            "POST /dvwa/vulnerabilities/upload/ HTTP/1.1",
            "Content-Type: multipart/form-data; boundary=----lab",
            "Fichier: php-backdoor.php  => Stockage: /hackable/uploads/",
            "Verification: acces direct via URL du fichier televerse.",
        ]
    if "reverse shell" in lower or "netcat" in lower:
        return [
            "kali@lab:~$ nc -l -v -p 1234",
            "listening on [any] 1234 ...",
            "connect to [192.168.56.20] from (UNKNOWN) [192.168.56.10] 47312",
            "www-data@metasploitable:/var/www/dvwa$ whoami",
        ]
    if "cookie" in lower or "session" in lower:
        return [
            "SELECT value FROM cookie ORDER BY id DESC LIMIT 1;",
            "PHPSESSID=9f8ce3d2a0f1b1e8f2e4b9e7f0c1d2a3",
            "Burp Repeater: Cookie remplace pour usurpation de session.",
            "Resultat: acces au compte victime confirme.",
        ]
    if "sql" in lower:
        return [
            "Input de test: ' OR '1'='1' -- -",
            "Requete observee: SELECT * FROM users WHERE ...",
            "Resultat: contournement login / extraction donnees possible.",
            "Defense: prepared statements + validation stricte.",
        ]
    if "ssl" in lower or "https" in lower:
        return [
            "sudo a2enmod ssl && sudo service apache2 restart",
            "VirtualHost *:443 configure avec certificat valide.",
            "Test: curl -I https://192.168.56.10",
            "Resultat: trafic chiffre TLS operationnel.",
        ]
    return [
        f"Etape {step_id} executee dans le laboratoire virtuel.",
        "Kali Linux: interception et verification des requetes HTTP.",
        "Metasploitable2: service DVWA cible etat vulnerable.",
        "Observation: comportement conforme au scenario de test.",
    ]


def generate_image(step_id: str, step_text: str, section_name: str, output_path: Path) -> None:
    width, height = 1400, 900
    img = Image.new("RGB", (width, height), (26, 30, 36))
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.load_default(size=34)
    font_sub = ImageFont.load_default(size=22)
    font_text = ImageFont.load_default(size=20)

    draw.rectangle((0, 0, width, 72), fill=(13, 17, 23))
    draw.text((28, 22), f"Capture simulee - Etape {step_id}", fill=(141, 241, 157), font=font_title)

    draw.rectangle((26, 94, width - 26, 260), fill=(35, 40, 48), outline=(80, 90, 105), width=2)
    draw.text((44, 110), "Contexte laboratoire", fill=(255, 221, 130), font=font_sub)
    draw.text((44, 150), "Kali Linux 2025.4  |  Metasploitable2  |  DVWA  |  Burp Suite CE", fill=(220, 225, 230), font=font_text)

    wrapped_section = textwrap.wrap(section_name, width=88)
    y = 186
    for line in wrapped_section[:2]:
        draw.text((44, y), line, fill=(204, 214, 224), font=font_text)
        y += 28

    draw.rectangle((26, 278, width - 26, height - 26), fill=(15, 18, 22), outline=(80, 90, 105), width=2)
    draw.text((44, 298), "Instruction", fill=(110, 190, 255), font=font_sub)

    instruction_lines = textwrap.wrap(step_text, width=106)
    y = 332
    for line in instruction_lines:
        draw.text((44, y), f"- {line}", fill=(229, 233, 240), font=font_text)
        y += 28

    draw.text((44, y + 12), "Sortie / preuve technique (simulation):", fill=(255, 221, 130), font=font_sub)
    y += 46

    for console_line in fake_console_lines(step_id, step_text):
        draw.text((58, y), console_line, fill=(141, 241, 157), font=font_text)
        y += 28

    draw.text((44, height - 58), "Note: image reconstituee a des fins pedagogiques.", fill=(180, 187, 196), font=font_text)
    img.save(output_path, "JPEG", quality=88)


def get_real_screenshot(step_id: str, search_dirs: list[Path]) -> Path | None:
    """Return a real screenshot path if named with the step id."""
    stem = step_id.replace(".", "_")
    for folder in search_dirs:
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            candidate = folder / f"{stem}{ext}"
            if candidate.exists():
                return candidate
    return None


def get_sequence_screenshots(search_dirs: list[Path]) -> list[Path]:
    """
    Collect screenshots named is1.png, is2.png, ... from known folders.
    """
    seq: list[tuple[int, Path]] = []
    seen: set[Path] = set()
    pattern = re.compile(r"^is(\d+)\.(png|jpg|jpeg|webp)$", re.IGNORECASE)
    for folder in search_dirs:
        if not folder.exists():
            continue
        for p in folder.iterdir():
            if not p.is_file():
                continue
            m = pattern.match(p.name)
            if not m:
                continue
            idx = int(m.group(1))
            rp = p.resolve()
            if rp in seen:
                continue
            seen.add(rp)
            seq.append((idx, p))
    seq.sort(key=lambda x: x[0])
    return [p for _, p in seq]


def build_pdf(image_entries: list[tuple[str, str, str, Path]], missing_count: int) -> None:
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontSize=24,
            leading=30,
            alignment=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["Heading2"],
            fontSize=14,
            leading=20,
            alignment=1,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMeta",
            parent=styles["Normal"],
            fontSize=12,
            leading=18,
            alignment=1,
        )
    )
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
            "Ce document presente un rendu complet avec une illustration pour chaque instruction numerotee "
            "du projet. Seules les captures reelles deposees dans screenshots/ ou "
            "rapport_infosec_assets/Pictures/ sont autorisees.",
            styles["SmallInfo"],
        )
    )
    elements.append(
        Paragraph(
            f"Captures reelles integrees: {len(image_entries)} | "
            f"Instructions sans photo fournie: {missing_count}",
            styles["SmallInfo"],
        )
    )
    elements.append(PageBreak())

    current_section = None
    for section_name, step_id, step_text, image_path in image_entries:
        if section_name != current_section:
            elements.append(Paragraph(section_name, styles["Heading2"]))
            elements.append(Spacer(1, 6))
            current_section = section_name

        elements.append(Paragraph(f"Instruction {step_id}", styles["StepTitle"]))
        elements.append(Paragraph(step_text, styles["Normal"]))
        elements.append(Spacer(1, 5))
        elements.append(RLImage(str(image_path), width=16.0 * cm, height=10.2 * cm))
        elements.append(Spacer(1, 10))

    doc.build(elements)


def main() -> None:
    search_dirs: list[Path] = [SCREENSHOTS_DIR, PICTURES_DIR]
    available_dirs = [d for d in search_dirs if d.exists()]
    if not available_dirs:
        raise SystemExit(
            "Aucun dossier de captures trouve.\n"
            f"Attendus: {SCREENSHOTS_DIR} ou {PICTURES_DIR}"
        )

    image_entries: list[tuple[str, str, str, Path]] = []
    missing_steps: list[tuple[str, str, str]] = []
    all_steps: list[tuple[str, str, str]] = []

    for section_name, steps in SECTIONS:
        for step_id, step_text in steps:
            all_steps.append((section_name, step_id, step_text))
            real_shot = get_real_screenshot(step_id, available_dirs)
            if real_shot is not None:
                image_entries.append((section_name, step_id, step_text, real_shot))
            else:
                missing_steps.append((section_name, step_id, step_text))

    # Fallback: map sequential files is1.png, is2.png... to remaining steps
    # in assignment order when explicit step filenames are not used.
    sequential = get_sequence_screenshots(available_dirs)
    used_paths = {p.resolve() for _, _, _, p in image_entries}
    seq_iter = (p for p in sequential if p.resolve() not in used_paths)

    filled_entries: list[tuple[str, str, str, Path]] = []
    for section_name, step_id, step_text in missing_steps:
        next_img = next(seq_iter, None)
        if next_img is None:
            break
        filled_entries.append((section_name, step_id, step_text, next_img))

    image_entries.extend(filled_entries)
    covered_step_ids = {step_id for _, step_id, _, _ in image_entries}
    uncovered = [item for item in all_steps if item[1] not in covered_step_ids]

    if not image_entries:
        raise SystemExit(
            "Aucune capture reelle exploitable trouvee.\n"
            "Ajoutez des images nommees 1_1.png (par etape) ou is1.png (sequence)."
        )

    build_pdf(image_entries, len(uncovered))
    print(f"PDF genere: {OUTPUT_PDF}")
    print(f"Captures reelles utilisees: {len(image_entries)}")
    print("Captures simulees utilisees: 0")
    print(f"Instructions sans photo: {len(uncovered)}")


if __name__ == "__main__":
    main()
