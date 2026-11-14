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
  - /assets/js/i18n-data.js
  - /sitemap.xml
  - /robots.txt
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
        "alternateName": ["Sabke German", "سبک ژرمن", "Sabke German Bildungsberatung"],
        "url": f"{domain}/{lang_code}" if lang_code != "fa" else domain,
        "logo": f"{domain}/assets/images/favicon.svg",
        "image": f"{domain}/assets/images/hero-campus.jpg",
        "description": d["meta"]["description"],
        "email": SITE_CONFIG["email"],
        "telephone": SITE_CONFIG["phone_de"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Kurfürstendamm 194",
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
    canonical_url = domain if is_root else f"{domain}/{lang_code}"
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

    # Pre-render Calculator Step 1
    calc_steps_html = "\n".join(
        [
            f'''            <button type="button" class="wizard-step-indicator {'active' if i == 0 else ''}" data-goto-step="{i + 1}">
              <span class="step-num">{i + 1}</span>
              <span>{escape(lbl)}</span>
            </button>'''
            for i, lbl in enumerate(d["calculator"]["steps_nav"])
        ]
    )
    calc_goals_html = "\n".join(
        [
            f'''              <button type="button" class="wizard-option-card {'selected' if g['id'] == 'master' else ''}" data-select-goal="{g['id']}">
                <span class="option-title">{escape(g['title'])}</span>
                <span class="option-sub">{escape(g['sub'])}</span>
              </button>'''
            for g in d["calculator"]["goals"]
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

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/assets/images/favicon.svg" />

  <!-- Google Fonts: Vazirmatn (Persian RTL) + Plus Jakarta Sans & Inter (DE/EN/AZ LTR) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Vazirmatn:wght@400;500;600;700;800&display=swap" rel="stylesheet" />

  <!-- Stylesheet -->
  <link rel="stylesheet" href="/assets/css/styles.css" />

  <!-- JSON-LD Structured Data (EducationalOrganization + FAQPage) -->
  {json_ld_block}
</head>
<body>
  <!-- Subtle German Flag Top Accent Bar -->
  <div class="german-tricolor-bar" aria-hidden="true"></div>

  <!-- ========================================================================
       STICKY HEADER & MULTILINGUAL NAVIGATION
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

      <nav class="main-nav" aria-label="Primary Navigation">
        <a href="#pathways" class="nav-link" data-i18n="nav.pathways">{escape(d['nav']['pathways'])}</a>
        <a href="#services" class="nav-link" data-i18n="nav.services">{escape(d['nav']['services'])}</a>
        <a href="#calculator" class="nav-link" data-i18n="nav.calculator">{escape(d['nav']['calculator'])}</a>
        <a href="#roadmap" class="nav-link" data-i18n="nav.roadmap">{escape(d['nav']['roadmap'])}</a>
        <a href="#pricing" class="nav-link" data-i18n="nav.pricing">{escape(d['nav']['pricing'])}</a>
        <a href="#stories" class="nav-link" data-i18n="nav.stories">{escape(d['nav']['stories'])}</a>
        <a href="#faq" class="nav-link" data-i18n="nav.faq">{escape(d['nav']['faq'])}</a>
        <a href="#contact" class="nav-link" data-i18n="nav.contact">{escape(d['nav']['contact'])}</a>
      </nav>

      <div class="header-controls">
        <!-- 4-Language Switcher (FA | DE | EN | AZ) -->
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

        <button type="button" class="mobile-menu-btn" id="mobile-menu-btn" aria-label="Open Navigation Menu">
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
              <a href="#calculator" class="btn btn-primary" id="hero-cta-eligibility">
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
         B. STUDY PATHWAYS IN GERMANY (Interactive Tabbed Detail View)
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
                <span>{escape(d['pathways']['cta_evaluate'])}</span>
              </button>
              <button type="button" class="btn btn-outline" data-open-modal="consult-modal" data-preselect-pathway="{escape(active_tab['title'])}" id="pathway-consult-cta">
                <span>{escape(d['pathways']['cta_consult'])}</span>
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
         D. INTERACTIVE SMART ELIGIBILITY CALCULATOR (4-Step Assessment Wizard)
         ====================================================================== -->
    <section class="section calculator-section" id="calculator">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow" data-i18n="calculator.eyebrow">{escape(d['calculator']['eyebrow'])}</div>
          <h2 class="section-title" data-i18n="calculator.title">{escape(d['calculator']['title'])}</h2>
          <p class="section-subtitle" data-i18n="calculator.subtitle">{escape(d['calculator']['subtitle'])}</p>
        </div>

        <div class="wizard-card" id="wizard-card-container">
          <div class="wizard-progress">
{calc_steps_html}
          </div>
          <div class="wizard-step-pane active">
            <h3 class="wizard-question-title">{escape(d['calculator']['step1_title'])}</h3>
            <p class="wizard-question-hint">{escape(d['calculator']['step1_hint'])}</p>
            <div class="wizard-options-grid">
{calc_goals_html}
            </div>
          </div>
          <div class="wizard-footer">
            <span></span>
            <button type="button" class="btn btn-primary" id="wizard-next-btn">{escape(d['calculator']['btn_next'])}</button>
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
         H. CONTACT, CONSULTATION & PDF DOCUMENT UPLOAD SECTION
         ====================================================================== -->
    <section class="section contact-section" id="contact">
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
                  <div class="contact-info-val">{escape(SITE_CONFIG['address_berlin'])}</div>
                </div>
              </div>
              <div class="contact-info-item">
                <span class="contact-info-icon">📞</span>
                <div>
                  <div class="contact-info-label">WhatsApp &amp; Direct Line</div>
                  <div class="contact-info-val" dir="ltr">+49 000 0000000 • {escape(SITE_CONFIG['phone_de'])}</div>
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
       FOOTER & GERMAN LEGAL COMPLIANCE LINKS (Impressum & GDPR)
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
            <a href="#calculator" data-i18n="nav.calculator">{escape(d['nav']['calculator'])}</a>
            <a href="#roadmap" data-i18n="nav.roadmap">{escape(d['nav']['roadmap'])}</a>
            <a href="#pricing" data-i18n="nav.pricing">{escape(d['nav']['pricing'])}</a>
            <a href="#faq" data-i18n="nav.faq">{escape(d['nav']['faq'])}</a>
            <a href="#contact" data-i18n="nav.contact">{escape(d['nav']['contact'])}</a>
          </div>
        </div>

        <div>
          <h3 class="footer-title" data-i18n="footer.col_pathways">{escape(d['footer']['col_pathways'])}</h3>
          <div class="footer-links">
            <a href="#pathways">University (Bachelor / Master / PhD)</a>
            <a href="#pathways">Gymnasium &amp; Boarding (Internat)</a>
            <a href="#pathways">Studienkolleg (M / T / W / G-Kurs)</a>
            <a href="#pathways">Duale Ausbildung (€1,000–€1,400/mo)</a>
            <a href="#pathways">Sperrkonto (Fintiba / Expatrio)</a>
            <a href="#pathways">Anmeldung &amp; Post-Arrival Berlin</a>
          </div>
        </div>

        <div>
          <h3 class="footer-title" data-i18n="footer.col_offices">{escape(d['footer']['col_offices'])}</h3>
          <div class="footer-office-box">
            <strong style="color:#FFFFFF;">🇩🇪 Berlin Headquarters:</strong><br />
            {escape(SITE_CONFIG['address_berlin'])}<br />
            Tel: <span dir="ltr">{escape(SITE_CONFIG['phone_de'])}</span>
          </div>
          <div class="footer-office-box">
            <strong style="color:#FFFFFF;">🌍 Regional Desks (Tehran &amp; Baku):</strong><br />
            {escape(SITE_CONFIG['address_tehran_baku'])}<br />
            Email: {escape(SITE_CONFIG['email'])}
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <div data-i18n="footer.rights">{escape(d['footer']['rights'])}</div>
        <div class="footer-legal-links">
          <button type="button" data-open-modal="impressum-modal" id="footer-impressum-btn" data-i18n="footer.impressum_btn">{escape(d['footer']['impressum_btn'])}</button>
          <button type="button" data-open-modal="privacy-modal" id="footer-privacy-btn" data-i18n="footer.privacy_btn">{escape(d['footer']['privacy_btn'])}</button>
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
       MODAL 2: GERMAN IMPRESSUM (§ 5 DDG / TMG Legal Compliance)
       ======================================================================== -->
  <div class="modal-backdrop" id="impressum-modal" role="dialog" aria-modal="true" aria-labelledby="impressum-modal-title">
    <div class="modal-dialog legal-prose" dir="ltr" style="text-align:left;">
      <div class="modal-header">
        <h3 class="modal-title" id="impressum-modal-title" data-i18n="modals.impressum_title">{escape(d['modals']['impressum_title'])}</h3>
        <button type="button" class="modal-close" data-close-modal aria-label="Close">✕</button>
      </div>
      <h4>Angaben gemäß § 5 Digitale-Dienste-Gesetz (DDG)</h4>
      <p>
        <strong>Sabke German Bildungs- &amp; Migrationsberatung GmbH</strong><br />
        Kurfürstendamm 194<br />
        10707 Berlin, Bundesrepublik Deutschland
      </p>
      <h4>Vertreten durch die Geschäftsführung</h4>
      <p>Dr.-Ing. Pedram Rahimi &amp; Dipl.-Kfm. Lukas Weber</p>
      <h4>Kontakt</h4>
      <p>
        Telefon: {escape(SITE_CONFIG['phone_de'])}<br />
        E-Mail: {escape(SITE_CONFIG['email'])}<br />
        Website: {escape(SITE_CONFIG['domain'])}
      </p>
      <h4>Registereintrag &amp; Umsatzsteuer-ID</h4>
      <p>
        Registergericht: Amtsgericht Charlottenburg (Berlin)<br />
        Handelsregisternummer: HRB 249812 B<br />
        Umsatzsteuer-Identifikationsnummer gemäß § 27 a Umsatzsteuergesetz: DE358910421
      </p>
      <h4>Verbraucherstreitbeilegung / Universalschlichtungsstelle</h4>
      <p>
        Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: https://ec.europa.eu/consumers/odr/.
        Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.
        Rechtsberatung im Sinne des Rechtsdienstleistungsgesetzes (RDG) wird ausschließlich durch kooperierende deutsche Fachanwälte für Migrationsrecht erbracht.
      </p>
    </div>
  </div>

  <!-- ========================================================================
       MODAL 3: DATENSCHUTZERKLÄRUNG (GDPR / DSGVO Privacy Policy)
       ======================================================================== -->
  <div class="modal-backdrop" id="privacy-modal" role="dialog" aria-modal="true" aria-labelledby="privacy-modal-title">
    <div class="modal-dialog legal-prose" dir="ltr" style="text-align:left;">
      <div class="modal-header">
        <h3 class="modal-title" id="privacy-modal-title" data-i18n="modals.privacy_title">{escape(d['modals']['privacy_title'])}</h3>
        <button type="button" class="modal-close" data-close-modal aria-label="Close">✕</button>
      </div>
      <h4>1. Datenschutz auf einen Blick (Art. 13 DSGVO / GDPR)</h4>
      <p>
        Der Schutz Ihrer personenbezogenen Daten hat für <strong>Sabke German</strong> höchste Priorität.
        Alle Eingaben im interaktiven Eignungsrechner (Eligibility Calculator) werden ausschließlich lokal in Ihrem Browser (Client-Side) berechnet und erst dann übermittelt, wenn Sie aktiv auf den WhatsApp- oder E-Mail-Button klicken.
      </p>
      <h4>2. Verantwortliche Stelle</h4>
      <p>
        Sabke German Bildungs- &amp; Migrationsberatung GmbH, Kurfürstendamm 194, 10707 Berlin, Deutschland.
        Datenschutzbeauftragter: datenschutz@sabkegerman.de
      </p>
      <h4>3. Lokale Speicherung (LocalStorage) &amp; Cookies</h4>
      <p>
        Diese Website nutzt ausschließlich technisch notwendige LocalStorage-Einträge (Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO sowie § 25 Abs. 2 TDDDG), um Ihre gewählte Sprache (<code>fa</code>, <code>de</code>, <code>en</code>, <code>az</code>), Ihr Farbschema (Dark/Light Mode) und Ihre Cookie-Einwilligung zu speichern. Es werden keine Werbe- oder Drittanbieter-Tracking-Cookies ohne Ihre ausdrückliche Zustimmung geladen.
      </p>
      <h4>4. Ihre Rechte nach DSGVO</h4>
      <p>
        Sie haben jederzeit das Recht auf unentgeltliche Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16 DSGVO), Löschung (Art. 17 DSGVO), Einschränkung der Verarbeitung (Art. 18 DSGVO) sowie Datenübertragbarkeit (Art. 20 DSGVO).
      </p>
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


def build_sitemap() -> str:
    domain = SITE_CONFIG["domain"]
    routes = ["", "/fa", "/de", "/en", "/az"]
    entries = []
    for r in routes:
        loc = f"{domain}{r}" if r else f"{domain}/"
        entries.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>2026-11-13</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{'1.0' if r in ('', '/fa') else '0.9'}</priority>
    <xhtml:link rel="alternate" hreflang="fa" href="{domain}/fa" />
    <xhtml:link rel="alternate" hreflang="de" href="{domain}/de" />
    <xhtml:link rel="alternate" hreflang="en" href="{domain}/en" />
    <xhtml:link rel="alternate" hreflang="az" href="{domain}/az" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{domain}/" />
  </url>"""
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


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

    # 4. Write sitemap.xml
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap())
    print("✓ Generated /sitemap.xml")

    # 5. Write robots.txt
    robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_CONFIG['domain']}/sitemap.xml
"""
    with open(os.path.join(ROOT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print("✓ Generated /robots.txt")


if __name__ == "__main__":
    main()
