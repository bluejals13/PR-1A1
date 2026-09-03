
const currentSlide = Number(document.body.dataset.slide);

const totalSlides = 3;

const progress = document.getElementById('presentation-progress');
const counter = document.getElementById('presentation-counter');

const speakerPanel = document.getElementById('speaker-panel');
const speakerText = document.getElementById('speaker-text');
const speakerToggle = document.getElementById('speaker-toggle');
const speakerClose = document.getElementById('speaker-close');

const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');


/**
 * 지정한 슬라이드 HTML로 이동
 */
function goToSlide(target) {
  if (target < 1 || target > totalSlides) {
    return;
  }

  window.location.href = `${target}번 슬라이드.html`;
}


/**
 * 발표 UI 초기화
 */
function updatePresentationUI() {
  counter.textContent =
    `${String(currentSlide).padStart(2, '0')} / ${String(totalSlides).padStart(2, '0')}`;

  progress.style.width =
    `${(currentSlide / totalSlides) * 100}%`;

  prevBtn.disabled = currentSlide === 1;
  nextBtn.disabled = currentSlide === totalSlides;

  const slide = document.querySelector('.slide');

  const note =
    slide?.dataset.speakerNote || '발표자 노트가 없습니다.';

  speakerText.textContent = note;
}


/**
 * 발표자 노트 열기 / 닫기
 */
function toggleSpeaker() {
  speakerPanel.classList.toggle('visible');
}


/**
 * 이전 슬라이드
 */
prevBtn.addEventListener('click', () => {
  goToSlide(currentSlide - 1);
});


/**
 * 다음 슬라이드
 */
nextBtn.addEventListener('click', () => {
  goToSlide(currentSlide + 1);
});


/**
 * SPEAKER 버튼
 */
speakerToggle.addEventListener('click', toggleSpeaker);


/**
 * 발표자 노트 닫기
 */
speakerClose.addEventListener('click', () => {
  speakerPanel.classList.remove('visible');
});


/**
 * 키보드 발표 제어
 *
 * ← : 이전 슬라이드
 * → : 다음 슬라이드
 * Space : 다음 슬라이드
 * N : 발표자 노트
 * ESC : 발표자 노트 닫기
 */
document.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowLeft') {
    event.preventDefault();
    goToSlide(currentSlide - 1);

  } else if (event.key === 'ArrowRight' || event.key === ' ') {
    event.preventDefault();
    goToSlide(currentSlide + 1);

  } else if (event.key.toLowerCase() === 'n') {
    event.preventDefault();
    toggleSpeaker();

  } else if (event.key === 'Escape') {
    speakerPanel.classList.remove('visible');
  }
});


/**
 * 최초 UI 업데이트
 */
updatePresentationUI();