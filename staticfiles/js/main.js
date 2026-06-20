/**
 * DAST NEWGEN'SPARK — Main JavaScript
 * Vanilla JS. No framework dependencies.
 */
"use strict";

/* ────────────────────────────────────────────────────────
   NAVBAR
   ──────────────────────────────────────────────────────── */
const navbar  = document.getElementById("navbar");
const toggle  = document.getElementById("navToggle");
const mobileMenu = document.getElementById("mobileMenu");

// Scroll state
window.addEventListener("scroll", () => {
  if (window.scrollY > 20) {
    navbar.classList.add("is-scrolled");
  } else {
    navbar.classList.remove("is-scrolled");
  }
}, { passive: true });

// Mobile menu toggle
function openMenu() {
  mobileMenu.classList.add("is-open");
  toggle.setAttribute("aria-expanded", "true");
  document.body.style.overflow = "hidden";
}

function closeMenu() {
  mobileMenu.classList.remove("is-open");
  toggle.setAttribute("aria-expanded", "false");
  document.body.style.overflow = "";
}

if (toggle && mobileMenu) {
  toggle.addEventListener("click", () => {
    if (mobileMenu.classList.contains("is-open")) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  // Close on outside click
  document.addEventListener("click", (e) => {
    if (!navbar.contains(e.target) && mobileMenu.classList.contains("is-open")) {
      closeMenu();
    }
  });

  // Close on Escape
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && mobileMenu.classList.contains("is-open")) {
      closeMenu();
      toggle.focus();
    }
  });

  // Mobile sub-menus
  mobileMenu.querySelectorAll(".navbar__mobile-dropdown-toggle").forEach((btn) => {
    btn.addEventListener("click", () => {
      const sub = btn.nextElementSibling;
      if (!sub) return;
      const isExpanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!isExpanded));
      sub.hidden = isExpanded;
    });
  });

  // Close mobile menu on any link click
  mobileMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => closeMenu());
  });
}

/* ────────────────────────────────────────────────────────
   BACK TO TOP
   ──────────────────────────────────────────────────────── */
const backToTop = document.getElementById("backToTop");
if (backToTop) {
  window.addEventListener("scroll", () => {
    if (window.scrollY > 400) {
      backToTop.classList.add("is-visible");
    } else {
      backToTop.classList.remove("is-visible");
    }
  }, { passive: true });

  backToTop.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/* ────────────────────────────────────────────────────────
   SCROLL ANIMATIONS (Intersection Observer)
   ──────────────────────────────────────────────────────── */
const animateEls = document.querySelectorAll("[data-animate]");

if (animateEls.length && "IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const delay = el.dataset.delay ? parseInt(el.dataset.delay, 10) : 0;
          setTimeout(() => el.classList.add("is-visible"), delay);
          observer.unobserve(el);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  animateEls.forEach((el) => observer.observe(el));
} else {
  // Fallback: show all immediately
  animateEls.forEach((el) => el.classList.add("is-visible"));
}

/* ────────────────────────────────────────────────────────
   COUNTER ANIMATION
   ──────────────────────────────────────────────────────── */
function animateCounter(el, target, duration = 2000) {
  let start = 0;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    el.textContent = Math.floor(eased * target);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target;
  };
  requestAnimationFrame(step);
}

const statsSection = document.querySelector(".stats");
if (statsSection) {
  const counterObserver = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        statsSection.querySelectorAll(".stats__item").forEach((item) => {
          const target = parseInt(item.dataset.count, 10);
          const counter = item.querySelector(".counter");
          if (counter && target) animateCounter(counter, target);
        });
        counterObserver.disconnect();
      }
    },
    { threshold: 0.3 }
  );
  counterObserver.observe(statsSection);
}

/* ────────────────────────────────────────────────────────
   TESTIMONIALS SLIDER
   ──────────────────────────────────────────────────────── */
const track  = document.getElementById("testimonialsTrack");
const dotsEl = document.getElementById("testimonialsDots");

if (track) {
  const cards     = Array.from(track.children);
  const prevBtn   = document.querySelector(".testimonials__btn--prev");
  const nextBtn   = document.querySelector(".testimonials__btn--next");
  let current     = 0;
  let autoInterval;

  function getVisible() {
    if (window.innerWidth >= 1024) return 3;
    if (window.innerWidth >= 640)  return 2;
    return 1;
  }

  function maxIndex() {
    return Math.max(0, cards.length - getVisible());
  }

  function buildDots() {
    if (!dotsEl) return;
    dotsEl.innerHTML = "";
    for (let i = 0; i <= maxIndex(); i++) {
      const dot = document.createElement("button");
      dot.className = "testimonials__dot" + (i === current ? " is-active" : "");
      dot.setAttribute("role", "tab");
      dot.setAttribute("aria-label", `Témoignage ${i + 1}`);
      dot.addEventListener("click", () => goTo(i));
      dotsEl.appendChild(dot);
    }
  }

  function goTo(index) {
    current = Math.max(0, Math.min(index, maxIndex()));
    const cardWidth = cards[0].offsetWidth + parseInt(getComputedStyle(track).gap, 10);
    track.style.transform = `translateX(-${current * cardWidth}px)`;
    if (dotsEl) {
      dotsEl.querySelectorAll(".testimonials__dot").forEach((d, i) => {
        d.classList.toggle("is-active", i === current);
      });
    }
  }

  function startAuto() {
    clearInterval(autoInterval);
    autoInterval = setInterval(() => {
      goTo(current >= maxIndex() ? 0 : current + 1);
    }, 5000);
  }

  if (prevBtn) prevBtn.addEventListener("click", () => { goTo(current - 1); startAuto(); });
  if (nextBtn) nextBtn.addEventListener("click", () => { goTo(current + 1); startAuto(); });

  // Touch / swipe
  let startX = 0;
  track.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; }, { passive: true });
  track.addEventListener("touchend", (e) => {
    const diff = startX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) {
      goTo(diff > 0 ? current + 1 : current - 1);
      startAuto();
    }
  });

  window.addEventListener("resize", () => { buildDots(); goTo(current); }, { passive: true });

  buildDots();
  startAuto();
}

/* ────────────────────────────────────────────────────────
   FAQ ACCORDION — sync icons with <details> state
   ──────────────────────────────────────────────────────── */
document.querySelectorAll(".faq__item").forEach((details) => {
  details.addEventListener("toggle", () => {
    const icon = details.querySelector(".faq__icon");
    if (!icon) return;
    // Icon rotation handled via CSS [open] selector — no JS needed
  });
});

/* ────────────────────────────────────────────────────────
   AUTO-DISMISS FLASH MESSAGES
   ──────────────────────────────────────────────────────── */
document.querySelectorAll(".alert").forEach((alert) => {
  setTimeout(() => {
    alert.style.transition = "opacity 0.5s, transform 0.5s";
    alert.style.opacity    = "0";
    alert.style.transform  = "translateX(100%)";
    setTimeout(() => alert.remove(), 500);
  }, 6000);
});

/* ────────────────────────────────────────────────────────
   FORM SUBMIT LOADING STATE
   ──────────────────────────────────────────────────────── */
document.querySelectorAll(".contact-form__submit").forEach((btn) => {
  btn.closest("form")?.addEventListener("submit", () => {
    btn.disabled = true;
    const span = btn.querySelector("span");
    if (span) span.textContent = "Envoi en cours…";
    const icon = btn.querySelector("i");
    if (icon) { icon.className = "bx bx-loader-alt"; icon.style.animation = "spin 1s linear infinite"; }
  });
});

// Add CSS for spin animation dynamically
const spinStyle = document.createElement("style");
spinStyle.textContent = "@keyframes spin { to { transform: rotate(360deg); } }";
document.head.appendChild(spinStyle);
