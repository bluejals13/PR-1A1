/**
 * ===== PR-1A1 Presentation Runtime =====
 * Modular, dependency-free presentation runtime supporting:
 * - Standalone slide execution
 * - Presentation assembly and navigation
 * - Keyboard shortcuts (Arrows, Space, N, F, Home, End)
 * - Speaker notes panel sync
 * - Viewport progress tracking
 */

(function () {
  'use strict';

  // Default fallback slide manifest
  const DEFAULT_SLIDES = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012', '013', '014', '015'];
  let slidesList = [...DEFAULT_SLIDES];

  // DOM Elements
  const body = document.body;
  const progressEl = document.getElementById('presentation-progress');
  const counterEl = document.getElementById('presentation-counter');
  const speakerPanelEl = document.getElementById('speaker-panel');
  const speakerTextEl = document.getElementById('speaker-text');
  const speakerToggleEl = document.getElementById('speaker-toggle');
  const speakerCloseEl = document.getElementById('speaker-close');
  const prevBtnEl = document.getElementById('prev-btn');
  const nextBtnEl = document.getElementById('next-btn');

  // Identify Current Slide
  function getCurrentSlideInfo() {
    // Priority 1: dataset.slide (e.g. "001")
    let slideId = body.dataset.slide;
    
    // Priority 2: derive from pathname if not in dataset
    if (!slideId) {
      const match = window.location.pathname.match(/slides\/(\d{3})/i);
      if (match) {
        slideId = match[1];
      }
    }

    if (!slideId) {
      slideId = '001';
    }

    // Ensure 3-digit format
    slideId = String(slideId).padStart(3, '0');

    let slideIndex = slidesList.indexOf(slideId);
    if (slideIndex === -1) {
      const numericIndex = Number(body.dataset.slideIndex || body.dataset.slide || 1);
      slideIndex = numericIndex - 1;
      if (slideIndex >= 0 && slideIndex < slidesList.length) {
        slideId = slidesList[slideIndex];
      } else {
        slideIndex = 0;
        slideId = slidesList[0];
      }
    }

    return {
      slideId,
      slideIndex: slideIndex + 1, // 1-indexed
      totalSlides: slidesList.length
    };
  }

  /**
   * Navigate to a slide by 1-based index
   */
  function goToSlideIndex(targetIndex) {
    if (targetIndex < 1 || targetIndex > slidesList.length) {
      return;
    }
    const targetSlideId = slidesList[targetIndex - 1];
    
    // Check if we are inside a slide subfolder (e.g. /slides/001/index.html)
    const isInSlideDir = window.location.pathname.includes('/slides/');
    const targetPath = isInSlideDir ? `../${targetSlideId}/index.html` : `slides/${targetSlideId}/index.html`;

    window.location.href = targetPath;
  }

  /**
   * Update UI controls (counter, progress, buttons, speaker notes)
   */
  function updateUI() {
    const { slideId, slideIndex, totalSlides } = getCurrentSlideInfo();

    if (counterEl) {
      counterEl.textContent = `${String(slideIndex).padStart(2, '0')} / ${String(totalSlides).padStart(2, '0')}`;
    }

    if (progressEl) {
      progressEl.style.width = `${(slideIndex / totalSlides) * 100}%`;
    }

    if (prevBtnEl) {
      prevBtnEl.disabled = (slideIndex <= 1);
    }
    if (nextBtnEl) {
      nextBtnEl.disabled = (slideIndex >= totalSlides);
    }

    // Speaker notes sync
    const activeSlide = document.querySelector('.slide.active') || document.querySelector('.slide');
    const note = activeSlide?.dataset.speakerNote || '발표자 노트가 없습니다.';
    if (speakerTextEl) {
      speakerTextEl.textContent = note;
    }
  }

  /**
   * Toggle Speaker Panel
   */
  function toggleSpeakerNotes() {
    if (speakerPanelEl) {
      speakerPanelEl.classList.toggle('visible');
    }
  }

  /**
   * Toggle Fullscreen
   */
  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
      }
    }
  }

  /**
   * Event Listeners Setup
   */
  function setupEvents() {
    if (prevBtnEl) {
      prevBtnEl.addEventListener('click', () => {
        const { slideIndex } = getCurrentSlideInfo();
        goToSlideIndex(slideIndex - 1);
      });
    }

    if (nextBtnEl) {
      nextBtnEl.addEventListener('click', () => {
        const { slideIndex } = getCurrentSlideInfo();
        goToSlideIndex(slideIndex + 1);
      });
    }

    if (speakerToggleEl) {
      speakerToggleEl.addEventListener('click', toggleSpeakerNotes);
    }

    if (speakerCloseEl) {
      speakerCloseEl.addEventListener('click', () => {
        speakerPanelEl?.classList.remove('visible');
      });
    }

    // Keyboard Shortcuts
    document.addEventListener('keydown', (event) => {
      // Avoid capturing when typing inside inputs/textareas
      const tag = event.target.tagName?.toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') {
        return;
      }

      const { slideIndex, totalSlides } = getCurrentSlideInfo();

      if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
        event.preventDefault();
        goToSlideIndex(slideIndex - 1);
      } else if (event.key === 'ArrowRight' || event.key === ' ' || event.key === 'PageDown') {
        event.preventDefault();
        goToSlideIndex(slideIndex + 1);
      } else if (event.key === 'Home') {
        event.preventDefault();
        goToSlideIndex(1);
      } else if (event.key === 'End') {
        event.preventDefault();
        goToSlideIndex(totalSlides);
      } else if (event.key.toLowerCase() === 'n') {
        event.preventDefault();
        toggleSpeakerNotes();
      } else if (event.key.toLowerCase() === 'f') {
        event.preventDefault();
        toggleFullscreen();
      } else if (event.key === 'Escape') {
        speakerPanelEl?.classList.remove('visible');
      }
    });
  }

  /**
   * Attempt to load manifest.json if accessible
   */
  function loadManifest() {
    const manifestPath = window.location.pathname.includes('/slides/') ? '../../manifest.json' : 'manifest.json';
    
    fetch(manifestPath)
      .then(res => res.ok ? res.json() : null)
      .then(data => {
        if (data && Array.isArray(data.slides) && data.slides.length > 0) {
          slidesList = data.slides;
          updateUI();
        }
      })
      .catch(() => {
        // Silently fallback to DEFAULT_SLIDES on CORS / file:// errors
      });
  }

  // Initialization
  document.addEventListener('DOMContentLoaded', () => {
    setupEvents();
    loadManifest();
    updateUI();
  });

  // Export Presentation API for external scripts/tools
  window.Presentation = {
    goToSlideIndex,
    toggleSpeakerNotes,
    toggleFullscreen,
    getCurrentSlideInfo,
    getSlidesList: () => [...slidesList]
  };

})();
