"""Build the static site from templates/ into dist/."""
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

# Shadow site: keep it out of search engines. Set to False when the site goes live.
NOINDEX = True

# Per language: (template, output folder, title, menu label). Add "en" here later, with
# output folders that start with "en/", and move the texts in base.html to a translation.
PAGES = {
    "nl": [
        ("home.html", "", "Gijsbert Voorneveld", "Home"),
        ("diensten.html", "diensten", "Diensten", "Diensten"),
        ("over-mij.html", "over-mij", "Over mij", "Over mij"),
        ("contact.html", "contact", "Contact", "Contact"),
    ],
}


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
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(ROOT / "static", DIST / "static")
    for lang, pages in PAGES.items():
        for template, folder, title, _ in pages:
            # Relative links work locally, on github.io/<repo>/ and on the own domain.
            root = "../" * len(Path(folder).parts)
            menu = [
                {"href": href(root, f), "label": label, "current": f == folder}
                for _, f, _, label in pages
            ]
            html = env.get_template(f"{lang}/{template}").render(
                lang=lang,
                root=root,
                home=menu[0]["href"],
                title=title,
                menu=menu,
                noindex=NOINDEX,
                hide_cta=template == "contact.html",
            )
            target = DIST / folder / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build()
