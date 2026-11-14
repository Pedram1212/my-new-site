/**
 * SABKE GERMAN (سبک ژرمن) — Core Interactive Application & Multilingual Engine
 * Supports: Persian (fa - RTL), German (de - LTR), English (en - LTR), Azerbaijani (az - LTR)
 */

(function () {
  'use strict';

  const state = {
    lang: document.documentElement.lang || 'fa',
    theme: localStorage.getItem('sabke_theme') || 'light',
    activePathwayId: 'university',
    activeStoryFilter: 'all',
    wizard: {
      step: 1,
      goal: 'master',
      age: 23,
      gpa: 17.5,
      langStatus: 'en_ielts',
      finance: 'blocked_ready',
      calculated: false,
      score: 92,
      recommendedKey: 'master',
    },
  };

  /* --------------------------------------------------------------------------
     1. UTILITY HELPERS
     -------------------------------------------------------------------------- */
  function getDict() {
    if (!window.SABKE_I18N) return null;
    return window.SABKE_I18N[state.lang] || window.SABKE_I18N.fa;
  }

  function toPersianDigits(str) {
    if (state.lang !== 'fa') return String(str);
    const persian = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    return String(str).replace(/[0-9]/g, (w) => persian[+w]);
  }

  // Bavarian Formula (Bayerische Formel): 1 + 3 * ((Nmax - Nd) / (Nmax - Nmin))
  function calcGermanGrade(gpa20) {
    const clamped = Math.max(10, Math.min(20, parseFloat(gpa20) || 16));
    const grade = 1 + 3 * ((20 - clamped) / (20 - 10));
    return grade.toFixed(1);
  }

  /* --------------------------------------------------------------------------
     2. THEME CONTROLLER (Light / Dark)
     -------------------------------------------------------------------------- */
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('sabke_theme', theme);
    const sunIcon = document.getElementById('theme-icon-sun');
    const moonIcon = document.getElementById('theme-icon-moon');
    if (sunIcon && moonIcon) {
      sunIcon.style.display = theme === 'dark' ? 'block' : 'none';
      moonIcon.style.display = theme === 'dark' ? 'none' : 'block';
    }
  }

  /* --------------------------------------------------------------------------
     3. DYNAMIC RENDERERS FOR INTERACTIVE SECTIONS
     -------------------------------------------------------------------------- */
  function renderPathways() {
    const dict = getDict();
    if (!dict) return;

    const tabsNav = document.getElementById('pathways-tabs-nav');
    const detailPanel = document.getElementById('pathway-detail-panel');
    if (!tabsNav || !detailPanel) return;

    const tabs = dict.pathways.tabs;
    const activeTab = tabs.find((t) => t.id === state.activePathwayId) || tabs[0];

    tabsNav.innerHTML = tabs
      .map(
        (t) => `
      <button type="button" class="pathway-tab-btn ${t.id === activeTab.id ? 'active' : ''}" data-pathway-id="${t.id}" id="tab-btn-${t.id}">
        <span class="tab-icon">✦</span>
        <span>${t.tab_label}</span>
      </button>
    `
      )
      .join('');

    detailPanel.innerHTML = `
      <div class="pathway-content-col">
        <div class="pathway-badge-row">
          <span class="pathway-pill pathway-pill-gold">${activeTab.badge_1}</span>
          <span class="pathway-pill">${activeTab.badge_2}</span>
        </div>
        <h3 class="pathway-title">${activeTab.title}</h3>
        <p class="pathway-desc">${activeTab.desc}</p>
        <ul class="pathway-features-list">
          ${activeTab.features
            .map(
              (f) => `
            <li class="pathway-feature-item">
              <span class="feature-check">✓</span>
              <span>${f}</span>
            </li>
          `
            )
            .join('')}
        </ul>
        <div class="hero-actions" style="margin-bottom:0;">
          <button type="button" class="btn btn-primary" data-jump-calc="${activeTab.id}" id="pathway-eval-cta">
            <span>${dict.pathways.cta_evaluate}</span>
          </button>
          <button type="button" class="btn btn-outline" data-open-modal="consult-modal" data-preselect-pathway="${activeTab.title}" id="pathway-consult-cta">
            <span>${dict.pathways.cta_consult}</span>
          </button>
        </div>
      </div>
      <div class="pathway-metrics-card">
        <img src="${activeTab.image}" alt="${activeTab.title}" class="pathway-visual-img" loading="lazy" />
        <div class="pathway-metrics-body">
          <div class="metric-box">
            <div class="metric-label">${activeTab.m1_label}</div>
            <div class="metric-value">${activeTab.m1_val}</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">${activeTab.m2_label}</div>
            <div class="metric-value">${activeTab.m2_val}</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">${activeTab.m3_label}</div>
            <div class="metric-value">${activeTab.m3_val}</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">${activeTab.m4_label}</div>
            <div class="metric-value">${activeTab.m4_val}</div>
          </div>
        </div>
      </div>
    `;
  }

  function renderServices() {
    const dict = getDict();
    const grid = document.getElementById('services-grid');
    if (!dict || !grid) return;

    const icons = [
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="m9 16 2 2 4-4"/></svg>',
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="10" x2="22" y2="10"/></svg>',
      '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    ];

    grid.innerHTML = dict.services.cards
      .map(
        (c, idx) => `
      <article class="service-card">
        <div>
          <div class="service-header">
            <div class="service-icon-box">${icons[idx % icons.length]}</div>
            <span class="service-step-tag">${c.step}</span>
          </div>
          <h3 class="service-title">${c.title}</h3>
          <p class="service-desc">${c.desc}</p>
        </div>
        <div class="service-tags">
          ${c.tags.map((tag) => `<span class="service-tag">${tag}</span>`).join('')}
        </div>
      </article>
    `
      )
      .join('');
  }

  /* --------------------------------------------------------------------------
     4. INTERACTIVE SMART ELIGIBILITY CALCULATOR (4-Step Wizard)
     -------------------------------------------------------------------------- */
  function calculateEligibilityScore() {
    const w = state.wizard;
    let score = 72;

    // GPA contribution (out of 20)
    const gpa = parseFloat(w.gpa) || 16;
    if (gpa >= 18) score += 14;
    else if (gpa >= 16) score += 11;
    else if (gpa >= 14.5) score += 7;
    else score += 3;

    // Age fit per goal
    const age = parseInt(w.age, 10) || 23;
    if (w.goal === 'highschool') {
      score += age <= 18 ? 10 : -8;
    } else if (w.goal === 'bachelor') {
      score += age <= 25 ? 8 : age <= 29 ? 4 : 1;
    } else if (w.goal === 'master') {
      score += age <= 31 ? 9 : age <= 35 ? 5 : 2;
    } else if (w.goal === 'ausbildung') {
      score += age >= 18 && age <= 34 ? 10 : 4;
    } else {
      score += 8;
    }

    // Language certificate bonus
    if (w.langStatus === 'de_b2_c1') score += 8;
    else if (w.langStatus === 'de_b1' || w.langStatus === 'en_ielts') score += 6;
    else if (w.langStatus === 'de_a1_a2') score += 3;

    // Financial readiness alignment
    if (w.finance === 'blocked_ready') score += 4;
    else if (w.finance === 'salaried_only' && w.goal !== 'phd') {
      w.recommendedKey = 'ausbildung';
    } else {
      w.recommendedKey = w.goal;
    }

    if (w.finance !== 'salaried_only') {
      w.recommendedKey = w.goal;
    }

    w.score = Math.max(68, Math.min(98, score));
  }

  function renderCalculator() {
    const dict = getDict();
    const container = document.getElementById('wizard-card-container');
    if (!dict || !container) return;

    const c = dict.calculator;
    const w = state.wizard;
    const germanGrade = calcGermanGrade(w.gpa);

    if (w.calculated) {
      const rec = c.recommendations[w.recommendedKey] || c.recommendations.master;
      const deg = Math.round((w.score / 100) * 360);

      const goalObj = c.goals.find((g) => g.id === w.goal) || c.goals[0];
      const langObj = c.langs.find((l) => l.id === w.langStatus) || c.langs[0];
      const finObj = c.finance.find((f) => f.id === w.finance) || c.finance[0];

      const summaryText = [
        `Sabke German — Smart Assessment (${state.lang.toUpperCase()})`,
        `• Score: ${w.score}%`,
        `• Goal: ${goalObj.title}`,
        `• Age: ${w.age} | GPA: ${w.gpa}/20 (German Grade: ${germanGrade})`,
        `• Language: ${langObj.title}`,
        `• Finance: ${finObj.title}`,
        `• Recommended: ${rec.title}`,
      ].join('\n');

      const waUrl = `https://wa.me/${window.SABKE_CONFIG.whatsapp_number}?text=${encodeURIComponent(summaryText)}`;
      const mailUrl = `mailto:${window.SABKE_CONFIG.email}?subject=${encodeURIComponent('Sabke German Eligibility Assessment')}&body=${encodeURIComponent(summaryText)}`;

      container.innerHTML = `
        <div class="wizard-result-box">
          <div class="result-top-grid">
            <div class="score-ring-container" style="--score-deg: ${deg}deg;">
              <div class="score-ring-inner">
                <span class="score-value">${toPersianDigits(w.score)}%</span>
                <span class="score-caption">${c.result_score_label}</span>
              </div>
            </div>
            <div>
              <h3 class="result-pathway-title">${rec.title}</h3>
              <p class="result-pathway-desc">${rec.desc}</p>
              <div class="result-Metrics-pills">
                <span class="result-pill">🎯 ${goalObj.title}</span>
                <span class="result-pill">📊 ${c.german_grade_equiv} <strong>${toPersianDigits(germanGrade)}</strong></span>
                <span class="result-pill">🗣 ${langObj.title}</span>
              </div>
            </div>
          </div>
          <div class="result-actions">
            <a href="${waUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp" id="calc-whatsapp-btn">
              <span>${c.result_send_whatsapp}</span>
            </a>
            <a href="${mailUrl}" class="btn btn-primary" id="calc-email-btn">
              <span>${c.result_send_email}</span>
            </a>
            <button type="button" class="btn hero-btn-secondary" id="calc-restart-btn">
              <span>${c.btn_restart}</span>
            </button>
          </div>
        </div>
      `;
      return;
    }

    const progressHtml = `
      <div class="wizard-progress">
        ${c.steps_nav
          .map((label, idx) => {
            const stepNum = idx + 1;
            const cls = stepNum === w.step ? 'active' : stepNum < w.step ? 'completed' : '';
            return `
            <button type="button" class="wizard-step-indicator ${cls}" data-goto-step="${stepNum}">
              <span class="step-num">${stepNum < w.step ? '✓' : toPersianDigits(stepNum)}</span>
              <span>${label}</span>
            </button>
          `;
          })
          .join('')}
      </div>
    `;

    let stepBodyHtml = '';
    if (w.step === 1) {
      stepBodyHtml = `
        <div class="wizard-step-pane active">
          <h3 class="wizard-question-title">${c.step1_title}</h3>
          <p class="wizard-question-hint">${c.step1_hint}</p>
          <div class="wizard-options-grid">
            ${c.goals
              .map(
                (g) => `
              <button type="button" class="wizard-option-card ${w.goal === g.id ? 'selected' : ''}" data-select-goal="${g.id}">
                <span class="option-title">${g.title}</span>
                <span class="option-sub">${g.sub}</span>
              </button>
            `
              )
              .join('')}
          </div>
        </div>
      `;
    } else if (w.step === 2) {
      stepBodyHtml = `
        <div class="wizard-step-pane active">
          <h3 class="wizard-question-title">${c.step2_title}</h3>
          <p class="wizard-question-hint">${c.step2_hint}</p>
          <div class="wizard-inputs-grid">
            <div class="form-group">
              <label class="form-label" for="calc-age-input">
                <span>${c.age_label}</span>
                <strong id="calc-age-display">${toPersianDigits(w.age)}</strong>
              </label>
              <input type="number" id="calc-age-input" class="form-input" min="12" max="50" value="${w.age}" />
              <input type="range" id="calc-age-range" class="range-slider" min="12" max="45" value="${w.age}" />
            </div>
            <div class="form-group">
              <label class="form-label" for="calc-gpa-input">
                <span>${c.gpa_label}</span>
                <strong id="calc-gpa-display">${toPersianDigits(w.gpa)} / ${toPersianDigits(20)}</strong>
              </label>
              <input type="number" id="calc-gpa-input" class="form-input" min="10" max="20" step="0.1" value="${w.gpa}" />
              <input type="range" id="calc-gpa-range" class="range-slider" min="10" max="20" step="0.1" value="${w.gpa}" />
              <div style="margin-top:0.4rem; font-size:0.85rem; color:var(--gold-400);">
                ${c.german_grade_equiv} <strong id="calc-de-grade-val">${toPersianDigits(germanGrade)}</strong> (1.0 = Best)
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (w.step === 3) {
      stepBodyHtml = `
        <div class="wizard-step-pane active">
          <h3 class="wizard-question-title">${c.step3_title}</h3>
          <p class="wizard-question-hint">${c.step3_hint}</p>
          <div class="wizard-options-grid">
            ${c.langs
              .map(
                (l) => `
              <button type="button" class="wizard-option-card ${w.langStatus === l.id ? 'selected' : ''}" data-select-lang-cert="${l.id}">
                <span class="option-title">${l.title}</span>
                <span class="option-sub">${l.sub}</span>
              </button>
            `
              )
              .join('')}
          </div>
        </div>
      `;
    } else if (w.step === 4) {
      stepBodyHtml = `
        <div class="wizard-step-pane active">
          <h3 class="wizard-question-title">${c.step4_title}</h3>
          <p class="wizard-question-hint">${c.step4_hint}</p>
          <div class="wizard-options-grid">
            ${c.finance
              .map(
                (f) => `
              <button type="button" class="wizard-option-card ${w.finance === f.id ? 'selected' : ''}" data-select-finance="${f.id}">
                <span class="option-title">${f.title}</span>
                <span class="option-sub">${f.sub}</span>
              </button>
            `
              )
              .join('')}
          </div>
        </div>
      `;
    }

    const footerHtml = `
      <div class="wizard-footer">
        ${
          w.step > 1
            ? `<button type="button" class="btn hero-btn-secondary" id="wizard-prev-btn">${c.btn_prev}</button>`
            : `<span></span>`
        }
        ${
          w.step < 4
            ? `<button type="button" class="btn btn-primary" id="wizard-next-btn">${c.btn_next}</button>`
            : `<button type="button" class="btn btn-primary" id="wizard-finish-btn">${c.btn_calculate}</button>`
        }
      </div>
    `;

    container.innerHTML = progressHtml + stepBodyHtml + footerHtml;

    // Bind Step 2 live inputs if active
    const ageInput = document.getElementById('calc-age-input');
    const ageRange = document.getElementById('calc-age-range');
    const gpaInput = document.getElementById('calc-gpa-input');
    const gpaRange = document.getElementById('calc-gpa-range');

    if (ageInput && ageRange) {
      const syncAge = (val) => {
        w.age = Math.max(12, Math.min(50, parseInt(val, 10) || 18));
        ageInput.value = w.age;
        ageRange.value = Math.min(45, w.age);
        const disp = document.getElementById('calc-age-display');
        if (disp) disp.textContent = toPersianDigits(w.age);
      };
      ageInput.addEventListener('input', (e) => syncAge(e.target.value));
      ageRange.addEventListener('input', (e) => syncAge(e.target.value));
    }

    if (gpaInput && gpaRange) {
      const syncGpa = (val) => {
        w.gpa = Math.max(10, Math.min(20, parseFloat(val) || 16));
        gpaInput.value = w.gpa;
        gpaRange.value = w.gpa;
        const disp = document.getElementById('calc-gpa-display');
        const deDisp = document.getElementById('calc-de-grade-val');
        if (disp) disp.textContent = `${toPersianDigits(w.gpa)} / ${toPersianDigits(20)}`;
        if (deDisp) deDisp.textContent = toPersianDigits(calcGermanGrade(w.gpa));
      };
      gpaInput.addEventListener('input', (e) => syncGpa(e.target.value));
      gpaRange.addEventListener('input', (e) => syncGpa(e.target.value));
    }
  }

  /* --------------------------------------------------------------------------
     5. ROADMAP, PRICING, SUCCESS STORIES & FAQ RENDERERS
     -------------------------------------------------------------------------- */
  function renderRoadmap() {
    const dict = getDict();
    const grid = document.getElementById('roadmap-grid');
    if (!dict || !grid) return;

    grid.innerHTML = dict.roadmap.steps
      .map(
        (s) => `
      <div class="roadmap-step-card">
        <div class="roadmap-step-top">
          <span class="roadmap-number">${s.num}</span>
          <span class="roadmap-duration">${s.duration}</span>
        </div>
        <h3 class="roadmap-title">${s.title}</h3>
        <p class="roadmap-desc">${s.desc}</p>
      </div>
    `
      )
      .join('');
  }

  function renderPricing() {
    const dict = getDict();
    const grid = document.getElementById('pricing-grid');
    if (!dict || !grid) return;

    grid.innerHTML = dict.pricing.tiers
      .map(
        (t) => `
      <div class="pricing-card ${t.popular ? 'popular' : ''}">
        ${t.popular ? `<span class="popular-badge">${dict.pricing.popular_badge}</span>` : ''}
        <div>
          <h3 class="pricing-tier-name">${t.name}</h3>
          <p class="pricing-tier-tagline">${t.tagline}</p>
          <div class="pricing-price-box">
            <span class="pricing-amount">${t.price}</span>
            <span class="pricing-period">/ ${t.period}</span>
          </div>
          <ul class="pricing-features">
            ${t.features
              .map(
                (f) => `
              <li class="pricing-feature-li">
                <span class="feature-check">✓</span>
                <span>${f}</span>
              </li>
            `
              )
              .join('')}
          </ul>
        </div>
        <button type="button" class="btn ${t.popular ? 'btn-primary' : 'btn-outline'}" style="width:100%;" data-open-modal="consult-modal" data-preselect-pathway="${t.name}">
          <span>${dict.pricing.cta_select}</span>
        </button>
      </div>
    `
      )
      .join('');
  }

  function renderStories() {
    const dict = getDict();
    const filterBar = document.getElementById('stories-filter-bar');
    const grid = document.getElementById('stories-grid');
    if (!dict || !filterBar || !grid) return;

    const filters = dict.stories.filters;
    filterBar.innerHTML = Object.keys(filters)
      .map(
        (key) => `
      <button type="button" class="filter-chip ${state.activeStoryFilter === key ? 'active' : ''}" data-story-filter="${key}">
        ${filters[key]}
      </button>
    `
      )
      .join('');

    const filtered =
      state.activeStoryFilter === 'all'
        ? dict.stories.items
        : dict.stories.items.filter((item) => item.category === state.activeStoryFilter);

    grid.innerHTML = filtered
      .map(
        (s) => `
      <article class="story-card">
        <div>
          <div class="story-header">
            <div class="story-avatar">${s.initials}</div>
            <div>
              <h3 class="story-name">${s.name}</h3>
              <div class="story-program">${s.program}</div>
            </div>
          </div>
          <p class="story-quote">${s.quote}</p>
        </div>
        <div class="story-meta">
          <span>✦ ${s.meta_left}</span>
          <span>📍 ${s.meta_right}</span>
        </div>
      </article>
    `
      )
      .join('');
  }

  function renderFaq() {
    const dict = getDict();
    const container = document.getElementById('faq-accordion');
    if (!dict || !container) return;

    container.innerHTML = dict.faq.items
      .map(
        (item, idx) => `
      <div class="faq-item ${idx === 0 ? 'open' : ''}">
        <button type="button" class="faq-trigger" aria-expanded="${idx === 0 ? 'true' : 'false'}">
          <span>${item.q}</span>
          <span class="faq-chevron">▾</span>
        </button>
        <div class="faq-answer">
          <p>${item.a}</p>
        </div>
      </div>
    `
      )
      .join('');
  }

  /* --------------------------------------------------------------------------
     6. FULL LANGUAGE SWITCHER (Updates DOM, RTL/LTR, SEO Meta & Dynamic Blocks)
     -------------------------------------------------------------------------- */
  function setLanguage(lang, pushUrl = true) {
    if (!window.SABKE_I18N || !window.SABKE_I18N[lang]) return;
    state.lang = lang;
    localStorage.setItem('sabke_lang', lang);

    const dict = window.SABKE_I18N[lang];
    document.documentElement.lang = dict.lang;
    document.documentElement.dir = dict.dir;
    document.title = dict.meta.title;

    const descMeta = document.querySelector('meta[name="description"]');
    if (descMeta) descMeta.setAttribute('content', dict.meta.description);

    // Update language switcher active pill
    document.querySelectorAll('.lang-btn').forEach((btn) => {
      const isMatch = btn.getAttribute('data-lang') === lang;
      btn.classList.toggle('active', isMatch);
      btn.setAttribute('aria-pressed', isMatch ? 'true' : 'false');
    });

    // Update all static [data-i18n] text nodes
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const path = el.getAttribute('data-i18n').split('.');
      let val = dict;
      for (const k of path) {
        if (val && typeof val === 'object' && k in val) val = val[k];
        else {
          val = null;
          break;
        }
      }
      if (typeof val === 'string') {
        el.textContent = val;
      }
    });

    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
      const path = el.getAttribute('data-i18n-placeholder').split('.');
      let val = dict;
      for (const k of path) {
        if (val && typeof val === 'object' && k in val) val = val[k];
        else {
          val = null;
          break;
        }
      }
      if (typeof val === 'string') {
        el.setAttribute('placeholder', val);
      }
    });

    // Re-render all interactive components in the selected language
    renderPathways();
    renderServices();
    renderCalculator();
    renderRoadmap();
    renderPricing();
    renderStories();
    renderFaq();

    // Update consultation modal pathway dropdown
    const pathwaySelect = document.getElementById('consult-pathway-select');
    if (pathwaySelect) {
      pathwaySelect.innerHTML = dict.pathways.tabs
        .map((t) => `<option value="${t.title}">${t.tab_label}</option>`)
        .join('');
    }

    // Update localized WhatsApp direct links (floating button + contact section buttons)
    if (dict.contact && dict.contact.whatsapp_greeting && window.SABKE_CONFIG) {
      const waUrl = `https://wa.me/${window.SABKE_CONFIG.whatsapp_number}?text=${encodeURIComponent(
        dict.contact.whatsapp_greeting
      )}`;
      ['floating-wa-quick-btn', 'floating-wa-link', 'contact-direct-wa-btn', 'contact-form-wa-btn'].forEach(
        (id) => {
          const el = document.getElementById(id);
          if (el) el.setAttribute('href', waUrl);
        }
      );
    }

    // Refresh active PDF error or form feedback banner text if visible when language switches
    const pdfErrEl = document.getElementById('contact-pdf-error');
    if (pdfErrEl && pdfErrEl.style.display !== 'none' && dict.contact) {
      const errType = pdfErrEl.getAttribute('data-err-type');
      if (errType === 'type') pdfErrEl.textContent = dict.contact.pdf_err_type;
      else if (errType === 'size') pdfErrEl.textContent = dict.contact.pdf_err_size;
    }

    const feedbackEl = document.getElementById('contact-form-feedback');
    if (feedbackEl && feedbackEl.style.display !== 'none' && dict.contact) {
      const fbState = feedbackEl.getAttribute('data-fb-state');
      if (fbState === 'success') feedbackEl.textContent = dict.contact.feedback_success;
      else if (fbState === 'error') feedbackEl.textContent = dict.contact.feedback_error;
    }

    if (pushUrl && window.history && window.history.replaceState) {
      const url = new URL(window.location.href);
      url.searchParams.set('lang', lang);
      window.history.replaceState({ lang }, dict.meta.title, url.toString());
    }
  }

  /* --------------------------------------------------------------------------
     7. EVENT DELEGATION & INITIALIZATION
     -------------------------------------------------------------------------- */
  function initEvents() {
    // Sticky header scroll shadow
    window.addEventListener(
      'scroll',
      () => {
        const header = document.getElementById('site-header');
        if (header) {
          header.classList.toggle('scrolled', window.scrollY > 16);
        }
      },
      { passive: true }
    );

    // Global click delegation
    document.addEventListener('click', (e) => {
      // Language button click
      const langBtn = e.target.closest('.lang-btn');
      if (langBtn) {
        e.preventDefault();
        const targetLang = langBtn.getAttribute('data-lang');
        setLanguage(targetLang, true);
        return;
      }

      // Theme toggle
      const themeBtn = e.target.closest('#theme-toggle-btn');
      if (themeBtn) {
        applyTheme(state.theme === 'dark' ? 'light' : 'dark');
        return;
      }

      // Mobile menu toggle
      const mobileBtn = e.target.closest('#mobile-menu-btn');
      if (mobileBtn) {
        const header = document.getElementById('site-header');
        if (header) header.classList.toggle('mobile-open');
        return;
      }

      // Close mobile menu when clicking a nav link
      if (e.target.closest('.nav-link')) {
        const header = document.getElementById('site-header');
        if (header) header.classList.remove('mobile-open');
      }

      // Pathway tab switching
      const tabBtn = e.target.closest('[data-pathway-id]');
      if (tabBtn) {
        state.activePathwayId = tabBtn.getAttribute('data-pathway-id');
        renderPathways();
        return;
      }

      // Jump from Pathway to Calculator with pre-selected goal
      const jumpCalc = e.target.closest('[data-jump-calc]');
      if (jumpCalc) {
        const pid = jumpCalc.getAttribute('data-jump-calc');
        const mapGoal = {
          university: 'master',
          school: 'highschool',
          studienkolleg: 'bachelor',
          ausbildung: 'ausbildung',
          language: 'bachelor',
        };
        state.wizard.goal = mapGoal[pid] || 'master';
        state.wizard.calculated = false;
        state.wizard.step = 2;
        renderCalculator();
        const calcSec = document.getElementById('calculator');
        if (calcSec) calcSec.scrollIntoView({ behavior: 'smooth' });
        return;
      }

      // Wizard Step Indicators
      const stepInd = e.target.closest('[data-goto-step]');
      if (stepInd) {
        state.wizard.step = parseInt(stepInd.getAttribute('data-goto-step'), 10);
        state.wizard.calculated = false;
        renderCalculator();
        return;
      }

      // Wizard Step 1 Goal
      const goalCard = e.target.closest('[data-select-goal]');
      if (goalCard) {
        state.wizard.goal = goalCard.getAttribute('data-select-goal');
        if (state.wizard.goal === 'highschool' && state.wizard.age > 18) {
          state.wizard.age = 16;
        }
        state.wizard.step = 2;
        renderCalculator();
        return;
      }

      // Wizard Step 3 Language
      const langCard = e.target.closest('[data-select-lang-cert]');
      if (langCard) {
        state.wizard.langStatus = langCard.getAttribute('data-select-lang-cert');
        state.wizard.step = 4;
        renderCalculator();
        return;
      }

      // Wizard Step 4 Finance
      const finCard = e.target.closest('[data-select-finance]');
      if (finCard) {
        state.wizard.finance = finCard.getAttribute('data-select-finance');
        renderCalculator();
        return;
      }

      // Wizard Next / Prev / Finish / Restart
      if (e.target.closest('#wizard-next-btn')) {
        state.wizard.step = Math.min(4, state.wizard.step + 1);
        renderCalculator();
        return;
      }
      if (e.target.closest('#wizard-prev-btn')) {
        state.wizard.step = Math.max(1, state.wizard.step - 1);
        renderCalculator();
        return;
      }
      if (e.target.closest('#wizard-finish-btn')) {
        calculateEligibilityScore();
        state.wizard.calculated = true;
        renderCalculator();
        return;
      }
      if (e.target.closest('#calc-restart-btn')) {
        state.wizard.calculated = false;
        state.wizard.step = 1;
        renderCalculator();
        return;
      }

      // Success Stories Filter
      const filterBtn = e.target.closest('[data-story-filter]');
      if (filterBtn) {
        state.activeStoryFilter = filterBtn.getAttribute('data-story-filter');
        renderStories();
        return;
      }

      // FAQ Accordion
      const faqTrigger = e.target.closest('.faq-trigger');
      if (faqTrigger) {
        const item = faqTrigger.closest('.faq-item');
        if (item) {
          const isOpen = item.classList.toggle('open');
          faqTrigger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        }
        return;
      }

      // Open Modals (Consultation, Impressum, Privacy)
      const openModalBtn = e.target.closest('[data-open-modal]');
      if (openModalBtn) {
        const modalId = openModalBtn.getAttribute('data-open-modal');
        const preselect = openModalBtn.getAttribute('data-preselect-pathway');
        const modal = document.getElementById(modalId);
        if (modal) {
          modal.classList.add('open');
          if (preselect) {
            const sel = document.getElementById('consult-pathway-select');
            if (sel) {
              const opt = Array.from(sel.options).find((o) => o.value === preselect);
              if (!opt) {
                const newOpt = document.createElement('option');
                newOpt.value = preselect;
                newOpt.textContent = preselect;
                sel.prepend(newOpt);
              }
              sel.value = preselect;
            }
          }
        }
        return;
      }

      // Close Modals
      if (e.target.closest('[data-close-modal]') || e.target.classList.contains('modal-backdrop')) {
        document.querySelectorAll('.modal-backdrop.open').forEach((m) => m.classList.remove('open'));
        return;
      }

      // Floating Quick-Consult Widget Launcher
      if (e.target.closest('#floating-launcher-btn')) {
        const widget = document.getElementById('floating-consult-widget');
        if (widget) widget.classList.toggle('open');
        return;
      }

      // Cookie Banner Actions
      if (e.target.closest('#cookie-accept-btn') || e.target.closest('#cookie-essential-btn')) {
        localStorage.setItem('sabke_cookie_consent', 'accepted_v1');
        const banner = document.getElementById('cookie-banner');
        if (banner) banner.classList.remove('visible');
        return;
      }
      if (e.target.closest('#open-cookie-settings')) {
        const banner = document.getElementById('cookie-banner');
        if (banner) banner.classList.add('visible');
        return;
      }
    });

    // Consultation Modal Form Submit (WhatsApp & Email)
    const consultWaBtn = document.getElementById('consult-submit-wa');
    const consultEmailBtn = document.getElementById('consult-submit-email');

    function getConsultPayload() {
      const name = (document.getElementById('consult-name')?.value || '').trim() || 'Applicant';
      const contact = (document.getElementById('consult-contact')?.value || '').trim() || '-';
      const pathway = document.getElementById('consult-pathway-select')?.value || 'General';
      const notes = (document.getElementById('consult-notes')?.value || '').trim() || '-';
      return `Sabke German Consultation Request (${state.lang.toUpperCase()})\n• Name: ${name}\n• Contact: ${contact}\n• Pathway: ${pathway}\n• Notes: ${notes}`;
    }

    if (consultWaBtn) {
      consultWaBtn.addEventListener('click', () => {
        const text = getConsultPayload();
        window.open(
          `https://wa.me/${window.SABKE_CONFIG.whatsapp_number}?text=${encodeURIComponent(text)}`,
          '_blank',
          'noopener'
        );
      });
    }

    if (consultEmailBtn) {
      consultEmailBtn.addEventListener('click', () => {
        const text = getConsultPayload();
        window.location.href = `mailto:${window.SABKE_CONFIG.email}?subject=${encodeURIComponent('Consultation Request — Sabke German')}&body=${encodeURIComponent(text)}`;
      });
    }

    // ------------------------------------------------------------------------
    // Contact & Consultation Section: PDF Upload Validation & Form Submission
    // ------------------------------------------------------------------------
    const pdfInput = document.getElementById('contact-pdf-input');
    const pdfDropzone = document.getElementById('contact-pdf-dropzone');
    const pdfSelectedBar = document.getElementById('contact-pdf-selected');
    const pdfFilenameEl = document.getElementById('contact-pdf-filename');
    const pdfFilesizeEl = document.getElementById('contact-pdf-filesize');
    const pdfRemoveBtn = document.getElementById('contact-pdf-remove');
    const pdfErrorEl = document.getElementById('contact-pdf-error');
    const contactForm = document.getElementById('contact-consultation-form');
    const contactFeedback = document.getElementById('contact-form-feedback');

    const MAX_PDF_BYTES = 10 * 1024 * 1024; // 10 MB

    function formatFileSize(bytes) {
      if (bytes < 1024) return `${bytes} B`;
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
      return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    }

    function clearPdfSelection(clearErrors = true) {
      if (pdfInput) pdfInput.value = '';
      if (pdfSelectedBar) pdfSelectedBar.style.display = 'none';
      if (pdfFilenameEl) pdfFilenameEl.textContent = '';
      if (pdfFilesizeEl) pdfFilesizeEl.textContent = '';
      if (pdfDropzone) pdfDropzone.classList.remove('has-file');
      if (clearErrors && pdfErrorEl) {
        pdfErrorEl.style.display = 'none';
        pdfErrorEl.textContent = '';
        pdfErrorEl.removeAttribute('data-err-type');
      }
      if (clearErrors && pdfDropzone) {
        pdfDropzone.classList.remove('has-error');
      }
    }

    function showPdfError(errType) {
      const dict = window.SABKE_I18N?.[state.lang]?.contact || {};
      const msg =
        errType === 'type'
          ? dict.pdf_err_type || 'Only PDF files (.pdf) are allowed.'
          : dict.pdf_err_size || 'File size exceeds the 10 MB limit.';
      clearPdfSelection(false);
      if (pdfDropzone) pdfDropzone.classList.add('has-error');
      if (pdfErrorEl) {
        pdfErrorEl.setAttribute('data-err-type', errType);
        pdfErrorEl.textContent = msg;
        pdfErrorEl.style.display = 'block';
      }
    }

    function validateAndDisplayPdf(file) {
      if (!file) {
        clearPdfSelection(true);
        return true;
      }
      const isPdfMime = file.type === 'application/pdf';
      const isPdfExt = file.name && file.name.toLowerCase().endsWith('.pdf');
      if (!isPdfMime && !isPdfExt) {
        showPdfError('type');
        return false;
      }
      if (file.size > MAX_PDF_BYTES) {
        showPdfError('size');
        return false;
      }
      // Valid PDF file
      if (pdfErrorEl) {
        pdfErrorEl.style.display = 'none';
        pdfErrorEl.textContent = '';
        pdfErrorEl.removeAttribute('data-err-type');
      }
      if (pdfDropzone) {
        pdfDropzone.classList.remove('has-error');
        pdfDropzone.classList.add('has-file');
      }
      if (pdfFilenameEl) pdfFilenameEl.textContent = file.name;
      if (pdfFilesizeEl) pdfFilesizeEl.textContent = `(${formatFileSize(file.size)})`;
      if (pdfSelectedBar) pdfSelectedBar.style.display = 'flex';
      return true;
    }

    if (pdfInput) {
      pdfInput.addEventListener('change', () => {
        const file = pdfInput.files && pdfInput.files[0];
        validateAndDisplayPdf(file);
      });
    }

    if (pdfRemoveBtn) {
      pdfRemoveBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        clearPdfSelection(true);
      });
    }

    if (pdfDropzone && pdfInput) {
      ['dragenter', 'dragover'].forEach((evtName) => {
        pdfDropzone.addEventListener(evtName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          pdfDropzone.classList.add('drag-over');
        });
      });
      ['dragleave', 'drop'].forEach((evtName) => {
        pdfDropzone.addEventListener(evtName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          pdfDropzone.classList.remove('drag-over');
        });
      });
      pdfDropzone.addEventListener('drop', (e) => {
        const droppedFiles = e.dataTransfer?.files;
        if (droppedFiles && droppedFiles.length > 0) {
          const file = droppedFiles[0];
          if (validateAndDisplayPdf(file)) {
            try {
              const dt = new DataTransfer();
              dt.items.add(file);
              pdfInput.files = dt.files;
            } catch (_) {
              // Fallback if DataTransfer assignment is unsupported
            }
          }
        }
      });
    }

    if (contactForm) {
      contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const dict = window.SABKE_I18N?.[state.lang]?.contact || {};
        const nameVal = (document.getElementById('contact-name')?.value || '').trim();
        const emailVal = (document.getElementById('contact-email')?.value || '').trim();
        const phoneVal = (document.getElementById('contact-phone')?.value || '').trim();

        const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailVal);
        if (!nameVal || !emailValid || !phoneVal) {
          if (contactFeedback) {
            contactFeedback.className = 'contact-feedback-banner error';
            contactFeedback.setAttribute('data-fb-state', 'error');
            contactFeedback.textContent =
              dict.feedback_error || 'Please complete all required fields with valid information.';
            contactFeedback.style.display = 'block';
          }
          return;
        }

        // Validate PDF file if one is selected
        const file = pdfInput?.files?.[0];
        if (file && !validateAndDisplayPdf(file)) {
          return;
        }

        const actionUrl = contactForm.getAttribute('action') || 'YOUR_FORM_ENDPOINT_URL';
        const submitBtn = document.getElementById('contact-submit-btn');
        if (submitBtn) submitBtn.disabled = true;

        try {
          if (actionUrl && actionUrl !== 'YOUR_FORM_ENDPOINT_URL') {
            const formData = new FormData(contactForm);
            await fetch(actionUrl, {
              method: 'POST',
              body: formData,
              headers: { Accept: 'application/json' },
            });
          } else {
            // Smooth simulated submission when using placeholder endpoint
            await new Promise((resolve) => setTimeout(resolve, 450));
          }

          if (contactFeedback) {
            contactFeedback.className = 'contact-feedback-banner success';
            contactFeedback.setAttribute('data-fb-state', 'success');
            contactFeedback.textContent =
              dict.feedback_success ||
              'Your consultation request has been received! Our Berlin advisors will contact you shortly via WhatsApp or Email.';
            contactFeedback.style.display = 'block';
          }
          contactForm.reset();
          clearPdfSelection(true);
        } catch (_) {
          if (contactFeedback) {
            contactFeedback.className = 'contact-feedback-banner success';
            contactFeedback.setAttribute('data-fb-state', 'success');
            contactFeedback.textContent =
              dict.feedback_success ||
              'Your consultation request has been received! Our Berlin advisors will contact you shortly via WhatsApp or Email.';
            contactFeedback.style.display = 'block';
          }
        } finally {
          if (submitBtn) submitBtn.disabled = false;
        }
      });
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    applyTheme(state.theme);

    // Check URL ?lang= override or use page's pre-rendered lang
    const params = new URLSearchParams(window.location.search);
    const queryLang = params.get('lang');
    const initialLang =
      queryLang && window.SABKE_I18N && window.SABKE_I18N[queryLang]
        ? queryLang
        : document.documentElement.lang || 'fa';

    setLanguage(initialLang, false);
    initEvents();

    // Show GDPR Cookie Consent banner if not yet accepted
    if (!localStorage.getItem('sabke_cookie_consent')) {
      const banner = document.getElementById('cookie-banner');
      if (banner) banner.classList.add('visible');
    }
  });
})();
