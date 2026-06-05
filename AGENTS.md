# AGENTS.md — Apache Solr Website

This file helps AI agents understand the repository structure and workflow.

## What this repo is

Static website for [solr.apache.org](https://solr.apache.org), built with [Pelican](https://getpelican.com/) (Python static site generator). Content is written in Markdown. The build runs inside Docker to ensure a reproducible environment.

## How to build and preview

```bash
./build.sh -l    # build and serve with live reload at http://localhost:8000
./build.sh       # one-shot build into output/
./build.sh -h    # show all options
```

Docker must be installed. The script auto-builds the image if missing, and auto-rebuilds it if `requirements.txt` is newer than the cached image.

## Key files and directories

| Path | Purpose |
|---|---|
| `pelicanconf.py` | Pelican configuration; defines `SOLR_LATEST_RELEASE` and other site-wide variables |
| `content/pages/` | All site pages as Markdown files |
| `content/pages/blogposts/` | Blog posts |
| `themes/solr/templates/` | Jinja2 HTML templates |
| `themes/solr/static/` | CSS, JS, images |
| `plugins/` | Local Pelican plugins (Python) |
| `requirements.in` | Direct Python dependencies (human-editable) |
| `requirements.txt` | Hash-verified lockfile generated from `requirements.in` — do not edit by hand |
| `Dockerfile` | Base image pinned by digest; Dependabot tracks it |
| `.github/dependabot.yml` | Dependabot config for pip, docker, and github-actions ecosystems |

## Updating dependencies

Edit `requirements.in`, then regenerate the lockfile and rebuild the image:

```bash
./build.sh --lock -b
```

Or in two steps:

```bash
./build.sh --lock   # regenerates requirements.txt inside Docker
./build.sh -b       # rebuilds the Docker image
```

## Updating Solr release versions

Edit `pelicanconf.py` and bump `SOLR_LATEST_RELEASE`, `SOLR_LATEST_RELEASE_DATE`, and `SOLR_PREVIOUS_MAJOR_RELEASE`. These variables propagate throughout the theme automatically.

## Templates and pages

- Templates use Jinja2. Most pages use the `base.html` template.
- A page can specify a custom template with `Template: my-template` in its Markdown front matter.
- The `jinja2content` plugin allows Jinja2 expressions directly inside Markdown pages.

## Branch and deploy model

| Branch | Purpose |
|---|---|
| `main` | Staging — auto-deployed to [solr.staged.apache.org](https://solr.staged.apache.org) |
| `production` | Live site — merge `main` → `production` to publish |

Never commit directly to `production`. Always go through `main` (and a PR).

## CI

- Pull requests: Pelican build only (no publish), defined in `.github/workflows/pr-build-pelican.yml`
- Push to `main`/`production`: full build + publish, defined in `.github/workflows/build-pelican.yml`
- All GitHub Actions refs are pinned to commit SHAs and tracked by Dependabot.
