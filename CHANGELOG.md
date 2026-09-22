# Changelog

All notable changes to Soonpage are documented here.

## v1.2.0

### Added

- Self-hosted Barlow font files and Font Awesome (brands) assets under
  `assets/`, replacing the Google Fonts / cdnjs CDN links on every page

### Changed

- `changelog.html` now fetches and renders `CHANGELOG.md` at runtime instead
  of duplicating its content by hand, so the two can't drift out of sync

## v1.1.0

### Added

- Cross-origin `postMessage` title sync, so a page embedding this one in an
  iframe from any domain can mirror this page's `<title>`
- `changelog.html`, with a version number linked to it next to "Boring Legal
  Stuff" in the footer

## v1.0.1

### Fixed

- CI markdownlint failures against the mandated README/CHANGELOG/CONTRIBUTING/VERSION
  template (long lines, inline HTML for the centered logo, VERSION.md not
  starting with a heading) — added `.markdownlint.json` disabling the
  conflicting rules and fixed the remaining genuine formatting gaps
- `index.html` CI failures: a self-closing `<link/>` and a `<button>`
  missing `type="button"`
- Stale `/global/` path segment in shared media host URLs (left over from
  the `media.stux.group/global/` → `global.media.stux.group/` migration)

## v1.0.0

### Added

- `VERSION.md` / `CHANGELOG.md` / `CONTRIBUTING.md` / `commit.sh` / `commit.bat`
  versioning setup
- `dev-server.sh` / `dev-server.bat` for local previewing
- "Boring Legal Stuff" footer link to [stux.group/legal](https://stux.group/legal)
