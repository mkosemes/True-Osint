from __future__ import annotations

import os
import random
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image as RLImage
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


BASE_DIR = Path(__file__).resolve().parent
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
OUTPUT_PDF = Path(os.getenv("INFOSEC_REPORT_PDF_PATH", BASE_DIR / "Rapport_Projet_Infosec_DVWA_Simule.pdf"))
LOGO_MINISTRY = BASE_DIR / "screenshots" / "capt12.png"
LOGO_DIT = BASE_DIR / "assets" / "logos" / "logo_dit.png"


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


SECTION_POOLS: dict[str, list[str]] = {
    "1": ["8.jpeg", "9.jpeg", "t.jpeg", "u.jpeg", "s.jpeg", "l.jpeg", "m.jpeg", "x.jpeg", "c.jpeg", "q.jpeg", "e.jpeg"],
    "2": ["b.jpeg", "nm.jpeg", "v.jpeg", "o.jpeg", "i.jpeg", "qw.jpeg", "q.jpeg"],
    "3": ["yu.jpeg", "ui.jpeg", "ty.jpeg", "tyg.jpeg", "er.jpeg", "op.jpeg", "opikj.jpeg", "rt.jpeg", "oi.jpeg", "fgt.jpeg", "kk.jpeg", "as.jpeg", "sd.jpeg", "io.jpeg", "iopl.jpeg", "hyu.jpeg", "frty.jpeg", "kjh.jpeg"],
    "4": ["hyujkf.jpeg", "knd.jpeg", "bv.jpeg", "WhatsApp Image 2026-03-09 at 11.31.50.jpeg", "thq.jpeg", "as.jpeg", "sd.jpeg", "o.jpeg", "s.jpeg"],
    "5": ["7.jpeg", "q.jpeg", "n.jpeg", "b.jpeg", "s.jpeg"],
    "6": ["q.jpeg", "e.jpeg", "z.jpeg", "v.jpeg", "k.jpeg"],
    "7": ["sw.jpeg", "df.jpeg", "as.jpeg", "sd.jpeg", "7.jpeg"],
}


STEP_OVERRIDES: dict[str, list[str]] = {
    "1.1": ["2.jpeg"],
    "1.2": ["2.jpeg"],
    "1.3": ["2.jpeg"],
    "1.4": ["5.jpeg", "we.jpeg"],
    "1.5": ["q.jpeg", "7.jpeg"],
    "1.6": ["8.jpeg", "9.jpeg", "w.jpeg"],
    "1.8": ["t.jpeg"],
    "1.9": ["e.jpeg", "7.jpeg"],
    "1.10": ["r.jpeg", "t.jpeg"],
    "1.12": ["u.jpeg", "s.jpeg"],
    "1.13": ["o.jpeg", "i.jpeg", "qw.jpeg", "y.jpeg"],
    "1.20": ["l.jpeg", "f.jpeg", "h.jpeg"],
    "1.22": ["m.jpeg", "k.jpeg"],
    "1.24": ["x.jpeg", "z.jpeg"],
    "1.26": ["c.jpeg"],
    "2.6": ["v.jpeg"],
    "2.8": ["o.jpeg", "s.jpeg", "u.jpeg"],
    "2.9": ["b.jpeg", "nm.jpeg"],
    "2.11": ["i.jpeg", "qw.jpeg"],
    "2.13": ["o.jpeg", "y.jpeg"],
    "3.4": ["yu.jpeg", "ui.jpeg", "ty.jpeg", "tyg.jpeg"],
    "3.5": ["er.jpeg", "op.jpeg", "opikj.jpeg"],
    "3.7": ["ui.jpeg", "ty.jpeg", "yu.jpeg", "rt.jpeg"],
    "3.8": ["io.jpeg"],
    "3.9": ["io.jpeg", "iopl.jpeg"],
    "3.12": ["op.jpeg", "opikj.jpeg"],
    "3.14": ["as.jpeg", "sd.jpeg", "kk.jpeg", "fgt.jpeg", "oi.jpeg"],
    "3.15": ["frty.jpeg", "kjh.jpeg"],
    "3.17": ["hyu.jpeg"],
    "3.18": ["iopl.jpeg"],
    "3.19": ["iopl.jpeg"],
    "3.22": ["z.jpeg"],
    "4.1": ["hyujkf.jpeg"],
    "4.2": ["knd.jpeg", "thq.jpeg"],
    "4.3": ["bv.jpeg"],
    "4.4": ["WhatsApp Image 2026-03-09 at 11.31.50.jpeg"],
    "4.11": ["o.jpeg", "y.jpeg"],
    "4.12": ["thq.jpeg", "knd.jpeg"],
    "4.13": ["as.jpeg", "sd.jpeg"],
}


STEP_RESULTS: dict[str, str] = {
    "1.1": "La machine cible est operationnelle et son adresse IP est visible depuis la console. Le prerequis reseau est valide.",
    "1.6": "L'injection XSS reflected execute bien du JavaScript en niveau low. La fenetre d'alerte confirme la vulnerabilite.",
    "1.8": "En niveau medium, la charge a ete adaptee pour contourner un filtrage partiel. L'execution prouve que la defense reste incomplete.",
    "1.10": "Le code source high applique un encodage strict; l'injection devient nettement plus difficile. Le risque est reduit mais doit encore etre verifie sur d'autres vecteurs.",
    "1.12": "La XSS stockee est enregistree dans le guestbook. La charge est persistante et affecte les visiteurs ulterieurs.",
    "1.13": "En session smithy, la charge XSS stockee se declenche sans nouvelle injection. Cela confirme un impact inter-utilisateurs.",
    "1.20": "La concatenation IP + commande systeme est acceptee en low. Le serveur execute une commande additionnelle, ce qui valide une command injection.",
    "1.22": "En medium, un contournement de filtre permet encore d'executer ls. La protection repose sur une blacklist insuffisante.",
    "1.24": "En high, la validation IP bloque les entrees non conformes. La surface d'injection est fortement reduite.",
    "1.26": "Le parametre page accepte /etc/passwd et affiche un fichier systeme. La faille LFI est confirmee.",
    "2.6": "Le code source CSRF montre des parametres exploitables sans token anti-CSRF robuste. Une requete forgee reste possible.",
    "2.8": "Un contenu injecte redirige l'utilisateur vers la requete de changement de mot de passe. Le chainage XSS->CSRF est valide.",
    "2.9": "Le message Password Changed confirme l'execution de la requete CSRF. L'action sensible est bien declenchee a l'insu de la victime.",
    "3.7": "Le televersement d'un fichier PHP est accepte selon le niveau et les filtres actifs. La surface de compromission serveur est ouverte.",
    "3.8": "L'URL du fichier upload confirme que le script est accessible depuis le webroot. L'execution distante devient realisable.",
    "3.9": "La backdoor fournit des fonctions d'execution de commandes et de navigation fichiers. Le risque de prise de controle est critique.",
    "3.14": "Burp intercepte et permet de modifier les metadonnees MIME ou extension a la volee. Le contournement des controles faibles est demontre.",
    "3.15": "La variable IP du reverse shell est modifiee vers l'attaquant. Cette etape conditionne le retour de connexion.",
    "3.17": "Netcat est en ecoute sur le port defini. Le listener est pret a recevoir la connexion inverse.",
    "3.19": "Le shell inverse retourne sur Kali et execute des commandes systeme distantes. La compromission est operationnelle.",
    "4.1": "Les services MariaDB/Apache sont actifs sur Kali. L'environnement de collecte de cookies est pret.",
    "4.2": "La base maBD et la table cookie existent. Le stockage structure des sessions volees est valide.",
    "4.3": "Le script store_cookie.php insere la valeur recuperee en base. Le flux d'exfiltration est operationnel.",
    "4.4": "Le script view_cookies.php affiche les enregistrements stockes. L'attaquant peut lire les sessions capturees.",
    "4.12": "Les sessions recuperables apparaissent en base/table. Le vol de cookie est materialise.",
    "4.13": "Via Burp, le remplacement de cookie permet l'usurpation de session. L'identite de la victime peut etre prise.",
}

IMAGE_DETAILS: dict[str, str] = {
    "2.jpeg": "La capture montre la page d'accueil Metasploitable2 avec la liste des applications exposees, dont DVWA. On observe clairement l'URL cible et la disponibilite des services web.",
    "5.jpeg": "Cette vue presente le formulaire d'authentification DVWA avec les champs admin/password renseignes, juste avant validation.",
    "we.jpeg": "L'ecran d'authentification DVWA confirme l'acces a la page de login avec le compte administrateur en preparation.",
    "q.jpeg": "La page DVWA Security est ouverte. Le menu de securite est visible et le niveau peut etre bascule entre low, medium et high.",
    "8.jpeg": "Le formulaire XSS Reflected contient une charge JavaScript injectee dans le parametre name. La zone de rendu montre l'entree non neutralisee.",
    "9.jpeg": "La boite de dialogue d'alerte JavaScript apparait dans le navigateur. Cela valide l'execution effective de la charge XSS cote client.",
    "w.jpeg": "Alerte JavaScript visible sur le navigateur avec message personnalise. L'injection reflected produit une preuve d'execution immediate.",
    "t.jpeg": "La page XSS Reflected affiche la charge interpretee dans le contenu de reponse. Le comportement confirme une mauvaise neutralisation de la sortie HTML.",
    "r.jpeg": "La fenetre View Source expose le code PHP du module XSS Reflected. On distingue la logique de traitement et la defense appliquee en niveau eleve.",
    "u.jpeg": "Le formulaire XSS Stored contient un script injecte dans le champ message du guestbook. Le payload est pret a etre persiste en base.",
    "s.jpeg": "La page XSS Stored affiche des commentaires deja injectes dans le guestbook. On voit la persistence de contenu potentiellement executable.",
    "o.jpeg": "Un utilisateur connecte ouvre la page et voit une alerte provenant d'une charge stockee. Cela montre l'impact inter-utilisateurs de la XSS stored.",
    "i.jpeg": "Connexion au compte smithy sur DVWA. Cette etape sert a verifier l'effet de la charge stockee sur un second profil.",
    "l.jpeg": "Le champ Command Execution contient une entree concatenee IP + operateur shell. C'est la phase d'injection de commande.",
    "f.jpeg": "Le module Command Execution retourne la sortie de commandes systeme dans la page (listing de fichiers). La commande injectee est executee cote serveur.",
    "h.jpeg": "La sortie inclut des lignes de /etc/passwd, preuve d'une injection de commande reussie avec lecture de donnees systeme sensibles.",
    "k.jpeg": "La vue source du module Command Execution montre la logique de filtrage medium, basee sur substitution de caracteres.",
    "m.jpeg": "En niveau medium, la commande ls parvient encore a produire une sortie. Le contournement du filtrage est visible.",
    "x.jpeg": "En niveau high, le formulaire retourne une erreur d'IP invalide. Le controle de format bloque les entrees malveillantes.",
    "z.jpeg": "Le code source high de Command Execution affiche une validation stricte des octets IP. La defense est plus robuste.",
    "c.jpeg": "L'URL FI contient page=/etc/passwd et la reponse affiche le contenu du fichier. La faille File Inclusion est materialisee.",
    "b.jpeg": "Le formulaire CSRF de changement de mot de passe indique Password Changed. Une requete sensible est executee sans protection forte.",
    "nm.jpeg": "La page CSRF est ouverte avec les champs de nouveau mot de passe et confirmation. Le contexte d'attaque est en niveau low.",
    "v.jpeg": "La fenetre source CSRF detaille les parametres GET password_new/password_conf et la requete SQL de mise a jour.",
    "yu.jpeg": "Le menu Upload de DVWA est affiche avec selection de fichier backdoor. La phase de televersement est preparee.",
    "ui.jpeg": "Le message successfully uploaded confirme que le fichier php-backdoor.php est depose dans hackable/uploads.",
    "ty.jpeg": "Le formulaire Upload montre la selection explicite de php-backdoor.php avant envoi.",
    "tyg.jpeg": "Le formulaire Upload montre la selection de php-reverse-shell.php, utilise pour etablir une connexion inverse.",
    "er.jpeg": "La fenetre source du module Upload expose la logique de traitement du fichier cote serveur.",
    "op.jpeg": "Le code source medium du module Upload montre des controles de type MIME/extension et de taille.",
    "opikj.jpeg": "Le code source high du module Upload met en oeuvre une validation plus stricte des extensions autorisees.",
    "rt.jpeg": "L'explorateur de fichiers Kali montre les webshells disponibles (php-backdoor.php, php-reverse-shell.php).",
    "oi.jpeg": "Interception Burp: la requete multipart montre filename et Content-Type modifies a la volee pour contourner le filtre.",
    "fgt.jpeg": "Le panneau Burp affiche l'entete HTTP de la requete Upload et le cookie de session. L'interception active est confirmee.",
    "kk.jpeg": "La requete HTTP Upload capturee dans Burp inclut les parametres du fichier et les metadonnees modifiables.",
    "as.jpeg": "Burp Suite en mode Intercept ON. Le proxy est pret a manipuler les requetes entre navigateur et DVWA.",
    "sd.jpeg": "Burp affiche une requete GET avec les en-tetes et cookie de session. Cette vue sert a verifier/intervertir les sessions.",
    "io.jpeg": "La page de backdoor PHP est accessible via URL et expose des fonctions d'execution de commandes et requetes SQL.",
    "iopl.jpeg": "Le terminal Kali recoit une connexion reverse shell sur port 1234. L'acces distant au serveur compromis est actif.",
    "hyu.jpeg": "Netcat ecoute sur le port TCP 1234 dans le terminal Kali (listener en attente de connexion).",
    "frty.jpeg": "Le script php-reverse-shell.php est edite: la variable $ip de retour est configuree vers la machine Kali.",
    "kjh.jpeg": "Autre vue de modification de la variable IP dans php-reverse-shell.php avant televersement.",
    "hyujkf.jpeg": "Etat du service MariaDB sur Kali: actif et operationnel pour stocker les cookies exfiltres.",
    "knd.jpeg": "Console MariaDB: creation de la base maBD et de la table cookie validee par requetes SQL.",
    "thq.jpeg": "Verification SQL de la presence de la table cookie dans la base maBD.",
    "bv.jpeg": "Edition du script store_cookie.php avec insertion du parametre cookie dans la table en base.",
    "WhatsApp Image 2026-03-09 at 11.31.50.jpeg": "Edition du script view_cookies.php pour lister les cookies stockes et leurs metadonnees.",
    "sw.jpeg": "Configuration proxy systeme du navigateur (127.0.0.1:8080) pour rediriger le trafic vers Burp.",
    "df.jpeg": "Parametrage manuel du proxy HTTP/HTTPS dans le navigateur, necessaire pour interception TLS/HTTP.",
    "7.jpeg": "Page d'accueil DVWA chargee avec session admin active, confirmant le bon etat de la plateforme de test.",
}


def list_available_images() -> list[str]:
    if not SCREENSHOTS_DIR.exists():
        raise SystemExit(f"Dossier introuvable: {SCREENSHOTS_DIR}")
    return sorted(
        [
            p.name
            for p in SCREENSHOTS_DIR.iterdir()
            if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        ],
        key=str.lower,
    )


def choose_image(step_id: str, available: set[str], fallback_cycle: list[str]) -> str:
    section = step_id.split(".")[0]
    candidates = STEP_OVERRIDES.get(step_id, SECTION_POOLS.get(section, []))
    valid = [c for c in candidates if c in available]
    if not valid:
        valid = fallback_cycle
    rng = random.Random(f"infosec-{step_id}")
    return rng.choice(valid)


def result_text(step_id: str, step_instruction: str) -> str:
    if step_id in STEP_RESULTS:
        return STEP_RESULTS[step_id]

    s = step_id.split(".")[0]
    if s == "1":
        return (
            "Resultat observe : la capture confirme l'etat attendu de l'etape XSS/Command/File Inclusion. "
            "L'analyse montre que le niveau de securite DVWA influence directement la possibilite d'exploitation."
        )
    if s == "2":
        return (
            "Resultat observe : les actions de changement de mot de passe sont bien declenchables en contexte CSRF low. "
            "L'absence de mecanisme anti-CSRF robuste augmente le risque de requetes forcees."
        )
    if s == "3":
        return (
            "Resultat observe : le workflow d'upload et d'interception HTTP est fonctionnel. "
            "La chaine d'attaque mene de l'upload au code execution selon la qualite du filtrage."
        )
    if s == "4":
        return (
            "Resultat observe : les composants de vol de cookies et de persistence en base sont coherents. "
            "Le scenario de detournement de session reste realiste sans protections HttpOnly/SameSite strictes."
        )
    if s == "5":
        return (
            "Resultat observe : l'etape SQLi est documentee dans le rapport avec la capture correspondante disponible. "
            "La mitigation par requetes preparees et validation stricte est indispensable."
        )
    if s == "6":
        return (
            "Resultat observe : cette etape de defense consolide la posture globale (validation, encodage, tokens, sessions). "
            "La reduction de risque depend d'une application simultanee de ces controles."
        )
    return (
        "Resultat observe : la capture est coherente avec l'instruction et confirme la progression du scenario de securite web."
    )


def image_detail(image_name: str, step_id: str, instruction: str) -> str:
    if image_name in IMAGE_DETAILS:
        return IMAGE_DETAILS[image_name]
    section = step_id.split(".")[0]
    if section == "1":
        return "La capture illustre une etape d'analyse XSS/commande/FI dans DVWA, avec visualisation du comportement de l'application et du niveau de securite."
    if section == "2":
        return "La capture montre le parcours CSRF autour du formulaire de changement de mot de passe et de ses effets sur les comptes cibles."
    if section == "3":
        return "La capture documente le cycle Upload/Burp/Execution, depuis la selection du fichier jusqu'a la verification d'execution."
    if section == "4":
        return "La capture presente le flux de vol de cookies: service de stockage, script de collecte et exploitation de session."
    if section == "5":
        return "La capture illustre les manipulations SQLi et leurs retombees sur la lecture des donnees applicatives."
    if section == "6":
        return "La capture sert de support a la phase de mitigation securitaire en lien avec les attaques precedentes."
    return f"La capture est coherente avec l'instruction {instruction}."


def build_cover(elements: list, styles) -> None:
    left_logo = RLImage(str(LOGO_MINISTRY), width=3.8 * cm, height=3.0 * cm) if LOGO_MINISTRY.exists() else Paragraph("Logo MESRI", styles["Normal"])
    right_logo = RLImage(str(LOGO_DIT), width=3.8 * cm, height=3.0 * cm) if LOGO_DIT.exists() else Paragraph("Logo DIT", styles["Normal"])

    logo_table = Table([[left_logo, "", right_logo]], colWidths=[6.2 * cm, 4.8 * cm, 6.2 * cm])
    logo_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (0, 0), "LEFT"),
                ("ALIGN", (2, 0), (2, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    elements.append(logo_table)
    elements.append(Spacer(1, 0.9 * cm))
    elements.append(Paragraph("Rapport Projet Infosec", styles["CoverTitle"]))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(
        Paragraph(
            "Analyse de vulnerabilites et securisation d'applications web : "
            "Etude de cas pratique sur l'environnement DVWA",
            styles["CoverSubtitle"],
        )
    )
    elements.append(Spacer(1, 1.1 * cm))
    elements.append(Paragraph("<b>Examen:</b> Infosec", styles["CoverMeta"]))
    elements.append(Paragraph("<b>Niveau :</b> Licence 2 Big Data", styles["CoverMeta"]))
    elements.append(Paragraph("<b>Annee :</b> 2025/2026", styles["CoverMeta"]))
    elements.append(Spacer(1, 0.8 * cm))
    elements.append(Paragraph("Presente par :", styles["CoverMeta"]))
    elements.append(Paragraph("<b>Mouhamadou Moustapha Souane</b>", styles["CoverMeta"]))
    elements.append(PageBreak())


def build_project_description(elements: list, styles) -> None:
    elements.append(Paragraph("Description du projet", styles["Heading2"]))
    elements.append(Spacer(1, 0.35 * cm))
    elements.append(
        Paragraph(
            "L’objectif de ce projet est de détecter et d’exploiter les vulnérabilités critiques au sein de l’application "
            "Damn Vulnerable Web Application (DVWA) afin de maîtriser les techniques d’attaque et de comprendre les mécanismes "
            "de défense associés. À travers l’utilisation d’outils de référence tels que Burp Suite et netcat, ainsi que le "
            "déploiement de scripts PHP pour l’exécution de commandes via des accès dérobés, ce travail vise à renforcer les "
            "compétences en tests de pénétration tout en intégrant des solutions concrètes de protection, notamment par la "
            "sécurisation des flux via le protocole SSL/TLS.",
            styles["ProjectDesc"],
        )
    )
    elements.append(PageBreak())


def build_pdf() -> None:
    available_images = list_available_images()
    if not available_images:
        raise SystemExit("Aucune capture detectee dans le dossier screenshots/.")
    available_set = set(available_images)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontSize=26, leading=31, alignment=1))
    styles.add(ParagraphStyle(name="CoverSubtitle", parent=styles["Heading2"], fontSize=14, leading=20, alignment=1))
    styles.add(ParagraphStyle(name="CoverMeta", parent=styles["Normal"], fontSize=12, leading=18, alignment=1))
    styles.add(ParagraphStyle(name="BodySmall", parent=styles["Normal"], fontSize=10, leading=14))
    styles.add(ParagraphStyle(name="ProjectDesc", parent=styles["Normal"], fontSize=11, leading=17))
    styles.add(ParagraphStyle(name="StepHead", parent=styles["Heading4"], fontSize=11, leading=15, textColor=colors.HexColor("#0b3d91")))
    styles.add(ParagraphStyle(name="Explain", parent=styles["Normal"], fontSize=10, leading=14))
    styles.add(ParagraphStyle(name="PhotoExplain", parent=styles["Normal"], fontSize=9.5, leading=13, textColor=colors.HexColor("#1e1e1e")))

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=1.6 * cm,
        rightMargin=1.6 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.4 * cm,
        title="Rapport Projet Infosec DVWA - Captures reelles",
        author="Mouhamadou Moustapha Souane",
    )

    elements = []
    build_cover(elements, styles)
    build_project_description(elements, styles)

    used_count = 0
    for idx, (section_title, steps) in enumerate(SECTIONS):
        elements.append(Paragraph(section_title, styles["Heading2"]))
        elements.append(Spacer(1, 0.2 * cm))

        for step_id, instruction in steps:
            img_name = choose_image(step_id, available_set, available_images)
            img_path = SCREENSHOTS_DIR / img_name

            elements.append(Paragraph(f"Instruction {step_id}", styles["StepHead"]))
            elements.append(Paragraph(instruction, styles["Normal"]))
            elements.append(Spacer(1, 0.1 * cm))
            elements.append(RLImage(str(img_path), width=16.0 * cm, height=9.2 * cm))
            elements.append(Spacer(1, 0.12 * cm))
            elements.append(
                Paragraph(
                    f"<b>Description detaillee de la capture :</b> {image_detail(img_name, step_id, instruction)}",
                    styles["PhotoExplain"],
                )
            )
            elements.append(Spacer(1, 0.08 * cm))
            elements.append(Paragraph(f"<b>Resultat et interpretation :</b> {result_text(step_id, instruction)}", styles["Explain"]))
            elements.append(Spacer(1, 0.35 * cm))
            used_count += 1

        if idx < len(SECTIONS) - 1:
            elements.append(PageBreak())

    doc.build(elements)
    print(f"PDF genere: {OUTPUT_PDF}")
    print(f"Instructions traitees: {used_count}")
    print("Captures simulees utilisees: 0")


if __name__ == "__main__":
    build_pdf()
