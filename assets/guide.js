// All navigation and screenshots remain accessible without JavaScript.
document.querySelectorAll('.guide-recording').forEach(recording => {
  const video = recording.querySelector('video');
  const playButton = recording.querySelector('.recording-play');
  playButton.hidden = false;
  playButton.addEventListener('click', () => video.play().catch(() => video.focus()));
  ['play', 'pause', 'ended'].forEach(event => video.addEventListener(event, () => {
    playButton.hidden = !video.paused && !video.ended;
  }));
  const steps = [...recording.querySelectorAll('[data-video-time]')];
  steps.forEach(button => { button.disabled = false; });
  steps.forEach(button => button.addEventListener('click', () => {
    const seekAndPlay = () => {
      video.currentTime = Math.min(Number(button.dataset.videoTime), video.duration || Infinity);
      video.play().catch(() => video.focus());
    };
    if (video.readyState >= 1) seekAndPlay();
    else {
      video.addEventListener('loadedmetadata', seekAndPlay, { once: true });
      video.load();
    }
  }));
  video.addEventListener('timeupdate', () => {
    const active = steps.findLast(button => Number(button.dataset.videoTime) <= video.currentTime);
    steps.forEach(button => {
      if (button === active) button.setAttribute('aria-current', 'true');
      else button.removeAttribute('aria-current');
    });
  });
  video.addEventListener('play', () => {
    document.querySelectorAll('video').forEach(other => { if (other !== video) other.pause(); });
  });
});

const guideMenu = document.querySelector('.guide-mobile-menu');
if (guideMenu) {
  guideMenu.addEventListener('keydown', event => {
    if (event.key === 'Escape' && guideMenu.open) {
      guideMenu.open = false;
      guideMenu.querySelector('summary').focus();
    }
  });
  guideMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => { guideMenu.open = false; });
  });
}
const contentsLinks = [...document.querySelectorAll('.guide-toc a')];
if (contentsLinks.length) {
  const sections = contentsLinks.map(link => document.getElementById(link.hash.slice(1)));
  let pending = false;
  const syncContents = () => {
    pending = false;
    const atBottom = window.scrollY > 0 &&
      window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2;
    let active = 0;
    sections.forEach((section, index) => {
      if (section && section.getBoundingClientRect().top <= 160) active = index;
    });
    if (atBottom) active = contentsLinks.length - 1;
    contentsLinks.forEach((link, index) => {
      if (index === active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  const scheduleSync = () => {
    if (!pending) {
      pending = true;
      window.requestAnimationFrame(syncContents);
    }
  };
  window.addEventListener('scroll', scheduleSync, { passive: true });
  window.addEventListener('resize', scheduleSync);
  window.addEventListener('load', scheduleSync);
  scheduleSync();
}

// A small learning example; it does not edit or upload the visitor's photos.
document.querySelectorAll('.word-demo').forEach(demo => {
  const tokens = [...demo.querySelectorAll('.demo-token')];
  const update = () => {
    const count = tokens.filter(token => token.getAttribute('aria-pressed') === 'true').length;
    demo.querySelector('output').textContent = `${count} / ${tokens.length}`;
  };
  tokens.forEach(token => {
    token.addEventListener('click', () => {
      token.setAttribute('aria-pressed', String(token.getAttribute('aria-pressed') !== 'true'));
      update();
    });
  });
  demo.querySelector('.demo-reset').addEventListener('click', () => {
    tokens.forEach((token, index) => token.setAttribute('aria-pressed', String(index === 1)));
    update();
  });
});

const sidebar = document.querySelector('.guide-sidebar');
const currentChapter = sidebar?.querySelector('[aria-current="page"]');
if (currentChapter) {
  const revealCurrentChapter = () => {
    if (!sidebar.clientHeight) return;
    const area = sidebar.getBoundingClientRect();
    const current = currentChapter.getBoundingClientRect();
    if (current.bottom > area.bottom) sidebar.scrollTop += current.bottom - area.bottom + 12;
    else if (current.top < area.top) sidebar.scrollTop -= area.top - current.top + 12;
  };
  if (typeof ResizeObserver === 'function') new ResizeObserver(revealCurrentChapter).observe(sidebar);
  window.addEventListener('load', revealCurrentChapter);
  document.fonts?.ready.then(revealCurrentChapter);
  revealCurrentChapter();
}
