/**
 * Renderer Engine - Loader Module
 * File: PR-1A1/renderer/loader.js
 * Description: Loads Registry, Content, Template Contracts, and Design System assets
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const MY2_ROOT = path.resolve(ROOT_DIR, '..');

// Simple robust YAML parser for key-value, lists, multiline strings and nested maps
function parseSimpleYaml(content) {
  const lines = content.split(/\r?\n/);
  const root = {};
  let currentKey = null;
  let inMultiline = false;
  let multilineContent = [];
  let multilineIndent = 0;

  // We can use a lightweight line-by-line parsing or standard structure representation
  // For precise structure, let's load JSON where available, or line parse YAML
  const doc = {};
  let stack = [{ obj: doc, indent: -1 }];

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i];
    if (/^\s*#/.test(rawLine) || rawLine.trim() === '') continue;

    const indent = rawLine.search(/\S/);
    const line = rawLine.trim();

    if (inMultiline) {
      if (indent >= multilineIndent) {
        multilineContent.push(rawLine.slice(multilineIndent));
        continue;
      } else {
        inMultiline = false;
        if (currentKey && stack.length > 0) {
          stack[stack.length - 1].obj[currentKey] = multilineContent.join('\n');
        }
        multilineContent = [];
      }
    }

    if (line.includes(': |') || line.endsWith(': |')) {
      const parts = line.split(':');
      currentKey = parts[0].trim();
      inMultiline = true;
      multilineIndent = indent + 2;
      multilineContent = [];
      continue;
    }

    // Normal key-value / array handling
    if (line.startsWith('- ')) {
      // List item
      const itemContent = line.substring(2).trim();
      while (stack.length > 1 && stack[stack.length - 1].indent >= indent) {
        stack.pop();
      }
      const parent = stack[stack.length - 1].obj;
      const parentKey = Object.keys(parent).pop();
      if (!Array.isArray(parent[parentKey])) {
        parent[parentKey] = [];
      }
      if (itemContent.includes(':')) {
        const obj = {};
        const [k, ...v] = itemContent.split(':');
        obj[k.trim()] = v.join(':').trim().replace(/^["']|["']$/g, '');
        parent[parentKey].push(obj);
        stack.push({ obj, indent });
      } else {
        parent[parentKey].push(itemContent.replace(/^["']|["']$/g, ''));
      }
      continue;
    }

    if (line.includes(':')) {
      const colonIndex = line.indexOf(':');
      const key = line.slice(0, colonIndex).trim();
      let value = line.slice(colonIndex + 1).trim();

      while (stack.length > 1 && stack[stack.length - 1].indent >= indent) {
        stack.pop();
      }
      const currentParent = stack[stack.length - 1].obj;

      if (value === '') {
        currentParent[key] = {};
        stack.push({ obj: currentParent[key], indent });
      } else if (value.startsWith('[') && value.endsWith(']')) {
        currentParent[key] = value.slice(1, -1).split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
      } else {
        // Strip quotes
        value = value.replace(/^["']|["']$/g, '');
        if (value === 'true') value = true;
        else if (value === 'false') value = false;
        else if (!isNaN(Number(value)) && value !== '') value = Number(value);
        currentParent[key] = value;
      }
    }
  }

  if (inMultiline && currentKey && stack.length > 0) {
    stack[stack.length - 1].obj[currentKey] = multilineContent.join('\n');
  }

  return doc;
}

function loadRegistry() {
  const documentsYaml = fs.readFileSync(path.join(ROOT_DIR, 'registry', 'documents.yaml'), 'utf8');
  const evidenceYaml = fs.readFileSync(path.join(ROOT_DIR, 'registry', 'evidence.yaml'), 'utf8');
  const relationsYaml = fs.readFileSync(path.join(ROOT_DIR, 'registry', 'relations.yaml'), 'utf8');

  return {
    documents: parseSimpleYaml(documentsYaml),
    evidence: parseSimpleYaml(evidenceYaml),
    relations: parseSimpleYaml(relationsYaml)
  };
}

function loadContent(domain, documentId) {
  const contentPath = path.join(ROOT_DIR, 'content', 'domains', domain, `${documentId}.yaml`);
  if (!fs.existsSync(contentPath)) {
    throw new Error(`MISSING_CONTENT_FILE: ${contentPath}`);
  }
  const contentStr = fs.readFileSync(contentPath, 'utf8');
  return {
    filePath: contentPath,
    data: parseSimpleYaml(contentStr)
  };
}

function loadTemplateContracts() {
  const contractsDir = path.join(ROOT_DIR, 'templates', 'contracts');
  const files = fs.readdirSync(contractsDir).filter(f => f.endsWith('.yaml'));
  const contracts = {};
  for (const f of files) {
    const raw = fs.readFileSync(path.join(contractsDir, f), 'utf8');
    const id = f.replace('.contract.yaml', '').toUpperCase();
    contracts[id] = parseSimpleYaml(raw);
  }
  return contracts;
}

function loadDesignSystemCSS() {
  const dsDir = path.join(ROOT_DIR, 'design-system');
  const files = [
    'tokens/colors.css',
    'tokens/typography.css',
    'tokens/spacing.css',
    'components/badge.css',
    'components/card.css',
    'components/evidence.css',
    'components/code.css',
    'components/navigation.css',
    'layouts/longform.css',
    'layouts/feature.css',
    'layouts/slide.css'
  ];

  let combinedCSS = '';
  for (const file of files) {
    const fullPath = path.join(dsDir, file);
    if (fs.existsSync(fullPath)) {
      combinedCSS += `\n/* --- ${file} --- */\n` + fs.readFileSync(fullPath, 'utf8');
    }
  }
  return combinedCSS;
}

module.exports = {
  ROOT_DIR,
  MY2_ROOT,
  parseSimpleYaml,
  loadRegistry,
  loadContent,
  loadTemplateContracts,
  loadDesignSystemCSS
};
