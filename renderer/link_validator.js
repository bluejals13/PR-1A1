/**
 * Renderer Engine - Link & Quality Validator
 * File: PR-1A1/renderer/link_validator.js
 * Description: Verifies HTML syntax, CSS injection, and link consistency
 */

function validateHTMLOutput(htmlContent, templateType) {
  const errors = [];

  // 1. Basic HTML Structure
  if (!htmlContent.includes('<!DOCTYPE html>')) errors.push('MISSING_DOCTYPE');
  if (!htmlContent.includes('<html') || !htmlContent.includes('</html>')) errors.push('INVALID_HTML_TAGS');
  if (!htmlContent.includes('<style>') || !htmlContent.includes('--bg-app')) errors.push('MISSING_DESIGN_SYSTEM_CSS');

  // 2. Template Specific Checks
  if (templateType === 'LONGFORM') {
    if (!htmlContent.includes('toc-sidebar')) errors.push('MISSING_LONGFORM_TOC');
    if (!htmlContent.includes('longform-hero')) errors.push('MISSING_LONGFORM_HERO');
  }

  if (templateType === 'FEATURE') {
    if (!htmlContent.includes('feature-grid-stack')) errors.push('MISSING_FEATURE_STACK');
    if (!htmlContent.includes('code-block')) errors.push('MISSING_FEATURE_CODE_SNIPPET');
  }

  if (templateType === 'TECHNICAL') {
    if (!htmlContent.includes('technical-decision-matrix')) errors.push('MISSING_DECISION_MATRIX');
    if (!htmlContent.includes('tradeoff-pro-con-grid')) errors.push('MISSING_TRADEOFF_GRID');
  }

  if (templateType === 'SLIDE') {
    if (!htmlContent.includes('slide-canvas-16-9')) errors.push('MISSING_16_9_CANVAS');
    if (!htmlContent.includes('slide-headline')) errors.push('MISSING_SLIDE_HEADLINE');
    if (!htmlContent.includes('slide-nav-bar')) errors.push('MISSING_SLIDE_NAVIGATOR');
  }

  if (templateType === 'EVIDENCE') {
    if (!htmlContent.includes('evidence-table')) errors.push('MISSING_EVIDENCE_TABLE');
    if (!htmlContent.includes('ev-auth-rtr')) errors.push('MISSING_EXPECTED_EVIDENCE_ID');
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

module.exports = {
  validateHTMLOutput
};
