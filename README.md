# Voorneveld Consulting website

Static site: `build.py` turns the Jinja templates into plain HTML in `dist/`. Every push to
`main` publishes it to GitHub Pages. This repository is public.

- Services, cases and clients: `content/nl.toml`
- Other texts: `templates/nl/`
- Menu, footer and contact block: `templates/base.html`
- Styling and images: `static/`

## Build locally

One-time setup:

```bash
~/.local/bin/uv venv --python 3.12 .venv
~/.local/bin/uv pip install --python .venv/bin/python -r requirements.txt
```

Build and open:

```bash
.venv/bin/python build.py
open dist/index.html
```
