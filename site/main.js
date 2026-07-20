(function () {
  'use strict';

  /* ---------- Configuração da aba Contato ---------- */
  var SITE_CONFIG = {
    // Troque para true quando tiver o credenciamento de assessor para exibir a aba "Contato".
    contatoAtivo: true,
    // Seu WhatsApp com código do país e DDD, somente dígitos (ex: 5511999999999).
    whatsappNumero: '5511955951814'
  };

  var TABS = ['inicio', 'bio', 'trajetoria', 'eventos', 'portfolio', 'artigos'];
  if (SITE_CONFIG.contatoAtivo) {
    TABS.push('contato');
  } else {
    var contatoNav = document.querySelector('[data-tab-link="contato"]');
    if (contatoNav) contatoNav.remove();
  }

  var root = document.documentElement;
  var isTouch = 'ontouchstart' in window;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Theme ---------- */
  var themeToggle = document.getElementById('theme-toggle');
  var themeGlyph = document.getElementById('theme-glyph');

  function applyTheme(dark) {
    root.setAttribute('data-theme', dark ? 'dark' : 'light');
    themeGlyph.textContent = dark ? '☾' : '☀';
  }

  function initTheme() {
    var saved = localStorage.getItem('theme');
    var dark = saved ? saved === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(dark);
  }

  themeToggle.addEventListener('click', function () {
    var dark = root.getAttribute('data-theme') !== 'dark';
    applyTheme(dark);
    localStorage.setItem('theme', dark ? 'dark' : 'light');
  });

  initTheme();

  /* ---------- Scroll reveal ---------- */
  var io = null;
  function getObserver() {
    if (io) return io;
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    return io;
  }

  function observeReveals(scope) {
    var observer = getObserver();
    requestAnimationFrame(function () {
      (scope || document).querySelectorAll('[data-reveal]:not(.revealed)').forEach(function (el) {
        observer.observe(el);
      });
    });
  }

  /* ---------- Tabs ---------- */
  var panels = {};
  TABS.forEach(function (id) { panels[id] = document.getElementById(id); });
  var navLinks = document.querySelectorAll('[data-tab-link]');

  function setTab(id, opts) {
    if (!panels[id]) id = 'inicio';
    opts = opts || {};

    TABS.forEach(function (t) {
      panels[t].hidden = t !== id;
    });
    navLinks.forEach(function (btn) {
      var isNav = btn.classList.contains('nav-item');
      if (!isNav) return;
      btn.classList.toggle('active', btn.getAttribute('data-tab-link') === id);
    });

    if (history.replaceState) history.replaceState(null, '', '#' + id);

    if (!opts.silent) {
      window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
    }
    observeReveals(panels[id]);
  }

  navLinks.forEach(function (btn) {
    btn.addEventListener('click', function () {
      setTab(btn.getAttribute('data-tab-link'));
    });
  });

  window.addEventListener('popstate', function () {
    var id = location.hash.replace('#', '');
    setTab(TABS.indexOf(id) !== -1 ? id : 'inicio', { silent: true });
  });

  var initialTab = TABS.indexOf(location.hash.replace('#', '')) !== -1 ? location.hash.replace('#', '') : 'inicio';
  setTab(initialTab, { silent: true });

  /* ---------- Custom cursor + parallax blobs ---------- */
  if (!isTouch && !reduceMotion) {
    var cursor = document.getElementById('cursor');
    var blobs = Array.prototype.slice.call(document.querySelectorAll('.blob'));
    var factors = [0.035, -0.05, 0.02];

    var mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    var cpos = { x: mouse.x, y: mouse.y };
    var bpos = blobs.map(function () { return { x: 0, y: 0 }; });
    var hovering = false;

    window.addEventListener('mousemove', function (e) {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    });
    document.addEventListener('mouseover', function (e) {
      if (e.target.closest && e.target.closest('a,button,[data-hoverable]')) hovering = true;
    });
    document.addEventListener('mouseout', function (e) {
      if (e.target.closest && e.target.closest('a,button,[data-hoverable]')) hovering = false;
    });

    function lerp(a, b, t) { return a + (b - a) * t; }

    function tick() {
      cpos.x = lerp(cpos.x, mouse.x, 0.2);
      cpos.y = lerp(cpos.y, mouse.y, 0.2);
      var scale = hovering ? 2.3 : 1;
      cursor.style.transform = 'translate(' + cpos.x + 'px,' + cpos.y + 'px) translate(-50%,-50%) scale(' + scale + ')';
      cursor.style.opacity = '1';

      var dx = mouse.x - window.innerWidth / 2;
      var dy = mouse.y - window.innerHeight / 2;
      blobs.forEach(function (el, i) {
        bpos[i].x = lerp(bpos[i].x, dx * factors[i], 0.06);
        bpos[i].y = lerp(bpos[i].y, dy * factors[i], 0.06);
        el.style.transform = 'translate(' + bpos[i].x + 'px,' + bpos[i].y + 'px)';
      });

      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  } else {
    document.getElementById('cursor').remove();
  }

  /* ---------- Legal modal ---------- */
  var legalOverlay = document.getElementById('legal-overlay');
  var legalPanel = document.getElementById('legal-panel');
  var legalTitle = document.getElementById('legal-title');
  var legalBody = document.getElementById('legal-body');
  var legalClose = document.getElementById('legal-close');

  var LEGAL = {
    termos: {
      title: 'Termos de Uso',
      body: 'Bem-vindo(a). Ao acessar e usar este site, você concorda com os termos abaixo.\n\n' +
        '1. Conteúdo próprio — Todos os textos, artigos, materiais e criações publicados aqui são de autoria própria e protegidos por direitos autorais. É proibida a reprodução total ou parcial sem autorização.\n\n' +
        '2. Uso das informações — O conteúdo tem caráter informativo e educativo e não constitui recomendação individual de investimento. Decisões financeiras são de responsabilidade do leitor.\n\n' +
        '3. Links e terceiros — Este site pode conter links externos; não nos responsabilizamos pelo conteúdo de páginas de terceiros.\n\n' +
        '4. Alterações — Estes termos podem ser atualizados a qualquer momento, com efeito a partir da publicação.'
    },
    privacidade: {
      title: 'Política de Privacidade',
      body: 'Sua privacidade é importante. Esta política resume como as informações são tratadas neste site.\n\n' +
        '1. Dados coletados — Podem ser coletados apenas os dados que você fornecer voluntariamente (por exemplo, ao entrar em contato).\n\n' +
        '2. Uso dos dados — As informações são usadas exclusivamente para responder e manter contato, nunca vendidas a terceiros.\n\n' +
        '3. Cookies — Podem ser usados cookies para melhorar a navegação; você pode desativá-los no seu navegador.\n\n' +
        '4. Seus direitos — Você pode solicitar acesso, correção ou exclusão dos seus dados a qualquer momento.\n\n' +
        '5. Contato — Em caso de dúvidas sobre esta política, entre em contato pelos canais informados no site.'
    }
  };

  var lastFocused = null;

  function openLegal(kind) {
    var entry = LEGAL[kind] || LEGAL.termos;
    legalTitle.textContent = entry.title;
    legalBody.textContent = entry.body;
    legalOverlay.hidden = false;
    lastFocused = document.activeElement;
    legalClose.focus();
    document.body.style.overflow = 'hidden';
  }

  function closeLegal() {
    legalOverlay.hidden = true;
    document.body.style.overflow = '';
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }

  document.querySelectorAll('[data-legal]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      openLegal(btn.getAttribute('data-legal'));
    });
  });
  legalOverlay.addEventListener('click', closeLegal);
  legalPanel.addEventListener('click', function (e) { e.stopPropagation(); });
  legalClose.addEventListener('click', closeLegal);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !legalOverlay.hidden) closeLegal();
  });

  /* ---------- Quiz de qualificação (Contato) ---------- */
  if (SITE_CONFIG.contatoAtivo) {
    initQuiz();
  }

  function initQuiz() {
    var section = document.getElementById('contato');
    if (!section) return;

    var steps = section.querySelectorAll('[data-quiz-step]');
    var dots = section.querySelectorAll('[data-step-dot]');
    var answers = {};

    var FIELD_LABELS = {
      disponivel: 'Disponível para investir',
      jaInveste: 'Já investe atualmente',
      objetivo: 'Principal objetivo',
      urgencia: 'Quando pretende começar',
      horizonte: 'Horizonte de tempo',
      reacao: 'Reação a queda de 20%',
      experiencia: 'Experiência com investimentos',
      prioridade: 'Prioridade'
    };

    function showStep(id) {
      steps.forEach(function (s) {
        s.hidden = s.getAttribute('data-quiz-step') !== String(id);
      });
      dots.forEach(function (d) {
        d.classList.toggle('active', Number(d.getAttribute('data-step-dot')) <= Number(id));
      });
    }

    section.querySelectorAll('[data-quiz-group]').forEach(function (group) {
      var key = group.getAttribute('data-quiz-group');
      group.querySelectorAll('.quiz-option').forEach(function (btn) {
        btn.addEventListener('click', function () {
          group.querySelectorAll('.quiz-option').forEach(function (b) { b.classList.remove('selected'); });
          btn.classList.add('selected');
          answers[key] = { value: btn.getAttribute('data-value'), score: Number(btn.getAttribute('data-score') || 0) };
        });
      });
    });

    function requireContactFields() {
      var nome = section.querySelector('#q-nome').value.trim();
      var wpp = section.querySelector('#q-whatsapp').value.trim();
      if (!nome || !wpp) {
        alert('Preencha nome e WhatsApp para continuar.');
        return false;
      }
      return true;
    }

    section.querySelectorAll('[data-quiz-next]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (btn.closest('[data-quiz-step="1"]') && !requireContactFields()) return;
        showStep(btn.getAttribute('data-quiz-next'));
      });
    });

    section.querySelectorAll('[data-quiz-back]').forEach(function (btn) {
      btn.addEventListener('click', function () { showStep(btn.getAttribute('data-quiz-back')); });
    });

    var skipBtn = section.querySelector('[data-quiz-skip]');
    if (skipBtn) skipBtn.addEventListener('click', function () { finish(false); });

    var finishBtn = section.querySelector('[data-quiz-finish]');
    if (finishBtn) finishBtn.addEventListener('click', function () { finish(true); });

    function computeProfile() {
      var keys = ['horizonte', 'reacao', 'experiencia', 'prioridade'];
      var total = 0, count = 0;
      keys.forEach(function (k) { if (answers[k]) { total += answers[k].score; count++; } });
      if (count < keys.length) return null;
      if (total <= 6) return { label: 'Conservador', desc: 'Você prioriza segurança e prefere preservar o capital, mesmo com retornos mais modestos.' };
      if (total <= 10) return { label: 'Moderado', desc: 'Você busca equilíbrio entre segurança e rentabilidade, aceitando algum risco em troca de retornos melhores.' };
      return { label: 'Arrojado', desc: 'Você tolera mais oscilação em troca de potencial de retorno maior no longo prazo.' };
    }

    function buildMessage(profile) {
      var nome = section.querySelector('#q-nome').value.trim();
      var wpp = section.querySelector('#q-whatsapp').value.trim();
      var email = section.querySelector('#q-email').value.trim();
      var lines = ['Olá, Victor! Fiz a avaliação no seu site e gostaria de conversar.', ''];
      lines.push('Nome: ' + nome);
      lines.push('WhatsApp: ' + wpp);
      if (email) lines.push('E-mail: ' + email);

      var qualKeys = ['disponivel', 'jaInveste', 'objetivo', 'urgencia'];
      if (qualKeys.some(function (k) { return answers[k]; })) {
        lines.push('', '— Qualificação —');
        qualKeys.forEach(function (k) {
          if (answers[k]) lines.push(FIELD_LABELS[k] + ': ' + answers[k].value);
        });
      }

      if (profile) {
        lines.push('', '— Perfil de investidor —', 'Perfil indicativo: ' + profile.label);
        ['horizonte', 'reacao', 'experiencia', 'prioridade'].forEach(function (k) {
          if (answers[k]) lines.push(FIELD_LABELS[k] + ': ' + answers[k].value);
        });
      }

      return lines.join('\n');
    }

    function finish(tryProfile) {
      if (!requireContactFields()) {
        showStep('1');
        return;
      }

      var profile = tryProfile ? computeProfile() : null;
      var profileBox = section.querySelector('#quiz-result-profile');
      if (profile) {
        profileBox.hidden = false;
        section.querySelector('#quiz-result-value').textContent = profile.label;
        section.querySelector('#quiz-result-desc').textContent = profile.desc;
      } else {
        profileBox.hidden = true;
      }

      var message = buildMessage(profile);
      var link = section.querySelector('#quiz-whatsapp-btn');
      var number = SITE_CONFIG.whatsappNumero.replace(/\D/g, '');
      if (number) {
        link.href = 'https://wa.me/' + number + '?text=' + encodeURIComponent(message);
        link.classList.remove('disabled');
        link.removeAttribute('title');
      } else {
        link.href = '#';
        link.classList.add('disabled');
        link.setAttribute('title', 'Configure SITE_CONFIG.whatsappNumero em main.js');
      }

      showStep('result');
    }

    showStep('1');
  }

})();
