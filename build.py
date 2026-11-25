"""Build the static site from templates/ and content/ into dist/."""
import shutil
import tomllib
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
DOMAIN = "https://voorneveldconsulting.nl"

# Shadow site: keep it out of search engines. Set to False when the site goes live.
NOINDEX = True

# (template, output folder, title, menu label or None, description)
PAGES = [
    ("home.html", "", "Gijsbert Voorneveld", None,
     "Management consultant en projectleider voor fusies, nieuwe technologie en betere bedrijfsvoering, met veel ervaring in de media."),
    ("diensten.html", "diensten", "Diensten", "Diensten",
     "Analyse, besluitvorming en begeleiding bij organisatiebrede veranderingen."),
    ("cases.html", "cases", "Cases", "Cases",
     "Voorbeelden van veranderingen die Gijsbert Voorneveld begeleidde, en voor wie."),
    ("over-mij.html", "over-mij", "Over mij", "Over mij",
     "Wie is Gijsbert Voorneveld: achtergrond, loopbaan en drijfveren."),
    ("contact.html", "contact", "Contact", "Contact",
     "Kennismaken met Gijsbert Voorneveld: bij de koffie, online of op locatie."),
    ("privacy.html", "privacy", "Privacy", None,
     "Hoe deze site met gegevens omgaat."),
]


def href(root, folder):
    return f"{root}{folder}/index.html" if folder else f"{root}index.html"


def build():
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    content = tomllib.loads((ROOT / "content/nl.toml").read_text(encoding="utf-8"))
    content["cases_by_id"] = {c["id"]: c for c in content["cases"]}
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(ROOT / "static", DIST / "static")

    def render(template, folder, title, description, root, target):
        menu = [
            {"href": href(root, f), "label": label, "current": f == folder}
            for _, f, _, label, _ in PAGES if label
        ]
        html = env.get_template(f"nl/{template}").render(
            **content,
            lang="nl",
            root=root,
            title=title,
            description=description,
            url=f"{DOMAIN}/{folder}/" if folder else f"{DOMAIN}/",
            domain=DOMAIN,
            menu=menu,
            noindex=NOINDEX,
            hide_cta=template in ("contact.html", "privacy.html", "404.html"),
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    for template, folder, title, _, description in PAGES:
        # Relative links work locally, on github.io/<repo>/ and on the own domain.
        root = "../" * len(Path(folder).parts)
        render(template, folder, title, description, root, DIST / folder / "index.html")

    # The 404 page is served at any depth, so it needs absolute links.
    render("404.html", "404", "Pagina niet gevonden", "Deze pagina bestaat niet.",
           "/voorneveld-website/" if NOINDEX else "/", DIST / "404.html")

    if not NOINDEX:
        urls = "".join(
            f"<url><loc>{DOMAIN}/{f + '/' if f else ''}</loc></url>" for _, f, *_ in PAGES
        )
        (DIST / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
            encoding="utf-8",
        )


if __name__ == "__main__":
    build()
