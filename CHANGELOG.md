# Changelog

All notable changes to Soonpage are documented here.

## v1.4.2

### Changed

- The footer's copyright year is worked out automatically: the start year alone in the first year, then START–CURRENT

## v1.4.1

### Fixed

- The footer's Created-with icons are optically sized, so the heart no longer looks bigger than the code and coffee icons

## v1.4.0

### Added

- A dev-mode banner, the shared Stux site banner, shown on every page while `dev-server.sh`/`.bat` runs; `?banner=soon,maintenance,site` previews the other banner types locally, and production never shows one (`assets/site-banner.css`, `assets/site-banner.js`, `assets/site-banners.js`, `assets/dev-mode.js`)
- A "Created with love / code / coffee by Stux.Group" line in the footer of every page
- The footer brand line on every page: the Stux.Group mark and "A Stux.Group Service" (linking to services.stux.group), both muted until hovered or focused
- `/sitemap` (an HTML page in the site's layout listing every page) and `sitemap.xml`, committed as static files and regenerated with `python scripts/build-sitemap.py` (`lastmod` comes from each page's last git commit); `robots.txt` points at it and the footer links to it

### Changed

- `dev-server.sh`/`.bat` serve the site the way GitHub Pages does (`/changelog` for `changelog.html`, the 404 page for missing paths) through `.github/dev-router.php`, turn DEV_MODE on by default (`--no-dev-mode` to preview production), and run on PHP 7.4 like the other Stux projects (`PHP_BIN`, `php74`, or `%LOCALAPPDATA%\Programs\PHP\7.4`, with a warning otherwise)
- The copyright symbol in the footers is an icon, with a visually hidden "©" so screen readers still read it

## v1.3.7

### Changed
- `changelog.html` now sorts each release's `###` sections into a fixed order — Added, Changed, Fixed, Removed, Security, Deprecated — at render time, rather than trusting the order `CHANGELOG.md` lists them in; unknown section types go last
- Changelog type badges now use the fixed family palette — Added `#2ecc71`, Changed `#3ba7ff`, Fixed `#ffa64d`, Removed `#ff4d4d`, Security `#b06bff`, Deprecated `#8a8a94` — as tinted badges (coloured text on a light tint of the same hue), with darker variants of each for the light theme
- CHANGELOG sections reordered to Added, Changed, Fixed, Removed, Security, Deprecated

## v1.3.6

### Fixed
- The footer's changelog/version link (and other footer links) turned accent-purple once visited — `a:visited` carries a pseudo-class, giving it higher CSS specificity than the plain `footer a` selector meant to keep footer links muted, so it kept winning regardless of source order. Every affected footer link now also styles `footer a:visited` explicitly.
- `.markdownlint.json` was missing several rule overrides (MD001/MD009/MD022/MD031/MD032) that every other repo in the org already disables, which was intermittently failing CI. Brought it in line with the standard config.

## v1.3.5

### Fixed
- GitHub Pages was using the legacy branch-deploy build system, which can silently stop auto-deploying with no error recorded anywhere (discovered on SeasonalOverlaysLibrary — its live site served stale content for over an hour with no visible failure). Switched to GitHub Actions-based Pages deployment (`.github/workflows/pages.yml`), making every deploy an ordinary, observable CI run instead.

## v1.3.4

### Fixed

- CI's markdownlint step was failing: MD024 (no-duplicate-heading) doesn't understand the Keep-a-Changelog pattern of repeating `### Fixed`/`### Added`/`### Changed` under every version entry, and `VERSION.md` was missing its trailing newline (MD047). Added `.markdownlint.json` with `MD024.siblings_only: true`, and disabled MD013/MD033/MD041, which conflict with this org's established doc style (centered `<img>` logo headers, long changelog lines).

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

### Added

- A custom `404.html` error page

### Changed

- Internal links no longer include `.html` (GitHub Pages resolves extensionless URLs natively)
- Legal-page `<title>` tags now say "Legal" for the category, keeping "Boring Legal Stuff" as the visible `<h1>` heading only

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
