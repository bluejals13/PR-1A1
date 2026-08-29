/**
 * Renderer Engine - Slide & Evidence Renderers
 * File: PR-1A1/renderer/renderers/slide.js
 */

function renderSlideHTML(vm, inlineCSS) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${vm.title} (16:9 Slide Deck)</title>
  <style>
${inlineCSS}
    .slide-page { display: none; }
    .slide-page.active { display: flex; }
  </style>
</head>
<body style="margin: 0; background-color: #05070a; overflow: hidden;">

  <div class="slide-deck-viewport">
    ${vm.slides.map((sl, idx) => `
    <div id="slide-${idx + 1}" class="slide-canvas-16-9 slide-page ${idx === 0 ? 'active' : ''}">
      <!-- Slide Header -->
      <header class="slide-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span class="badge badge-ev-verified">SLIDE 0${idx + 1} / 0${vm.total_slides}</span>
          <span style="font-family: var(--font-mono); font-size: 12px; color: var(--text-dim);">APMS.SR ARCHITECTURE</span>
        </div>
        <h2 class="slide-headline">${sl.headline}</h2>
        <div class="slide-takeaway-badge">
          Takeaway: ${sl.takeaway}
        </div>
      </header>

      <!-- Slide Content Stage -->
      <main class="slide-content-stage">
        <div class="slide-layout-split">
          <div>${sl.left_html}</div>
          <div>${sl.right_html}</div>
        </div>
      </main>

      <!-- Slide Footer -->
      <footer class="slide-footer">
        <span>Evidence: ${sl.evidences.join(', ')}</span>
        <span>Source: ${sl.source}</span>
      </footer>
    </div>`).join('\n')}
  </div>

  <!-- Floating Navigation Controls -->
  <nav class="slide-nav-bar">
    <button class="slide-nav-btn" onclick="prevSlide()">◀ PREV</button>
    <span id="slide-num-indicator" class="slide-counter">SLIDE 1 / ${vm.total_slides}</span>
    <button class="slide-nav-btn" onclick="nextSlide()">NEXT ▶</button>
  </nav>

  <script>
    let currentSlide = 1;
    const totalSlides = ${vm.total_slides};

    function updateSlide() {
      document.querySelectorAll('.slide-page').forEach((el, idx) => {
        if (idx + 1 === currentSlide) el.classList.add('active');
        else el.classList.remove('active');
      });
      document.getElementById('slide-num-indicator').innerText = 'SLIDE ' + currentSlide + ' / ' + totalSlides;
    }

    function nextSlide() {
      if (currentSlide < totalSlides) {
        currentSlide++;
        updateSlide();
      }
    }

    function prevSlide() {
      if (currentSlide > 1) {
        currentSlide--;
        updateSlide();
      }
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
    });
  </script>

</body>
</html>`;
}

function renderEvidenceHTML(vm, inlineCSS) {
  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${vm.title} - Audit Ledger</title>
  <style>
${inlineCSS}
  </style>
</head>
<body style="background-color: var(--bg-app); color: var(--text-primary);">

  <div class="layout-evidence">
    <!-- Header -->
    <header style="border-bottom: 1px solid var(--border-subtle); padding-bottom: var(--space-6);">
      <div style="display: flex; gap: var(--space-2); align-items: center;">
        <span class="badge badge-ev-verified">100% VERIFIED LEDGER</span>
        <span class="badge badge-doc-fresh">AUDIT PASS</span>
      </div>
      <h1 style="font-size: var(--text-3xl); margin: var(--space-2) 0;">${vm.title}</h1>
      <p style="color: var(--text-muted); font-size: var(--text-base);">${vm.subtitle}</p>
    </header>

    <!-- Summary Metrics -->
    <div class="evidence-audit-summary-strip">
      <div class="metric-card">
        <span class="metric-label">Total Claims</span>
        <div class="metric-value-container">
          <span class="metric-value">${vm.total_claims}</span>
          <span class="metric-unit">Items</span>
        </div>
      </div>
      <div class="metric-card">
        <span class="metric-label">Verified Claims</span>
        <div class="metric-value-container">
          <span class="metric-value" style="color: var(--status-success);">${vm.verified_claims}</span>
          <span class="metric-unit">Items</span>
        </div>
      </div>
      <div class="metric-card">
        <span class="metric-label">Audit Pass Rate</span>
        <div class="metric-value-container">
          <span class="metric-value" style="color: var(--status-success);">${vm.pass_rate}</span>
        </div>
      </div>
    </div>

    <!-- Verification Table -->
    <main class="evidence-table-container">
      <table class="evidence-table">
        <thead>
          <tr>
            <th>Status</th>
            <th>Engineering Claim Statement</th>
            <th>Evidence ID</th>
            <th>Verification Test & Method</th>
            <th>Source Repository & File Path</th>
          </tr>
        </thead>
        <tbody>
          ${vm.items.map(it => `
          <tr>
            <td><span class="badge badge-ev-${it.status.toLowerCase().includes('verified') ? 'verified' : 'documented'}">${it.status}</span></td>
            <td><strong>${it.claim}</strong></td>
            <td><code>${it.evidence_id}</code></td>
            <td style="font-size: 13px;">${it.method}</td>
            <td><a class="source-ref" href="file:///${it.source_path}"><span class="source-repo-tag">${it.source_repo}:</span> ${it.source_path.split('/').pop()}</a></td>
          </tr>`).join('\n')}
        </tbody>
      </table>
    </main>
  </div>

</body>
</html>`;
}

module.exports = {
  renderSlideHTML,
  renderEvidenceHTML
};
