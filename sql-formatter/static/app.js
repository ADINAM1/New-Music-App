(function () {
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');

  function setTheme(theme) {
    root.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }

  const stored = localStorage.getItem('theme') || 'light';
  setTheme(stored);

  if (toggle) {
    toggle.addEventListener('click', function () {
      const current = root.getAttribute('data-theme');
      const next = current === 'light' ? 'dark' : 'light';
      setTheme(next);
    });
  }

  const copyBtn = document.getElementById('copy-btn');
  const pre = document.getElementById('formatted-sql');
  if (copyBtn && pre) {
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(pre.innerText);
      copyBtn.textContent = 'Copied!';
      setTimeout(() => (copyBtn.textContent = 'Copy to clipboard'), 1500);
    });
  }
})();
