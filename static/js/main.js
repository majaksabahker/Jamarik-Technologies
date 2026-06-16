/* ============================================================
   JAMARIK TECHNOLOGIES — main.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Navbar scroll ──────────────────────────────────────── */
  const navbar = document.querySelector('.navbar');
  const onScroll = () => {
    navbar?.classList.toggle('scrolled', window.scrollY > 30);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ── Mobile nav toggle ──────────────────────────────────── */
  const toggle = document.querySelector('.nav-toggle');
  const links  = document.querySelector('.nav-links');
  const cta    = document.querySelector('.nav-cta');

  toggle?.addEventListener('click', () => {
    const open = links?.classList.toggle('open');
    cta?.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    // Animate hamburger
    const spans = toggle.querySelectorAll('span');
    if (open) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
    } else {
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }
  });

  // Close mobile nav on link click
  links?.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      links.classList.remove('open');
      cta?.classList.remove('open');
    });
  });

  /* ── Active nav link ────────────────────────────────────── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === currentPath ||
        (currentPath !== '/' && a.getAttribute('href').startsWith(currentPath.split('/')[1]))) {
      a.classList.add('active');
    }
  });

  /* ── Scroll reveal ──────────────────────────────────────── */
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 80);
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  /* ── Counter animation ──────────────────────────────────── */
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-value[data-count]').forEach(el => counterObserver.observe(el));

  function animateCounter(el) {
    const target  = parseFloat(el.dataset.count);
    const suffix  = el.dataset.suffix || '';
    const prefix  = el.dataset.prefix || '';
    const decimal = (el.dataset.count.includes('.')) ? 1 : 0;
    const duration = 1800;
    const start = performance.now();

    const frame = (now) => {
      const progress = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 4);
      const value = (target * ease).toFixed(decimal);
      el.textContent = `${prefix}${value}${suffix}`;
      if (progress < 1) requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  }

  /* ── Hero metric bars ───────────────────────────────────── */
  document.querySelectorAll('.metric-bar-fill').forEach(bar => {
    const width = bar.dataset.width || '80%';
    setTimeout(() => { bar.style.width = width; }, 600);
  });

  /* ── Portfolio filter ───────────────────────────────────── */
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      document.querySelectorAll('.project-card').forEach(card => {
        const match = !filter || card.dataset.category === filter;
        card.style.display = match ? '' : 'none';
      });
    });
  });

  /* ── AJAX contact form ──────────────────────────────────── */
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = contactForm.querySelector('[type=submit]');
      const originalText = btn.innerHTML;
      btn.innerHTML = '<span>Sending…</span>';
      btn.disabled = true;

      try {
        const res = await fetch(contactForm.action, {
          method: 'POST',
          body: new FormData(contactForm),
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await res.json();

        if (data.success) {
          document.querySelector('.contact-form-card')?.classList.add('hidden');
          document.querySelector('.form-success')?.style.setProperty('display', 'block');
          showToast('Message sent! We\'ll reply within 24 hours. ✅');
        } else {
          showToast('Please fix the errors below.', 'error');
        }
      } catch {
        showToast('Network error. Please try again.', 'error');
      } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
      }
    });
  }

  /* ── Toast ──────────────────────────────────────────────── */
  function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.querySelector('.toast-text').textContent = message;
    toast.querySelector('.toast-icon').textContent = type === 'success' ? '✅' : '❌';
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 4000);
  }

  /* ── Cookie consent ─────────────────────────────────────── */
  const banner = document.getElementById('cookieBanner');
  if (banner && !localStorage.getItem('jmk_cookie_consent')) {
    setTimeout(() => banner.classList.add('visible'), 1500);
  }

  document.getElementById('cookieAccept')?.addEventListener('click', () => {
    localStorage.setItem('jmk_cookie_consent', '1');
    banner.classList.remove('visible');
  });

  document.getElementById('cookieDecline')?.addEventListener('click', () => {
    localStorage.setItem('jmk_cookie_consent', '0');
    banner.classList.remove('visible');
  });

  /* ── Smooth external link open ──────────────────────────── */
  document.querySelectorAll('a[href^="http"]').forEach(a => {
    if (!a.hasAttribute('target')) a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  });

});