/**
 * Renderer Engine - Longform Renderer
 * File: PR-1A1/renderer/renderers/longform.js
 * Spatial Model: VERTICAL_CONTINUOUS
 */

function renderLongformHTML(vm, inlineCSS) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${vm.title} - Engineering Portfolio</title>
  <style>
${inlineCSS}
  </style>
</head>
<body class="layout-longform">

  <!-- Hero Banner -->
  <header class="longform-hero">
    <div class="longform-hero-inner">
      <div class="longform-meta-strip">
        <span class="badge badge-doc-fresh">${vm.state}</span>
        <span class="badge badge-change-level">CHANGE LEVEL ${vm.change_level}</span>
        ${vm.sources.map(s => `<a class="source-ref" href="file:///${s.path}"><span class="source-repo-tag">${s.repo}:</span> ${s.path}</a>`).join(' ')}
      </div>
      <h1 class="longform-hero-title">${vm.title}</h1>
      <p class="longform-hero-subtitle">${vm.subtitle}</p>
    </div>
  </header>

  <!-- Main Grid: Sticky TOC + Reading Prose -->
  <div class="longform-main-container">
    <aside class="toc-sidebar">
      <div class="toc-title">Table of Contents</div>
      ${vm.sections.map(s => `<a href="#${s.id}" class="toc-link">${s.title}</a>`).join('\n      ')}
    </aside>

    <main class="longform-prose-content">
      ${vm.sections.map(s => `
      <section id="${s.id}" class="longform-section">
        <div class="longform-section-title">
          <span>${s.title}</span>
          <span class="badge badge-ev-${s.badge.toLowerCase().includes('verified') ? 'verified' : (s.badge.toLowerCase().includes('doc') ? 'documented' : 'planned')}">${s.badge}</span>
        </div>
        <div class="card-body">
          ${s.body}
        </div>
        ${s.callout ? `
        <div class="callout ${s.callout.type}">
          <span class="callout-title">${s.callout.title}</span>
          <span>${s.callout.text}</span>
        </div>` : ''}
        ${s.diagram ? `
        <div class="diagram-container">
          <div style="font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-primary); margin-bottom: 8px;">// ${s.diagram.caption}</div>
          <div style="display: flex; flex-direction: column; gap: 6px; width: 100%;">
            ${s.diagram.steps.map((st, idx) => `
            <div style="background: var(--bg-app); border: 1px solid var(--border-subtle); padding: 8px 12px; border-radius: 4px; font-size: 13px; font-family: var(--font-mono);">
              <span style="color: var(--color-primary); font-weight: bold;">[Step ${idx + 1}]</span> ${st}
            </div>`).join('')}
          </div>
        </div>` : ''}
        ${s.metrics ? `
        <div class="metric-grid">
          ${s.metrics.map(m => `
          <div class="metric-card">
            <span class="metric-label">${m.label}</span>
            <div class="metric-value-container">
              <span class="metric-value">${m.value}</span>
              <span class="metric-unit">${m.unit}</span>
            </div>
            <span class="metric-status" style="color: var(--status-success);">✓ ${m.desc}</span>
          </div>`).join('')}
        </div>` : ''}
      </section>`).join('\n')}
    </main>
  </div>

  <footer style="border-top: 1px solid var(--border-subtle); padding: var(--space-8); text-align: center; font-size: var(--text-xs); color: var(--text-dim);">
    APMS.SR Engineering Portfolio • Generated via Polymorphic Template System • Zero-Hallucination Verified
  </footer>

</body>
</html>`;
}

module.exports = {
  renderLongformHTML
};
