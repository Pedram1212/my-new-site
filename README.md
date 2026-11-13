# Sabke German (سبک ژرمن) — Multilingual Study-Abroad & Migration Platform

A production-ready, high-converting, static/Jamstack multilingual web platform for **Sabke German (سبک ژرمن)** — specializing in university admissions (`Bachelor`, `Master`, `PhD`), German boarding schools (`Gymnasium` / `Internat`), `Studienkolleg` (`M/T/W/G-Kurs`), salaried `Ausbildung` vocational training, and end-to-end settlement in Germany.

## 1. Multilingual & Bidirectional Architecture (`i18n` + `RTL`/`LTR`)

Supports **4 languages** out of the box with both **pre-rendered localized routes** (for 100/100 SEO & zero-JS crawler indexing) and **instant client-side switching**:

| Language | Code | Route | Direction | Typography |
| :--- | :--- | :--- | :--- | :--- |
| **Persian (فارسی)** | `fa` | `/` & `/fa` | `dir="rtl"` | `Vazirmatn` |
| **German (Deutsch)** | `de` | `/de` | `dir="ltr"` | `Plus Jakarta Sans` / `Inter` |
| **English** | `en` | `/en` | `dir="ltr"` | `Plus Jakarta Sans` / `Inter` |
| **Azerbaijani (Azərbaycan)** | `az` | `/az` | `dir="ltr"` | `Plus Jakarta Sans` / `Inter` |

## 2. Project Structure

```text
├── assets/
│   ├── css/styles.css          # Prussian Navy (#0F172A) & German Gold (#F59E0B) RTL/LTR Design System + Dark/Light Mode
│   ├── js/i18n-data.js         # Auto-generated 4-language client dictionary
│   ├── js/app.js               # Interactive controller (Language switcher, Calculator Wizard, Tabs, Filters, Modals, GDPR)
│   └── images/                 # Editorial photography & SVG brand crest
├── i18n/
│   └── translations.py         # Single source of truth for FA, DE, EN, and AZ copy
├── build_site.py               # Python static site generator
├── index.html                  # Pre-rendered root route (Persian RTL default)
├── fa/index.html               # Pre-rendered Persian route
├── de/index.html               # Pre-rendered German route
├── en/index.html               # Pre-rendered English route
├── az/index.html               # Pre-rendered Azerbaijani route
├── sitemap.xml                 # Multi-language XML sitemap with xhtml:link hreflang annotations
├── robots.txt                  # Search engine crawler directives
└── vercel.json                 # Zero-config Vercel deployment with clean URLs & security headers
```

## 3. Building & Previewing Locally

To regenerate all localized HTML pages, `assets/js/i18n-data.js`, `sitemap.xml`, and `robots.txt` after editing `i18n/translations.py`:

```bash
python3 build_site.py
```

To serve locally on port `3000`:

```bash
python3 -m http.server 3000
```

## 4. Deploying on Vercel

This repository is pre-configured for zero-config deployment on **Vercel**:
1. Push the repository to GitHub (`Pedram1212/my-new-site`).
2. Import the repository in Vercel — all localized routes (`/`, `/fa`, `/de`, `/en`, `/az`), clean URLs, and security headers in `vercel.json` work automatically.