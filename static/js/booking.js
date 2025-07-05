document.addEventListener('DOMContentLoaded', function () {
  function setupPopup(openBtnId, popupId, closeBtnId) {
    const popup = document.getElementById(popupId);
    const openBtn = document.getElementById(openBtnId);
    const closeBtn = document.getElementById(closeBtnId);

    if (!popup) return;

    function show() {
      popup.classList.remove('hidden');
      popup.setAttribute('aria-hidden', 'false');
      popup.focus();
    }

    function hide() {
      popup.classList.add('hidden');
      popup.setAttribute('aria-hidden', 'true');
    }

    if (openBtn) {
      openBtn.addEventListener('click', show);
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', hide);
    }

    // Inside content click doesn’t close
    const content = popup.querySelector('.payment-popup-content');
    if (content) {
      content.addEventListener('click', (e) => e.stopPropagation());
    }

    // Outside click closes
    popup.addEventListener('click', hide);

    // Escape closes
    document.addEventListener('keydown', (e) => {
      if (e.key === "Escape" && !popup.classList.contains('hidden')) {
        hide();
      }
    });
  }

  // Initialize both popups (even if only one exists)
  setupPopup('openPaymentPopup', 'paymentPopup', 'closePaymentPopup');
  setupPopup('showBookingDetails', 'bookingDetailsPopup', 'closeBookingDetails');

  // Auto-dismiss alerts
  const alerts = document.querySelectorAll('.alert');
  setTimeout(() => {
    alerts.forEach(alert => alert.remove());
  }, 10000);
});
