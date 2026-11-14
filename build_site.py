#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sabke German (سبک ژرمن) — Static Multilingual Jamstack Builder
Generates:
  - /index.html (Persian default, RTL)
  - /fa/index.html (Persian, RTL)
  - /de/index.html (German, LTR)
  - /en/index.html (English, LTR)
  - /az/index.html (Azerbaijani, LTR)
  - /impressum/index.html (German § 5 DDG / TMG Legal Notice)
  - /datenschutz/index.html (GDPR / DSGVO Privacy Policy covering forms, WhatsApp & PDF uploads)
  - /assets/js/i18n-data.js
  - /sitemap.xml
  - /robots.txt
  - /llms.txt (AEO / AI Search Engine Optimization)
"""

import json
import os
from html import escape
from urllib.parse import quote
from i18n.translations import SITE_CONFIG, TRANSLATIONS

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def build_json_ld(lang_code: str, d: dict) -> str:
    domain = SITE_CONFIG["domain"]
    org_schema = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "@id": f"{domain}/#organization",
        "name": "Sabke German (سبک ژرمن)",
        "legalName": SITE_CONFIG["legal_name"],
        "alternateName": ["Sabke German", "سبک ژرمن", "Sabke German Bildungsberatung"],
        "url": f"{domain}/{lang_code}" if lang_code != "fa" else domain,
        "logo": f"{domain}/assets/images/favicon.svg",
        "image": f"{domain}/assets/images/hero-campus.jpg",
        "description": d["meta"]["description"],
        "email": SITE_CONFIG["email"],
        "telephone": SITE_CONFIG["phone"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE_CONFIG["street_address"],
            "addressLocality": "Berlin",
            "postalCode": "10707",
            "addressCountry": "DE",
        },
        "areaServed": ["DE", "IR", "AZ", "AT", "CH"],
        "availableLanguage": ["Persian", "German", "English", "Azerbaijani"],
        "sameAs": [
            f"https://t.me/{SITE_CONFIG['telegram_handle']}",
            f"https://wa.me/{SITE_CONFIG['whatsapp_number']}",
        ],
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"],
                },
            }
            for item in d["faq"]["items"]
        ],
    }

    return (
        f'<script type="application/ld+json">\n{json.dumps(org_schema, ensure_ascii=False, indent=2)}\n</script>\n'
        f'  <script type="application/ld+json">\n{json.dumps(faq_schema, ensure_ascii=False, indent=2)}\n</script>'
    )


def render_page_html(lang_code: str, is_root: bool = False) -> str:
    d = TRANSLATIONS[lang_code]
    domain = SITE_CONFIG["domain"]
    canonical_url = f"{domain}/" if is_root else f"{domain}/{lang_code}"
    active_tab = d["pathways"]["tabs"][0]
    wa_direct_url = f"https://wa.me/{SITE_CONFIG['whatsapp_number']}?text={quote(d['contact']['whatsapp_greeting'])}"

    # Pre-render pathway tabs
    pathway_tabs_html = "\n".join(
        [
            f'''          <button type="button" class="pathway-tab-btn {'active' if idx == 0 else ''}" data-pathway-id="{t['id']}" id="tab-btn-{t['id']}">
            <span class="tab-icon">✦</span>
            <span>{escape(t['tab_label'])}</span>
          </button>'''
            for idx, t in enumerate(d["pathways"]["tabs"])
        ]
    )

    pathway_features_html = "\n".join(
        [
            f'''              <li class="pathway-feature-item">
                <span class="feature-check">✓</span>
                <span>{escape(feat)}</span>
              </li>'''
            for feat in active_tab["features"]
        ]
    )

    # Pre-render services cards
    service_icons = [
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>',
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    ]
    services_html = "\n".join(
        [
            f'''          <article class="service-card">
            <div>
              <div class="service-header">
                <div class="service-icon-box">{service_icons[i % len(service_icons)]}</div>
                <span class="service-step-tag">{escape(c['step'])}</span>
              </div>
              <h3 class="service-title">{escape(c['title'])}</h3>
              <p class="service-desc">{escape(c['desc'])}</p>
            </div>
            <div class="service-tags">
              {''.join(f'<span class="service-tag">{escape(tag)}</span>' for tag in c['tags'])}
            </div>
          </article>'''
            for i, c in enumerate(d["services"]["cards"])
        ]
    )

    # Pre-render Roadmap
    roadmap_html = "\n".join(
        [
            f'''          <div class="roadmap-step-card">
            <div class="roadmap-step-top">
              <span class="roadmap-number">{escape(s['num'])}</span>
              <span class="roadmap-duration">{escape(s['duration'])}</span>
            </div>
            <h3 class="roadmap-title">{escape(s['title'])}</h3>
            <p class="roadmap-desc">{escape(s['desc'])}</p>
          </div>'''
            for s in d["roadmap"]["steps"]
        ]
    )

    # Pre-render Pricing Tiers
    pricing_html = "\n".join(
        [
            f'''          <div class="pricing-card {'popular' if t['popular'] else ''}">
            {f'<span class="popular-badge">{escape(d["pricing"]["popular_badge"])}</span>' if t['popular'] else ''}
            <div>
              <h3 class="pricing-tier-name">{escape(t['name'])}</h3>
              <p class="pricing-tier-tagline">{escape(t['tagline'])}</p>
              <div class="pricing-price-box">
                <span class="pricing-amount">{escape(t['price'])}</span>
                <span class="pricing-period">/ {escape(t['period'])}</span>
              </div>
              <ul class="pricing-features">
                {''.join(f'<li class="pricing-feature-li"><span class="feature-check">✓</span><span>{escape(feat)}</span></li>' for feat in t['features'])}
              </ul>
            </div>
            <button type="button" class="btn {'btn-primary' if t['popular'] else 'btn-outline'}" style="width:100%;" data-open-modal="consult-modal" data-preselect-pathway="{escape(t['name'])}">
              <span>{escape(d['pricing']['cta_select'])}</span>
            </button>
          </div>'''
            for t in d["pricing"]["tiers"]
        ]
    )

    # Pre-render Success Stories
    stories_filters_html = "\n".join(
        [
            f'''          <button type="button" class="filter-chip {'active' if k == 'all' else ''}" data-story-filter="{k}">{escape(v)}</button>'''
            for k, v in d["stories"]["filters"].items()
        ]
    )
    stories_cards_html = "\n".join(
        [
            f'''          <article class="story-card">
            <div>
              <div class="story-header">
                <div class="story-avatar">{escape(s['initials'])}</div>
                <div>
                  <h3 class="story-name">{escape(s['name'])}</h3>
                  <div class="story-program">{escape(s['program'])}</div>
                </div>
              </div>
              <p class="story-quote">{escape(s['quote'])}</p>
            </div>
            <div class="story-meta">
              <span>✦ {escape(s['meta_left'])}</span>
              <span>📍 {escape(s['meta_right'])}</span>
            </div>
          </article>'''
            for s in d["stories"]["items"]
        ]
    )

    # Pre-render FAQ Accordion
    faq_html = "\n".join(
        [
            f'''          <div class="faq-item {'open' if idx == 0 else ''}">
            <button type="button" class="faq-trigger" aria-expanded="{'true' if idx == 0 else 'false'}">
              <span>{escape(item['q'])}</span>
              <span class="faq-chevron">▾</span>
            </button>
            <div class="faq-answer">
              <p>{escape(item['a'])}</p>
            </div>
          </div>'''
            for idx, item in enumerate(d["faq"]["items"])
        ]
    )

    # Pre-render 4-Step Smart Assessment Step 1 (Academic GPA)
    asm = d["assessment"]
    asm_steps_html = "\n".join(
        [
            f'''            <button type="button" class="wizard-step-indicator {'active' if i == 0 else ''}" data-goto-step="{i + 1}">
              <span class="step-num">{i + 1}</span>
              <span>{escape(lbl)}</span>
            </button>'''
            for i, lbl in enumerate(asm["steps_nav"])
        ]
    )
    asm_gpa_html = "\n".join(
        [
            f'''              <button type="button" class="wizard-option-card {'selected' if g['id'] == '16_18' else ''}" data-select-gpa="{g['id']}">
                <span class="option-title">{escape(g['title'])}</span>
                <span class="option-sub">{escape(g['sub'])}</span>
              </button>'''
            for g in asm["gpa_options"]
        ]
    )

    # Pre-render Cost Calculator (Default: Master, 12 Months)
    cc = d["cost_calc"]
    cost_pathway_btns_html = "\n".join(
        [
            f'''              <button type="button" class="cost-pill-btn {'active' if k == 'Master' else ''}" data-cost-pathway="{k}">{escape(v)}</button>'''
            for k, v in cc["pathways"].items()
        ]
    )

    # Pre-render Visa Checklist Items
    cl = d["checklist_lead"]
    checklist_items_html = "\n".join(
        [
            f'''              <label class="checklist-doc-item">
                <input type="checkbox" class="checklist-doc-checkbox" checked />
                <div class="checklist-doc-body">
                  <div class="checklist-doc-title">{escape(item['title'])}</div>
                  <div class="checklist-doc-detail">{escape(item['detail'])}</div>
                </div>
              </label>'''
            for item in cl["items"]
        ]
    )

    json_ld_block = build_json_ld(lang_code, d)

    return f"""<!DOCTYPE html>
<html lang="{d['lang']}" dir="{d['dir']}" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(d['meta']['title'])}</title>
  <meta name="description" content="{escape(d['meta']['description'])}" />
  <meta name="keywords" content="{escape(d['meta']['keywords'])}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="theme-color" content="#0F172A" />

  <!-- Canonical & Multilingual Hreflang Annotations -->
  <link rel="canonical" href="{canonical_url}" />
  <link rel="alternate" hreflang="fa" href="{domain}/fa" />
  <link rel="alternate" hreflang="de" href="{domain}/de" />
  <link rel="alternate" hreflang="en" href="{domain}/en" />
  <link rel="alternate" hreflang="az" href="{domain}/az" />
  <link rel="alternate" hreflang="x-default" href="{domain}/" />

  <!-- OpenGraph / Social Metadata -->
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Sabke German (سبک ژرمن)" />
  <meta property="og:title" content="{escape(d['meta']['title'])}" />
  <meta property="og:description" content="{escape(d['meta']['description'])}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:locale" content="{d['locale']}" />
  <meta property="og:image" content="{domain}/assets/images/hero-campus.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{escape(d['meta']['title'])}" />
  <meta name="twitter:description" content="{escape(d['meta']['description'])}" />
  <meta name="twitter:image" content="{domain}/assets/images/hero-campus.jpg" />

  <!-- Favicon & AI Discovery -->
  <link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg" />
  <link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs.txt AI Guide" />

  <!-- Google Fonts: Vazirmatn (Persian RTL) + Plus Jakarta Sans & Inter (DE/EN/AZ LTR) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Vazirmatn:wght@400;500;600;700;800&display=swap" rel="stylesheet" />

  <!-- Stylesheet -->
  <link rel="stylesheet" href="/assets/css/styles.css" />

  <!-- JSON-LD Structured Data (EducationalOrganization + FAQPage) -->
  {json_ld_block}

  <!-- Vercel Web Analytics -->
  <script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
  <!-- Subtle German Flag Top Accent Bar -->
  <div class="german-tricolor-bar" aria-hidden="true"></div>

  <!-- ========================================================================
       STICKY HEADER & MULTILINGUAL NAVIGATION (3-Column Layout + 4x2 Nav Grid)
       ======================================================================== -->
  <header class="site-header" id="site-header">
    <div class="container header-inner">
      <a href="/{'' if lang_code == 'fa' else lang_code}" class="brand-logo" aria-label="Sabke German Home">
        <img src="/assets/images/favicon.svg" alt="Sabke German Crest" class="brand-crest" width="42" height="42" />
        <div class="brand-text">
          <span class="brand-name" data-i18n="nav.brand_name">{escape(d['nav']['brand_name'])}</span>
          <span class="brand-tagline" data-i18n="nav.brand_tagline">{escape(d['nav']['brand_tagline'])}</span>
        </div>
      </a>

      <nav class="main-nav nav-links" aria-label="Primary Navigation">
        <a href="#pathways" class="nav-link" data-i18n="nav.pathways">{escape(d['nav']['pathways'])}</a>
        <a href="#services" class="nav-link" data-i18n="nav.services">{escape(d['nav']['services'])}</a>
        <a href="#assessment" class="nav-link" data-i18n="nav.calculator">{escape(d['nav']['calculator'])}</a>
        <a href="#roadmap" class="nav-link" data-i18n="nav.roadmap">{escape(d['nav']['roadmap'])}</a>
        <a href="#pricing" class="nav-link" data-i18n="nav.pricing">{escape(d['nav']['pricing'])}</a>
        <a href="#stories" class="nav-link" data-i18n="nav.stories">{escape(d['nav']['stories'])}</a>
        <a href="#faq" class="nav-link" data-i18n="nav.faq">{escape(d['nav']['faq'])}</a>
        <a href="#contact" class="nav-link" data-i18n="nav.contact">{escape(d['nav']['contact'])}</a>
      </nav>

      <div class="header-controls">
        <!-- Single Horizontal Pill Language Bar (FA | DE | EN | AZ) -->
        <div class="lang-switcher" role="group" aria-label="Language Switcher">
          <a href="/fa" class="lang-btn {'active' if lang_code == 'fa' else ''}" data-lang="fa" id="lang-switch-fa" title="فارسی (Persian)">
            <span class="lang-flag">🇮🇷</span><span>FA</span>
          </a>
          <a href="/de" class="lang-btn {'active' if lang_code == 'de' else ''}" data-lang="de" id="lang-switch-de" title="Deutsch (German)">
            <span class="lang-flag">🇩🇪</span><span>DE</span>
          </a>
          <a href="/en" class="lang-btn {'active' if lang_code == 'en' else ''}" data-lang="en" id="lang-switch-en" title="English">
            <span class="lang-flag">🇬🇧</span><span>EN</span>
          </a>
          <a href="/az" class="lang-btn {'active' if lang_code == 'az' else ''}" data-lang="az" id="lang-switch-az" title="Azərbaycan">
            <span class="lang-flag">🇦🇿</span><span>AZ</span>
          </a>
        </div>

        <!-- Dark / Light Mode Toggle -->
        <button type="button" class="theme-toggle" id="theme-toggle-btn" aria-label="Toggle Dark or Light Mode">
          <svg id="theme-icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
          <svg id="theme-icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none;">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
        </button>

        <button type="button" class="btn btn-primary header-cta" data-open-modal="consult-modal" id="header-book-btn">
          <span data-i18n="nav.cta_book">{escape(d['nav']['cta_book'])}</span>
        </button>

        <button type="button" class="mobile-menu-btn" id="mobile-menu-btn" aria-label="Open Navigation Menu" aria-expanded="false">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
      </div>
    </div>
  </header>

  <main>
    <!-- ======================================================================
         A. HIGH-IMPACT HERO SECTION & LIVE TRUST BAR
         ====================================================================== -->
    <section class="hero-section" id="hero">
      <div class="hero-backdrop" aria-hidden="true"></div>
      <div class="container">
        <div class="hero-grid">
          <div class="hero-copy">
            <div class="hero-kicker">
              <span>🏛</span>
              <span data-i18n="hero.kicker">{escape(d['hero']['kicker'])}</span>
            </div>
            <h1 class="hero-title" data-i18n="hero.title">{escape(d['hero']['title'])}</h1>
            <p class="hero-subtitle" data-i18n="hero.subtitle">{escape(d['hero']['subtitle'])}</p>

            <div class="hero-actions">
              <a href="#assessment" class="btn btn-primary" id="hero-cta-eligibility">
                <span data-i18n="hero.cta_primary">{escape(d['hero']['cta_primary'])}</span>
                <span class="dir-flip">→</span>
              </a>
              <button type="button" class="btn hero-btn-secondary" data-open-modal="consult-modal" id="hero-cta-consult">
                <span data-i18n="hero.cta_secondary">{escape(d['hero']['cta_secondary'])}</span>
              </button>
            </div>

            <div class="hero-highlights">
              <div class="hero-highlight-item">
                <span class="hero-highlight-icon">✦</span>
                <span data-i18n="hero.h1">{escape(d['hero']['h1'])}</span>
              </div>
              <div class="hero-highlight-item">
                <span class="hero-highlight-icon">✦</span>
                <span data-i18n="hero.h2">{escape(d['hero']['h2'])}</span>
              </div>
              <div class="hero-highlight-item">
                <span class="hero-highlight-icon">✦</span>
                <span data-i18n="hero.h3">{escape(d['hero']['h3'])}</span>
              </div>
            </div>
          </div>

          <div class="hero-visual">
            <div class="hero-image-frame">
              <img src="/assets/images/hero-campus.jpg" alt="German University Campus Architecture" width="960" height="640" fetchpriority="high" />
              <div class="hero-image-overlay"></div>
            </div>

            <div class="hero-floating-card hero-card-top">
              <div class="floating-badge-icon">🎓</div>
              <div>
                <div class="floating-card-title" data-i18n="hero.card_top_title">{escape(d['hero']['card_top_title'])}</div>
                <div class="floating-card-sub" data-i18n="hero.card_top_sub">{escape(d['hero']['card_top_sub'])}</div>
              </div>
            </div>

            <div class="hero-floating-card hero-card-bottom">
              <div>
                <div class="floating-card-title" data-i18n="hero.card_bottom_title">{escape(d['hero']['card_bottom_title'])}</div>
                <div class="floating-card-sub" data-i18n="hero.card_bottom_sub">{escape(d['hero']['card_bottom_sub'])}</div>
              </div>
              <span class="pathway-pill pathway-pill-gold" data-i18n="hero.card_bottom_badge">{escape(d['hero']['card_bottom_badge'])}</span>
            </div>
          </div>
        </div>

        <!-- Live Trust Bar -->
        <div class="trust-bar-wrapper">
          <div class="trust-bar">
            <div class="trust-stat">
              <div class="trust-number" data-i18n="trust.s1_num">{escape(d['trust']['s1_num'])}</div>
              <div class="trust-label" data-i18n="trust.s1_label">{escape(d['trust']['s1_label'])}</div>
            </div>
            <div class="trust-stat">
              <div class="trust-number" data-i18n="trust.s2_num">{escape(d['trust']['s2_num'])}</div>
              <div class="trust-label" data-i18n="trust.s2_label">{escape(d['trust']['s2_label'])}</div>
            </div>
            <div class="trust-stat">
              <div class="trust-number" data-i18n="trust.s3_num">{escape(d['trust']['s3_num'])}</div>
              <div class="trust-label" data-i18n="trust.s3_label">{escape(d['trust']['s3_label'])}</div>
            </div>
            <div class="trust-stat">
              <div class="trust-number" data-i18n="trust.s4_num">{escape(d['trust']['s4_num'])}</div>
              <div class="trust-label" data-i18n="trust.s4_label">{escape(d['trust']['s4_label'])}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================
         B. 5 CORE EDUCATIONAL & MIGRATION PATHWAYS (Interactive Tabs)
         ====================================================================== -->
    <section class="section" id="pathways">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="pathways.eyebrow">{escape(d['pathways']['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="pathways.title">{escape(d['pathways']['title'])}</h2>
          <p class="section-subtitle" data-i18n="pathways.subtitle">{escape(d['pathways']['subtitle'])}</p>
        </div>

        <div class="pathways-tabs-nav" id="pathways-tabs-nav" role="tablist">
{pathway_tabs_html}
        </div>

        <div class="pathway-detail-panel" id="pathway-detail-panel">
          <div class="pathway-content-col">
            <div class="pathway-badge-row">
              <span class="pathway-pill pathway-pill-gold">{escape(active_tab['badge_1'])}</span>
              <span class="pathway-pill">{escape(active_tab['badge_2'])}</span>
            </div>
            <h3 class="pathway-title">{escape(active_tab['title'])}</h3>
            <p class="pathway-desc">{escape(active_tab['desc'])}</p>
            <ul class="pathway-features-list">
{pathway_features_html}
            </ul>
            <div class="hero-actions" style="margin-bottom:0;">
              <button type="button" class="btn btn-primary" data-jump-calc="{active_tab['id']}" id="pathway-eval-cta">
                <span data-i18n="pathways.cta_evaluate">{escape(d['pathways']['cta_evaluate'])}</span>
              </button>
              <button type="button" class="btn btn-outline" data-open-modal="consult-modal" data-preselect-pathway="{escape(active_tab['title'])}" id="pathway-consult-cta">
                <span data-i18n="pathways.cta_consult">{escape(d['pathways']['cta_consult'])}</span>
              </button>
            </div>
          </div>

          <div class="pathway-metrics-card">
            <img src="{active_tab['image']}" alt="{escape(active_tab['title'])}" class="pathway-visual-img" loading="lazy" />
            <div class="pathway-metrics-body">
              <div class="metric-box">
                <div class="metric-label">{escape(active_tab['m1_label'])}</div>
                <div class="metric-value">{escape(active_tab['m1_val'])}</div>
              </div>
              <div class="metric-box">
                <div class="metric-label">{escape(active_tab['m2_label'])}</div>
                <div class="metric-value">{escape(active_tab['m2_val'])}</div>
              </div>
              <div class="metric-box">
                <div class="metric-label">{escape(active_tab['m3_label'])}</div>
                <div class="metric-value">{escape(active_tab['m3_val'])}</div>
              </div>
              <div class="metric-box">
                <div class="metric-label">{escape(active_tab['m4_label'])}</div>
                <div class="metric-value">{escape(active_tab['m4_val'])}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================
         C. END-TO-END VISA & SETTLEMENT SERVICES
         ====================================================================== -->
    <section class="section section-alt" id="services">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="services.eyebrow">{escape(d['services']['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="services.title">{escape(d['services']['title'])}</h2>
          <p class="section-subtitle" data-i18n="services.subtitle">{escape(d['services']['subtitle'])}</p>
        </div>

        <div class="services-grid" id="services-grid">
{services_html}
        </div>
      </div>
    </section>

    <!-- ======================================================================
         D.1 INTERACTIVE 4-STEP SMART PATHWAY ASSESSMENT (ارزیابی هوشمند)
         ====================================================================== -->
    <section class="section calculator-section" id="assessment">
      <span id="calculator" aria-hidden="true"></span>
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="assessment.eyebrow">{escape(asm['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="assessment.title">{escape(asm['title'])}</h2>
          <p class="section-subtitle" data-i18n="assessment.subtitle">{escape(asm['subtitle'])}</p>
        </div>

        <div class="wizard-card" id="wizard-card-container">
          <div class="wizard-progress">
{asm_steps_html}
          </div>
          <div class="wizard-step-pane active">
            <h3 class="wizard-question-title">{escape(asm['step1_title'])}</h3>
            <p class="wizard-question-hint">{escape(asm['step1_hint'])}</p>
            <div class="wizard-options-grid">
{asm_gpa_html}
            </div>
          </div>
          <div class="wizard-footer">
            <span></span>
            <button type="button" class="btn btn-primary" id="wizard-next-btn">{escape(asm['btn_next'])}</button>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================
         D.2 INTERACTIVE BLOCKED ACCOUNT & GERMANY STUDY COST CALCULATOR (ماشینحساب تمکن مالی)
         ====================================================================== -->
    <section class="section section-alt cost-calc-section" id="cost-calculator">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="cost_calc.eyebrow">{escape(cc['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="cost_calc.title">{escape(cc['title'])}</h2>
          <p class="section-subtitle" data-i18n="cost_calc.subtitle">{escape(cc['subtitle'])}</p>
        </div>

        <div class="cost-calc-card" id="cost-calc-card">
          <div class="cost-controls-grid">
            <div class="cost-control-group">
              <label class="cost-control-label" data-i18n="cost_calc.pathway_label">{escape(cc['pathway_label'])}</label>
              <div class="cost-pills-row" id="cost-pathway-pills">
{cost_pathway_btns_html}
              </div>
            </div>

            <div class="cost-control-group">
              <label class="cost-control-label" data-i18n="cost_calc.duration_label">{escape(cc['duration_label'])}</label>
              <div class="cost-pills-row" id="cost-duration-pills">
                <button type="button" class="cost-pill-btn" data-cost-months="6" data-i18n="cost_calc.months_6">{escape(cc['months_6'])}</button>
                <button type="button" class="cost-pill-btn active" data-cost-months="12" data-i18n="cost_calc.months_12">{escape(cc['months_12'])}</button>
              </div>
            </div>
          </div>

          <div class="cost-breakdown-panel" id="cost-breakdown-panel">
            <div class="cost-items-list">
              <div class="cost-line-item highlight">
                <div>
                  <div class="cost-line-title" data-i18n="cost_calc.sperrkonto_label">{escape(cc['sperrkonto_label'])}</div>
                  <div class="cost-line-sub" id="cost-sperrkonto-sub" data-i18n="cost_calc.sperrkonto_sub">{escape(cc['sperrkonto_sub'])}</div>
                </div>
                <div class="cost-line-amount" id="cost-val-sperrkonto" dir="ltr">€11,904</div>
              </div>

              <div class="cost-line-item">
                <div>
                  <div class="cost-line-title" data-i18n="cost_calc.insurance_label">{escape(cc['insurance_label'])}</div>
                  <div class="cost-line-sub" data-i18n="cost_calc.insurance_sub">{escape(cc['insurance_sub'])}</div>
                </div>
                <div class="cost-line-amount" id="cost-val-insurance" dir="ltr">€1,560</div>
              </div>

              <div class="cost-line-item">
                <div>
                  <div class="cost-line-title" data-i18n="cost_calc.semester_label">{escape(cc['semester_label'])}</div>
                  <div class="cost-line-sub" data-i18n="cost_calc.semester_sub">{escape(cc['semester_sub'])}</div>
                </div>
                <div class="cost-line-amount" id="cost-val-semester" dir="ltr">€600</div>
              </div>

              <div class="cost-line-item">
                <div>
                  <div class="cost-line-title" data-i18n="cost_calc.visa_fee_label">{escape(cc['visa_fee_label'])}</div>
                  <div class="cost-line-sub" data-i18n="cost_calc.visa_fee_sub">{escape(cc['visa_fee_sub'])}</div>
                </div>
                <div class="cost-line-amount" id="cost-val-visa" dir="ltr">€75</div>
              </div>
            </div>

            <div class="cost-summary-box">
              <div>
                <div class="cost-total-caption" data-i18n="cost_calc.total_label">{escape(cc['total_label'])}</div>
                <div class="cost-total-number" id="cost-val-total" dir="ltr">€14,139</div>
                <p class="cost-total-note" id="cost-total-note" data-i18n="cost_calc.total_note_study">{escape(cc['total_note_study'])}</p>
              </div>
              <a href="#contact" class="btn btn-primary" id="cost-calc-cta-btn" style="width:100%; justify-content:center;">
                <span data-i18n="cost_calc.cta_btn">{escape(cc['cta_btn'])}</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================
         E. VISUAL 6-STEP ROADMAP (Tehran / Baku to Germany)
         ====================================================================== -->
    <section class="section" id="roadmap">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="roadmap.eyebrow">{escape(d['roadmap']['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="roadmap.title">{escape(d['roadmap']['title'])}</h2>
          <p class="section-subtitle" data-i18n="roadmap.subtitle">{escape(d['roadmap']['subtitle'])}</p>
        </div>

        <div class="roadmap-grid" id="roadmap-grid">
{roadmap_html}
        </div>
      </div>
    </section>

    <!-- ======================================================================
         F. TRANSPARENT PRICING PACKAGES
         ====================================================================== -->
    <section class="section section-alt" id="pricing">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="pricing.eyebrow">{escape(d['pricing']['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="pricing.title">{escape(d['pricing']['title'])}</h2>
          <p class="section-subtitle" data-i18n="pricing.subtitle">{escape(d['pricing']['subtitle'])}</p>
        </div>

        <div class="pricing-grid" id="pricing-grid">
{pricing_html}
        </div>
      </div>
    </section>

    <!-- ======================================================================
         G.1 STUDENT SUCCESS STORIES (Filterable)
         ====================================================================== -->
    <section class="section" id="stories">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="stories.eyebrow">{escape(d['stories']['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="stories.title">{escape(d['stories']['title'])}</h2>
          <p class="section-subtitle" data-i18n="stories.subtitle">{escape(d['stories']['subtitle'])}</p>
        </div>

        <div class="stories-filter-bar" id="stories-filter-bar">
{stories_filters_html}
        </div>

        <div class="stories-grid" id="stories-grid">
{stories_cards_html}
        </div>
      </div>
    </section>

    <!-- ======================================================================
         G.2 INTERACTIVE FAQ ACCORDION
         ====================================================================== -->
    <section class="section section-alt" id="faq">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="faq.eyebrow">{escape(d['faq']['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="faq.title">{escape(d['faq']['title'])}</h2>
          <p class="section-subtitle" data-i18n="faq.subtitle">{escape(d['faq']['subtitle'])}</p>
        </div>

        <div class="faq-container" id="faq-accordion">
{faq_html}
        </div>
      </div>
    </section>

    <!-- ======================================================================
         G.3 LEAD MAGNET: FREE GERMANY STUDENT VISA DOCUMENT CHECKLIST
         ====================================================================== -->
    <section class="section checklist-lead-section" id="visa-checklist">
      <div class="container">
        <div class="checklist-lead-card">
          <div class="checklist-lead-top">
            <div class="checklist-lead-copy">
              <div class="eyebrow" data-i18n="checklist_lead.eyebrow">{escape(cl['eyebrow'])}</div>
              <h2 class="section-title" style="margin-bottom:0.75rem;" data-i18n="checklist_lead.title">{escape(cl['title'])}</h2>
              <p class="section-subtitle" style="margin-bottom:1rem;" data-i18n="checklist_lead.subtitle">{escape(cl['subtitle'])}</p>
              <span class="pathway-pill pathway-pill-gold" data-i18n="checklist_lead.badge">✦ {escape(cl['badge'])}</span>
            </div>

            <form id="checklist-lead-form" class="checklist-lead-form" action="{escape(SITE_CONFIG['form_endpoint'])}" method="POST" novalidate>
              <input type="hidden" name="lead_type" value="visa_checklist" />
              <div class="contact-field-group">
                <label class="contact-label" for="checklist-lead-name" data-i18n="checklist_lead.name_label">{escape(cl['name_label'])}</label>
                <input type="text" id="checklist-lead-name" name="full_name" class="contact-input" required placeholder="{escape(cl['name_placeholder'])}" data-i18n-placeholder="checklist_lead.name_placeholder" />
              </div>
              <div class="contact-field-group">
                <label class="contact-label" for="checklist-lead-contact" data-i18n="checklist_lead.contact_label">{escape(cl['contact_label'])}</label>
                <input type="text" id="checklist-lead-contact" name="email_or_whatsapp" class="contact-input" required dir="ltr" placeholder="{escape(cl['contact_placeholder'])}" data-i18n-placeholder="checklist_lead.contact_placeholder" />
              </div>
              <button type="submit" class="btn btn-primary" id="checklist-unlock-btn" style="width:100%; justify-content:center;">
                <span data-i18n="checklist_lead.submit_btn">{escape(cl['submit_btn'])}</span>
              </button>
              <p class="contact-privacy-note" style="text-align:center;" data-i18n="checklist_lead.privacy_hint">{escape(cl['privacy_hint'])}</p>
            </form>
          </div>

          <!-- Unlocked Printable / PDF-Ready Checklist Panel -->
          <div class="checklist-unlocked-panel" id="checklist-unlocked-panel" hidden>
            <div class="checklist-unlocked-header">
              <div>
                <h3 class="checklist-unlocked-title" data-i18n="checklist_lead.unlocked_title">{escape(cl['unlocked_title'])}</h3>
                <p class="checklist-unlocked-sub" data-i18n="checklist_lead.unlocked_subtitle">{escape(cl['unlocked_subtitle'])}</p>
              </div>
              <button type="button" class="btn btn-primary" id="checklist-print-btn">
                <span data-i18n="checklist_lead.print_btn">{escape(cl['print_btn'])}</span>
              </button>
            </div>
            <div class="checklist-docs-grid" id="checklist-docs-grid">
{checklist_items_html}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ======================================================================
         H. CONTACT, CONSULTATION & PDF DOCUMENT UPLOAD SECTION
         ====================================================================== -->
    <section class="section section-alt contact-section" id="contact">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="contact.eyebrow">{escape(d['contact']['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="contact.title">{escape(d['contact']['title'])}</h2>
          <p class="section-subtitle" data-i18n="contact.subtitle">{escape(d['contact']['subtitle'])}</p>
        </div>

        <div class="contact-grid">
          <!-- Direct WhatsApp & Berlin Advisory Card -->
          <aside class="contact-direct-card">
            <div>
              <div class="wa-status-pill">
                <span class="wa-status-dot" aria-hidden="true"></span>
                <span data-i18n="contact.wa_card_badge">{escape(d['contact']['wa_card_badge'])}</span>
              </div>
              <h3 class="contact-direct-title" data-i18n="contact.info_card_title">{escape(d['contact']['info_card_title'])}</h3>
              <p class="contact-direct-desc" data-i18n="contact.info_card_desc">{escape(d['contact']['info_card_desc'])}</p>

              <a href="{wa_direct_url}" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp btn-lg contact-wa-main-btn" id="contact-direct-wa-btn">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M12.031 2c-5.516 0-9.969 4.453-9.969 9.969 0 1.766.469 3.484 1.359 5.016L2 22l5.156-1.359c1.484.813 3.172 1.25 4.875 1.25 5.516 0 9.969-4.453 9.969-9.969S17.547 2 12.031 2zm5.828 14.125c-.25.703-1.453 1.344-2.016 1.422-.531.078-1.203.109-1.953-.125-.453-.141-1.047-.344-1.797-.672-3.156-1.359-5.219-4.547-5.375-4.766-.156-.203-1.281-1.703-1.281-3.25s.813-2.313 1.094-2.625c.281-.313.625-.391.828-.391.203 0 .406.016.594.016.188.016.438-.078.688.531.25.609.859 2.094.938 2.25.078.156.125.344.031.547-.094.203-.141.328-.297.5-.156.172-.313.391-.453.516-.141.141-.297.297-.125.594.172.297.766 1.266 1.641 2.047 1.125 1.016 2.078 1.328 2.375 1.484.297.156.469.125.641-.078.172-.203.75-.875.953-1.172.203-.297.406-.25.688-.141.281.109 1.766.828 2.063.984.297.156.5.234.578.359.078.125.078.734-.172 1.438z"/>
                </svg>
                <span data-i18n="contact.wa_cta_btn">{escape(d['contact']['wa_cta_btn'])}</span>
              </a>
            </div>

            <div class="contact-info-list">
              <div class="contact-info-item">
                <span class="contact-info-icon">🇩🇪</span>
                <div>
                  <div class="contact-info-label">Berlin Headquarters</div>
                  <div class="contact-info-val">{escape(SITE_CONFIG['street_address'])}, {escape(SITE_CONFIG['postal_city'])}</div>
                </div>
              </div>
              <div class="contact-info-item">
                <span class="contact-info-icon">📞</span>
                <div>
                  <div class="contact-info-label">WhatsApp &amp; Direct Line</div>
                  <div class="contact-info-val" dir="ltr">+49 000 0000000 • {escape(SITE_CONFIG['phone'])}</div>
                </div>
              </div>
              <div class="contact-info-item">
                <span class="contact-info-icon">✉️</span>
                <div>
                  <div class="contact-info-label">Official Admissions Desk</div>
                  <div class="contact-info-val" dir="ltr">{escape(SITE_CONFIG['email'])}</div>
                </div>
              </div>
              <div class="contact-info-item">
                <span class="contact-info-icon">🕒</span>
                <div>
                  <div class="contact-info-label" data-i18n="contact.office_hours_label">{escape(d['contact']['office_hours_label'])}</div>
                  <div class="contact-info-val" data-i18n="contact.office_hours_val">{escape(d['contact']['office_hours_val'])}</div>
                </div>
              </div>
            </div>
          </aside>

          <!-- Consultation Request & PDF Document Upload Form -->
          <div class="contact-form-card">
            <h3 class="contact-form-heading" data-i18n="contact.form_title">{escape(d['contact']['form_title'])}</h3>

            <form id="contact-consultation-form" class="consultation-form" action="{escape(SITE_CONFIG['form_endpoint'])}" method="POST" enctype="multipart/form-data" novalidate>
              <div class="contact-form-row">
                <div class="contact-field-group">
                  <label class="contact-label" for="contact-name" data-i18n="contact.name_label">{escape(d['contact']['name_label'])}</label>
                  <input type="text" id="contact-name" name="full_name" class="contact-input" required placeholder="{escape(d['contact']['name_placeholder'])}" data-i18n-placeholder="contact.name_placeholder" autocomplete="name" />
                </div>
                <div class="contact-field-group">
                  <label class="contact-label" for="contact-email" data-i18n="contact.email_label">{escape(d['contact']['email_label'])}</label>
                  <input type="email" id="contact-email" name="email" class="contact-input" required dir="ltr" placeholder="{escape(d['contact']['email_placeholder'])}" data-i18n-placeholder="contact.email_placeholder" autocomplete="email" />
                </div>
              </div>

              <div class="contact-form-row">
                <div class="contact-field-group">
                  <label class="contact-label" for="contact-phone" data-i18n="contact.phone_label">{escape(d['contact']['phone_label'])}</label>
                  <input type="tel" id="contact-phone" name="whatsapp_phone" class="contact-input" required dir="ltr" placeholder="{escape(d['contact']['phone_placeholder'])}" data-i18n-placeholder="contact.phone_placeholder" autocomplete="tel" />
                </div>
                <div class="contact-field-group">
                  <label class="contact-label" for="contact-pathway" data-i18n="contact.pathway_label">{escape(d['contact']['pathway_label'])}</label>
                  <select id="contact-pathway" name="target_pathway" class="contact-select" required>
                    <option value="Studienkolleg" data-i18n="contact.pathway_options.studienkolleg">{escape(d['contact']['pathway_options']['studienkolleg'])}</option>
                    <option value="Bachelor" data-i18n="contact.pathway_options.bachelor">{escape(d['contact']['pathway_options']['bachelor'])}</option>
                    <option value="Master" selected data-i18n="contact.pathway_options.master">{escape(d['contact']['pathway_options']['master'])}</option>
                    <option value="Ausbildung" data-i18n="contact.pathway_options.ausbildung">{escape(d['contact']['pathway_options']['ausbildung'])}</option>
                    <option value="Language Course" data-i18n="contact.pathway_options.language">{escape(d['contact']['pathway_options']['language'])}</option>
                  </select>
                </div>
              </div>

              <div class="contact-field-group">
                <label class="contact-label" for="contact-message" data-i18n="contact.message_label">{escape(d['contact']['message_label'])}</label>
                <textarea id="contact-message" name="message" rows="4" class="contact-input contact-textarea" placeholder="{escape(d['contact']['message_placeholder'])}" data-i18n-placeholder="contact.message_placeholder"></textarea>
              </div>

              <!-- Styled PDF Document Upload Field (Max 10MB, .pdf only) -->
              <div class="contact-field-group">
                <label class="contact-label" for="contact-pdf-input" data-i18n="contact.pdf_label">{escape(d['contact']['pdf_label'])}</label>
                <div class="pdf-upload-wrapper">
                  <input type="file" id="contact-pdf-input" name="document_pdf" accept=".pdf,application/pdf" class="pdf-file-input-hidden" aria-describedby="contact-pdf-hint contact-pdf-error" />
                  <label for="contact-pdf-input" class="pdf-dropzone" id="contact-pdf-dropzone">
                    <div class="pdf-dropzone-icon" aria-hidden="true">
                      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <path d="M12 18v-6"></path>
                        <path d="m9 15 3-3 3 3"></path>
                      </svg>
                    </div>
                    <div class="pdf-dropzone-text">
                      <span class="pdf-drop-title" data-i18n="contact.pdf_drop_title">{escape(d['contact']['pdf_drop_title'])}</span>
                      <span class="pdf-drop-hint" id="contact-pdf-hint" data-i18n="contact.pdf_drop_hint">{escape(d['contact']['pdf_drop_hint'])}</span>
                    </div>
                  </label>

                  <div class="pdf-selected-bar" id="contact-pdf-selected" hidden>
                    <div class="pdf-selected-info">
                      <span class="pdf-badge-icon" aria-hidden="true">📄 PDF</span>
                      <span class="pdf-filename" id="contact-pdf-filename" dir="ltr"></span>
                      <span class="pdf-filesize" id="contact-pdf-filesize" dir="ltr"></span>
                    </div>
                    <button type="button" class="pdf-remove-btn" id="contact-pdf-remove" data-i18n="contact.pdf_remove_btn">{escape(d['contact']['pdf_remove_btn'])}</button>
                  </div>

                  <div class="pdf-error-msg" id="contact-pdf-error" role="alert" hidden></div>
                </div>
              </div>

              <!-- Submit & Direct WhatsApp CTA Row -->
              <div class="contact-form-actions">
                <button type="submit" class="btn btn-primary btn-lg contact-submit-btn" id="contact-submit-btn">
                  <span data-i18n="contact.submit_btn">{escape(d['contact']['submit_btn'])}</span>
                </button>
                <a href="{wa_direct_url}" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp btn-lg contact-wa-inline-btn" id="contact-form-wa-btn">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path d="M12.031 2c-5.516 0-9.969 4.453-9.969 9.969 0 1.766.469 3.484 1.359 5.016L2 22l5.156-1.359c1.484.813 3.172 1.25 4.875 1.25 5.516 0 9.969-4.453 9.969-9.969S17.547 2 12.031 2zm5.828 14.125c-.25.703-1.453 1.344-2.016 1.422-.531.078-1.203.109-1.953-.125-.453-.141-1.047-.344-1.797-.672-3.156-1.359-5.219-4.547-5.375-4.766-.156-.203-1.281-1.703-1.281-3.25s.813-2.313 1.094-2.625c.281-.313.625-.391.828-.391.203 0 .406.016.594.016.188.016.438-.078.688.531.25.609.859 2.094.938 2.25.078.156.125.344.031.547-.094.203-.141.328-.297.5-.156.172-.313.391-.453.516-.141.141-.297.297-.125.594.172.297.766 1.266 1.641 2.047 1.125 1.016 2.078 1.328 2.375 1.484.297.156.469.125.641-.078.172-.203.75-.875.953-1.172.203-.297.406-.25.688-.141.281.109 1.766.828 2.063.984.297.156.5.234.578.359.078.125.078.734-.172 1.438z"/>
                  </svg>
                  <span data-i18n="contact.direct_wa_btn">{escape(d['contact']['direct_wa_btn'])}</span>
                </a>
              </div>

              <!-- Smooth Submission Feedback Message -->
              <div class="contact-feedback-banner" id="contact-form-feedback" role="status" aria-live="polite" hidden></div>

              <p class="contact-privacy-note" data-i18n="contact.privacy_note">{escape(d['contact']['privacy_note'])}</p>
            </form>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- ========================================================================
       FOOTER & GERMAN LEGAL COMPLIANCE LINKS (Impressum & Datenschutzerklärung)
       ======================================================================== -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="brand-logo" style="margin-bottom:1rem;">
            <img src="/assets/images/favicon.svg" alt="Sabke German" class="brand-crest" width="40" height="40" />
            <div class="brand-text">
              <span class="brand-name" style="color:#FFFFFF;" data-i18n="nav.brand_name">{escape(d['nav']['brand_name'])}</span>
              <span class="brand-tagline">BERLIN • TEHRAN • BAKU</span>
            </div>
          </div>
          <p style="font-size:0.9rem; line-height:1.7; color:#94A3B8; margin-bottom:1.25rem;" data-i18n="footer.about">
            {escape(d['footer']['about'])}
          </p>
          <div style="display:flex; gap:0.65rem; flex-wrap:wrap;">
            <a href="/fa" class="pathway-pill">🇮🇷 فارسی</a>
            <a href="/de" class="pathway-pill">🇩🇪 Deutsch</a>
            <a href="/en" class="pathway-pill">🇬🇧 English</a>
            <a href="/az" class="pathway-pill">🇦🇿 Azərbaycan</a>
          </div>
        </div>

        <div>
          <h3 class="footer-title" data-i18n="footer.col_links">{escape(d['footer']['col_links'])}</h3>
          <div class="footer-links">
            <a href="#pathways" data-i18n="nav.pathways">{escape(d['nav']['pathways'])}</a>
            <a href="#services" data-i18n="nav.services">{escape(d['nav']['services'])}</a>
            <a href="#assessment" data-i18n="nav.calculator">{escape(d['nav']['calculator'])}</a>
            <a href="#cost-calculator" data-i18n="cost_calc.title">{escape(cc['title'])}</a>
            <a href="#visa-checklist" data-i18n="checklist_lead.title">{escape(cl['title'])}</a>
            <a href="#contact" data-i18n="nav.contact">{escape(d['nav']['contact'])}</a>
            <a href="/impressum" data-i18n="footer.impressum_btn">{escape(d['footer']['impressum_btn'])}</a>
            <a href="/datenschutz" data-i18n="footer.privacy_btn">{escape(d['footer']['privacy_btn'])}</a>
          </div>
        </div>

        <div>
          <h3 class="footer-title" data-i18n="footer.col_pathways">{escape(d['footer']['col_pathways'])}</h3>
          <div class="footer-links">
            <a href="#pathways">University (Bachelor / Master / PhD)</a>
            <a href="#pathways">Gymnasium &amp; Boarding (Internat)</a>
            <a href="#pathways">Studienkolleg (M / T / W / G-Kurs)</a>
            <a href="#pathways">Duale Ausbildung (€1,050–€1,400/mo)</a>
            <a href="#cost-calculator">Sperrkonto (€992/mo = €11,904/yr)</a>
            <a href="#visa-checklist">Free Visa Document Checklist</a>
          </div>
        </div>

        <div>
          <h3 class="footer-title" data-i18n="footer.col_offices">{escape(d['footer']['col_offices'])}</h3>
          <div class="footer-office-box">
            <strong style="color:#FFFFFF;">🇩🇪 Berlin Headquarters:</strong><br />
            {escape(SITE_CONFIG['street_address'])}, {escape(SITE_CONFIG['postal_city'])}<br />
            Tel: <span dir="ltr">{escape(SITE_CONFIG['phone'])}</span>
          </div>
          <div class="footer-office-box">
            <strong style="color:#FFFFFF;">🌍 Regional Desks (Tehran &amp; Baku):</strong><br />
            {escape(SITE_CONFIG['address_tehran_baku'])}<br />
            Email: <span dir="ltr">{escape(SITE_CONFIG['email'])}</span>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div data-i18n="footer.rights">{escape(d['footer']['rights'])}</div>
        <div class="footer-legal-links">
          <a href="/impressum" id="footer-impressum-link" data-i18n="footer.impressum_btn">{escape(d['footer']['impressum_btn'])}</a>
          <a href="/datenschutz" id="footer-privacy-link" data-i18n="footer.privacy_btn">{escape(d['footer']['privacy_btn'])}</a>
          <button type="button" id="open-cookie-settings" data-i18n="footer.cookie_settings_btn">{escape(d['footer']['cookie_settings_btn'])}</button>
        </div>
      </div>
    </div>
  </footer>

  <!-- ========================================================================
       FLOATING WHATSAPP & TELEGRAM QUICK-CONSULT WIDGET
       ======================================================================== -->
  <div class="floating-consult-widget" id="floating-consult-widget">
    <div class="floating-channels">
      <a href="{wa_direct_url}" target="_blank" rel="noopener noreferrer" class="channel-link" id="floating-wa-link">
        <span>💬</span>
        <span data-i18n="floating.whatsapp">{escape(d['floating']['whatsapp'])}</span>
      </a>
      <a href="https://t.me/{SITE_CONFIG['telegram_handle']}" target="_blank" rel="noopener noreferrer" class="channel-link" id="floating-tg-link">
        <span>✈️</span>
        <span data-i18n="floating.telegram">{escape(d['floating']['telegram'])}</span>
      </a>
      <a href="#contact" class="channel-link" id="floating-book-link">
        <span>📄</span>
        <span data-i18n="floating.book">{escape(d['floating']['book'])}</span>
      </a>
    </div>
    <div class="floating-bar-row">
      <a href="{wa_direct_url}" target="_blank" rel="noopener noreferrer" class="floating-wa-quick-btn" id="floating-wa-quick-btn">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12.031 2c-5.516 0-9.969 4.453-9.969 9.969 0 1.766.469 3.484 1.359 5.016L2 22l5.156-1.359c1.484.813 3.172 1.25 4.875 1.25 5.516 0 9.969-4.453 9.969-9.969S17.547 2 12.031 2zm5.828 14.125c-.25.703-1.453 1.344-2.016 1.422-.531.078-1.203.109-1.953-.125-.453-.141-1.047-.344-1.797-.672-3.156-1.359-5.219-4.547-5.375-4.766-.156-.203-1.281-1.703-1.281-3.25s.813-2.313 1.094-2.625c.281-.313.625-.391.828-.391.203 0 .406.016.594.016.188.016.438-.078.688.531.25.609.859 2.094.938 2.25.078.156.125.344.031.547-.094.203-.141.328-.297.5-.156.172-.313.391-.453.516-.141.141-.297.297-.125.594.172.297.766 1.266 1.641 2.047 1.125 1.016 2.078 1.328 2.375 1.484.297.156.469.125.641-.078.172-.203.75-.875.953-1.172.203-.297.406-.25.688-.141.281.109 1.766.828 2.063.984.297.156.5.234.578.359.078.125.078.734-.172 1.438z"/>
        </svg>
        <span data-i18n="floating.launcher">{escape(d['floating']['launcher'])}</span>
      </a>
      <button type="button" class="floating-more-btn" id="floating-launcher-btn" aria-label="More Contact Channels" title="More Channels">
        <span>▾</span>
      </button>
    </div>
  </div>

  <!-- ========================================================================
       MODAL 1: CONSULTATION BOOKING
       ======================================================================== -->
  <div class="modal-backdrop" id="consult-modal" role="dialog" aria-modal="true" aria-labelledby="consult-modal-title">
    <div class="modal-dialog">
      <div class="modal-header">
        <h3 class="modal-title" id="consult-modal-title" data-i18n="modals.consult_title">{escape(d['modals']['consult_title'])}</h3>
        <button type="button" class="modal-close" data-close-modal aria-label="Close">✕</button>
      </div>
      <p style="font-size:0.92rem; color:var(--text-secondary); margin-bottom:1.25rem;" data-i18n="modals.consult_sub">
        {escape(d['modals']['consult_sub'])}
      </p>
      <form id="consult-form" onsubmit="return false;" style="display:flex; flex-direction:column; gap:1rem;">
        <div class="form-group">
          <label class="form-label" style="color:var(--text-primary);" for="consult-name" data-i18n="modals.name_label">{escape(d['modals']['name_label'])}</label>
          <input type="text" id="consult-name" class="form-input" style="background:var(--bg-subtle); color:var(--text-primary); border-color:var(--border-strong);" placeholder="{escape(d['modals']['name_placeholder'])}" data-i18n-placeholder="modals.name_placeholder" />
        </div>
        <div class="form-group">
          <label class="form-label" style="color:var(--text-primary);" for="consult-contact" data-i18n="modals.contact_label">{escape(d['modals']['contact_label'])}</label>
          <input type="text" id="consult-contact" class="form-input" style="background:var(--bg-subtle); color:var(--text-primary); border-color:var(--border-strong);" placeholder="{escape(d['modals']['contact_placeholder'])}" data-i18n-placeholder="modals.contact_placeholder" dir="ltr" />
        </div>
        <div class="form-group">
          <label class="form-label" style="color:var(--text-primary);" for="consult-pathway-select" data-i18n="modals.pathway_label">{escape(d['modals']['pathway_label'])}</label>
          <select id="consult-pathway-select" class="form-select" style="background:var(--bg-subtle); color:var(--text-primary); border-color:var(--border-strong);">
            {''.join(f'<option value="{escape(t["title"])}">{escape(t["tab_label"])}</option>' for t in d['pathways']['tabs'])}
          </select>
        </div>
        <div class="form-group">
          <label class="form-label" style="color:var(--text-primary);" for="consult-notes" data-i18n="modals.notes_label">{escape(d['modals']['notes_label'])}</label>
          <textarea id="consult-notes" rows="3" class="form-input" style="background:var(--bg-subtle); color:var(--text-primary); border-color:var(--border-strong);" placeholder="{escape(d['modals']['notes_placeholder'])}" data-i18n-placeholder="modals.notes_placeholder"></textarea>
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:0.75rem; margin-top:0.5rem;">
          <button type="button" class="btn btn-whatsapp" id="consult-submit-wa" style="flex:1;">
            <span data-i18n="modals.submit_whatsapp">{escape(d['modals']['submit_whatsapp'])}</span>
          </button>
          <button type="button" class="btn btn-primary" id="consult-submit-email" style="flex:1;">
            <span data-i18n="modals.submit_email">{escape(d['modals']['submit_email'])}</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- ========================================================================
       GDPR COOKIE CONSENT BANNER
       ======================================================================== -->
  <aside class="cookie-banner" id="cookie-banner" aria-label="Cookie Consent Banner">
    <div class="cookie-title" data-i18n="cookie.title">{escape(d['cookie']['title'])}</div>
    <p class="cookie-text" data-i18n="cookie.text">{escape(d['cookie']['text'])}</p>
    <div class="cookie-actions">
      <button type="button" class="cookie-btn btn-primary" id="cookie-accept-btn" data-i18n="cookie.accept">{escape(d['cookie']['accept'])}</button>
      <button type="button" class="cookie-btn hero-btn-secondary" id="cookie-essential-btn" data-i18n="cookie.essential">{escape(d['cookie']['essential'])}</button>
    </div>
  </aside>

  <!-- Scripts -->
  <script src="/assets/js/i18n-data.js"></script>
  <script src="/assets/js/app.js"></script>
</body>
</html>
"""


def render_legal_page_html(page_type: str) -> str:
    """Renders dedicated /impressum/index.html or /datenschutz/index.html compliant with German DDG & GDPR."""
    domain = SITE_CONFIG["domain"]
    is_impressum = page_type == "impressum"
    slug = "impressum" if is_impressum else "datenschutz"
    title = (
        f"Impressum (§ 5 DDG) | {SITE_CONFIG['legal_name']}"
        if is_impressum
        else f"Datenschutzerklärung (DSGVO / GDPR) | {SITE_CONFIG['legal_name']}"
    )
    description = (
        f"Offizielles Impressum gemäß § 5 Digitale-Dienste-Gesetz (DDG) für {SITE_CONFIG['legal_name']} in Berlin."
        if is_impressum
        else f"Datenschutzerklärung gemäß DSGVO (GDPR) für {SITE_CONFIG['domain']} – Informationen zu Kontaktformular, PDF-Dokumenten-Upload und WhatsApp-Kommunikation."
    )

    if is_impressum:
        body_content = f"""
        <div class="eyebrow">RECHTLICHE ANGABEN • § 5 DDG / TMG</div>
        <h1 class="section-title" style="text-align:left; margin-bottom:1.5rem;">Impressum (Legal Notice)</h1>

        <div class="legal-page-card legal-prose">
          <h4>1. Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)</h4>
          <p>
            <strong>{escape(SITE_CONFIG['legal_name'])}</strong><br />
            {escape(SITE_CONFIG['street_address'])}<br />
            {escape(SITE_CONFIG['postal_city'])}
          </p>

          <h4>2. Vertreten durch die Geschäftsführung</h4>
          <p>Dr.-Ing. Pedram Rahimi &amp; Dipl.-Kfm. Lukas Weber (Geschäftsführung / Managing Directors)</p>

          <h4>3. Kontakt</h4>
          <p>
            Telefon: <a href="tel:{escape(SITE_CONFIG['phone'].replace(' ', ''))}">{escape(SITE_CONFIG['phone'])}</a><br />
            WhatsApp Direktberatung: <a href="https://wa.me/{escape(SITE_CONFIG['whatsapp_number'])}" target="_blank" rel="noopener noreferrer">+{escape(SITE_CONFIG['whatsapp_number'])}</a><br />
            E-Mail: <a href="mailto:{escape(SITE_CONFIG['email'])}">{escape(SITE_CONFIG['email'])}</a><br />
            Website: <a href="{escape(domain)}">{escape(domain)}</a>
          </p>

          <h4>4. Registereintrag &amp; Umsatzsteuer-ID</h4>
          <p>
            Registergericht: Amtsgericht Charlottenburg (Berlin)<br />
            Handelsregisternummer: HRB 249812 B (Platzhalter / i.G.)<br />
            Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz: DE358910421
          </p>

          <h4>5. Inhaltlich Verantwortlicher gemäß § 18 Abs. 2 MStV</h4>
          <p>
            Dr.-Ing. Pedram Rahimi<br />
            {escape(SITE_CONFIG['street_address'])}, {escape(SITE_CONFIG['postal_city'])}
          </p>

          <h4>6. Hinweis nach dem Rechtsdienstleistungsgesetz (RDG)</h4>
          <p>
            Sabke German erbringt akademische Bildungsberatung, Studienplatzvermittlung (Studienkolleg, Bachelor, Master), Ausbildungsplatzvermittlung sowie administrative Unterstützung bei Sperrkonto-Eröffnung und Einschreibung.
            Rechtsberatung im Sinne des Rechtsdienstleistungsgesetzes (RDG) – insbesondere im Rahmen von Visum- und Aufenthaltsverfahren – erfolgt ausschließlich durch kooperierende, in Deutschland zugelassene Rechtsanwälte für Migrationsrecht.
          </p>

          <h4>7. EU-Streitschlichtung &amp; Verbraucherstreitbeilegung (§ 36 VSBG)</h4>
          <p>
            Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit:
            <a href="https://ec.europa.eu/consumers/odr/" target="_blank" rel="noopener noreferrer">https://ec.europa.eu/consumers/odr/</a>.<br />
            Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.
          </p>
        </div>
        """
    else:
        body_content = f"""
        <div class="eyebrow">DSGVO / GDPR • DATENSCHUTZ</div>
        <h1 class="section-title" style="text-align:left; margin-bottom:1.5rem;">Datenschutzerklärung (Privacy Policy)</h1>

        <div class="legal-page-card legal-prose">
          <h4>1. Verantwortliche Stelle (Art. 4 Nr. 7 DSGVO)</h4>
          <p>
            Verantwortlich für die Datenverarbeitung auf dieser Website (<strong>{escape(domain)}</strong>) ist:<br />
            <strong>{escape(SITE_CONFIG['legal_name'])}</strong><br />
            {escape(SITE_CONFIG['street_address'])}, {escape(SITE_CONFIG['postal_city'])}<br />
            Telefon: {escape(SITE_CONFIG['phone'])}<br />
            E-Mail: <a href="mailto:{escape(SITE_CONFIG['email'])}">{escape(SITE_CONFIG['email'])}</a>
          </p>

          <h4>2. Hosting &amp; Vercel Web Analytics</h4>
          <p>
            Diese Website wird über <strong>Vercel Inc.</strong> bereitgestellt. Zur anonymisierten statistischen Auswertung und Optimierung unseres Webangebots nutzen wir <strong>Vercel Web Analytics</strong> (<code>/_vercel/insights/script.js</code>). Vercel Web Analytics verwendet keine Drittanbieter-Tracking-Cookies und speichert keine personenbezogenen IP-Profile (Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO).
          </p>

          <h4>3. Kontaktformular, Beratungsanfragen &amp; PDF-Dokumenten-Upload</h4>
          <p>
            Wenn Sie uns über das Beratungsformular (<code>#contact-consultation-form</code>) oder das Checklisten-Formular (<code>#checklist-lead-form</code>) kontaktieren, werden Ihre Angaben (Vollständiger Name, E-Mail-Adresse, WhatsApp-/Telefonnummer, gewünschter Bildungsweg, Nachricht sowie optional hochgeladene <strong>PDF-Bewerbungsunterlagen wie Zeugnisse oder Lebenslauf</strong> bis max. 10 MB) ausschließlich zum Zweck der Bearbeitung Ihrer Bildungsberatungsanfrage verarbeitet (Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO – vorvertragliche Maßnahmen – sowie Art. 6 Abs. 1 lit. a DSGVO).
          </p>
          <p>
            <strong>Hinweis zum PDF-Upload:</strong> Die Dateiprüfung (Dateityp <code>.pdf</code> und Maximalgröße 10 MB) erfolgt zunächst lokal in Ihrem Browser. Erst mit dem Absenden des Formulars werden die Daten verschlüsselt (TLS/HTTPS) an unseren Formular-Endpunkt übermittelt und nach Abschluss der Beratung bzw. gemäß gesetzlichen Aufbewahrungsfristen gelöscht.
          </p>

          <h4>4. Direkte WhatsApp-Kommunikation</h4>
          <p>
            Auf unserer Website bieten wir direkte Links zur Kontaktaufnahme über <strong>WhatsApp</strong> (<code>https://wa.me/{escape(SITE_CONFIG['whatsapp_number'])}</code>, betrieben durch WhatsApp Ireland Limited, 4 Grand Canal Square, Dublin 2, Irland) an. Erst wenn Sie aktiv auf einen WhatsApp-Button klicken, werden Ihre Telefonnummer und der vorausgefüllte Begrüßungs- bzw. Auswertungstext an WhatsApp übertragen (Rechtsgrundlage: Art. 6 Abs. 1 lit. a und b DSGVO).
          </p>

          <h4>5. Interaktiver 4-Schritte-Eignungscheck &amp; Sperrkonto-Rechner</h4>
          <p>
            Alle Berechnungen im interaktiven Eignungscheck (<code>#assessment</code>) sowie im Sperrkonto- und Studienkostenrechner (<code>#cost-calculator</code>) finden zu 100 % lokal in Ihrem Webbrowser (Client-Side JavaScript) statt. Es erfolgt keine automatische Übertragung Ihrer Eingaben an Server, solange Sie diese nicht aktiv per Formular oder WhatsApp absenden.
          </p>

          <h4>6. Lokale Speicherung (LocalStorage)</h4>
          <p>
            Wir nutzen technisch notwendige LocalStorage-Einträge (gemäß § 25 Abs. 2 TDDDG und Art. 6 Abs. 1 lit. f DSGVO), um Ihre Spracheinstellung (<code>fa</code>, <code>de</code>, <code>en</code>, <code>az</code>), Ihr Darstellungsschema (Light/Dark Mode) und Ihre Cookie-Präferenz zu speichern.
          </p>

          <h4>7. Ihre Betroffenenrechte nach DSGVO (Art. 15–21 DSGVO)</h4>
          <p>
            Sie haben jederzeit das Recht auf unentgeltliche Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16 DSGVO), Löschung (Art. 17 DSGVO), Einschränkung der Verarbeitung (Art. 18 DSGVO), Datenübertragbarkeit (Art. 20 DSGVO) sowie Widerspruch (Art. 21 DSGVO). Zudem besteht ein Beschwerderecht bei der Berliner Beauftragten für Datenschutz und Informationsfreiheit.
          </p>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="de" dir="ltr" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{domain}/{slug}" />
  <link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Vazirmatn:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/css/styles.css" />
  <script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
  <div class="german-tricolor-bar" aria-hidden="true"></div>
  <header class="site-header" id="site-header">
    <div class="container header-inner">
      <a href="/" class="brand-logo" aria-label="Sabke German Home">
        <img src="/assets/images/favicon.svg" alt="Sabke German Crest" class="brand-crest" width="42" height="42" />
        <div class="brand-text">
          <span class="brand-name">Sabke German</span>
          <span class="brand-tagline">BILDUNGSAGENTUR • BERLIN</span>
        </div>
      </a>
      <div class="header-controls">
        <div class="lang-switcher" role="group" aria-label="Language Switcher">
          <a href="/fa" class="lang-btn"><span class="lang-flag">🇮🇷</span><span>FA</span></a>
          <a href="/de" class="lang-btn active"><span class="lang-flag">🇩🇪</span><span>DE</span></a>
          <a href="/en" class="lang-btn"><span class="lang-flag">🇬🇧</span><span>EN</span></a>
          <a href="/az" class="lang-btn"><span class="lang-flag">🇦🇿</span><span>AZ</span></a>
        </div>
        <a href="/#contact" class="btn btn-primary header-cta">Beratung buchen</a>
      </div>
    </div>
  </header>

  <main class="section">
    <div class="container" style="max-width: 860px;">
      {body_content}
      <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
        <a href="/" class="btn btn-primary">← Zurück zur Startseite / بازگشت به صفحه اصلی</a>
        <a href="/{'datenschutz' if is_impressum else 'impressum'}" class="btn btn-outline">
          {'Datenschutzerklärung (GDPR)' if is_impressum else 'Impressum (§ 5 DDG)'}
        </a>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-bottom" style="border-top:none; padding-top:0;">
        <div>© 2026 {escape(SITE_CONFIG['legal_name'])}. Alle Rechte vorbehalten.</div>
        <div class="footer-legal-links">
          <a href="/impressum">Impressum</a>
          <a href="/datenschutz">Datenschutzerklärung</a>
          <a href="/">Startseite</a>
        </div>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def build_sitemap() -> str:
    domain = SITE_CONFIG["domain"]
    routes = ["", "/fa", "/de", "/en", "/az", "/impressum", "/datenschutz"]
    entries = []
    for r in routes:
        loc = f"{domain}{r}" if r else f"{domain}/"
        is_legal = r in ("/impressum", "/datenschutz")
        prio = "1.0" if r in ("", "/fa") else ("0.6" if is_legal else "0.9")
        hreflang_links = ""
        if not is_legal:
            hreflang_links = f"""
    <xhtml:link rel="alternate" hreflang="fa" href="{domain}/fa" />
    <xhtml:link rel="alternate" hreflang="de" href="{domain}/de" />
    <xhtml:link rel="alternate" hreflang="en" href="{domain}/en" />
    <xhtml:link rel="alternate" hreflang="az" href="{domain}/az" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{domain}/" />"""
        entries.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>2026-11-14</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{prio}</priority>{hreflang_links}
  </url>"""
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def build_llms_txt() -> str:
    domain = SITE_CONFIG["domain"]
    return f"""# Sabke German (سبک ژرمن) — Educational & Vocational Migration to Germany

> Official multilingual advisory agency headquartered in Berlin (`{SITE_CONFIG['street_address']}, {SITE_CONFIG['postal_city']}`) with regional desks in Tehran and Baku. Sabke German specializes in German public university admissions (Bachelor, Master, PhD), preparatory colleges (`Studienkolleg` M/T/W/G-Kurs), salaried vocational training (`Duale Ausbildung`), intensive German language visas, and Blocked Account (`Sperrkonto`) setup.

## Primary Website & Language Editions
- Canonical Root (Persian / RTL): {domain}/
- Persian (`fa` — فارسی): {domain}/fa
- German (`de` — Deutsch): {domain}/de
- English (`en` — English): {domain}/en
- Azerbaijani (`az` — Azərbaycan): {domain}/az

## Core Educational & Migration Pathways in Germany
1. **Studienkolleg (Preparatory College — M/T/W/G/S-Kurs)**:
   - Target group: 12-year high school diploma holders seeking tuition-free German university admission.
   - Requirements: High school diploma, German B1/B2 certificate, `Aufnahmetest` preparation, and €11,904/year Blocked Account (`Sperrkonto` at €992/month).
2. **Bachelor's Degree (`Direct Bachelor` at German Public Universities)**:
   - Target group: Applicants with direct university entrance qualification (`HZB`), 1 year of university study, or completed `Feststellungsprüfung (FSP)`.
   - Requirements: German C1 (`TestDaF` / `DSH-2`) or IELTS 6.5+ (English tracks), €11,904/year `Sperrkonto`, statutory student health insurance (~€130/month), and ~€300/semester `Semesterbeitrag` (0€ tuition at public universities).
3. **Master's Degree (`Master's Program` in English or German)**:
   - Target group: Bachelor's graduates from `Anabin H+` recognized universities.
   - Benefits: Tuition-free study at top public/TU9 universities, 20 hours/week student work permit, and 18-month post-graduation job-seeker residence permit.
4. **Salaried Vocational Training (`Duale Ausbildung`)**:
   - Target group: Applicants aged 18–34 with a high school diploma and German B1/B2 proficiency in Nursing (`Pflege`), IT, Mechatronics, Electrical Engineering, or Hospitality.
   - Financial structure: Monthly gross training salary of €1,050 to €1,400 from month one; no €11,904 Blocked Account required when salary meets the statutory threshold.
5. **Intensive German Language Course Visa (6–12 Months)**:
   - Target group: Applicants starting German immersion in Berlin, Munich, Hamburg, or Frankfurt (minimum 18 lessons/week) prior to university or `Studienkolleg`.

## Interactive Tools on {domain}
- **4-Step Smart Pathway Assessment (`{domain}/#assessment`)**: Evaluates Academic GPA, Language Level, Current Education & Age, and Financial Readiness to recommend the optimal German pathway with one-click WhatsApp export and consultation form pre-filling.
- **Blocked Account & Study Cost Calculator (`{domain}/#cost-calculator`)**: Calculates official 2026 German `Sperrkonto` deposits (€992/month = €5,952 for 6 months or €11,904 for 12 months), embassy visa fee (€75), student health insurance (~€130/month), and `Semesterbeitrag` (~€300/semester).
- **Free Germany Student Visa Document Checklist (`{domain}/#visa-checklist`)**: Printable/PDF-ready 9-point embassy checklist covering VIDEX, passport, admission letter, `Sperrkonto`, translations, language certificates, CV/SOP, health insurance, and embassy fees.

## Contact & Legal Compliance (German DDG & GDPR / DSGVO)
- **Legal Entity**: {SITE_CONFIG['legal_name']}
- **Berlin Address**: {SITE_CONFIG['street_address']}, {SITE_CONFIG['postal_city']}
- **Official Email**: {SITE_CONFIG['email']}
- **Phone (Berlin)**: {SITE_CONFIG['phone']}
- **WhatsApp Direct Consultation**: https://wa.me/{SITE_CONFIG['whatsapp_number']}
- **Impressum (§ 5 DDG)**: {domain}/impressum
- **Privacy Policy (Datenschutzerklärung / GDPR)**: {domain}/datenschutz
"""


def main():
    # 1. Write /assets/js/i18n-data.js
    js_path = os.path.join(ROOT_DIR, "assets", "js", "i18n-data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by build_site.py — Do not edit manually\n")
        f.write(f"window.SABKE_CONFIG = {json.dumps(SITE_CONFIG, ensure_ascii=False, indent=2)};\n")
        f.write(f"window.SABKE_I18N = {json.dumps(TRANSLATIONS, ensure_ascii=False, indent=2)};\n")
    print("✓ Generated assets/js/i18n-data.js")

    # 2. Write root /index.html (Defaulting to Persian 'fa')
    root_html = render_page_html("fa", is_root=True)
    with open(os.path.join(ROOT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(root_html)
    print("✓ Generated /index.html (fa default, dir=rtl)")

    # 3. Write localized pre-rendered routes (/fa, /de, /en, /az)
    for lang in ("fa", "de", "en", "az"):
        lang_dir = os.path.join(ROOT_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        html_content = render_page_html(lang, is_root=False)
        with open(os.path.join(lang_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✓ Generated /{lang}/index.html (dir={TRANSLATIONS[lang]['dir']})")

    # 4. Write dedicated German legal pages (/impressum/index.html & /datenschutz/index.html)
    for legal_slug in ("impressum", "datenschutz"):
        legal_dir = os.path.join(ROOT_DIR, legal_slug)
        os.makedirs(legal_dir, exist_ok=True)
        legal_html = render_legal_page_html(legal_slug)
        with open(os.path.join(legal_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(legal_html)
        print(f"✓ Generated /{legal_slug}/index.html")

    # 5. Write sitemap.xml
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap())
    print("✓ Generated /sitemap.xml")

    # 6. Write robots.txt
    robots = f"""User-agent: *
Allow: /
Allow: /llms.txt

Sitemap: {SITE_CONFIG['domain']}/sitemap.xml
"""
    with open(os.path.join(ROOT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print("✓ Generated /robots.txt")

    # 7. Write llms.txt (AEO / AI Search Engine Optimization)
    with open(os.path.join(ROOT_DIR, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(build_llms_txt())
    print("✓ Generated /llms.txt")


if __name__ == "__main__":
    main()
