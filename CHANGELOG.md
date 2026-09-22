# Changelog

All notable changes to Soonpage are documented here.

## v1.3.3

### Fixed

- Local checkout folder renamed from `SoonPage` to `soonpage` to match the repo name's actual casing; a stale `MaintenancePage` reference in CONTRIBUTING.md corrected to `maintenancepage`

## v1.3.2

### Changed

- Copy now reads "this website and/or service", since this page is reused whenever a specific Stux.Group service (not just the website) is coming soon

## v1.3.1

### Changed

- Copy now mentions services alongside the website, since Stux.Group represents both

## v1.3.0

### Changed

- Internal links no longer include `.html` (GitHub Pages resolves extensionless URLs natively)
- Legal-page `<title>` tags now say "Legal" for the category, keeping "Boring Legal Stuff" as the visible `<h1>` heading only

### Added

- A custom `404.html` error page

## v1.2.2

### Changed

- The footer's version link now fetches `VERSION.md` at runtime and fills in
  its own text, instead of being hand-typed on every release

## v1.2.1

### Fixed

- Legal pages (`privacy`, `opt-out`, `disclaimer`) and `CONTRIBUTING.md`
  still described Barlow and Font Awesome as loaded from Google Fonts /
  Cloudflare's cdnjs &mdash; updated to reflect that both are now
  self-hosted under `assets/`

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
