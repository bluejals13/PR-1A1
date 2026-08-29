/**
 * Renderer Engine - Feature & Technical Renderers
 * Files: PR-1A1/renderer/renderers/feature.js
 */

function renderFeatureHTML(vm, inlineCSS) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${vm.title} - Feature Spec</title>
  <style>
${inlineCSS}
  </style>
</head>
<body style="background-color: var(--bg-app); color: var(--text-primary);">

  <div class="layout-feature">
    <!-- Header -->
    <header class="feature-header">
      <div style="display: flex; gap: var(--space-2); align-items: center;">
        <span class="badge badge-ev-verified">VERIFIED FEATURE</span>
        <span class="source-ref"><span class="source-repo-tag">${vm.domain}</span></span>
      </div>
      <h1 style="font-size: var(--text-3xl); margin: var(--space-2) 0;">${vm.title}</h1>
      <p style="color: var(--text-muted); font-size: var(--text-base);">${vm.subtitle}</p>
    </header>

    <!-- One-Page Card Stack -->
    <main class="feature-grid-stack">
      ${vm.steps.map(st => `
      <div class="feature-step-row">
        <div class="feature-step-label">${st.step_num}. ${st.label}</div>
        <div style="width: 100%;">
          ${st.box_type ? `
          <div class="callout ${st.box_type}" style="margin: 0;">
            <span class="callout-title">${st.title}</span>
            <span>${st.desc}</span>
          </div>` : ''}
          ${st.is_code ? `
          <div class="code-block" style="margin: 0;">
            <div class="code-header">
              <span class="code-filename">${st.filename}</span>
              <span class="source-ref">${st.source_ref}</span>
            </div>
            <pre class="code-body"><code>${st.code}</code></pre>
          </div>` : ''}
          ${st.is_evidence ? `
          <div class="evidence-card" style="margin: 0;">
            <div class="evidence-claim-text">${st.claim_title}</div>
            <div class="evidence-meta-grid">
              <div class="evidence-meta-item">
                <span class="evidence-meta-label">Evidence ID</span>
                <span class="evidence-meta-value">${st.evidence_id}</span>
              </div>
              <div class="evidence-meta-item">
                <span class="evidence-meta-label">Test Source File</span>
                <span class="evidence-meta-value">${st.test_file}</span>
              </div>
              <div class="evidence-meta-item">
                <span class="evidence-meta-label">Audit Status</span>
                <span class="badge badge-ev-verified">${st.status}</span>
              </div>
            </div>
          </div>` : ''}
        </div>
      </div>`).join('\n')}
    </main>
  </div>

</body>
</html>`;
}

function renderTechnicalHTML(vm, inlineCSS) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${vm.title} - Technical Decision Deep-Dive</title>
  <style>
${inlineCSS}
  </style>
</head>
<body style="background-color: var(--bg-app); color: var(--text-primary);">

  <div class="layout-technical">
    <!-- Header -->
    <header style="border-bottom: 1px solid var(--border-subtle); padding-bottom: var(--space-6);">
      <span class="badge badge-ev-documented">DECISION & TRADE-OFF DEEP-DIVE</span>
      <h1 style="font-size: var(--text-3xl); margin-top: var(--space-2);">${vm.title}</h1>
      <p style="color: var(--text-muted); font-size: var(--text-base);">${vm.subtitle}</p>
    </header>

    <!-- Decisions Matrix -->
    <section>
      <h2 style="font-size: var(--text-xl); color: var(--color-primary); margin-bottom: var(--space-4);">1. Architecture Decisions & Rejected Alternatives</h2>
      <div class="technical-decision-matrix">
        ${vm.decisions.map(d => `
        <div class="card card-highlight">
          <h3 class="card-title" style="color: var(--color-primary);">${d.name}</h3>
          <p class="card-body" style="font-size: 14px; margin: var(--space-3) 0;"><strong>Rationale (Why):</strong> ${d.rationale}</p>
          <div style="border-top: 1px solid var(--border-subtle); padding-top: var(--space-3);">
            <div style="font-size: 12px; font-weight: bold; color: var(--text-dim); text-transform: uppercase; margin-bottom: 4px;">Rejected Alternatives:</div>
            ${d.rejected.map(r => `
            <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px;">
              • <span style="text-decoration: line-through; color: var(--status-error);">${r.option}:</span> ${r.reason}
            </div>`).join('')}
          </div>
        </div>`).join('\n')}
      </div>
    </section>

    <!-- Trade-offs Ledger -->
    <section>
      <h2 style="font-size: var(--text-xl); color: var(--color-primary); margin-bottom: var(--space-4);">2. Trade-offs Breakdown & Mitigation</h2>
      <div style="display: flex; flex-direction: column; gap: var(--space-4);">
        ${vm.tradeoffs.map(t => `
        <div class="card">
          <div style="font-weight: bold; font-size: var(--text-base); color: var(--text-primary); margin-bottom: var(--space-3);">${t.aspect}</div>
          <div class="tradeoff-pro-con-grid">
            <div class="pro-box">
              <span style="font-weight: bold; font-size: 12px; color: var(--status-success); display: block; margin-bottom: 4px;">[+] BENEFIT (이점)</span>
              <span style="font-size: 13px; color: var(--text-secondary);">${t.pro}</span>
            </div>
            <div class="con-box">
              <span style="font-weight: bold; font-size: 12px; color: var(--status-error); display: block; margin-bottom: 4px;">[-] COST & MITIGATION (비용 및 완화)</span>
              <span style="font-size: 13px; color: var(--text-secondary);">${t.con}<br><strong>Mitigation:</strong> ${t.mitigation}</span>
            </div>
          </div>
        </div>`).join('\n')}
      </div>
    </section>

    <!-- Benchmarks -->
    <section>
      <h2 style="font-size: var(--text-xl); color: var(--color-primary); margin-bottom: var(--space-4);">3. Measured Benchmarks vs Thresholds</h2>
      <div class="evidence-table-container">
        <table class="evidence-table">
          <thead>
            <tr>
              <th>Benchmark Metric</th>
              <th>Threshold Target</th>
              <th>Actual Measured Value</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${vm.benchmarks.map(b => `
            <tr>
              <td><strong>${b.metric}</strong></td>
              <td><code>${b.target}</code></td>
              <td style="color: var(--color-primary); font-family: var(--font-mono); font-weight: bold;">${b.actual}</td>
              <td><span class="badge badge-ev-verified">${b.status}</span></td>
            </tr>`).join('\n')}
          </tbody>
        </table>
      </div>
    </section>
  </div>

</body>
</html>`;
}

module.exports = {
  renderFeatureHTML,
  renderTechnicalHTML
};
