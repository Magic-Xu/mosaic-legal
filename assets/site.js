// Measure the shared header so anchors and sticky navigation clear every locale's layout.
const header = document.querySelector('.site-header');
if (header && typeof ResizeObserver === 'function') {
  new ResizeObserver(() => {
    document.documentElement.style.setProperty('--header-height', `${header.getBoundingClientRect().height}px`);
  }).observe(header);
}

// Navigation stays usable without JavaScript; enhancement adds a keyboard-operable demo.
const picker = document.querySelector('.language-picker');
if (picker) {
  document.addEventListener('click', event => {
    if (!picker.contains(event.target)) picker.open = false;
  });
  picker.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      picker.open = false;
      picker.querySelector('summary').focus();
    }
  });
  picker.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      if (location.hash) link.hash = location.hash;
    });
  });
}

const tabs = [...document.querySelectorAll('.tool-tabs button')];
if (tabs.length) {
  const list = document.querySelector('.tool-tabs');
  list.setAttribute('role', 'tablist');
  const select = (index, focus = false) => {
    tabs.forEach((tab, i) => {
      const active = i === index;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      document.getElementById(tab.dataset.panel).hidden = !active;
    });
    if (focus) tabs[index].focus({ preventScroll: true });
  };
  tabs.forEach((tab, index) => {
    const panel = document.getElementById(tab.dataset.panel);
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', panel.id);
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('aria-labelledby', tab.id);
    panel.tabIndex = 0;
    tab.addEventListener('click', () => select(index));
    tab.addEventListener('keydown', event => {
      const rtl = document.documentElement.dir === 'rtl';
      let next;
      if (event.key === 'ArrowRight') next = (index + (rtl ? -1 : 1) + tabs.length) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + (rtl ? 1 : -1) + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        select(next, true);
      }
    });
  });
  select(0);
  document.documentElement.classList.add('enhanced');
}

// The native dialog keeps focus inside the enlarged screenshot and restores it on close.
const imageDialog = document.querySelector('.image-dialog');
if (imageDialog && typeof imageDialog.showModal === 'function') {
  document.querySelectorAll('a[data-lightbox]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const image = imageDialog.querySelector('img');
      const caption = link.querySelector('img')?.alt || link.closest('figure')?.querySelector('img')?.alt || '';
      image.src = link.href;
      image.alt = caption;
      imageDialog.querySelector('.image-dialog-caption').textContent = caption;
      imageDialog.showModal();
      document.body.classList.add('dialog-open');
    });
  });
  imageDialog.addEventListener('close', () => document.body.classList.remove('dialog-open'));
  imageDialog.addEventListener('click', event => {
    const rect = imageDialog.getBoundingClientRect();
    if (event.target === imageDialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) imageDialog.close();
  });
}
const faqSearch = document.querySelector('.faq-search input');
if (faqSearch) {
  faqSearch.closest('.faq-search').hidden = false;
  const questions = [...document.querySelectorAll('.faq-content .faq-item')];
  const fold = value => value.normalize('NFKC').toLocaleLowerCase().trim();
  const filter = () => {
    const query = fold(faqSearch.value);
    let matches = 0;
    questions.forEach(question => {
      const matchesQuery = fold(question.textContent).includes(query);
      question.hidden = !matchesQuery;
      question.open = Boolean(query) && matchesQuery;
      if (matchesQuery) matches++;
    });
    document.querySelector('.faq-empty').hidden = matches > 0;
  };
  faqSearch.addEventListener('input', filter);
  faqSearch.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      faqSearch.value = '';
      filter();
    }
  });
}

// Keep the active page in view when the mobile navigation scrolls horizontally.
const primaryNav = document.querySelector('.primary-nav');
const activePage = primaryNav?.querySelector('[aria-current="page"]');
if (activePage) {
  const navRect = primaryNav.getBoundingClientRect();
  const activeRect = activePage.getBoundingClientRect();
  if (activeRect.right > navRect.right) primaryNav.scrollLeft += activeRect.right - navRect.right;
  else if (activeRect.left < navRect.left) primaryNav.scrollLeft += activeRect.left - navRect.left;
}
