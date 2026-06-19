/* ── Catalogo lezioni ── */
const LESSONS = [
  {
    id: 'intro-ai',
    file: 'lessons/01-intro-ai.md',
    title: "Introduzione all'Intelligenza Artificiale",
    desc: "Cos'è l'AI, storia, tipi di apprendimento automatico e applicazioni reali.",
    tag: 'Fondamenti',
    duration: '20 min'
  },
  {
    id: 'llm',
    file: 'lessons/02-large-language-models.md',
    title: 'Come funzionano i Large Language Models',
    desc: 'Transformer, token, embeddings e architettura dei modelli linguistici moderni.',
    tag: 'Fondamenti',
    duration: '25 min'
  },
  {
    id: 'prompt-engineering',
    file: 'lessons/03-prompt-engineering.md',
    title: 'Prompt Engineering',
    desc: 'Tecniche avanzate per scrivere prompt efficaci: few-shot, chain-of-thought, role prompting.',
    tag: 'Pratico',
    duration: '30 min'
  },
  {
    id: 'agenti-ai',
    file: 'lessons/04-agenti-ai.md',
    title: 'Agenti AI: Architettura e Componenti',
    desc: 'Cosa rende un LLM un agente: memoria, strumenti, pianificazione e ciclo ReAct.',
    tag: 'Agenti',
    duration: '35 min'
  },
  {
    id: 'tools-function-calling',
    file: 'lessons/05-tools-function-calling.md',
    title: 'Tools e Function Calling',
    desc: "Come dare strumenti agli agenti: API, ricerca web, esecuzione di codice e database.",
    tag: 'Agenti',
    duration: '30 min'
  },
  {
    id: 'rag',
    file: 'lessons/06-rag.md',
    title: 'RAG — Retrieval Augmented Generation',
    desc: 'Connetti i tuoi dati agli LLM con embedding, vector database e retrieval semantico.',
    tag: 'Avanzato',
    duration: '35 min'
  },
  {
    id: 'multi-agent',
    file: 'lessons/07-sistemi-multi-agente.md',
    title: 'Sistemi Multi-Agente',
    desc: 'Orchestrazione, handoff, supervisori e pattern per agenti che collaborano in team.',
    tag: 'Avanzato',
    duration: '40 min'
  },
  {
    id: 'primo-agente',
    file: 'lessons/08-primo-agente.md',
    title: 'Costruisci il tuo Primo Agente',
    desc: 'Tutorial pratico: agente con tool use, memoria e loop di ragionamento con Python.',
    tag: 'Pratico',
    duration: '45 min'
  }
];

/* ── Stato ── */
let currentLesson = -1;
const progress = JSON.parse(localStorage.getItem('aischool_progress') || '{}');

/* ── DOM refs ── */
const sidebar       = document.getElementById('sidebar');
const overlay       = document.getElementById('overlay');
const menuBtn       = document.getElementById('menuBtn');
const sidebarToggle = document.getElementById('sidebarToggle');
const homeView      = document.getElementById('homeView');
const lessonView    = document.getElementById('lessonView');
const lessonContent = document.getElementById('lessonContent');
const breadcrumb    = document.getElementById('breadcrumb');
const progressBar   = document.getElementById('progressBar');
const btnPrev       = document.getElementById('btnPrev');
const btnNext       = document.getElementById('btnNext');
const btnStart      = document.getElementById('btnStart');
const modulesGrid   = document.getElementById('modulesGrid');
const lessonNav     = document.getElementById('lessonNav');

/* ── Init ── */
function init() {
  buildSidebarNav();
  buildModulesGrid();
  updateProgressBar();

  menuBtn.addEventListener('click', openSidebar);
  sidebarToggle.addEventListener('click', closeSidebar);
  overlay.addEventListener('click', closeSidebar);
  btnPrev.addEventListener('click', () => navigateTo(currentLesson - 1));
  btnNext.addEventListener('click', () => navigateTo(currentLesson + 1));
  btnStart.addEventListener('click', () => navigateTo(0));

  // Deep link via hash
  const hash = location.hash.replace('#', '');
  if (hash) {
    const idx = LESSONS.findIndex(l => l.id === hash);
    if (idx !== -1) { navigateTo(idx); return; }
  }
  showHome();
}

/* ── Sidebar ── */
function buildSidebarNav() {
  const navEl = document.createElement('div');
  LESSONS.forEach((lesson, i) => {
    const btn = document.createElement('button');
    btn.className = 'nav-item';
    btn.dataset.idx = i;
    btn.innerHTML = `<span class="nav-num">${String(i + 1).padStart(2, '0')}</span><span class="nav-title">${lesson.title}</span>`;
    btn.addEventListener('click', () => { navigateTo(i); closeSidebar(); });
    navEl.appendChild(btn);
  });
  lessonNav.appendChild(navEl);
}

function openSidebar()  { sidebar.classList.add('open'); overlay.classList.add('open'); }
function closeSidebar() { sidebar.classList.remove('open'); overlay.classList.remove('open'); }

/* ── Home ── */
function buildModulesGrid() {
  const tagColors = {
    'Fondamenti': '#6c63ff',
    'Pratico': '#22d3a5',
    'Agenti': '#a78bfa',
    'Avanzato': '#f472b6'
  };

  LESSONS.forEach((lesson, i) => {
    const card = document.createElement('div');
    card.className = 'module-card';
    const done = progress[lesson.id];
    card.innerHTML = `
      <div class="card-num">MODULO ${String(i + 1).padStart(2, '0')}</div>
      <div class="card-title">${lesson.title}</div>
      <div class="card-desc">${lesson.desc}</div>
      <div class="card-footer">
        <span class="card-tag" style="color:${tagColors[lesson.tag] || '#fff'}">${lesson.tag}</span>
        <span>⏱ ${lesson.duration}</span>
        ${done ? '<span style="color:#22d3a5">✓ Completata</span>' : ''}
      </div>
    `;
    card.addEventListener('click', () => navigateTo(i));
    modulesGrid.appendChild(card);
  });
}

function showHome() {
  homeView.style.display = '';
  lessonView.style.display = 'none';
  breadcrumb.textContent = 'Home';
  location.hash = '';
  currentLesson = -1;
  updateActiveNav(-1);
}

/* ── Navigazione lezioni ── */
async function navigateTo(idx) {
  if (idx < 0 || idx >= LESSONS.length) return;
  currentLesson = idx;
  const lesson = LESSONS[idx];
  location.hash = lesson.id;

  homeView.style.display = 'none';
  lessonView.style.display = '';
  lessonContent.innerHTML = '<div class="loading">Caricamento lezione...</div>';
  breadcrumb.textContent = `Modulo ${idx + 1} — ${lesson.title}`;

  updateActiveNav(idx);
  btnPrev.disabled = idx === 0;
  btnNext.disabled = idx === LESSONS.length - 1;
  btnNext.textContent = idx === LESSONS.length - 1 ? '✓ Fine corso' : 'Successiva →';

  try {
    const res = await fetch(lesson.file);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const md = await res.text();
    renderLesson(md, lesson);
    markComplete(lesson.id);
    updateProgressBar();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } catch (e) {
    lessonContent.innerHTML = `<div class="loading" style="color:#f87171">Errore nel caricamento della lezione.<br><small>${e.message}</small></div>`;
  }
}

function renderLesson(md, lesson) {
  marked.setOptions({
    highlight: (code, lang) => {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value;
      }
      return hljs.highlightAuto(code).value;
    },
    breaks: true
  });

  const html = marked.parse(md);
  lessonContent.innerHTML = html;

  // Meta badge sotto h1
  const h1 = lessonContent.querySelector('h1');
  if (h1) {
    const meta = document.createElement('div');
    meta.className = 'lesson-meta';
    meta.innerHTML = `<span>⏱ ${lesson.duration}</span><span>🏷 ${lesson.tag}</span>`;
    h1.after(meta);
  }

  // Syntax highlight su blocchi senza classe
  lessonContent.querySelectorAll('pre code:not([class])').forEach(el => {
    hljs.highlightElement(el);
  });
}

function updateActiveNav(idx) {
  document.querySelectorAll('.nav-item').forEach((el, i) => {
    el.classList.toggle('active', i === idx);
  });
}

/* ── Progresso ── */
function markComplete(id) {
  progress[id] = true;
  localStorage.setItem('aischool_progress', JSON.stringify(progress));
}

function updateProgressBar() {
  const pct = Math.round((Object.keys(progress).length / LESSONS.length) * 100);
  progressBar.style.width = pct + '%';
}

/* ── Avvio ── */
document.addEventListener('DOMContentLoaded', init);
