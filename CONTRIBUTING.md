<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stux.group/logo-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stux.group/logo-dark.png"><img src="https://global.media.stux.group/logo-dark.png" height="80" alt="Stux.Group Logo"></picture>
</p>

# Contributing to Soonpage

Soonpage is a [Stux.Group](https://stux.group) project — the repository is not
open to public pull requests. This document exists for anyone with write
access to the repo who wants to work on it consistently.

## Local setup

Just clone the repo and run `./dev-server.sh [port]` (or `dev-server.bat [port]`
on Windows) — starts PHP's built-in server pointed at the directory, since it's
a static site with no build step. Then open `http://127.0.0.1:8000`.

## Project conventions

- **Plain static HTML.** No framework, no build step. Barlow and Font Awesome
  are self-hosted under `assets/` (not loaded from a CDN) — if you bump the
  Font Awesome version or add font weights, update `assets/` and re-check
  which files each page actually references.
- Deployed via GitHub Pages to [soonpage.stux.group](https://soonpage.stux.group)
  (see `CNAME`) — pushing to `main` deploys automatically.
- `maintenancepage` is a sister repo based on this one's design — if you
  change shared styling/structure here (theme toggle, social links, legal
  link, animated background), consider whether it should change there too.
- The sitemap (`sitemap.xml`, `sitemap/index.html`, `robots.txt`) is generated: after adding or removing a page, edit the `PAGES` list in `scripts/build-sitemap.py` and run `python scripts/build-sitemap.py`, then commit the result

## Discord previews and icons

- Every page except `404.html` has a Discord link preview: a pre-built `<script id="discord:component-embed">` block in its `<head>`, written by `python scripts/build-discord-embeds.py` from the page's `<title>`/`<meta name="description">` and the `PAGES` list (`build-sitemap.py` runs it too). Re-run it after changing a page's title or description, or adding a page; `--check` only reports stale pages
- The icon set is `favicon.ico`, `apple-touch-icon.png`, `site.webmanifest` and `assets/img/icon-*.png`. Every page's `<head>` carries the same four tags for them (`favicon.ico`, `icon-512.png`, `apple-touch-icon.png`, `site.webmanifest`); copy them as-is into any new page

## Tests

Run `bash tests/run.sh` before every release. It's plain Python `unittest` (3.8+, no dependencies) and checks the version, the changelog page's parser (run under Node.js, skipped if it isn't installed), every Discord preview and the icon set. CI runs it on every push.

## Versioning and changelog

- Soonpage uses [Date Versioning](https://datevers.ing): the version is the UTC release date as `YY.MM.DD`, with `-1`, `-2`… for later releases the same UTC day (check `git tag` for that date first). Use `date -u +%y.%m.%d`, never local time — just after midnight in the UK it's still yesterday in UTC — and never a future date. Up to v1.4.4 it used Semantic Versioning
- The version lives in `VERSION.md` as the bare version (`26.10.23`, no `v`); git tags and changelog headings add the `v` (`v26.10.23`)
- Every release gets a `## vYY.MM.DD` entry at the top of `CHANGELOG.md` using `### Added` / `### Changed` / `### Fixed` / `### Removed` / `### Security` / `### Deprecated` subsections, in that order — never a bare bullet list directly under a version heading
- `commit.sh` (bash) and `commit.bat` (Windows) read `VERSION.md`, refuse a version that isn't a valid Date Version or is dated in the future (UTC), warn when it's dated before today, then commit and `git tag` the release — no need to edit them per release. They don't push; they print the push command
