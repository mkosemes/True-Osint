from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from core.domain import domain_has_mx
from core.email_utils import extract_domain, is_valid_email
from core.gravatar import gravatar_lookup
from modules.social_accounts import find_social_accounts


def _render_page(email="", error="", result=None):
    rows = ""
    if result and result.get("accounts"):
        for account in result["accounts"]:
            rows += (
                "<tr>"
                f"<td>{escape(account['site'])}</td>"
                f"<td><a href='{escape(account['url'])}' target='_blank'>{escape(account['url'])}</a></td>"
                f"<td>{escape(account['source'])}</td>"
                f"<td>{escape(account['confidence'])}</td>"
                "</tr>"
            )
    elif result:
        rows = "<tr><td colspan='4'>Aucun compte associe trouve</td></tr>"

    report = ""
    if result:
        report = (
            "<div class='card'>"
            f"<p><strong>Email:</strong> {escape(result['email'])}</p>"
            f"<p><strong>Domaine actif (MX):</strong> {result['domain_active']}</p>"
            f"<p><strong>Gravatar:</strong> {escape(result['gravatar'] or 'Aucun')}</p>"
            "<table>"
            "<thead><tr><th>Plateforme</th><th>URL</th><th>Source</th><th>Confiance</th></tr></thead>"
            f"<tbody>{rows}</tbody>"
            "</table>"
            "</div>"
        )

    error_html = f"<p class='error'>{escape(error)}</p>" if error else ""

    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Recherche de comptes lies a un email</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 32px auto; padding: 0 16px; }}
    h1 {{ margin-bottom: 8px; }}
    form {{ display: flex; gap: 8px; margin: 16px 0 12px; }}
    input[type="email"] {{ flex: 1; padding: 10px; font-size: 14px; }}
    button {{ padding: 10px 14px; cursor: pointer; }}
    .error {{ color: #b00020; }}
    .card {{ background: #f8f9fb; border: 1px solid #d5dbe3; border-radius: 8px; padding: 14px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ border: 1px solid #dde3eb; text-align: left; padding: 8px; font-size: 14px; }}
    th {{ background: #eef2f7; }}
  </style>
</head>
<body>
  <h1>Recherche de comptes associes a une adresse email</h1>
  <p>Entrez un email pour obtenir des comptes verifies (high/medium) et probables (low).</p>
  <form method="get" action="/">
    <input type="email" name="email" placeholder="email@example.com" value="{escape(email)}" required />
    <button type="submit">Rechercher</button>
  </form>
  {error_html}
  {report}
</body>
</html>"""


class EmailLookupHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        email = params.get("email", [""])[0].strip()

        if not email:
            self._send_html(_render_page())
            return

        if not is_valid_email(email):
            self._send_html(_render_page(email=email, error="Adresse email invalide."))
            return

        domain = extract_domain(email)
        result = {
            "email": email,
            "domain_active": domain_has_mx(domain),
            "gravatar": gravatar_lookup(email),
            "accounts": find_social_accounts(email),
        }
        self._send_html(_render_page(email=email, result=result))

    def log_message(self, format, *args):
        return

    def _send_html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(host="0.0.0.0", port=8000):
    server = HTTPServer((host, port), EmailLookupHandler)
    print(f"Interface web disponible sur http://{host}:{port}")
    print("Appuyez sur CTRL+C pour arreter.")
    server.serve_forever()
