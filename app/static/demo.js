// The presenter-notes layer and the guided demo's spotlights (app/templates/demo/_notes.html). No build step.
// Notes: closed by default; in the guided demo they open on every screen unless the presenter closed them, which is
// remembered on this device ("notes-closed" in localStorage) until they are opened again.
(function () {
  var notes = document.getElementById('presenter-notes');
  if (!notes) return;
  var guided = notes.dataset.guided === 'on';
  var KEY = 'notes-closed';

  function open() { notes.hidden = false; document.body.classList.add('notes-open'); try { localStorage.removeItem(KEY); } catch (e) {} }
  function close(remember) {
    notes.hidden = true; document.body.classList.remove('notes-open');
    if (remember) { try { localStorage.setItem(KEY, '1'); } catch (e) {} }
  }
  document.querySelectorAll('[data-notes-toggle]').forEach(function (b) {
    b.addEventListener('click', function () { notes.hidden ? open() : close(true); });
  });
  document.querySelectorAll('[data-notes-close]').forEach(function (b) {
    b.addEventListener('click', function () { close(true); });
  });
  var closed = false; try { closed = localStorage.getItem(KEY) === '1'; } catch (e) {}
  if (guided && !closed) open();

  // Spotlight: Driver.js over this screen's elements (steps.yaml `spotlight`), skipping any not on the page now.
  var start = document.querySelector('[data-spotlight-start]');
  if (!start || !window.driver) return;
  start.addEventListener('click', function () {
    var list = []; try { list = JSON.parse(notes.dataset.spotlight || '[]'); } catch (e) {}
    var steps = list.filter(function (s) {
      var el = document.querySelector(s.el);
      if (!el) return false;
      for (var f = el.closest('details'); f; f = f.parentElement && f.parentElement.closest('details')) f.open = true;
      return el.getClientRects().length > 0;
    }).map(function (s) { return { element: s.el, popover: { description: s.text } }; });
    if (!steps.length) return;
    var wasOpen = !notes.hidden; close(false);
    var d = window.driver.js.driver({ showProgress: steps.length > 1, animate: true, steps: steps,
      nextBtnText: 'Next', prevBtnText: 'Back', doneBtnText: 'Done',
      onDestroyed: function () { if (wasOpen) open(); } });
    d.drive();
  });
})();
