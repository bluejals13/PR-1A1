/**
 * ===== PR-1A1 Presentation Export Helper =====
 * Utilities for PDF export and print formatting
 */

(function () {
  'use strict';

  function preparePrint() {
    // Reveal speaker notes or format layout for clean PDF printing if needed
    window.print();
  }

  window.PresentationExport = {
    print: preparePrint
  };
})();
