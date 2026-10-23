<p align="center">
  <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stux.group/logo-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stux.group/logo-dark.png"><img src="https://global.media.stux.group/logo-dark.png" height="100" alt="Stux.Group Logo"></picture>
</p>

# Soonpage

A clean and simple "coming soon" landing page template for Stux.Group projects.

## Overview

This repository contains a lightweight HTML landing page designed to announce upcoming projects or services. It's perfect for maintaining audience engagement while your project is in development.

## Features

- 📄 Simple, clean HTML structure
- ⚡ Lightweight and fast-loading
- 🎨 Ready to customize
- 📱 Responsive design
- 🚀 Deployed at [soonpage.stux.group](http://soonpage.stux.group/)

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/StuxGroup/soonpage.git
   ```

2. Open `index.html` in your browser or deploy to your hosting provider

## Customization

Edit the HTML files to:

- Update the coming soon message
- Add your branding and logo
- Customize colors and styling
- Include email signup or social links

## Deployment

This project uses GitHub Pages and is automatically deployed to [soonpage.stux.group](http://soonpage.stux.group/).

## Versioning

Soonpage uses [Date Versioning](https://datevers.ing): each release is numbered by its UTC release date as `YY.MM.DD` (for example `26.10.23`), with `-1`, `-2`… added for later releases the same day. The current version is in `VERSION.md`, and every release is listed in [`CHANGELOG.md`](CHANGELOG.md) (also shown at [/changelog](https://soonpage.stux.group/changelog)). Releases up to v1.4.4 used Semantic Versioning.

## Tests

Run `bash tests/run.sh` (Python 3.8+, no dependencies; Node.js for the changelog page's checks). See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is open source and available for use and modification.

---

Made by [Stux.Group](https://github.com/StuxGroup)

*Stux.Group is the parent of the <picture><source media="(prefers-color-scheme: dark)" srcset="https://global.media.stux.group/icon-light.png"><source media="(prefers-color-scheme: light)" srcset="https://global.media.stux.group/icon-dark.png"><img src="https://global.media.stux.group/icon-dark.png" height="14" alt="Stux.Group" valign="middle"></picture> Stux.Group Brand of Companies.*

## Local preview

Run `./dev-server.sh` (or `dev-server.bat`, add a port as the last argument) to serve the site at `http://127.0.0.1:8000` the way GitHub Pages does, with the dev-mode banner on. Add `--no-dev-mode` to see it exactly as production does, or `?banner=soon,maintenance,site` to preview the other banner types. It uses PHP 7.4's built-in server (set `PHP_BIN` to pick another PHP).
