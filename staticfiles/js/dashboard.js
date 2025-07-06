document.addEventListener('DOMContentLoaded', function () {
  // Expand/collapse dashboard cards
  document.querySelectorAll('.dashboard-card').forEach(card => {
    card.addEventListener('click', function (e) {
      if (
        e.target.closest('.no-toggle') ||
        e.target.closest('a') || 
        e.target.closest('button') ||
        e.target.closest('textarea') ||
        e.target.closest('input') ||
        card.classList.contains('static')
      ) {
        return;
      }
      this.classList.toggle('expanded');
      this.classList.toggle('collapsed');
      const details = this.querySelector('.card-details');
      if (details) {
        details.classList.toggle('d-none');
      }
    });
  });

  // Show/hide payment popup
  const paymentPopup = document.getElementById('membershipPopup');
  const payBtn = document.getElementById('triggerPaymentPopup');
  const closePayBtn = document.getElementById('closePaymentPopup');

  if (payBtn && paymentPopup && closePayBtn) {
    payBtn.addEventListener('click', function (e) {
      e.preventDefault();
      paymentPopup.classList.add('active');
    });

    closePayBtn.addEventListener('click', function () {
      paymentPopup.classList.remove('active');
    });
  }

  // Show/hide transactions popup
  const transactionsPopup = document.getElementById('transactionsPopup');
  const openTransactionsBtn = document.getElementById('triggerTransactionsPopup');
  const closeTransactionsBtn = document.getElementById('closeTransactionsPopup');

  if (openTransactionsBtn && transactionsPopup) {
    openTransactionsBtn.addEventListener('click', function (e) {
      e.preventDefault();
      transactionsPopup.classList.add('active');
    });
  }

  if (closeTransactionsBtn && transactionsPopup) {
    closeTransactionsBtn.addEventListener('click', function () {
      transactionsPopup.classList.remove('active');
    });
  }

  // Show/hide questions popup (use active class toggle for consistency)
  const questionsPopup = document.getElementById('questionsPopup');
  const openQuestionsBtn = document.getElementById('triggerQuestionsPopup');
  const closeQuestionsBtn = document.getElementById('closeQuestionsPopup');

  if (openQuestionsBtn && questionsPopup) {
    openQuestionsBtn.addEventListener('click', function (e) {
      e.preventDefault();
      if (questionsPopup.classList.contains('active')) {
        questionsPopup.classList.remove('active');
      } else {
        questionsPopup.classList.add('active');
      }
    });
  }

  if (closeQuestionsBtn && questionsPopup) {
    closeQuestionsBtn.addEventListener('click', function () {
      questionsPopup.classList.remove('active');
    });
  }

  // Click outside questions popup closes it
  document.addEventListener('click', function (e) {
    if (
      questionsPopup &&
      !questionsPopup.contains(e.target) &&
      !openQuestionsBtn.contains(e.target)
    ) {
      questionsPopup.classList.remove('active');
    }
  });
});
