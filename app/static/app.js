// What makes the path usable (decisions 47 and 48), no build step:
// - "Leave without saving?" before leaving a form with unsaved typing, by any link, button or the browser;
// - an AI button (and a decision the AI's work follows) reads "The AI is working…" and cannot be pressed twice;
// - a figure typed into a decision updates its button ("Seller: list at $650,000");
// - "Clear the form to type your own".
(function () {
  var LEAVE = 'Leave without saving? What you typed on this screen is not saved yet.';
  var dirty = null;  // the form with unsaved typing
  var submitting = false;

  document.querySelectorAll('form[data-guard]').forEach(function (f) {
    f.addEventListener('input', function () { dirty = f; });
    f.addEventListener('change', function () { dirty = f; });
  });

  function belongsToDirty(el) {
    if (!dirty || !el) return false;
    if (dirty.contains(el)) return true;
    var fid = el.getAttribute && el.getAttribute('form');
    return !!fid && fid === dirty.id;
  }

  // Any link out (not an in-page anchor), or any other form's button, asks first.
  document.addEventListener('click', function (e) {
    if (!dirty || submitting) return;
    var a = e.target.closest('a[href]');
    var b = e.target.closest('button[type=submit], button:not([type])');
    if (a) {
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || a.target === '_blank') return;
      if (!window.confirm(LEAVE)) { e.preventDefault(); return; }
      dirty = null;
    } else if (b && !belongsToDirty(b) && b.form && b.form !== dirty) {
      if (!window.confirm(LEAVE)) { e.preventDefault(); return; }
      dirty = null;
    }
  }, true);
  window.addEventListener('beforeunload', function (e) {
    if (dirty && !submitting) { e.preventDefault(); e.returnValue = LEAVE; return LEAVE; }
  });

  // Working state: one press only; an AI step says it is working until the next page arrives.
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form.dataset.sent === '1') { e.preventDefault(); return; }
    form.dataset.sent = '1';
    submitting = true;
    var b = e.submitter;
    if (b && b.name) {  // keep the pressed button's choice in the form (some browsers drop it once restyled)
      var h = document.createElement('input'); h.type = 'hidden'; h.name = b.name; h.value = b.value; form.appendChild(h);
    }
    document.querySelectorAll('.actionbar .button, #actionbar .button').forEach(function (x) { x.classList.add('is-busy'); x.setAttribute('aria-disabled', 'true'); });
    if (b && b.hasAttribute('data-working')) { b.textContent = 'The AI is working…'; b.classList.add('is-working'); }
    else if (b && b.closest('.actionbar')) { b.textContent = 'Saving…'; }
  }, true);
  window.addEventListener('pageshow', function (e) {  // back to a page from the cache: buttons work again
    if (e.persisted) { submitting = false; document.querySelectorAll('form').forEach(function (f) { delete f.dataset.sent; }); }
  });

  // A figure typed into a decision updates its button.
  function money(v) { var n = parseInt(String(v).replace(/[^0-9]/g, ''), 10); return isNaN(n) ? '' : '$' + n.toLocaleString('en-US'); }
  document.querySelectorAll('[data-label-template]').forEach(function (b) {
    var tpl = b.getAttribute('data-label-template');
    var form = document.getElementById(b.getAttribute('form'));
    if (!form) return;
    function update() {
      b.textContent = tpl.replace(/\{(\w+)\}/g, function (_, name) {
        var el = form.elements[name]; return el ? money(el.value) : '';
      });
    }
    form.addEventListener('input', update);
  });

  // "Clear the form to type your own".
  document.querySelectorAll('[data-clear-form]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var f = document.getElementById(a.getAttribute('data-clear-form'));
      if (!f) return;
      f.querySelectorAll('input[type=text], input:not([type]), input[inputmode], textarea').forEach(function (i) { if (i.type !== 'hidden') i.value = ''; });
      f.querySelectorAll('input[type=radio], input[type=checkbox]').forEach(function (i) { i.checked = false; });
      dirty = f;
      var first = f.querySelector('input:not([type=hidden])'); if (first) first.focus();
    });
  });

  // The menu closes when you press outside it.
  var menu = document.getElementById('menu');
  if (menu) document.addEventListener('click', function (e) { if (menu.open && !menu.contains(e.target)) menu.open = false; });
})();
