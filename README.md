# True-Osint
This project is created for educational and cybersecurity research purposes only. The author is not responsible for any illegal or malicious use of this tool. Please ensure you respect local laws and the privacy of others.


## Usage

Install dependencies:

pip install -r requirements.txt

Run the CLI tool:

python main.py email@example.com

You can also launch interactive mode (email prompt):

python main.py

Run the web interface:

python main.py --web

Then open:

http://localhost:8000

## Detection logic

The tool now prioritizes public, email-based signals:

- Gravatar linked accounts (high confidence)
- GitHub users exposing the exact email on public profile (high confidence)
- GitHub public commits authored with the exact email (medium confidence)
- Public profile pages containing the exact email text (medium confidence)

If no account is returned, it usually means no public evidence links that email to a profile.
