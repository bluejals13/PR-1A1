const currentSlide = Number(document.body.dataset.slide);
const totalSlides = 14;

const progress = document.getElementById('presentation-progress');
const counter = document.getElementById('presentation-counter');

const speakerPanel = document.getElementById('speaker-panel');
const speakerText = document.getElementById('speaker-text');
const speakerToggle = document.getElementById('speaker-toggle');
const speakerClose = document.getElementById('speaker-close');

const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');


/* =========================================================
   슬라이드 이동
   ========================================================= */

function goToSlide(target) {
  if (target < 1 || target > totalSlides) {
    return;
  }

  window.location.href = `${target}번 슬라이드.html`;
}


/* =========================================================
   발표 UI
   ========================================================= */

function updatePresentationUI() {

  if (counter) {
    counter.textContent =
      `${String(currentSlide).padStart(2, '0')} / ${String(totalSlides).padStart(2, '0')}`;
  }

  if (progress) {
    progress.style.width =
      `${(currentSlide / totalSlides) * 100}%`;
  }

  if (prevBtn) {
    prevBtn.disabled = currentSlide === 1;
  }

  if (nextBtn) {
    nextBtn.disabled = currentSlide === totalSlides;
  }

  const slide = document.querySelector('.slide');

  const note =
    slide?.dataset.speakerNote ||
    '발표자 노트가 없습니다.';

  if (speakerText) {
    speakerText.textContent = note;
  }
}


/* =========================================================
   Speaker
   ========================================================= */

function toggleSpeaker() {

  if (!speakerPanel) {
    return;
  }

  speakerPanel.classList.toggle('visible');
}


if (prevBtn) {
  prevBtn.addEventListener('click', () => {
    goToSlide(currentSlide - 1);
  });
}


if (nextBtn) {
  nextBtn.addEventListener('click', () => {
    goToSlide(currentSlide + 1);
  });
}


if (speakerToggle) {
  speakerToggle.addEventListener('click', toggleSpeaker);
}


if (speakerClose) {
  speakerClose.addEventListener('click', () => {
    speakerPanel.classList.remove('visible');
  });
}


/* =========================================================
   Keyboard Control
   ← 이전
   → 다음
   Space 다음
   N Speaker
   ESC Speaker 닫기
   ========================================================= */

document.addEventListener('keydown', (event) => {

  if (event.key === 'ArrowLeft') {

    event.preventDefault();
    goToSlide(currentSlide - 1);

  } else if (
    event.key === 'ArrowRight' ||
    event.key === ' '
  ) {

    event.preventDefault();
    goToSlide(currentSlide + 1);

  } else if (
    event.key.toLowerCase() === 'n'
  ) {

    event.preventDefault();
    toggleSpeaker();

  } else if (
    event.key === 'Escape'
  ) {

    speakerPanel?.classList.remove('visible');
  }
});


/* =========================================================
   최초 실행
   ========================================================= */

updatePresentationUI();
