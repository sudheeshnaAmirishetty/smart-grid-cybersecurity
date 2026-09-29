document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.fade-in').forEach((el, index) => {
    el.style.animationDelay = `${index * 0.1}s`;
  });

  const toasts = document.querySelectorAll('.toast');
  toasts.forEach((toast) => {
    setTimeout(() => {
      toast.classList.remove('show');
    }, 4200);
  });
});
