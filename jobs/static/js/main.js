/**
 * CareerConnect - Core Interactive JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initApplicationModal();
  initDeleteConfirmations();
  initFaqAccordion();
  initAutoDismissAlerts();
});

/* ==========================================================================
   MOBILE NAVIGATION DRAWER
   ========================================================================== */
function initMobileMenu() {
  const menuBtn = document.getElementById('mobileMenuBtn');
  const menuCloseBtn = document.getElementById('mobileMenuCloseBtn');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const mobileOverlay = document.getElementById('mobileOverlay');

  if (menuBtn && mobileDrawer) {
    menuBtn.addEventListener('click', () => {
      mobileDrawer.classList.remove('-translate-x-full');
      if (mobileOverlay) mobileOverlay.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    });
  }

  function closeDrawer() {
    if (mobileDrawer) mobileDrawer.classList.add('-translate-x-full');
    if (mobileOverlay) mobileOverlay.classList.add('hidden');
    document.body.style.overflow = '';
  }

  if (menuCloseBtn) menuCloseBtn.addEventListener('click', closeDrawer);
  if (mobileOverlay) mobileOverlay.addEventListener('click', closeDrawer);
}

/* ==========================================================================
   APPLICATION MODAL (Vanilla JS Modal)
   ========================================================================== */
function initApplicationModal() {
  const openModalBtns = document.querySelectorAll('[data-open-modal="applyModal"]');
  const closeModalBtns = document.querySelectorAll('[data-close-modal="applyModal"]');
  const modal = document.getElementById('applyModal');

  openModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  closeModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }
    });
  });

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }
    });
  }
}

/* ==========================================================================
   JOB DELETE CONFIRMATION DIALOG
   ========================================================================== */
function initDeleteConfirmations() {
  const deleteForms = document.querySelectorAll('form.confirm-delete-form');
  deleteForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      const jobTitle = form.getAttribute('data-job-title') || 'this job';
      const confirmed = window.confirm(`Are you sure you want to permanently delete "${jobTitle}"? This cannot be undone.`);
      if (!confirmed) {
        e.preventDefault();
      }
    });
  });
}

/* ==========================================================================
   QUICK DEMO CREDENTIALS AUTOFILL
   ========================================================================== */
window.fillDemoCredentials = function(username, password) {
  const usernameInput = document.querySelector('input[name="username"]');
  const passwordInput = document.querySelector('input[name="password"]');
  if (usernameInput && passwordInput) {
    usernameInput.value = username;
    passwordInput.value = password;
    showToast(`Filled credentials for ${username}!`, 'info');
  }
};

/* ==========================================================================
   FAQ ACCORDION
   ========================================================================== */
function initFaqAccordion() {
  const faqButtons = document.querySelectorAll('.faq-toggle');
  faqButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const content = btn.nextElementSibling;
      const icon = btn.querySelector('.faq-icon');
      if (content) {
        const isHidden = content.classList.contains('hidden');
        content.classList.toggle('hidden');
        if (icon) {
          icon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
        }
      }
    });
  });
}

/* ==========================================================================
   AUTO-DISMISS NOTIFICATION ALERTS
   ========================================================================== */
function initAutoDismissAlerts() {
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 4500);
  });
}

/* ==========================================================================
   FLOATING TOAST NOTIFICATION
   ========================================================================== */
function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'fixed bottom-4 right-4 z-50 flex flex-col gap-2 max-w-sm';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  const bgColor = type === 'success' ? 'bg-emerald-600' : (type === 'danger' ? 'bg-rose-600' : 'bg-navy-900');
  toast.className = `${bgColor} text-white px-4 py-3 rounded-lg shadow-lg text-sm font-medium flex items-center justify-between gap-3 transition-all duration-300 transform translate-y-2 opacity-0`;
  toast.innerHTML = `
    <span>${message}</span>
    <button type="button" class="text-white/80 hover:text-white">&times;</button>
  `;

  container.appendChild(toast);
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  });

  const closeBtn = toast.querySelector('button');
  closeBtn.addEventListener('click', () => toast.remove());

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}
