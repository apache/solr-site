# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the source code repository for the Apache Solr website (solr.apache.org). The site is built using Pelican (Python-based static site generator) and deployed through GitHub Actions to Apache infrastructure.

## Build and Development Commands

### Building the site locally

The easiest way is with Docker (recommended):

```bash
./build.sh -l
```

This starts a live-reloading development server at http://localhost:8000.

For a one-time build without live reload:

```bash
./build.sh
```

The build script automatically:
- Creates a Docker image with Python and all dependencies
- Rebuilds the image if `requirements.txt` changes
- Outputs the site to `output/` directory

### Manual installation (without Docker)

If you need to build without Docker:

```bash
# Create virtual environment
python3 -m venv myenv
source myenv/bin/activate  # or `myenv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Build site
pelican content -o output

# Build with live reload
pelican content -o output --autoreload --listen
```

## Deployment Workflow

**CRITICAL**: Never commit directly to `production` branch. All changes must go through `main` first.

1. **Development**: Make changes and commit to feature branches, create PRs to `main`
2. **Staging**: When merged to `main`, GitHub Actions automatically builds and deploys to https://solr.staged.apache.org
3. **Production**: After verifying staging, merge `main` → `production` (use merge commit, not squash) to deploy to https://solr.apache.org

Small edits can be made directly in GitHub's web UI.

## Repository Structure

### Content Organization

- `content/pages/` - Main website pages (Markdown files)
  - `content/pages/blogposts/` - Blog posts
  - `content/pages/operator/` - Solr Operator documentation
- `content/images/` - Images and static assets
- `content/solr/` - Solr-specific content
- `content/doap/` - DOAP project description files

### Themes and Templates

- `themes/solr/` - Custom Pelican theme for Solr site
  - `themes/solr/templates/` - Jinja2 templates for page layouts
  - `themes/solr/static/` - CSS, JavaScript, and static assets

### Plugins

The site uses custom Pelican plugins in `plugins/`:

- **extract_toc** - Extracts table of contents from Markdown
- **jinja2content** - Enables Jinja2 templating in Markdown content
- **regex_replace** - Regex-based text replacement in content
- **age_days_lt** - Date/age comparison utilities
- **vex** - Security vulnerability disclosure system (processes `vex-input.json`)

## Configuration

### Main Configuration File: `pelicanconf.py`

Key settings to update during releases:

```python
SOLR_LATEST_RELEASE = '9.9.0'  # Latest patch version
SOLR_LATEST_RELEASE_DATE = datetime(2025, 7, 24)
SOLR_PREVIOUS_MAJOR_RELEASE = '8.11.4'  # Previous major version

SOLR_OPERATOR_LATEST_RELEASE = 'v0.9.1'  # Operator version
SOLR_OPERATOR_LATEST_RELEASE_DATE = datetime(2025, 3, 25)
```

These variables control:
- Download page version references
- Links to source code, javadocs, PGP, and SHA512 files
- Version-specific messaging throughout the site

### Version Numbering Conventions

The configuration uses underscores in artifact filenames (e.g., `6_3_0`) while displaying dots in HTML (e.g., `6.3.0`).

## Security Vulnerability Tracking

The site includes a VEX (Vulnerability Exploitability eXchange) system:

- **Input**: `vex-input.json` - JSON array of CVE entries with analysis
- **Plugin**: `plugins/vex/` - Processes VEX data for display on security page
- **Output**: Generates security disclosures on the website

When adding new CVE information, edit `vex-input.json` following the existing structure with fields:
- `ids` - CVE identifiers
- `versions` - Affected Solr versions
- `jars` - Affected JAR files
- `analysis` - State (exploitable/not_affected) and details

## Apache Infrastructure Integration

- `.asf.yaml` - ASF infrastructure configuration
  - Defines staging/production branch behavior
  - Configures GitHub settings (merge buttons, protected branches)
  - Sets up email notifications for issues/PRs to mailing lists
- `.github/workflows/` - CI/CD pipelines
  - `build-pelican.yml` - Builds and deploys main/production branches
  - `pr-build-pelican.yml` - Validates PRs without deploying

## Pelican-Specific Details

- **Theme**: Custom theme at `themes/solr`
- **Markdown Extensions**: Configured in `pelicanconf.py` with TOC, code highlighting, and metadata support
- **Static Resource Versioning**: Uses directory hash suffix (via `checksumdir`) to bust caches on updates
- **Template Pages**: `.htaccess` is generated from `htaccess.template`

## Release Manager Tasks

During a Solr release, update these items:

1. Bump version numbers in `pelicanconf.py`
2. Update release dates
3. Add any new CVE disclosures to `vex-input.json`
4. Update download links (handled automatically by templates once version is updated)

**Note**: JavaDoc and Reference Guide publishing happens via SVN (not this repo) - see Release Manager documentation.
