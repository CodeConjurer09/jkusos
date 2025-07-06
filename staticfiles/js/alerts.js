document.addEventListener('DOMContentLoaded', function () {
    setTimeout(() => {
        document.querySelectorAll('.alert.auto-dismiss .progress-bar').forEach(bar => {
            bar.style.width = '0%';
        });
    }, 100);
    setTimeout(() => {
        document.querySelectorAll('.alert.auto-dismiss').forEach(alert => {
            alert.classList.remove('show');
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 500); // match fade duration
        });
    }, 5000);
});
