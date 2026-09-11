/* PassForge V7 Vanilla JS Interactivity */
document.addEventListener('DOMContentLoaded', () => {

  // Copy to clipboard helper
  window.copyToClipboard = function(text, btn) {
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
      const originalText = btn.innerText;
      btn.innerText = 'Copied';
      btn.classList.add('btn-secondary');
      setTimeout(() => {
        btn.innerText = originalText;
        btn.classList.remove('btn-secondary');
      }, 1800);
    }).catch(err => {
      console.error('Clipboard write failed', err);
    });
  };

  // Reveal password via POST endpoint
  window.revealPassword = function(credId, btn) {
    const pwdCell = document.getElementById(`pwd-cell-${credId}`);
    if (!pwdCell) return;

    if (pwdCell.getAttribute('data-state') === 'revealed') {
      pwdCell.innerText = '••••••••••••';
      pwdCell.setAttribute('data-state', 'masked');
      btn.innerText = 'Reveal';
      return;
    }

    btn.innerText = 'Loading...';
    fetch(`/vault/reveal/${credId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.password) {
        pwdCell.innerText = data.password;
        pwdCell.setAttribute('data-state', 'revealed');
        pwdCell.setAttribute('data-plain', data.password);
        btn.innerText = 'Hide';
      } else {
        alert(data.error || 'Decryption failed.');
        btn.innerText = 'Reveal';
      }
    })
    .catch(err => {
      console.error('Reveal request failed', err);
      btn.innerText = 'Reveal';
    });
  };

  // Copy decrypted secret
  window.copySecret = function(credId, btn) {
    const pwdCell = document.getElementById(`pwd-cell-${credId}`);
    if (!pwdCell) return;

    if (pwdCell.getAttribute('data-state') === 'revealed') {
      window.copyToClipboard(pwdCell.innerText, btn);
    } else {
      // Fetch secret to copy without displaying in text if user clicks copy directly
      btn.innerText = '...';
      fetch(`/vault/reveal/${credId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      })
      .then(res => res.json())
      .then(data => {
        if (data.password) {
          window.copyToClipboard(data.password, btn);
        } else {
          alert('Copy failed.');
          btn.innerText = 'Copy';
        }
      });
    }
  };

  // Show / Hide password input toggle
  window.togglePasswordInput = function(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;

    if (input.type === 'password') {
      input.type = 'text';
      btn.innerText = 'Hide';
    } else {
      input.type = 'password';
      btn.innerText = 'Show';
    }
  };

  // Vault client-side search filter
  const searchInput = document.getElementById('vaultSearch');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      const rows = document.querySelectorAll('.vault-row');
      rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? '' : 'none';
      });
    });
  }

});
