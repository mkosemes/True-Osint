from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from core.domain import domain_has_mx
from core.email_utils import extract_domain, is_valid_email
from core.gravatar import gravatar_lookup
from modules.social_accounts import find_social_accounts


def _confidence_badge(confidence):
    labels = {
        "high": ("badge high", "high"),
        "medium": ("badge medium", "medium"),
        "low": ("badge low", "low"),
    }
    css_class, text = labels.get(confidence, ("badge", confidence))
    return f"<span class='{css_class}'>{escape(text)}</span>"


def _render_page(email="", error="", result=None):
    verified_rows = ""
    probable_rows = ""
    diagnostics_html = ""
    if result and result.get("diagnostics"):
        diagnostics_html = "<ul class='warnings'>" + "".join(
            f"<li>{escape(message)}</li>" for message in result["diagnostics"]
        ) + "</ul>"

    if result and result.get("accounts"):
        for account in result["accounts"]:
            row = (
                "<tr>"
                f"<td>{escape(account['site'])}</td>"
                f"<td><a href='{escape(account['url'])}' target='_blank' rel='noopener noreferrer'>{escape(account['url'])}</a></td>"
                f"<td>{escape(account['source'])}</td>"
                f"<td>{_confidence_badge(account['confidence'])}</td>"
                "</tr>"
            )
            if account.get("confidence") in {"high", "medium"}:
                verified_rows += row
            else:
                probable_rows += row

    report = ""
    if result:
        verified_table = (
            "<h3>Comptes verifies (preuves publiques)</h3>"
            "<table>"
            "<thead><tr><th>Plateforme</th><th>URL</th><th>Source</th><th>Confiance</th></tr></thead>"
            f"<tbody>{verified_rows or '<tr><td colspan=\"4\">Aucun compte verifie</td></tr>'}</tbody>"
            "</table>"
        )
        probable_table = (
            "<h3>Comptes probables (similarite pseudo)</h3>"
            "<table>"
            "<thead><tr><th>Plateforme</th><th>URL</th><th>Source</th><th>Confiance</th></tr></thead>"
            f"<tbody>{probable_rows or '<tr><td colspan=\"4\">Aucun compte probable</td></tr>'}</tbody>"
            "</table>"
        )
        report = (
            "<div class='card result'>"
            "<div class='meta-grid'>"
            f"<p><span>Email</span>{escape(result['email'])}</p>"
            f"<p><span>Domaine actif (MX)</span>{result['domain_active']}</p>"
            f"<p><span>Gravatar</span>{escape(result['gravatar'] or 'Aucun')}</p>"
            "</div>"
            f"{verified_table}"
            f"{probable_table}"
            f"{diagnostics_html}"
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
    :root {{
      --bg: #f2f5ff;
      --card: #ffffff;
      --text: #1d2532;
      --muted: #5c6778;
      --border: #dde3ef;
      --primary: #4a63f6;
      --high: #087f5b;
      --medium: #9c6b00;
      --low: #3f4b5e;
      --danger: #b00020;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, Arial, sans-serif;
      color: var(--text);
      background: radial-gradient(circle at top, #e8eeff 0%, var(--bg) 45%, #edf1f9 100%);
      min-height: 100vh;
      padding: 24px;
    }}
    .container {{ max-width: 980px; margin: 0 auto; }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px;
      box-shadow: 0 12px 32px rgba(42, 57, 102, 0.08);
    }}
    .hero h1 {{ margin: 0; font-size: 1.45rem; }}
    .hero p {{ margin: 8px 0 0; color: var(--muted); }}
    form {{ display: flex; gap: 10px; margin: 14px 0 8px; }}
    input[type="email"] {{
      flex: 1;
      padding: 12px 13px;
      border: 1px solid var(--border);
      border-radius: 10px;
      font-size: 0.95rem;
      outline: none;
    }}
    input[type="email"]:focus {{ border-color: var(--primary); box-shadow: 0 0 0 3px rgba(74, 99, 246, 0.15); }}
    button {{
      border: 0;
      background: var(--primary);
      color: white;
      border-radius: 10px;
      font-weight: 600;
      padding: 12px 16px;
      cursor: pointer;
    }}
    .error {{ color: var(--danger); margin: 6px 0 0; }}
    .result {{ margin-top: 16px; }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 10px;
      margin-bottom: 8px;
    }}
    .meta-grid p {{
      margin: 0;
      padding: 10px;
      background: #f7f9fe;
      border: 1px solid #e3e8f5;
      border-radius: 10px;
      font-size: 0.92rem;
      overflow-wrap: anywhere;
    }}
    .meta-grid span {{ display: block; color: var(--muted); font-size: 0.76rem; margin-bottom: 3px; text-transform: uppercase; }}
    h3 {{ margin: 14px 0 8px; font-size: 1rem; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; }}
    th, td {{ border: 1px solid var(--border); text-align: left; padding: 8px; font-size: 0.88rem; vertical-align: top; }}
    th {{ background: #f3f6ff; }}
    a {{ color: #2340dd; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .badge {{
      display: inline-block;
      border-radius: 999px;
      padding: 3px 8px;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      border: 1px solid transparent;
    }}
    .badge.high {{ color: var(--high); background: #e7f7f1; border-color: #b8ebd9; }}
    .badge.medium {{ color: var(--medium); background: #fff4dc; border-color: #f1d799; }}
    .badge.low {{ color: var(--low); background: #eef1f7; border-color: #d6deec; }}
    .warnings {{
      margin: 10px 0 0;
      padding: 10px 12px 10px 26px;
      border-radius: 10px;
      border: 1px solid #f6dda7;
      background: #fff9eb;
      color: #8a5c00;
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card hero">
      <h1>Recherche de comptes associes a une adresse email</h1>
      <p>Le moteur combine preuves publiques (verifiees) et similarite de pseudo (probables).</p>
      <form method="get" action="/">
        <input type="email" name="email" placeholder="email@example.com" value="{escape(email)}" required />
        <button type="submit">Rechercher</button>
      </form>
      {error_html}
    </div>
    {report}
  </div>
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
        lookup = find_social_accounts(email, return_details=True)
        result = {
            "email": email,
            "domain_active": domain_has_mx(domain),
            "gravatar": gravatar_lookup(email),
            "accounts": lookup["accounts"],
            "diagnostics": lookup["diagnostics"],
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
