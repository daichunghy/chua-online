    function spawnBlessingText(text, x, y) {
      const el = document.createElement('div');
      el.className = 'floating-blessing';
      el.textContent = text;
      el.style.left = `${x || window.innerWidth / 2}px`;
      el.style.top = `${y || window.innerHeight / 2}px`;
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 1600);
    }
    window.spawnBlessingText = spawnBlessingText;
